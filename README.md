# ASTRA

ASTRA is a secure real-time messaging platform with SQLite persistence, Argon2id PIN hashing, authenticated AES-256-GCM message storage, ASTRA ID identity, contact authorization, real-time presence, and an inspectable OSI 7-layer security architecture view.

## Run

Install Python 3.11+ and install dependencies:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py app.py
```

Open `http://localhost:5000/`. For a LAN demo, use the host machine's LAN address (`http://192.168.x.x:5000`) and allow the port through the private Windows Firewall profile. Configure `ASTRA_ALLOWED_ORIGINS` as a comma-separated explicit allowlist when serving the API or Socket.IO on another origin.

## Expected API contract

Login is `ASTRA ID + PIN`; registration creates a unique server-generated ID displayed as `ASTRA-XXXX-XXXX-XXXX` using an unambiguous alphabet. Recovery is a challenge -> verification -> one-time reset token -> new PIN flow. Contact requests are accepted by the recipient before messaging is authorized.

Messages are stored as ciphertext, nonce, and GCM tag. This educational build encrypts at the relay with a server-held master key, so it is **not true end-to-end encryption**; a production version must add an authenticated client-side public-key exchange and per-conversation keys. The tamper demo sends an altered real packet to the AES-GCM verifier and reports the resulting authentication failure.

## Frontend modules

`api.js` (fetch boundary), `auth.js`, `profiles.js`, `contacts.js`, `messaging.js`, `websocket.js`, `encryption.js`, `osi.js`, `themes.js`, and `presentation.js` are loaded by `app.js`. OSI entries without browser/OS telemetry are explicitly labelled **SIMULATED**.

## LAN safety

Use TLS or a private trusted network, bind only to the LAN interface, keep debug mode off, use strong per-user credentials, and never expose the development server directly to the public internet. See `docs/security.md`.
