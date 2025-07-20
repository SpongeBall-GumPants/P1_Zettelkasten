# CRUD API Design

## Context

We need stateless REST endpoints to allow **authenticated** users to create, read, update, and delete their individual notes. Each note is an atomic piece of information tied to a single user.

## Decision

- **Router prefix**: `/notes`
    
- **HTTP Methods & Endpoints**:
    
    - `POST /notes` – Create a new note
        
    - `GET /notes` – List all notes for the authenticated user
        
    - `GET /notes/{id}` – Retrieve a single note by its unique ID
        
    - `PUT /notes/{id}` – Update an existing note
        
    - `DELETE /notes/{id}` – Delete a note by its ID
        
- **Python Schemas**:
    
    - `NoteCreate`:
        
        ```
        class NoteCreate(BaseModel):
            title: str
            content: str
        ```
        
    - `NoteRead`:
        
        ```
        class NoteRead(NoteCreate):
            id: int
            created_at: datetime
            updated_at: datetime
            user_id: int
        ```
        
- **Authentication**: Use existing JWT Bearer token.
    
- **Storage**:
    
    - SQLModel `Note` table with fields:
        
        - `id: int` (PK)
            
        - `title: str`
            
        - `content: str`
            
        - `created_at: datetime`
            
        - `updated_at: datetime`
            
        - `user_id: int` (FK → User.id)
            

## Consequences

- **Pros**:
    
    - Uniform, predictable RESTful pattern.
        
    - Leverage existing JWT-based auth infrastructure.
        
    - Simple separation of concerns between authentication and note-taking logic.
        
- **Cons**:
        
    - Must ensure proper error handling for 404 and permission checks (note ownership).
        