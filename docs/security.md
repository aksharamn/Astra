# Security notes

ASTRA's UI is designed to make security visible, not to replace server controls. The backend hashes PINs with Argon2id, uses secure/HttpOnly/SameSite session cookies, rotates session versions on recovery, rate-limits authentication, validates message size/content, and authorizes every conversation lookup.

Serve over HTTPS when credentials leave localhost. For a LAN demonstration, use a private network, firewall the port to the LAN subnet, disable Flask debug mode, and do not port-forward it. Configure an explicit Socket.IO origin rather than `*` when cookies are enabled.

The frontend escapes message text before inserting it into the DOM and does not persist tokens in localStorage. It persists only visual theme preferences. The packet inspector shows metadata/ciphertext previews and the tamper action mutates a captured ciphertext, then calls the backend AES-GCM verifier; the altered packet is rejected by the authentication tag. Because the relay currently owns the AES key, this is authenticated encryption at rest/in transit to the relay, not true E2EE. Production scope is an authenticated public-key exchange with client-held per-conversation keys.
