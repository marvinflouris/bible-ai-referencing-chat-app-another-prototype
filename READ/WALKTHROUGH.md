# Scripture AI - Complete Step-by-Step Walkthrough

## Part 1: Download and Setup

### Step 1.1: Download All Files

1. Go to `/mnt/user-data/outputs/`
2. Download these files:
   - `.env`
   - `.gitignore`
   - `requirements.txt`
   - `main.py`
   - `seed_bible.py`
   - `app_init.py`
   - `app_config.py`
   - `app_database.py`
   - `app_models.py`
   - `app_seed.py`
   - `app_routes_init.py`
   - `app_routes_verses.py`

Also save these for reference:
   - `README.md`
   - `TESTING_GUIDE.md`
   - `SETUP_SUMMARY.md`
   - `QUICK_REFERENCE.md`

### Step 1.2: Create Project Folder

```bash
# Create project directory
mkdir scripture-ai
cd scripture-ai

# Create subfolders
mkdir app
mkdir app/routes
```

### Step 1.3: Copy Files to Correct Locations

**Root level files** (in `scripture-ai/`):
```bash
# Copy these files here
cp .env ./
cp .gitignore ./
cp requirements.txt ./
cp main.py ./
cp seed_bible.py ./
```

**App folder** (in `scripture-ai/app/`):
```bash
cp app_init.py ./app/__init__.py
cp app_config.py ./app/config.py
cp app_database.py ./app/database.py
cp app_models.py ./app/models.py
cp app_seed.py ./app/seed.py
```

**Routes folder** (in `scripture-ai/app/routes/`):
```bash
cp app_routes_init.py ./app/routes/__init__.py
cp app_routes_verses.py ./app/routes/verses.py
```

### Step 1.4: Verify Folder Structure

```bash
cd scripture-ai
tree  # or: ls -R

# Should show:
# .
# ├── .env
# ├── .gitignore
# ├── requirements.txt
# ├── main.py
# ├── seed_bible.py
# └── app/
#     ├── __init__.py
#     ├── config.py
#     ├── database.py
#     ├── models.py
#     ├── seed.py
#     └── routes/
#         ├── __init__.py
#         └── verses.py
```

---

## Part 2: Configure Database

### Step 2.1: Ensure PostgreSQL is Running

```bash
# On Mac (with Homebrew)
brew services start postgresql

# On Linux (Ubuntu/Debian)
sudo systemctl start postgresql

# On Windows
# Open Services app and start PostgreSQL service
```

Verify it's running:
```bash
psql --version
psql -U postgres -c "SELECT 1;"
```

### Step 2.2: Create Database

```bash
psql -U postgres -c "CREATE DATABASE scripture_db;"
```

Verify:
```bash
psql -U postgres -l | grep scripture_db
```

### Step 2.3: Update .env File

Edit `.env` in your project root:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/scripture_db
HOST=0.0.0.0
PORT=8000
ENV=development
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
KJV_PLUS_FILE=kjv_with_strongs.json
```

Replace `YOUR_PASSWORD` with your PostgreSQL password set during installation.

---

## Part 3: Install Dependencies

### Step 3.1: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

### Step 3.2: Install Python Packages

```bash
pip install -r requirements.txt
```

Wait for installation to complete (should take 2-5 minutes).

### Step 3.3: Verify Installation

```bash
python -c "import sqlmodel; import fastapi; print('✓ All packages installed')"
```

---

## Part 4: Download Bible Data

### Step 4.1: Get KJV+ with Strong's Numbers

1. Go to: https://github.com/openbibleinfo/Bible-datasets
2. Find `kjv_with_strongs.json`
3. Click "Raw" button
4. Save the file (Ctrl+S or Cmd+S)
5. Place in `scripture-ai/` folder

### Step 4.2: Verify File

```bash
# Check file exists and has content
ls -lh kjv_with_strongs.json

# Should show size around 5-10 MB
# Example output: -rw-r--r--  1 user  staff  7.2M kjv_with_strongs.json
```

---

## Part 5: Load Bible Data into Database

### Step 5.1: Run Seed Script

```bash
python seed_bible.py
```

You should see output like:
```
============================================================
SCRIPTURE AI - BIBLE DATABASE SEEDING
============================================================

Make sure you have kjv_with_strongs.json in this directory!
Download from: https://github.com/openbibleinfo/Bible-datasets

✓ Database tables created

Loading kjv_with_strongs.json...
✓ Loaded JSON

Parsing verses and extracting Strong's numbers...

✓ Parsed 31102 verses
✓ Extracted 8281 unique Strong's IDs
✓ Created 783137 word links

Inserting data into database...

  [1/3] Inserting verses...
  ✓ 31102 verses

  [2/3] Creating lexicon entries...
  ✓ 8281 entries

  [3/3] Inserting word links (junction table)...
  ✓ 783137 links

============================================================
✓ SUCCESS! Your Bible database is ready!
============================================================

You can now:
  1. Run: python main.py
  2. Visit: http://localhost:8000/docs
  3. Build your API endpoints!
```

**This takes 1-2 minutes. Wait for it to complete!**

### Step 5.2: Verify Data Loaded

```bash
# Connect to database
psql -U postgres -d scripture_db

# Check verse table
SELECT COUNT(*) FROM verse;
# Should show: 31102

# Check lexicon table
SELECT COUNT(*) FROM lexicon;
# Should show: 8281

# Check word links
SELECT COUNT(*) FROM verse_word_link;
# Should show: 783137

# Get Genesis 1:1
SELECT * FROM verse WHERE reference = 'Genesis 1:1';

# Exit
\q
```

---

## Part 6: Start the Server

### Step 6.1: Run FastAPI

```bash
python main.py
```

You should see:
```
============================================================
✓ Scripture AI API Started
============================================================
Server: 0.0.0.0:8000
Environment: development
Documentation: http://0.0.0.0:8000/docs
============================================================

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 6.2: Open Swagger Documentation

1. Open your browser
2. Go to: **http://localhost:8000/docs**
3. You should see interactive API documentation

---

## Part 7: Test the API

### Test 7.1: Health Check

Click on `GET /health` and click "Try it out"

Response:
```json
{
  "status": "healthy"
}
```

### Test 7.2: Get Genesis 1:1

Click on `GET /api/verses/{verse_id}` and:
1. Enter `verse_id`: `1`
2. Click "Execute"

Response:
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

### Test 7.3: Search Verses

Click on `GET /api/verses/search` and:
1. Enter `query`: `God`
2. Click "Execute"

Should show all verses containing "God"

### Test 7.4: Find Word Occurrences

Click on `GET /api/verses/strongs/{strongs_id}` and:
1. Enter `strongs_id`: `H430` (Hebrew word for "God")
2. Click "Execute"

Response shows all 2,312+ verses containing "God"

---

## Part 8: Next Steps

### Option A: Explore the API
1. Try different endpoints in Swagger UI
2. Read the `TESTING_GUIDE.md` for more examples
3. Study how the relationships work

### Option B: Add Authentication
1. Enable auth endpoints by updating `main.py`
2. Implement JWT tokens
3. Test with protected endpoints

### Option C: Build Features
1. Add semantic search with embeddings
2. Implement RAG for AI assistant
3. Build a frontend UI

---

## Troubleshooting

### Problem: "Database does not exist"
```bash
# Solution: Create database
psql -U postgres -c "CREATE DATABASE scripture_db;"
```

### Problem: "Connection refused"
```bash
# Solution: Start PostgreSQL
brew services start postgresql  # Mac
sudo systemctl start postgresql  # Linux
```

### Problem: "Module not found"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Problem: "kjv_with_strongs.json not found"
```bash
# Solution: Download from GitHub
# https://github.com/openbibleinfo/Bible-datasets
# Place in project root: scripture-ai/kjv_with_strongs.json
```

### Problem: "Port 8000 already in use"
```bash
# Solution 1: Kill the process
lsof -ti:8000 | xargs kill -9

# Solution 2: Change port in .env
PORT=8001
```

### Problem: "Permission denied" on .env
```bash
# Solution: Set permissions
chmod 600 .env
```

---

## Verification Checklist

- [ ] Python 3.9+ installed (`python --version`)
- [ ] PostgreSQL running (`psql --version`)
- [ ] Virtual environment created and activated (`(venv)` in prompt)
- [ ] Dependencies installed (`pip list | grep sqlmodel`)
- [ ] Database created (`psql -l | grep scripture_db`)
- [ ] .env file configured with correct password
- [ ] Bible data file downloaded (`ls kjv_with_strongs.json`)
- [ ] Seed script completed successfully (31,102 verses loaded)
- [ ] Server running (`python main.py` without errors)
- [ ] Swagger UI accessible (`http://localhost:8000/docs`)
- [ ] Health check passes (`GET /health`)
- [ ] Genesis 1:1 loads with words (`GET /api/verses/1`)
- [ ] Search works (`GET /api/verses/search?query=God`)

---

## You're Ready!

Congratulations! Your Scripture AI backend is running and fully functional.

**Next:** 
- Build API endpoints for your specific needs
- Add user authentication
- Implement advanced search features
- Create a frontend application

See `README.md` for complete documentation and example queries.

Good luck! 🚀
