# Scripture AI - Feature Roadmap & Extension Guide

## Current Features (Already Implemented)

### ✅ Core Scripture Database
- 31,102 KJV verses
- 8,281 Hebrew words with Strong's numbers
- Full-text search
- Word-to-verse relationships with position tracking

### ✅ API Endpoints
- `GET /api/verses` - List verses with pagination
- `GET /api/verses/search?query=...` - Search by text
- `GET /api/verses/{id}` - Get verse with words and definitions
- `GET /api/verses/reference/{book}/{chapter}/{verse}` - Search by reference
- `GET /api/verses/strongs/{id}` - Find all verses with a word

### ✅ Database Schema
- Verse, Lexicon, VerseWordLink tables
- User, Note, StudySession tables (schema defined, endpoints TODO)
- Proper foreign keys and relationships
- word_index for tracking word positions

---

## Coming Soon (Partially Implemented)

### 🔄 User Authentication
**Status:** Code written, not integrated yet

**What to do:**
1. Update `main.py` to include auth routes:
```python
from app.routes import auth as auth_routes
app.include_router(auth_routes.router, prefix="/api", tags=["auth"])
```

2. Endpoints that will work:
   - `POST /api/auth/register` - Create account
   - `POST /api/auth/login` - Get token
   - `GET /api/auth/me` - Get user info
   - `POST /api/auth/refresh` - Refresh token
   - `DELETE /api/auth/account` - Delete account

### 🔄 Personal Notes System
**Status:** Code written, not integrated yet

**What to do:**
1. Update `main.py` to include notes routes:
```python
from app.routes import notes as notes_routes
app.include_router(notes_routes.router, prefix="/api", tags=["notes"])
```

2. Endpoints that will work:
   - `POST /api/notes/` - Create note
   - `GET /api/notes/` - Get user's notes
   - `GET /api/notes/{id}` - Get specific note
   - `PUT /api/notes/{id}` - Update note
   - `DELETE /api/notes/{id}` - Delete note
   - `POST /api/notes/search` - Search notes
   - `GET /api/notes/stats` - User statistics

---

## Planned Features (Not Yet Implemented)

### 1. Semantic Search (Medium Difficulty)

**What it does:** Search by meaning, not just text

**Technologies:**
- `sentence-transformers` (already in requirements.txt)
- FAISS for vector search
- PostgreSQL pgvector extension (optional)

**Implementation Steps:**

```python
# app/embeddings.py
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for each verse
embeddings = model.encode(verse.text_content)

# Store in database (or separate FAISS index)
# Later: search by similarity
```

**API Endpoint:**
```
POST /api/verses/search-semantic
{
  "query": "creation of the world",
  "limit": 10
}
```

**Difficulty:** Medium (3-4 hours)  
**Impact:** Huge - much better search experience

---

### 2. AI Question Answering (Hard)

**What it does:** Ask "What does the Bible say about love?" and get answer with verses

**Technologies:**
- OpenAI API (or open source LLM)
- RAG (Retrieval-Augmented Generation)
- Semantic search (from feature #1)

**Implementation Steps:**

```python
# app/rag.py
from openai import OpenAI

def answer_question(question: str, verses: List[Verse]) -> str:
    """
    1. Get relevant verses using semantic search
    2. Build context from verses
    3. Ask LLM to answer based on context
    4. Return answer with verse references
    """
    
    # Step 1: Semantic search
    relevant_verses = semantic_search(question)
    
    # Step 2: Build context
    context = "\n\n".join([
        f"{v.reference}: {v.text_content}"
        for v in relevant_verses
    ])
    
    # Step 3: Ask OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a Bible scholar..."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    
    return response.choices[0].message.content
```

**API Endpoint:**
```
POST /api/ai/ask
{
  "question": "What does the Bible say about love?"
}
```

**Difficulty:** Hard (8-10 hours)  
**Impact:** Revolutionary - AI-powered Bible study  
**Cost:** ~$0.01-0.10 per question (if using OpenAI)

---

### 3. Word Study Tools (Medium)

**What it does:** Deep analysis of Hebrew/Greek words

**Features:**
- Compare word usage across Bible
- See word frequency
- Word etymology (if available)
- Related words

**Implementation:**

```python
# app/routes/words.py
@app.get("/api/words/{strongs_id}/analysis")
def analyze_word(strongs_id: str, session: Session = Depends(get_session)):
    """
    Return comprehensive word analysis
    """
    
    word = session.get(Lexicon, strongs_id)
    occurrences = get_occurrences(strongs_id)
    
    return {
        "strongs_id": strongs_id,
        "hebrew_word": word.hebrew_word,
        "definition": word.definition,
        "total_occurrences": len(occurrences),
        "books": get_books_with_word(occurrences),
        "verses": occurrences
    }
```

**Difficulty:** Easy (2-3 hours)  
**Impact:** High - useful for study

---

### 4. Reading Plans (Easy)

**What it does:** Structured Bible reading schedules

**Features:**
- Pre-made plans (daily, 30-day, etc.)
- Track progress per user
- Reminders

**Implementation:**

```python
# Database
class ReadingPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    verses: List[int]  # JSON list of verse IDs
    
class UserProgress(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id")
    plan_id: int = Field(foreign_key="reading_plan.id")
    current_position: int
    started_at: datetime
```

**Difficulty:** Easy (2-3 hours)  
**Impact:** Medium - helps user engagement

---

### 5. Cross-References (Medium)

**What it does:** Show related verses

**Features:**
- Manual cross-references
- Automatic semantic matching
- Commentary links

**Implementation:**

```python
class CrossReference(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    from_verse_id: int = Field(foreign_key="verse.id")
    to_verse_id: int = Field(foreign_key="verse.id")
    type: str  # "similar_topic", "quote", "prophecy_fulfillment"
    description: str
```

**Difficulty:** Medium (4-5 hours)  
**Impact:** Medium - enriches study

---

### 6. Commentary Integration (Hard)

**What it does:** Add scholar commentaries to verses

**Features:**
- Integrate public domain commentaries
- Allow user comments
- Voting on helpful comments

**Commentaries available:**
- Matthew Henry's Commentary
- Pulpit Commentary
- Ellicott's Commentary

**Implementation:**

```python
class Commentary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    verse_id: int = Field(foreign_key="verse.id")
    source: str  # "matthew_henry", "pulpit", etc.
    text: str
    author: str
```

**Difficulty:** Hard (12-15 hours)  
**Impact:** High - professional study tool

---

## Quick Start: Enable Auth & Notes

### Step 1: Update main.py

Replace this section:
```python
# ============= INCLUDE ROUTES =============

# Include verse routes
app.include_router(
    verses_routes.router,
    prefix="/api",
    tags=["verses"]
)
```

With:
```python
# ============= INCLUDE ROUTES =============

# Include verse routes
app.include_router(
    verses_routes.router,
    prefix="/api",
    tags=["verses"]
)

# Include auth routes
from app.routes import auth as auth_routes
app.include_router(
    auth_routes.router,
    prefix="/api",
    tags=["auth"]
)

# Include notes routes
from app.routes import notes as notes_routes
app.include_router(
    notes_routes.router,
    prefix="/api",
    tags=["notes"]
)
```

### Step 2: Restart server

```bash
python main.py
```

### Step 3: Test in Swagger UI

Visit `http://localhost:8000/docs` and you'll see:
- `/api/auth/register`
- `/api/auth/login`
- `/api/auth/me`
- `/api/notes/`
- `/api/notes/search`
- etc.

---

## Feature Implementation Priority Matrix

| Feature | Difficulty | Impact | Time | Priority |
|---------|-----------|--------|------|----------|
| Enable Auth & Notes | Easy | Medium | 10 min | 🔴 **Do First** |
| Word Study Tools | Easy | High | 2-3 hrs | 🔴 **High** |
| Reading Plans | Easy | Medium | 2-3 hrs | 🟡 **Medium** |
| Semantic Search | Medium | Huge | 4-5 hrs | 🔴 **High** |
| Cross-References | Medium | Medium | 4-5 hrs | 🟡 **Medium** |
| AI Question Answering | Hard | Huge | 8-10 hrs | 🔴 **High** |
| Commentary Integration | Hard | High | 12-15 hrs | 🟡 **Medium** |

---

## Estimated Feature Timeline

### Week 1: Polish Core
- Enable Auth & Notes (10 min)
- Add Word Study Tools (2-3 hrs)
- Fix edge cases and bugs (1-2 hrs)

### Week 2: Advanced Search
- Implement Semantic Search (4-5 hrs)
- Add related verses/cross-refs (2-3 hrs)
- Testing and optimization (2-3 hrs)

### Week 3+: AI & Polish
- AI Question Answering (8-10 hrs)
- Commentary integration (optional, 12-15 hrs)
- Frontend UI (10-20 hrs)
- Production deployment

---

## External Resources

### Open Source Commentaries
- https://github.com/openbibleinfo/Bible-datasets
- https://github.com/scrollmapper/bible_databases
- Project Gutenberg (public domain commentaries)

### LLM Options
- OpenAI API ($0.01-0.05 per request)
- HuggingFace Models (free, self-hosted)
- LLaMA 2 (free, open source)
- Claude API (more powerful)

### Embeddings
- Sentence-Transformers (already in requirements)
- OpenAI Embeddings (paid)
- Cohere Embeddings (free tier available)

### Vector Search
- FAISS (free, CPU-based)
- Pinecone (paid, cloud-based)
- Weaviate (open source, cloud available)
- pgvector (PostgreSQL extension, free)

---

## Common Extension Patterns

### Adding New Endpoints
```python
# app/routes/new_feature.py
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session

router = APIRouter(prefix="/new-feature", tags=["new-feature"])

@router.get("/{id}")
def get_something(id: int, session: Session = Depends(get_session)):
    # Your code here
    return {}
```

Then in `main.py`:
```python
from app.routes import new_feature
app.include_router(new_feature.router, prefix="/api")
```

### Adding Models to Database
```python
# app/models.py
class NewModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Your fields
```

Existing models are auto-created on startup via:
```python
SQLModel.metadata.create_all(engine)
```

### Adding Authentication to Endpoints
```python
from app.routes.auth import get_current_user
from app.models import User

@router.get("/protected")
def protected_endpoint(user: User = Depends(get_current_user)):
    # Only authenticated users can access
    return {"user": user.email}
```

---

## You're Ready to Extend!

Your foundation is solid. Pick a feature and build it!

Recommended order:
1. ✅ Enable Auth & Notes (10 minutes)
2. 📊 Add Word Study Tools (3 hours)
3. 🔍 Implement Semantic Search (5 hours)
4. 🤖 Add AI Question Answering (10 hours)

Good luck! 🚀
