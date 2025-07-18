# 📋 Requirements Analysis Template

This Requirements Specification Document defines requirements for the project, a Zettelkasten-inspired Personal Knowledge Management (PKM) tool. It aims to provide a clear, traceable foundation for design, implementation, and validation, ensuring that all stakeholders share a common understanding of the system’s intended behavior and quality.

---

## 1. Identification & Stakeholder Viewpoints

**1.1. Primary (Interactor) Viewpoints**  

- **End User / Knowledge Worker**: creates, edits, links, tags, and visualizes notes.
    
- **Project Administrator**: manages deployments, monitors system health.
    

**1.2. Secondary (Indirect) Viewpoints**

- **DevOps / DBA**: installs, configures, and maintains PostgreSQL/MongoDB, Neo4j, and CI/CD pipelines.
    
- **Test Engineer**: writes and runs unit/integration tests.
    

**1.3. Domain Viewpoints**

- **PKM Expert**: defines Zettelkasten conventions (atomicity, linking semantics).
    
- **Security Officer**: ensures authentication, data privacy, and compliance.

---

## 2. Viewpoint Hierarchy

![[Pasted image 20250718180237.png]]

---

## 3. Requirements

3.1. Functional Requirements (FR)

1. **FR-1:** User registration & authentication (OAuth or username/password).
    
2. **FR-2:** CRUD APIs for notes (RESTful endpoints).
    
3. **FR-3:** Tag management: create, delete, assign tags to notes.
    
4. **FR-4:** Link management: create, retrieve “LINKS_TO” relationships with context.
    
5. **FR-5:** Neo4j storage for notes, tags, links; PostgreSQL/MongoDB for user data.
    
6. **FR-6:** Graph-query APIs: fetch direct neighbors, notes by tag.
    
7. **FR-7:** Interactive frontend visualization using Cytoscape.js or Sigma.js.
    
8. **FR-8:** Unit and integration tests for all core backend logic.
    
9. **FR-9:** CI/CD pipeline for linting, testing, and deploy.
    
10. **FR-10:** Full-text search over notes content.
	
11. FR-11: User profile and settings.

### 3.2. Non-Functional Requirements (NFR)

- **NFR-1 (Performance):** Note retrieval (≤100 notes) under 200 ms.
    
- **NFR-2 (Scalability):** Support up to 10 000 notes per user without significant slow-down.
    
- **NFR-3 (Security):** Passwords hashed (bcrypt), all APIs over HTTPS.
    
- **NFR-4 (Usability):** Graph UI should allow zoom/pan and node-click detail view.
    
- **NFR-5 (Maintainability):** Code coverage ≥80%; clear module separation (MVC/MVP).
    
- **NFR-6 (Availability):** 99.5% uptime of core services.
    

### 3.3. Domain Requirements (DR)

- **DR-1:** Notes must follow “atomic” principle: one idea per note.
    
- **DR-2:** Links must store context metadata (“why”/“how”).
    
- **DR-3:** Tags are nodes in the graph; HAS_TAG relationships must be normalized.
    
- **DR-4:** Unique Note IDs must be stable (e.g., ULID/UUID).


---

## 4. MoSCoW Prioritization

Prioritize requirements into four categories:

- **MUST have**: Critical for MVP (e.g., R-F-1, R-F-2).
    
- **SHOULD have**: Important but not critical (e.g., tagging system).
    
- **COULD have**: Nice-to-have if time permits (e.g., graph analytics).
    
- **WON’T have**: Out-of-scope for current release (e.g., mobile app).
    

| Category   | Requirement IDs                                                      |
| ---------- | -------------------------------------------------------------------- |
| **Must**   | FR-1, FR-2, FR-3, FR-4, FR-5, NFR-3, DR-1, DR-2, US-01…US-06         |
| **Should** | FR-6, FR-7, NFR-1, NFR-5, US-07, DR-3                                |
| **Could**  | FR-8, FR-9, FR-10, NFR-2, US-08, US-09                               |
| **Won’t**  | Cloud deployment (Phase 2+), user profiles beyond basic settings now |

---

## 5. Negotiation & Conflict Resolution

- **Conflict**: Fast API queries vs. rich graph analytics may slow responses.
    
- **Negotiation Strategy**: Defer heavy analytics to background tasks; cache results.
    
- **Decision Log**: Record trade-offs and agreed compromises in ADRs.
    

---

## 6. Risk Management

Maintain a **Risk Register** to track potential issues.

| ID  | Risk Description                              | Type           | Probability (L/M/H) | Impact (L/M/H) | Mitigation                                    |
| --- | --------------------------------------------- | -------------- | ------------------- | -------------- | --------------------------------------------- |
| R-1 | Data inconsistency between PostgreSQL & Neo4j | Data Integrity | M                   | H              | Use transactional scripts; batch sync         |
| R-2 | CORS misconfiguration blocking frontend       | Security       | L                   | M              | Configure middleware; include in CI tests     |
| R-3 | OneDrive file-lock conflicts in dev           | Operational    | M                   | L              | Use Docker volumes; avoid editing in OneDrive |
| R-4 | High vulnerability count in npm packages      | Security       | H                   | M              | Regular `npm audit` in CI; update deps        |

---

## 7. Core Use Cases
### Use Case 1: Create, Read, Update, Delete an Atomic Note

**Description:**  
Manage the lifecycle of a single, self-contained (“atomic”) note: create new ideas, view existing ones, edit content, or delete when obsolete.

**Trigger:**  
User clicks “New Note,” selects an existing note to view/edit, or hits “Delete” on a note.

#### Actors

- **End User** (note author)
    
- **System**
    

#### Preconditions

1. User is authenticated (session token valid).
    
2. Backend services (PostgreSQL/MongoDB and Neo4j) are online.
    
3. Editor UI is loaded.
    

#### Postconditions

- On create/update: note stored in relational store and as a Neo4j node; unique ID assigned or preserved.
    
- On delete: note removed from relational store and graph; all relationships cleaned up.
    
- UI list of notes refreshes.
    

#### Inputs

- Note title (non-empty string)
    
- Note content (Markdown)
    
- Optional tags (comma-separated)
    
- For update/delete: Note ID
    

#### Main Flow (Create)

1. **User** clicks “New Note.”
    
2. Editor opens with empty Title & Content fields.
    
3. **User** enters title, content, and tags.
    
4. **User** clicks “Save.”
    
5. **System** validates:
    
    - Title ≠ blank
        
    - Content ≤ allowed size (e.g. 100 KB)
        
6. **System** generates UUID, writes to PostgreSQL/MongoDB, and creates a `(:Note {id, title, created, modified})` in Neo4j.
    
7. **System** returns success; UI shows the new note in the list.
    

#### Main Flow (Read)

1. **User** selects a note from the list.
    
2. **System** fetches note metadata from SQL and content from Neo4j (or vice versa).
    
3. **System** displays note in read-only mode.
    

#### Main Flow (Update)

1. **User** opens existing note in editor.
    
2. **User** modifies title/content/tags.
    
3. **User** clicks “Save.”
    
4. **System** re-validates, updates modified timestamp, persists changes in both stores.
    

#### Main Flow (Delete)

1. **User** clicks “Delete” on a note.
    
2. **System** prompts “Are you sure?”
    
3. On confirm, **System** deletes record from SQL/NoSQL, removes node and all `LINKS_TO`/`HAS_TAG` relationships in Neo4j.
    

#### Alternate Flows

- **AF-1: Validation Error:** Blank title or too-long content → show inline error, abort save.
    
- **AF-2: Network/DB Failure:** Write fails → retry twice, then display “Error saving note” with “Try again” button.
    

#### Outputs

- Confirmation toast (“Note saved.” / “Note deleted.”)
    
- Updated note list in sidebar.
    

#### Exceptions

- **E-1:** Duplicate title allowed (notes distinguished by ID), but warn if title already exists.
    
- **E-2:** If Neo4j node creation fails after SQL write, roll back SQL write and notify user.
    

#### Special Requirements

- **Uniqueness:** IDs must be ULIDs/UUIDs to avoid collisions.
    
- **Performance:** Create/update/delete round-trip < 300 ms.
    
- **Security:** All endpoints require valid JWT; inputs sanitized to prevent XSS/NoSQL injection.
    

---

### Use Case 2: Link Two Notes with Context

**Description:**  
Establish a contextual relationship between two atomic notes, capturing the “why” or “how” behind their connection.

**Trigger:**  
While editing a note, user invokes “Add Link” or types internal link syntax (e.g. `[[`).

#### Actors

- **End User**
    
- **System**
    

#### Preconditions

1. Both source and target notes already exist.
    
2. User is editing the source note in the editor.
    
3. Neo4j service reachable.
    

#### Postconditions

- A `(:Note {source})-[:LINKS_TO {context}]->(:Note {target})` relationship exists in Neo4j.
    
- Editor displays a clickable link; graph visualization will include this edge.
    

#### Inputs

- Source Note ID (current editing note)
    
- Target Note ID or title lookup
    
- Link context (free-text explanation, ≤ 500 chars)
    

#### Main Flow

1. **User** highlights text or types `[[` to open “Link Note” dialog.
    
2. **System** shows searchable list of existing notes.
    
3. **User** selects a target note and enters link context (“because X leads to Y”).
    
4. **User** clicks “Add Link.”
    
5. **System** validates:
    
    - Source ≠ Target
        
    - Context not blank
        
6. **System** issues Cypher:
		```MATCH (s:Note {id: $source}), (t:Note {id: $target})
		MERGE (s)-[r:LINKS_TO]->(t)
		SET r.context = $context, r.created = timestamp()```
		
7. **System** returns success; editor shows `[[TargetNoteTitle]]` with tooltip of context.
    

#### Alternate Flows

- **AF-1: Target Not Found:** User enters free text not matching any note → offer “Create new note” inline.
    
- **AF-2: Duplicate Link:** If relationship already exists, prompt “Link already exists—update context?”
    

#### Outputs

- Visual inline link in note body.
    
- New edge visible in graph view.
    

#### Exceptions

- **E-1: Neo4j Down:** If graph DB unavailable, queue link creation in local cache and retry on next save.
    
- **E-2: Context Too Long:** If context > 500 chars, truncate with warning.
    

#### Special Requirements

- **Atomicity:** Both SQL update of note body and Neo4j link creation must happen in one logical transaction (or compensate on failure).
    
- **Latency:** Link creation round-trip < 500 ms.
    
- **Usability:** Link dialog must filter results as user types; show note snippet for clarity.
    

---

### Use Case 3: Visualize & Explore the Knowledge Graph

**Description:**  
Render an interactive graph of notes and links, allowing the user to navigate, filter, and inspect relationships.

**Trigger:**  
User clicks “Graph View” or the graph icon in the UI.

#### Actors

- **End User**
    
- **System**
    

#### Preconditions

1. At least one `Note` node and one `LINKS_TO` relationship exist in Neo4j.
    
2. Cytoscape.js (or Sigma.js) library loaded client-side.
    
3. Graph-query API reachable.
    

#### Postconditions

- Graph is displayed; user can pan/zoom, select nodes to see details.
    
- User can apply filters (by tag, date, centrality threshold).
    

#### Inputs

- Optional:
    
    - **Root Note ID** (focus on a subgraph)
        
    - **Tag filter** set (one or more tags)
        
    - **Depth** (e.g., 1–3 hops)
        

#### Main Flow

1. **User** opens Graph View; system shows default “all notes” graph, limited to N nodes (e.g., 100).
    
2. **User** optionally enters a root Note ID or selects a tag from dropdown.
    
3. **System** calls API:
    
    - `GET /api/graph?root=$id&tags=$tags&depth=$d`
        
4. **System** returns JSON payload of nodes (`{id, title, tagList}`) and edges (`{source, target, context}`).
    
5. Client configures Cytoscape: adds nodes with labels, colors by tag; adds edges with hoverable context.
    
6. **User** pans/zooms; clicks a node.
    
7. **System** fetches full note content for that node and displays it in a side panel.
    

#### Alternate Flows

- **AF-1: Large Graph:** If node count > 500, system prompts “Too many nodes—please apply a filter or reduce depth.”
    
- **AF-2: Tag-Only View:** User selects only a tag → system returns all notes & links where `HAS_TAG` includes that tag, ignoring others.
    

#### Outputs

- Interactive canvas showing nodes and edges.
    
- Side panel with note details on node click.
    
- Legend mapping tag colors.
    

#### Exceptions

- **E-1: Query Timeout:** If graph query > 2 s, return partial result with warning “Partial graph—results truncated.”
    
- **E-2: Rendering Error:** If client fails to render (e.g., out of memory), fall back to a paginated list view of notes and links.
    

#### Special Requirements

- **Performance:** Initial render for up to 100 nodes < 1 s.
    
- **Accessibility:** Keyboard navigation through nodes; ARIA labels for screen readers.
    
- **Scalability:** Support incremental graph loading (infinite pan/zoom) for very large graphs.
---

## 8. References & Glossary

- **MoSCoW**: Must/Should/Could/Won’t prioritization model.
    
- **ADRs**: Architecture Decision Records, stored in `docs/adr/`.
    
- **WCAG**: Web Content Accessibility Guidelines.

---
