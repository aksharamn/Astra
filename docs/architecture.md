# ASTRA frontend architecture

The template is a three-pane application: identity/sidebar, conversation, and an optional packet inspector. The auth shell is separate so unauthenticated users never receive contact data. CSS variables make the visual system themeable and responsive.

`api.js` is the only module that performs HTTP requests. It sends cookies (`credentials: include`) and normalizes JSON errors. `state.js` is a small evented store; modules update it and render only their concern. `messaging.js` uses REST for history and as a fallback when Socket.IO is unavailable; normal sends use one Socket.IO event so messages are not duplicated. Reconnects can safely reload history.

The API should return stable IDs (`user.id`, `conversation.id`, `message.id`) and ISO timestamps. A message can use `body` or `content`; a contact can use `display_name` or `username`. This tolerance lets the UI work with incremental backend implementations.

## Event flow

1. Login creates the server session.
2. Profile, contacts, and conversations load concurrently.
3. A contact opens a conversation and history is fetched.
4. Send emits `message:send`; the server persists the encrypted message and emits the authenticated packet metadata and `message:new`.
5. `packet` and `osi:event` are event-backed telemetry. The seven-layer panel marks browser/OS-inaccessible physical and frame details `SIMULATED`.
