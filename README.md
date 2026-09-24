# ASTRA

### Secure Real-Time Messaging & OSI Network Visualization

**ASTRA** is a secure, real-time messaging platform designed to demonstrate how modern communication systems work from the user's message all the way down through the **OSI model**.

It combines a modern messaging experience with practical cybersecurity concepts including authentication, encrypted communication, session management, WebSockets, and interactive network-layer visualization.

> **ASTRA — Secure communication, visualized.**

---

## ✨ Features

### 💬 Real-Time Messaging

* Real-time one-to-one messaging
* Persistent conversations
* Message timestamps
* Delivered/read status
* Typing indicators
* Online/offline presence
* Automatic reconnection
* Message deletion
* Conversation management

### 🔐 Secure Authentication

* Unique ASTRA Profile ID
* Username and display name
* Password authentication
* Separate security PIN
* Secure password hashing
* Session management
* Password recovery
* Authentication rate limiting
* Input validation

### 🛡️ Encrypted Communication

ASTRA is designed around secure message handling rather than simply displaying an encryption animation.

Message flow:

```text
User Message
     │
     ▼
Encoding
     │
     ▼
Encryption
     │
     ▼
Encrypted Payload
     │
     ▼
Real-Time Transport
     │
     ▼
Encrypted Payload
     │
     ▼
Decryption
     │
     ▼
Original Message
```

Authenticated encryption such as **AES-GCM** is used where appropriate.

> Cryptographic operations are implemented using established libraries and primitives rather than custom cryptographic algorithms.

---

# 🌐 OSI Visualization

One of ASTRA's main features is its interactive **OSI Model visualization**.

When a message is sent, ASTRA can visualize the conceptual journey of that data through the seven OSI layers.

```text
┌──────────────────────────────┐
│  7. Application              │
├──────────────────────────────┤
│  6. Presentation             │
├──────────────────────────────┤
│  5. Session                  │
├──────────────────────────────┤
│  4. Transport                │
├──────────────────────────────┤
│  3. Network                  │
├──────────────────────────────┤
│  2. Data Link                │
├──────────────────────────────┤
│  1. Physical                 │
└──────────────────────────────┘
```

### Example flow

```text
Application
   ↓
Message creation

Presentation
   ↓
Encoding / Encryption

Session
   ↓
Session management

Transport
   ↓
TCP / WebSocket transport

Network
   ↓
IP addressing / routing

Data Link
   ↓
Frames / local network communication

Physical
   ↓
Physical transmission
```

The visualization is intended to connect networking theory with the actual messaging workflow.

Users can inspect individual layers and understand their role in communication.

---

# 🧠 Architecture

ASTRA follows a modular client-server architecture.

```text
                   ┌───────────────────┐
                   │     ASTRA Web     │
                   │     Frontend      │
                   └─────────┬─────────┘
                             │
                    HTTPS / WebSocket
                             │
                             ▼
                   ┌───────────────────┐
                   │     ASTRA API     │
                   │      Backend      │
                   └───────┬─────┬─────┘
                           │     │
                ┌──────────┘     └──────────┐
                ▼                           ▼
        ┌───────────────┐           ┌───────────────┐
        │   Database    │           │ Crypto / Auth │
        └───────────────┘           └───────────────┘
```

### Major components

```text
Frontend
├── Authentication
├── Messaging UI
├── Contacts
├── Profile
├── Settings
├── Security Center
└── OSI Visualization

Backend
├── Authentication
├── Users
├── Connections
├── Conversations
├── Messages
├── WebSockets
├── Sessions
└── Security

Database
├── Users
├── Profiles
├── Sessions
├── Connections
├── Conversations
└── Messages
```

---

# 🔑 ASTRA Profile ID

Every ASTRA user receives a unique identifier.

Instead of requiring users to expose personal information to connect with someone, users can share their **ASTRA Profile ID**.

Example:

```text
ASTRA ID
A7X9-K2P4-91QZ
```

A user can search for another person using their ASTRA ID and initiate a connection request.

---

# 🔒 Security Architecture

Security is treated as a core part of ASTRA rather than an additional UI feature.

ASTRA is designed to address:

* Secure authentication
* Password hashing
* Session security
* Authorization
* Input validation
* Rate limiting
* Secure WebSocket communication
* Authenticated encryption
* Access control
* Secure database queries
* Error handling
* Protection against common web vulnerabilities

### Security principles

```text
Never trust client input
Never store plaintext passwords
Never expose cryptographic secrets
Never rely on client-side authorization
Never implement custom cryptography
```

ASTRA is an educational project and should not be considered a production-grade secure messenger without independent security auditing.

---

# 🎨 Interface

ASTRA uses a modern minimal interface inspired by contemporary software design.

The UI focuses on:

* Minimal visual hierarchy
* Smooth transitions
* Glass-style surfaces
* Responsive layouts
* Dark and light themes
* Micro-interactions
* Morphing transitions
* Interactive network visualization

Animations are used to communicate state and information rather than being purely decorative.

---

# 🧩 Technology Stack

The exact stack may evolve during development, but ASTRA is structured around modern web technologies.

### Frontend

* React / Next.js
* TypeScript
* Modern CSS / Tailwind CSS
* Framer Motion or equivalent animation library

### Backend

* Node.js
* REST APIs
* WebSockets
* Authentication middleware

### Database

* PostgreSQL or equivalent relational database

### Security

* AES-GCM
* Secure password hashing
* Cryptographically secure random generation
* HTTPS / TLS
* Secure session handling

---

# 📁 Project Structure

```text
ASTRA/
│
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── lib/
│   └── styles/
│
├── backend/
│   ├── auth/
│   ├── users/
│   ├── chats/
│   ├── messages/
│   ├── websocket/
│   ├── encryption/
│   └── database/
│
├── shared/
│   ├── types/
│   └── crypto/
│
├── .env.example
├── package.json
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

Make sure the following are installed:

* Node.js 20+
* npm / pnpm / yarn
* PostgreSQL
* Git

---

## Clone the Repository

```bash
git clone https://github.com/aksharamn/Astra.git

cd Astra
```

---

## Install Dependencies

```bash
npm install
```

If the project uses separate frontend and backend packages:

```bash
cd frontend
npm install

cd ../backend
npm install
```

---

# ⚙️ Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
DATABASE_URL=

JWT_SECRET=

SESSION_SECRET=

PORT=5000

CLIENT_URL=http://localhost:3000
```

Never commit real secrets to Git.

---

# 🗄️ Database Setup

Create a PostgreSQL database and configure `DATABASE_URL`.

Then run the project's database migration commands.

Example:

```bash
npm run db:migrate
```

Seed development data only if the project provides a seed command:

```bash
npm run db:seed
```

---

# ▶️ Running ASTRA

Start the development environment:

```bash
npm run dev
```

The application should then be available locally.

Frontend:

```text
http://localhost:3000
```

Backend:

```text
http://localhost:5000
```

The exact ports may vary depending on the project configuration.

---

# 🧪 Testing

Run the test suite:

```bash
npm test
```

For linting:

```bash
npm run lint
```

For production builds:

```bash
npm run build
```

---

# 🔄 Message Lifecycle

A simplified ASTRA message lifecycle looks like this:

```text
             SENDER
                │
                ▼
        ┌───────────────┐
        │ Create Message│
        └───────┬───────┘
                ▼
        ┌───────────────┐
        │    Encrypt    │
        └───────┬───────┘
                ▼
        ┌───────────────┐
        │ WebSocket/TLS │
        └───────┬───────┘
                ▼
             SERVER
                │
                ▼
        ┌───────────────┐
        │ Store/Relay   │
        │  Ciphertext   │
        └───────┬───────┘
                ▼
        ┌───────────────┐
        │ WebSocket/TLS │
        └───────┬───────┘
                ▼
           RECEIVER
                │
                ▼
        ┌───────────────┐
        │    Decrypt    │
        └───────┬───────┘
                ▼
        ┌───────────────┐
        │ Display Text  │
        └───────────────┘
```

The exact cryptographic and storage model depends on the implementation.

---

# 🌐 OSI Demonstration

ASTRA provides an educational visualization of how network communication can be understood through the OSI model.

| Layer | Name         | ASTRA Concept           |
| ----: | ------------ | ----------------------- |
|     7 | Application  | Messaging application   |
|     6 | Presentation | Encoding / encryption   |
|     5 | Session      | Session management      |
|     4 | Transport    | TCP / WebSocket         |
|     3 | Network      | IP addressing           |
|     2 | Data Link    | Frames / local delivery |
|     1 | Physical     | Physical transmission   |

This visualization is an educational abstraction and should not be interpreted as a literal one-to-one mapping of every implementation detail to the OSI model.

---

# 🛡️ Threat Model

ASTRA considers common threats such as:

* Credential theft
* Brute-force authentication
* Session theft
* Unauthorized conversation access
* Malicious input
* Injection attacks
* Cross-site scripting
* WebSocket abuse
* Replay attempts
* Insecure direct object references
* Accidental secret exposure

Security controls should be continuously reviewed as the project evolves.

---

# ⚠️ Disclaimer

ASTRA is primarily an **educational cybersecurity and networking project**.

It demonstrates concepts such as:

* Secure authentication
* Cryptography
* Real-time networking
* WebSockets
* Database security
* Access control
* OSI networking
* Secure application architecture

It has **not been independently audited** and should not be used as a replacement for professionally audited end-to-end encrypted messaging software.

---

# 🗺️ Roadmap

### Authentication

* [x] User registration
* [x] Login
* [ ] Password recovery
* [ ] Session management improvements
* [ ] Account security controls

### Messaging

* [x] Basic messaging architecture
* [ ] Real-time messaging
* [ ] Message persistence
* [ ] Read receipts
* [ ] Typing indicators
* [ ] Message search
* [ ] Media attachments

### Security

* [ ] Authenticated encryption
* [ ] Key management
* [ ] Rate limiting
* [ ] Security audit
* [ ] Improved threat detection

### OSI Visualization

* [x] Seven-layer model
* [ ] Animated packet flow
* [ ] Interactive layer inspection
* [ ] Sender/receiver visualization
* [ ] Real-time visualization tied to message events

### UI/UX

* [x] Responsive interface
* [ ] Dark/light themes
* [ ] Advanced morph animations
* [ ] Accessibility improvements
* [ ] Mobile optimization

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/your-feature
```

3. Make your changes.
4. Test the project.
5. Commit your changes.

```bash
git commit -m "feat: add your feature"
```

6. Push the branch.

```bash
git push origin feature/your-feature
```

7. Open a Pull Request.

---

# 📜 License

This project is currently intended as an educational project.

Add the appropriate license before distributing ASTRA publicly.

---

# 👨‍💻 Project

**ASTRA**

> Secure communication.
> Visible architecture.
> Practical cybersecurity.

GitHub:

https://github.com/aksharamn/Astra
