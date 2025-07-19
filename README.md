# 🚀 Synapse: A Zettelkasten-Inspired PKM with Knowledge Graph Visualization
> A full-stack personal knowledge management application that holds connections between ideas via interactive graph analytics.

---

## 📝 Feature Checklist
> _Update this list before coding each feature._
- [X] Initial Setup
- [X] User Registration
- [X] User Login
- [ ] 
---

## 📖 Table of Contents
1. [Overview](#overview)  
2. [Tech Stack](#tech-stack)  
3. [Use Case & Target Roles](#use-case-&-target-roles)
4. [Prerequisites](#prerequisites)
3. [Installation](#installation)  
   - [Backend](#backend)  
   - [Frontend](#frontend)  
   - [Docker Compose (optional)](#docker‑compose‑optional)  
4. [Running the App](#running‑the‑app)  
5. [API Reference](#api‑reference)  
6. [Development Workflow](#development‑workflow)  
7. [Testing](#testing)  
8. [Architecture Decision Records (ADRs)](#architecture‑decision‑records‑adrs)  
9. [Contributing](#contributing)  
10. [License](#license)  

---

## 📘 Overview
"Synapse" is a Zettelkasten-inspired personal knowledge management (PKM) tool designed to help students, researchers, and knowledge workers capture atomic ideas, interlink them, and visualize connections through an interactive graph. By storing notes in a graph database and leveraging graph analytics, Synapse holds relationships, fostering deeper learning and novel insights.

---

## 🔧 Tech Stack
- Frontend: React, Tailwind CSS, Cytoscape.js (or Sigma.js)
- Backend: Python (FastAPI)
- Databases:
  - Graph: Neo4j for note relationships 
  - Relational/NoSQL: PostgreSQL or MongoDB for users and structured data 
- Version Control: Git, GitHub 
- DevOps: Docker, Docker Compose, GitHub Actions (CI/CD)
---
## 🎯 Use Case & Target Roles
- Use Case: A “second brain” for managing notes, connecting ideas, and conducting graph-based analysis. 
- Target Roles:
  - Full-Stack Developer 
  - Backend Developer 
  - Data Engineer (graph databases)
  - Product Manager (focus on user-centric product lifecycle)
---
## 🔧 Prerequisites

Node.js ≥18

Python ≥3.11 (with FastAPI) or Node.js runtime

Docker & Docker Compose (optional)

Git & GitHub account
---
## ⚙️ Installation

### Backend
```bash
cd backend
python -m venv venv
source venv/Scripts/activate        # (or `source venv/bin/activate` on mac/linux)
pip install -r requirements.txt
```
### Frontend
```
cd frontend
npm install
```
### Docker Compose (optional)
```
# from repo root
docker-compose up --build
```
## ▶️ Running the App
### Run Backend Only
```
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
### Run Frontend Only
```
cd frontend
npm start
```
### Run Both via Docker Compose
```
docker-compose up
```

## 📑 API Reference

### GET /ping

    Response: { "pong": true }

### /notes CRUD
| Method | Path          | Description       |
| ------ | ------------- |-------------------|
| GET    | `/notes`      | List all notes    |
| POST   | `/notes`      | Create a new note |
| GET    | `/notes/{id}` | Get note by ID    |
| PUT    | `/notes/{id}` | Update note by ID |
| DELETE | `/notes/{id}` | Delete note by ID |

## 🛠 Development Workflow

1. Pick a feature from the 📝 Feature Checklist. 
2. Update this README:
   - Add or check off the appropriate checkbox. 
   - Flesh out any usage examples under [API Reference]. 
3. Create a feature branch:
- ```
     git checkout -b feature/<your-feature>
     ```
4. Write failing tests (TDD) or update docs (RDD). 
5. Implement your code to make tests pass / satisfy the spec. 
6. Commit & PR against develop. 
7. Merge into main when approved.

## Testing
### Backend
```
cd backend
pytest --cov=backend
```
### Frontend
```
cd frontend
npm test
```
## 📂 Architecture Decision Records (ADRs)

Keep your ADRs in docs/adr/. Each file should follow this template:
```
# ADR <YYYY‑MM‑DD>: Title of Decision

## Context
What problem or choice are we addressing?

## Decision
What did we choose?

## Consequences
What trade‑offs does this introduce?
```
## 🤝 Contributing
1. Fork the repo 
2. Create a branch off develop 
3. Follow Development Workflow above 
4. Open a Pull Request

## License
MIT © SpongeBall-GumPants
```

**How to use this template for RDD**  
1. **Before** writing any code for a new feature, **check or add** its item under **📝 Feature Checklist** (and write its acceptance criteria in README).  
2. **Then** update any relevant section—e.g. add new API Reference rows, new setup steps, or new test commands.  
3. **Finally**, implement the feature so that the README instructions actually work when someone follows them.  

This ensures your docs always stay in sync with your code.
```

