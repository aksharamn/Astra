# Five-minute ASTRA demo

1. Start the Flask server on `0.0.0.0:5000`; open the LAN URL on two browsers. Register two real users and sign in.
2. From **Contacts**, send a request. Accept it through the backend workflow, then open the resulting conversation. Point out that there are no hardcoded Alice/Bob records.
3. Send a message. Show the real timestamp, secure badge, REST response, and live `message:new` update.
4. Open **Packet inspector**. Show the real ciphertext, nonce, GCM tag, integrity and transport fields. Select **Tamper demo**, flip a ciphertext character, and show the backend AES-GCM verifier returning `INTEGRITY CHECK FAILED`.
5. Select **OSI path**. Trigger a message and show live backend telemetry; explain why lower layers say **SIMULATED** unless the backend emits evidence.
6. Open Settings, switch presets, adjust the accent, export/import JSON, and finish in Presentation mode.
