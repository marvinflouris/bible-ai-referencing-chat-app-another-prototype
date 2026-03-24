# Scripture AI - Bible Study Application

A Python FastAPI application for studying the Bible with Hebrew/Greek word analysis using Strong's numbers.

## Features

- 📖 Complete KJV Bible with 31,102 verses
- 🏷️ Strong's number linking for Hebrew/Greek words
- 🔍 Full-text search and word lookup
- 👤 User authentication with JWT
- 📝 Personal notes on verses
- 📊 Study session tracking
- 🚀 REST API with automatic Swagger documentation

## Architecture

```
scripture-ai/
├── .env                    # Environment variables (DO NOT COMMIT)
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
├── main.py               # FastAPI entry point
├── seed_bible.py         # Load Bible data (run once)
└── app/
    ├── __init__.py       # Package initialization
    ├── config.py         # Configuration
    ├── database.py       # Database connection
    ├── models.py         # SQLModel schemas
    ├── seed.py           # Seeding functions
    └── routes/
        ├── __init__.py
        ├── verses.py     # Verse endpoints
        ├── auth.py       # Authentication endpoints
        └── notes.py      # Notes endpoints
```

## Setup

### 1. Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Git

### 2. Create Project Structure

```bash
mkdir scripture-ai
cd scripture-ai
mkdir app app/routes
```

### 3. Create Files

Copy all the files from above into your project structure:

```
.env
.gitignore
requirements.txt
main.py
seed_bible.py
app/__init__.py
app/config.py
app/database.py
app/models.py
app/seed.py
app/routes/__init__.py
app/routes/verses.py
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Database

Edit `.env` with your PostgreSQL credentials:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/scripture_db
```

Create the database:

```bash
psql -U postgres -c "CREATE DATABASE scripture_db;"
```

### 6. Download Bible Data

Download `kjv_with_strongs.json` from:
https://github.com/openbibleinfo/Bible-datasets

Place it in your project root directory.

### 7. Load Bible Data

Run the seeding script (takes 1-2 minutes):

```bash
python seed_bible.py
```

Output should show:
```
✓ Parsed 31102 verses
✓ Extracted 8281 unique Strong's IDs
✓ Created 783,137 word links
✓ DATABASE SEEDING COMPLETE!
```

### 8. Start Server

```bash
python main.py
```

Visit: **http://localhost:8000/docs**

You'll see interactive Swagger documentation for all API endpoints.

## API Endpoints

### Verses

#### List Verses
```
GET /api/verses?skip=0&limit=10
```

#### Search Verses
```
GET /api/verses/search?query=God
```

#### Get Verse by ID
```
GET /api/verses/1
```

Returns:
```json
{
  "id": 1,
  "reference": "Genesis 1:1",
  "text": "In the beginning God created the heavens and the earth.",
  "words": [
    {
      "word_index": 0,
      "word_text": "In",
      "strongs_id": "H853",
      "definition": "marker of object",
      "hebrew_word": "את",
      "transliteration": "et"
    },
    ...
  ]
}
```

#### Get Verse by Reference
```
GET /api/verses/reference/Genesis/1/1
```

#### Get All Verses with a Word
```
GET /api/verses/strongs/H430
```

Returns all verses containing "God" (H430):
```json
{
  "strongs_id": "H430",
  "definition": "God, gods",
  "hebrew_word": "אלהים",
  "transliteration": "elohim",
  "occurrences": 2312,
  "verses": [...]
}
```

## Database Schema

### Verse
- `id` (PK): Auto-incremented ID
- `reference`: Book Chapter:Verse (e.g., "Genesis 1:1")
- `text_content`: Full verse text (without Strong's codes)

### Lexicon
- `strongs_id` (PK): Strong's number (e.g., "H430")
- `hebrew_word`: Hebrew/Greek word
- `transliteration`: Latin transliteration
- `definition`: Word definition

### VerseWordLink (Junction Table)
- `verse_id` (FK, PK): References Verse
- `strongs_id` (FK, PK): References Lexicon
- `word_index` (PK): Position in verse (0, 1, 2, ...)
- `word_text`: The actual word from verse

The composite primary key `(verse_id, strongs_id, word_index)` ensures:
- Same word can appear multiple times in a verse (different index)
- Exact position of each word is preserved
- No duplicate links

### User
- `id` (PK): Auto-incremented ID
- `email` (unique): User email
- `hashed_password`: Hashed password
- `created_at`: Account creation timestamp

### Note
- `id` (PK): Auto-incremented ID
- `user_id` (FK): References User
- `verse_id` (FK): References Verse
- `content`: Note text
- `created_at`: Note creation timestamp
- `updated_at`: Last update timestamp

### StudySession
- `id` (PK): Auto-incremented ID
- `user_id` (FK): References User
- `verse_id` (FK): References Verse
- `studied_at`: When studied
- `duration_seconds`: How long studied

## Example Queries

### Get Genesis 1:1 with All Words

```python
from sqlmodel import Session, select
from app.database import create_session
from app.models import Verse, VerseWordLink, Lexicon

session = create_session()

# Get the verse
verse = session.exec(
    select(Verse).where(Verse.reference == "Genesis 1:1")
).first()

print(f"{verse.reference}: {verse.text_content}\n")

# Get all words in order
for link in sorted(verse.word_links, key=lambda w: w.word_index):
    print(f"Word {link.word_index}: '{link.word_text}' → {link.strongs_id}")
    print(f"  Definition: {link.lexicon.definition}")
```

### Find All Verses with "God" (H430)

```python
god_word = session.get(Lexicon, "H430")

print(f"'{god_word.hebrew_word}' appears in {len(god_word.links)} verses:\n")

for link in god_word.links[:5]:
    print(f"{link.verse.reference}: {link.word_text}")
```

### Search Verses with Full Text

```python
from sqlalchemy import func

results = session.exec(
    select(Verse).where(
        Verse.text_content.ilike("%God%")
    ).limit(10)
).all()

for verse in results:
    print(f"{verse.reference}: {verse.text_content}")
```

## Next Steps

1. **Add Authentication Routes** (`app/routes/auth.py`)
   - User registration
   - Login with JWT tokens
   - Token refresh

2. **Add Notes Endpoints** (`app/routes/notes.py`)
   - Create/read/update/delete notes
   - Get user's notes
   - Get notes for a verse

3. **Implement AI Features**
   - Semantic search using embeddings
   - RAG (Retrieval-Augmented Generation)
   - Bible question answering

4. **Add Frontend**
   - React/Vue application
   - Verse reader interface
   - Note-taking UI

## Troubleshooting

### "kjv_with_strongs.json not found"
- Download from: https://github.com/openbibleinfo/Bible-datasets
- Place in project root directory

### "database scripture_db does not exist"
- Create with: `psql -U postgres -c "CREATE DATABASE scripture_db;"`
- Update DATABASE_URL in .env

### "psycopg2 connection refused"
- Check PostgreSQL is running
- Verify credentials in .env
- Test with: `psql -U postgres -h localhost`

### Port 8000 already in use
- Change PORT in .env to another port (e.g., 8001)
- Or kill existing process: `lsof -ti:8000 | xargs kill -9`

## Development

### Enable SQL Debug Logging

In `app/database.py`, change:
```python
engine = create_engine(settings.DATABASE_URL, echo=False)
```

To:
```python
engine = create_engine(settings.DATABASE_URL, echo=True)
```

### Run Tests

```bash
pytest tests/
```

### Format Code

```bash
black .
isort .
```

## Deployment

For production deployment:

1. Set `ENV=production` in `.env`
2. Generate strong `SECRET_KEY`: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
3. Use PostgreSQL with backups
4. Deploy with Gunicorn/Uvicorn
5. Use Nginx as reverse proxy
6. Enable HTTPS with SSL certificate

Example Gunicorn command:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app
```

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [link]
- Documentation: [link]
- Discord Community: [link]

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

Made with ❤️ for Bible students and developers
