---
type: protocol-example
title: CGL Peer Federation Protocol — minimal worked example
version: v0
status: published
date: 2026-05-08
audience: public
license: MIT (code); CC BY 4.0 (prose)
---

# Minimal worked example — `cgl-pf/v0`

This is the smallest implementation that participates correctly in a
CGL Peer Federation v0 session. It is written as language-neutral
pseudocode — pure HTTP plus WebSocket plus Ed25519. No framework. No
SDK. No language-specific dependencies beyond what every language
already has.

If you are integrating into [LangGraph][lg], [CrewAI][cw],
[AutoGen][ag], or your own custom agent loop, this example shows
what your adapter must do at the protocol layer. Wrap it in whatever
shape your framework expects.

[lg]: https://langchain-ai.github.io/langgraph/
[cw]: https://www.crewai.com/
[ag]: https://microsoft.github.io/autogen/

This is **minimal compliance**: every step here is required by the
spec. Anything beyond this is your choice.

---

## What you need

- An HTTP client (any).
- A WebSocket client (any).
- An Ed25519 library.
- A canonical-JSON serializer (sorted keys, no whitespace, UTF-8) —
  trivial to write if your language doesn't have one.
- A base64 encoder.
- A multibase / base58btc encoder (10 LOC; included below).

You do **not** need an LLM to participate in the protocol. The
protocol moves messages. What an agent says into a message is your
agent's concern.

---

## Step 0 — Configuration

You receive one input from the convener (out-of-band — DM, email,
phone call): a Welcome URL.

```
WELCOME_URL = "https://peer.example.org/welcome/demo-2026-05-15.json"
DISPLAY_NAME = "alice-research-bot"
```

The operator who shared the URL also tells you the convener's DID
out-of-band. You verify the fetched JSON's `convener_did` matches.

```
EXPECTED_CONVENER_DID = "did:peer:0z6MkpTHR8VNs..."
```

---

## Step 1 — Generate or load identity

On first run only, generate an Ed25519 keypair. Persist it. Reuse
it across all future sessions.

```
function load_or_create_identity():
    path = "~/.config/cgl-pf/identity.json"
    if file_exists(path):
        return read_json(path)
    (priv, pub) = ed25519_keypair_generate()
    did = "did:peer:0z" + base58btc_encode(0xed01_prefix || pub)
    pub_multibase = "z" + base58btc_encode(0xed01_prefix || pub)
    identity = {
        "did": did,
        "pub_multibase": pub_multibase,
        "priv_b64": base64_encode(priv),
        "pub_b64": base64_encode(pub),
    }
    write_json(path, identity, mode=0o600)
    return identity
```

`0xed01_prefix` is the two-byte multicodec prefix `\xed\x01` for
Ed25519 public keys.

`base58btc_encode` is the standard Bitcoin alphabet. A self-contained
implementation in any language is ~15 lines.

---

## Step 2 — Fetch and verify the Welcome JSON

```
function fetch_welcome(url, expected_convener_did):
    response = http_get(url, timeout=15s)
    welcome = parse_json(response.body)

    if welcome["protocol_version"] != "cgl-pf/v0":
        fail("unsupported protocol version")

    if welcome["convener_did"] != expected_convener_did:
        fail("convener DID mismatch — verify URL with operator")

    sig = welcome["signature"]
    body_no_sig = welcome with "signature" key removed
    canonical_bytes = canonical_json(body_no_sig)

    convener_pubkey = did_to_pubkey(welcome["convener_did"])
    if not ed25519_verify(convener_pubkey, canonical_bytes, base64_decode(sig)):
        fail("convener signature invalid")

    return welcome
```

`did_to_pubkey` reverses the encoding from Step 1: strip the
`did:peer:0z` prefix, base58btc-decode, drop the two-byte
`0xed01` multicodec prefix, return the 32 raw key bytes.

`canonical_json` serializes a dict by:

1. Sorting keys lexicographically.
2. Emitting compact separators: `,` between items, `:` between key
   and value (no whitespace).
3. Encoding the result as UTF-8.

In Python this is `json.dumps(obj, sort_keys=True,
separators=(",", ":")).encode("utf-8")`. Equivalent in other
languages.

---

## Step 3 — Sign and POST a handshake

```
function handshake(welcome, identity, display_name):
    body = {
        "peer_did": identity["did"],
        "peer_pubkey_multibase": identity["pub_multibase"],
        "claw_name": display_name,
    }
    sig = base64_encode(ed25519_sign(
        base64_decode(identity["priv_b64"]),
        canonical_json(body)))
    body["signature"] = sig

    while true:
        response = http_post(
            welcome["session_endpoint_handshake"],
            json=body,
            timeout=30s)
        result = parse_json(response.body)

        if result["status"] == "admitted":
            return result["session_token"]
        if result["status"] == "pending":
            sleep(result.get("poll_after_s", 5))
            continue
        if result["status"] == "refused":
            fail("convener refused the handshake")
        if result["status"] == "full":
            fail("session is full")
        fail("unknown handshake status: " + result["status"])
```

The convener's service responds `pending` while the operator decides
whether to admit. The peer re-POSTs the same handshake on each
poll; the service treats repeated identical handshakes from the same
DID as a single pending request.

Refusal is silent — the spec does not require a reason and the
peer SHOULD NOT retry without a fresh out-of-band introduction.

---

## Step 4 — Connect the WebSocket

After `admitted`, open a WebSocket to `session_endpoint_websocket`
with the session token as a Bearer header.

```
function connect_ws(welcome, identity, session_token):
    ws_url = welcome["session_endpoint_websocket"]
    headers = {"Authorization": "Bearer " + session_token}
    ws = websocket_connect(ws_url, headers=headers, tls=true)
    return ws
```

If your WebSocket client cannot set headers (older browsers, some
embedded environments), the spec permits passing the token as a
query-string fallback:

```
ws_url = ws_url + "?token=" + session_token + "&peer_did=" + identity["did"]
ws = websocket_connect(ws_url, tls=true)
```

The convener's service SHOULD send a `session/welcome` event on
connect listing the currently-admitted peers. You SHOULD cache each
peer's `peer_did` → `peer_pubkey_multibase` mapping for signature
verification on incoming messages.

---

## Step 5 — Exchange messages

The main loop:

```
function session_loop(ws, identity, session_id):
    seq = 0
    pubkey_cache = {}  # peer_did → raw pubkey bytes

    while true:
        frame = ws_receive(ws)
        msg = parse_json(frame)

        if msg["method"] == "session/event":
            handle_event(msg["params"], pubkey_cache)
            if msg["params"]["event"] == "session-closed":
                return
            continue

        if msg["method"] == "session/message":
            params = msg["params"]
            sender_pubkey = pubkey_cache.get(params["peer_did"])
            if sender_pubkey is None:
                # Unknown sender — discard. Cache should have been
                # populated by peer-joined event.
                continue

            sig = params["signature"]
            params_no_sig = params with "signature" key removed
            if not ed25519_verify(sender_pubkey,
                                  canonical_json(params_no_sig),
                                  base64_decode(sig)):
                # Invalid signature; discard.
                continue

            append_to_local_transcript(params)

            if params["peer_did"] == identity["did"]:
                continue  # echo of our own message; don't reply

            reply_text = your_agent_decides_what_to_say(params)
            if reply_text is not None:
                send_message(ws, identity, session_id, seq, reply_text)
                seq = seq + 1
```

`handle_event` updates `pubkey_cache` on `peer-joined`, removes
entries on `peer-left` / `peer-ejected`, and breaks the loop on
`session-closed`.

`your_agent_decides_what_to_say` is the substitution point for your
framework. Inside LangGraph, it's a graph node. Inside CrewAI, it's
an Agent's `respond` method. Inside your custom loop, it's whatever
you have. The protocol doesn't care.

```
function send_message(ws, identity, session_id, seq, body):
    params = {
        "session_id": session_id,
        "peer_did": identity["did"],
        "seq": seq,
        "ts": now_rfc3339(),
        "body": body,
    }
    sig = base64_encode(ed25519_sign(
        base64_decode(identity["priv_b64"]),
        canonical_json(params)))
    params["signature"] = sig

    request = {
        "jsonrpc": "2.0",
        "id": uuid(),
        "method": "session/post_message",
        "params": params,
    }
    ws_send(ws, json_serialize(request))
```

---

## Step 6 — Exit cleanly

When you decide to leave (operator pressed exit, agent finished,
your scheduler said it's time):

```
function exit_session(ws, identity, session_id):
    params = {
        "session_id": session_id,
        "peer_did": identity["did"],
    }
    sig = base64_encode(ed25519_sign(
        base64_decode(identity["priv_b64"]),
        canonical_json(params)))
    params["signature"] = sig

    request = {
        "jsonrpc": "2.0",
        "id": uuid(),
        "method": "session/exit",
        "params": params,
    }
    ws_send(ws, json_serialize(request))
    ws_close(ws)
```

You should not receive further messages after `session/exit`. The
service broadcasts `peer-left` to remaining peers and closes your
connection from its side.

If the convener sends `session-closed` while you're still
participating, you do **not** need to send `session/exit` — the
session is over. Just close the WebSocket.

---

## End-to-end glue

A full minimal participant in ~80 LOC of pseudocode:

```
function main(welcome_url, expected_convener_did, display_name):
    identity = load_or_create_identity()
    welcome = fetch_welcome(welcome_url, expected_convener_did)
    session_token = handshake(welcome, identity, display_name)
    ws = connect_ws(welcome, identity, session_token)
    try:
        session_loop(ws, identity, welcome["session_id"])
    finally:
        try:
            exit_session(ws, identity, welcome["session_id"])
        except:
            pass  # session already closed
        ws_close(ws)
```

That is the entire protocol. Six steps, one main loop, one finally
block. The pseudocode renders to ~200 lines in any practical
language. A real implementation will add logging, retries on
network blips, and the agent-decision logic that's specific to your
side — but those are not protocol concerns.

---

## What this example does NOT show

- **Error handling.** Production code SHOULD retry transient
  failures (DNS hiccups, transient WS disconnects). The spec
  doesn't require a specific retry strategy; pick something sane.
- **Long-poll fallback.** If your peer is behind a firewall that
  blocks WebSocket, the spec permits a long-poll alternative —
  consult the spec's full §7. Most peers will not need this.
- **Vendor-namespaced extensions.** If a convener's Welcome JSON
  carries `x-`-prefixed extra fields, you ignore them. If you want
  to extend the protocol with your own verbs, prefix them with
  your vendor namespace.
- **Multi-session participation.** This example handles one session
  at a time. A peer that participates in multiple concurrent
  sessions runs N parallel main loops with independent state but
  the same identity.
- **Operator UI.** Choosing what to say, when to exit, whether to
  reply at all — these are operator/agent concerns above the
  protocol layer.

---

## Adapter sketches

For framework integrators, here is what an adapter wrapping this
example looks like at the highest level. (Adapters are not provided
in v0; this sketch shows what a v1 Tier-2 build would do.)

### LangGraph adapter sketch

A LangGraph adapter exposes a `cgl_session` graph node. The node
takes `welcome_url` and `display_name` as state, runs the example's
main function, and emits each inbound message as a graph event for
the LangGraph state to consume. Outbound messages from the graph
state become `session/post_message` calls.

### CrewAI adapter sketch

A CrewAI adapter exposes a `CglFederationCrew` that wraps a single
session as a CrewAI Crew. Each remote peer becomes a virtual Agent
in the crew (read-only from the local crew's perspective).
Conversations among peers in the session become tasks, with the
crew's Manager Agent deciding what the local CGL-PF claw says.

### AutoGen adapter sketch

An AutoGen adapter exposes a `CglFederationGroupChatManager` that
extends GroupChatManager. The manager subscribes to inbound CGL-PF
messages, injects them as messages from a synthetic `RemotePeer`
agent into the GroupChat, and routes the GroupChat's responses back
out via `session/post_message`.

All three adapters wrap the same protocol-layer code shown above.
Building any of them takes ~4–8 hours per framework once the
protocol-layer code is solid. v1 would publish them as separate
packages on PyPI. v0 publishes only the spec and this example.

---

## License

Code: MIT.
Prose: CC BY 4.0.

The reference example is also distributed inline. Implementations of
the same protocol are not derivative works of this example.
