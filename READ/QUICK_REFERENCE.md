# Scripture AI - Quick Reference Card

## Your Project Structure

```
scripture-ai/                          ← PROJECT ROOT
│
├── .env                               ← Database credentials (COPY: .env)
├── .gitignore                         ← Git rules (COPY: .gitignore)
├── requirements.txt                   ← Dependencies (COPY: requirements.txt)
├── main.py                            ← FastAPI app (COPY: main.py)
├── seed_bible.py                      ← Load Bible (COPY: seed_bible.py)
├── kjv_with_strongs.json             ← DOWNLOAD from GitHub
│
└── app/                               ← Create this folder
    ├── __init__.py                    ← (COPY: app_init.py, rename to __init__.py)
    ├── config.py                      ← (COPY: app_config.py)
    ├── database.py                    ← (COPY: app_database.py)
    ├── models.py                      ← (COPY: app_models.py)
    ├── seed.py                        ← (COPY: app_seed.py)
    │
    └── routes/                        ← Create this folder
        ├── __init__.py                ← (COPY: app_routes_init.py, rename)
        └── verses.py                  ← (COPY: app_routes_verses.py)
```

---

## All Files You Have

### Root Level (Copy to project root)
1. ✅ **`.env`** - Environment variables
2. ✅ **`.gitignore`** - Git ignore file
3. ✅ **`requirements.txt`** - Dependencies
4. ✅ **`main.py`** - FastAPI application
5. ✅ **`seed_bible.py`** - Load Bible data
6. 📥 **`kjv_with_strongs.json`** - Download from GitHub

### App Folder (Copy to app/)
7. ✅ **`app/__init__.py`** - Copy `app_init.py` and rename
8. ✅ **`app/config.py`** - Copy `app_config.py`
9. ✅ **`app/database.py`** - Copy `app_database.py`
10. ✅ **`app/models.py`** - Copy `app_models.py`
11. ✅ **`app/seed.py`** - Copy `app_seed.py`

### Routes Folder (Copy to app/routes/)
12. ✅ **`app/routes/__init__.py`** - Copy `app_routes_init.py` and rename
13. ✅ **`app/routes/verses.py`** - Copy `app_routes_verses.py`

---

## File Purposes (What Each Does)

### Entry Points
| File | Purpose |
|------|---------|
| `main.py` | Run FastAPI server (`python main.py`) |
| `seed_bible.py` | Load Bible data once (`python seed_bible.py`) |

### Configuration
| File | Purpose |
|------|---------|
| `.env` | Database credentials & settings |
| `app/config.py` | Load settings from .env |

### Database
| File | Purpose |
|------|---------|
| `app/database.py` | PostgreSQL connection & sessions |
| `app/models.py` | Database schema (Verse, Lexicon, etc.) |
| `app/seed.py` | Functions to load Bible data |

### API
| File | Purpose |
|------|---------|
| `app/routes/verses.py` | Bible verse endpoints |

### Package Setup
| File | Purpose |
|------|---------|
| `app/__init__.py` | Make app a Python package |
| `app/routes/__init__.py` | Make routes a Python package |

---

## Setup Steps (Copy-Paste Ready)

### 1. Create Folders
```bash
mkdir scripture-ai
cd scripture-ai
mkdir app app/routes
```

### 2. Copy Files
Copy from outputs folder to your project:

**Root files:**
```bash
cp .env scripture-ai/
cp .gitignore scripture-ai/
cp requirements.txt scripture-ai/
cp main.py scripture-ai/
cp seed_bible.py scripture-ai/
```

**App files:**
```bash
cp app_init.py scripture-ai/app/__init__.py
cp app_config.py scripture-ai/app/config.py
cp app_database.py scripture-ai/app/database.py
cp app_models.py scripture-ai/app/models.py
cp app_seed.py scripture-ai/app/seed.py
```

**Routes files:**
```bash
cp app_routes_init.py scripture-ai/app/routes/__init__.py
cp app_routes_verses.py scripture-ai/app/routes/verses.py
```

### 3. Install & Setup
```bash
cd scripture-ai
pip install -r requirements.txt
# Download kjv_with_strongs.json and place here
python seed_bible.py
```

### 4. Run
```bash
python main.py
# Visit: http://localhost:8000/docs
```

---

## Important Files to Remember

### Edit This (Change Credentials)
- **`.env`** - Update `DATABASE_URL` with your PostgreSQL password

### Don't Commit These
- **`.env`** - Contains secret credentials
- **`kjv_with_strongs.json`** - Too large
- **`__pycache__/`** - Python cache

### Check These for Reference
- **`README.md`** - Full documentation
- **`SETUP_SUMMARY.md`** - Detailed setup
- **`COMPLETE_PROJECT_STRUCTURE.docx`** - Code content

---

## Quick Commands

| Command | Purpose |
|---------|---------|
| `pip install -r requirements.txt` | Install dependencies |
| `python seed_bible.py` | Load Bible data (run once) |
| `python main.py` | Start server |
| `curl http://localhost:8000/health` | Check if running |
| `http://localhost:8000/docs` | Swagger documentation |

---

## API Endpoints (Ready to Use)

```
GET  /api/verses                          List all verses
GET  /api/verses/search?query=God         Search verses
GET  /api/verses/1                        Get verse #1 (Genesis 1:1)
GET  /api/verses/reference/Genesis/1/1    Get by reference
GET  /api/verses/strongs/H430             Find all with Strong's #430
```

---

## Database Tables

| Table | Purpose | Key |
|-------|---------|-----|
| **verse** | Bible verses | id |
| **lexicon** | Hebrew/Greek words | strongs_id |
| **verse_word_link** | Word-to-verse mapping | (verse_id, strongs_id, word_index) |
| **user** | User accounts | id |
| **note** | User notes | id |
| **study_session** | Study tracking | id |

---

## What's Included

✅ Complete FastAPI application  
✅ PostgreSQL database setup  
✅ All 31,102 KJV verses ready to load  
✅ Strong's number linking (Hebrew/Greek words)  
✅ Verse search API  
✅ User authentication scaffolding  
✅ Notes system scaffolding  
✅ Complete documentation  

---

## What's NOT Included (Build These Next)

⚪ User authentication routes  
⚪ Notes CRUD endpoints  
⚪ Semantic search (embeddings)  
⚪ AI question answering (RAG)  
⚪ Frontend UI (React/Vue)  

---

## Need Help?

Check these files:
1. **SETUP_SUMMARY.md** - Detailed setup instructions
2. **README.md** - Complete documentation & examples
3. **COMPLETE_PROJECT_STRUCTURE.docx** - All code content
4. **QUICK_FILE_SETUP.docx** - Visual setup guide

---

## You're Ready! 🚀

All files are prepared. Just copy them to your project, run the setup, and start building!

Good luck with your Scripture AI project!
