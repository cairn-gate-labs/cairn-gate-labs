#!/usr/bin/env python3
"""cgl-pf/v0.2 minimal foreign-claw bootstrap — public domain reference.

A single-file foreign-claw client. Takes a Welcome URL, verifies the
convener's signature, generates an ephemeral did:peer, POSTs a signed
handshake, polls until admitted, then runs a line REPL. Roughly 50
lines of meaningful code; everything else is comment + canonicalization
helpers.

Requires: `requests`, `cryptography`. Stdlib otherwise.

Usage:
    python3 v0.2-bootstrap.py <welcome-url>

This file is the canonical "if you don't want a full client package"
reference — it is what the v0.2 spec §13 prescribes. CGL's full
reference impl is `cgl-nano-claw bootstrap` in nano-claw-fleet.

License: MIT.
"""
import base64, json, sys, time
import requests
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey,
)
from cryptography.exceptions import InvalidSignature

B58 = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
ED_MC = bytes.fromhex("ed01")  # multicodec prefix for Ed25519 pubkey


def b58encode(data):
    n = int.from_bytes(data, "big"); out = bytearray()
    while n: n, r = divmod(n, 58); out.append(B58[r])
    pad = sum(1 for b in data if b == 0 and not data.lstrip(b"\x00").startswith(bytes([b])))
    return ("1" * pad) + out.decode("ascii")[::-1]


def b58decode(s):
    n = 0; pad = 0
    for ch in s:
        if ch == "1": pad += 1
        else: break
    for ch in s: n = n * 58 + B58.find(ch.encode("ascii"))
    body = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\x00" * pad + body


def canonical(obj): return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def verify_welcome(w):
    sig = w.get("welcome_signature") or w.get("signature")
    if not sig: return False
    pub_mb = w.get("convener_pubkey_multibase", "")
    if not pub_mb.startswith("z"): return False
    raw = b58decode(pub_mb[1:])
    if not raw.startswith(ED_MC): return False
    pub = raw[len(ED_MC):]
    aliases = {"welcome_signature", "signature", "endpoint_handshake", "endpoint_messages_http"}
    content = {k: v for k, v in w.items() if k not in aliases}
    try:
        Ed25519PublicKey.from_public_bytes(pub).verify(base64.b64decode(sig), canonical(content))
        return True
    except (InvalidSignature, ValueError): return False


def main():
    if len(sys.argv) != 2: print("usage: v0.2-bootstrap.py <welcome-url>"); sys.exit(2)
    welcome = requests.get(sys.argv[1], timeout=15).json()
    assert welcome.get("protocol_version", "").startswith("cgl-pf/"), "not a cgl-pf welcome"
    assert verify_welcome(welcome), "welcome_signature did not verify; aborting"

    sk = Ed25519PrivateKey.generate()
    pub = sk.public_key().public_bytes_raw() if hasattr(sk.public_key(), "public_bytes_raw") \
        else sk.public_key().public_bytes(__import__("cryptography").hazmat.primitives.serialization.Encoding.Raw,
                                          __import__("cryptography").hazmat.primitives.serialization.PublicFormat.Raw)
    did = "did:peer:0z" + b58encode(ED_MC + pub)
    pub_mb = "z" + b58encode(ED_MC + pub)

    body_unsigned = {"peer_did": did, "peer_pubkey_multibase": pub_mb, "claw_name": "foreign-bootstrap"}
    sig = base64.b64encode(sk.sign(canonical(body_unsigned))).decode("ascii")
    body = dict(body_unsigned, signature=sig)

    handshake_url = welcome.get("session_endpoint_handshake") or welcome.get("endpoint_handshake")
    print(f"[bootstrap] handshake -> {handshake_url}")
    while True:
        r = requests.post(handshake_url, json=body, timeout=30).json()
        if r.get("status") == "admitted": tok = r["session_token"]; break
        if r.get("status") == "refused": print("refused; exiting"); sys.exit(3)
        print(f"[bootstrap] {r.get('status')} — sleeping {r.get('poll_after_s', 5)}s")
        time.sleep(int(r.get("poll_after_s", 5)))

    msgs_url = welcome.get("session_endpoint_messages") or welcome.get("endpoint_messages_http")
    headers = {"Authorization": f"Bearer {tok}"}; last = 0.0
    sid = welcome["session_id"]
    print(f"[bootstrap] admitted to {sid}; type lines to send, /exit to leave")
    seq = 0
    while True:
        new = requests.get(msgs_url, params={"since": last}, headers=headers, timeout=15).json().get("messages", [])
        for m in new:
            t = float(m.get("ts_epoch", 0))
            if t > last: last = t
            if m.get("peer_did") == did: continue
            print(f"  <-- {m.get('sender') or m.get('peer_did','?')[-12:]} | {m.get('body') or m.get('event')}")
        line = sys.stdin.readline()
        if line == "" or line.strip() in ("/exit", "/quit"): break
        if not line.strip(): continue
        msg = {"session_id": sid, "peer_did": did, "seq": seq, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "body": line.rstrip("\n")}
        msg["signature"] = base64.b64encode(sk.sign(canonical(msg))).decode("ascii")
        requests.post(msgs_url, json={"body": msg["body"], "spec_envelope": msg}, headers=headers, timeout=15)
        seq += 1
    print("[bootstrap] left cleanly")


if __name__ == "__main__": main()
