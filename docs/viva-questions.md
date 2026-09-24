# Viva questions and answers

**Why Socket.IO and REST?** REST is reliable for login/history and gives an auditable send response; Socket.IO provides low-latency presence and message events.

**Is the browser observing all OSI layers?** No. Application/session events are observable. Transport and below are represented only when the backend supplies telemetry; otherwise the UI labels them SIMULATED.

**How is XSS reduced?** Message content is escaped before DOM insertion. The backend must still sanitize/validate and set a strict Content-Security-Policy.

**Where are credentials stored?** In backend-managed secure cookies, not localStorage. The API should use CSRF protection where cookie-authenticated state changes require it.

**What does the tamper demo prove?** Only the user experience of an integrity failure. Production authenticity must be provided by an authenticated encryption construction and server-side verification.

**How do two LAN devices connect?** Bind Flask to `0.0.0.0`, use the host's private IP, permit the port in the private firewall profile, and ensure Socket.IO and CORS accept that origin. Never expose the development server to the public internet.

**What happens if the API is unavailable?** Authentication displays status, while the app remains structurally usable for an offline preview; contacts/messages are never fabricated.
