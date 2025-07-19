# Authentication Register

## Context
We need a secure, standards-based user authentication mechanism for Synapse:
- Register new users with username, email, and password.
- Login with credentials to establish a session or token.

## Decision
- **Password hashing**: use `passlib[bcrypt]` for salted hashing.
- **Routes**: mount under `/auth`:
  - `POST /auth/register`
  - `POST /auth/login`
- **Data model**: SQLModel `User` table contains `hashed_password`; API never returns it.

## Consequences
- Strong password hashes
- Clear separation of auth‑related routes
- External dependency (`passlib[bcrypt]`)