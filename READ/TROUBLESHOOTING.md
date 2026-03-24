# Scripture AI - Troubleshooting & Common Issues

## Installation & Setup Issues

### Problem: "Python not found" or "python: command not found"

**Cause:** Python is not installed or not in PATH

**Solution:**
```bash
# Check if installed
python --version
python3 --version

# If not installed, download from:
# https://www.python.org/downloads/

# Make sure to check "Add Python to PATH" during installation
```

### Problem: "pip: command not found"

**Cause:** pip is not installed or not in PATH

**Solution:**
```bash
# Try with Python directly
python -m pip --version

# If this works, use:
python -m pip install -r requirements.txt

# If not, reinstall Python with pip included
```

### Problem: "pip install" takes forever or fails

**Cause:** Network issues or incompatible packages

**Solution:**
```bash
# Try with no cache
pip install --no-cache-dir -r requirements.txt

# Use different Python version
python3.9 -m pip install -r requirements.txt

# Update pip first
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Database Issues

### Problem: "psql: command not found"

**Cause:** PostgreSQL is not installed or not in PATH

**Solution:**

**Mac (Homebrew):**
```bash
brew install postgresql
brew services start postgresql
psql -U postgres
```

**Ubuntu/Debian:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres psql
```

**Windows:**
```
# Download from https://www.postgresql.org/download/windows/
# Install with default settings
# PostgreSQL command line tools are added to PATH
```

### Problem: "psql: FATAL: role "postgres" does not exist"

**Cause:** PostgreSQL user setup issue

**Solution:**

**Ubuntu (most common):**
```bash
# Switch to postgres user
sudo -u postgres psql

# Create postgres user if missing
sudo -u postgres createuser -s postgres

# Set password
sudo -u postgres psql
postgres=# ALTER USER postgres WITH PASSWORD 'your_password';
```

### Problem: "FATAL: password authentication failed for user "postgres""

**Cause:** Wrong password in .env file

**Solution:**
```bash
# 1. Reset PostgreSQL password
# Ubuntu:
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'your_password';"

# 2. Update .env with same password
# .env:
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/scripture_db

# 3. Test connection
psql -U postgres -h localhost -c "SELECT 1;"
```

### Problem: "FATAL: Ident authentication failed for user "postgres""

**Cause:** PostgreSQL authentication method configuration

**Solution:**
```bash
# Edit pg_hba.conf
# On Mac: /usr/local/var/postgres/pg_hba.conf
# On Linux: /etc/postgresql/*/main/pg_hba.conf

# Change this line:
# local   all             postgres                                ident
# To:
# local   all             postgres                                md5

# Restart PostgreSQL:
# Mac:
brew services restart postgresql

# Linux:
sudo systemctl restart postgresql
```

### Problem: "database scripture_db does not exist"

**Cause:** Database wasn't created

**Solution:**
```bash
# Create it
psql -U postgres -c "CREATE DATABASE scripture_db;"

# Verify
psql -U postgres -l | grep scripture_db

# If that doesn't work, connect first:
psql -U postgres
# Then in psql:
CREATE DATABASE scripture_db;
\q
```

### Problem: "Column word_index does not exist"

**Cause:** Tables weren't created or old schema

**Solution:**
```bash
# Drop and recreate database
psql -U postgres -c "DROP DATABASE scripture_db;"
psql -U postgres -c "CREATE DATABASE scripture_db;"

# Delete database and run seed again:
rm -f *.db
python seed_bible.py
```

---

## Seeding Issues

### Problem: "kjv_with_strongs.json not found"

**Cause:** Bible data file is missing

**Solution:**
```bash
# 1. Download from GitHub
# https://github.com/openbibleinfo/Bible-datasets
# Find: kjv_with_strongs.json

# 2. Place in project root
ls -la kjv_with_strongs.json

# Should show file with size ~7MB
# Example: -rw-r--r--  1 user  staff  7.2M kjv_with_strongs.json

# 3. Try seeding again
python seed_bible.py
```

### Problem: "JSONDecodeError" while seeding

**Cause:** Corrupted or incorrect JSON file

**Solution:**
```bash
# 1. Verify JSON is valid
python -c "import json; json.load(open('kjv_with_strongs.json'))"

# 2. If error, re-download file
# Delete the file
rm kjv_with_strongs.json

# Download again from:
# https://github.com/openbibleinfo/Bible-datasets

# 3. Verify and retry
python seed_bible.py
```

### Problem: "timeout or keyboard interrupt during seeding"

**Cause:** Seeding took too long or was interrupted

**Solution:**
```bash
# 1. Wait longer - seeding takes 1-2 minutes per 10,000 verses

# 2. If interrupted, reset database:
psql -U postgres -c "DROP DATABASE scripture_db; CREATE DATABASE scripture_db;"

# 3. Run seeding again (don't interrupt!)
python seed_bible.py

# 3. If system too slow, run without progress output:
python seed_bible.py 2>/dev/null
```

### Problem: "Memory error" or "Out of memory"

**Cause:** Not enough RAM for large JSON parsing

**Solution:**
```bash
# 1. Close other applications to free up memory

# 2. Add swap (if on Linux)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 3. Increase Python memory limit (advanced)
# Not typically necessary for this dataset
```

---

## Server & API Issues

### Problem: "Address already in use" or "Port 8000 in use"

**Cause:** Another application is using port 8000

**Solution:**
```bash
# Option 1: Kill the process using port 8000
# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Option 2: Change port in .env
# .env:
PORT=8001

# Then run:
python main.py  # Now runs on 8001
```

### Problem: "ModuleNotFoundError: No module named 'app'"

**Cause:** Running from wrong directory

**Solution:**
```bash
# Make sure you're in project root
pwd  # Should show: .../scripture-ai
ls app/  # Should show models.py, config.py, etc.

# Run from correct directory
cd scripture-ai
python main.py
```

### Problem: "ImportError: cannot import name 'settings' from 'app.config'"

**Cause:** app/config.py is missing or has wrong content

**Solution:**
```bash
# 1. Check file exists
ls -la app/config.py

# 2. Verify content has Settings class
grep "class Settings:" app/config.py

# 3. If missing, copy again:
cp app_config.py app/config.py

# 4. Restart server
python main.py
```

### Problem: "Connection refused" when accessing localhost:8000

**Cause:** Server is not running

**Solution:**
```bash
# 1. Start the server
python main.py

# 2. Don't close the terminal - keep it running

# 3. Open new terminal and test:
curl http://localhost:8000/health

# Expected response: {"status":"healthy"}
```

### Problem: "AttributeError: module 'app' has no attribute 'routes'"

**Cause:** app/__init__.py is missing or incorrect

**Solution:**
```bash
# 1. Check file exists
ls -la app/__init__.py

# 2. Should have proper imports:
head -20 app/__init__.py

# 3. If wrong, replace:
cp app_init.py app/__init__.py

# 4. Restart server
python main.py
```

---

## API Endpoint Issues

### Problem: "404 Not Found" on endpoint

**Cause:** 
- Endpoint doesn't exist
- Route not registered
- Wrong URL path

**Solution:**
```bash
# 1. Check Swagger docs
# Visit: http://localhost:8000/docs
# Look for your endpoint in the list

# 2. If missing, check main.py has route registered:
grep "include_router" main.py

# Should have:
# app.include_router(verses_routes.router, prefix="/api")

# 3. Verify URL is correct
# Example correct: GET http://localhost:8000/api/verses/1
# Not: http://localhost:8000/verses/1  (missing /api)
```

### Problem: "422 Unprocessable Entity"

**Cause:** Invalid request body or parameters

**Solution:**
```bash
# 1. Check parameters in Swagger UI
# Endpoint might require specific data type

# 2. Verify JSON syntax in curl:
curl -X POST http://localhost:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -d '{"verse_id": 1, "content": "test"}'

# 3. Check required fields:
# Some endpoints require: verse_id, content, etc.

# 4. Use Swagger UI to see required fields
# Visit: http://localhost:8000/docs
```

### Problem: "401 Unauthorized"

**Cause:** Missing or invalid token (for protected endpoints)

**Solution:**
```bash
# 1. Get a token first:
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Response includes access_token

# 2. Use token in header:
TOKEN="your_token_here"
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"

# 3. Make sure format is exactly: "Bearer YOUR_TOKEN"
# Not: "Token YOUR_TOKEN"
# Not: "YOUR_TOKEN"
```

### Problem: "Verse not found" or "404"

**Cause:** Verse ID doesn't exist in database

**Solution:**
```bash
# 1. Check Bible is seeded:
# Run: python seed_bible.py
# Check for "31102 verses inserted"

# 2. Verify verse ID is valid:
# Valid IDs: 1 to 31,102

# Try Genesis 1:1:
curl http://localhost:8000/api/verses/1

# Try John 3:16:
curl http://localhost:8000/api/verses/26000  # Approximately
```

---

## Performance Issues

### Problem: "Server is slow" or "requests timeout"

**Cause:**
- Large result sets
- Inefficient queries
- Low system resources

**Solution:**
```bash
# 1. Use pagination:
# Instead of: GET /api/verses/search?query=God
# Use: GET /api/verses/search?query=God&limit=10

# 2. Check server logs for errors:
# Look for RED error messages in terminal

# 3. Monitor resources:
# Mac:
top -l 1 | grep "PhysMem"

# Linux:
free -h

# Windows:
Get-Process | Select-Object Name, WorkingSet | Sort-Object WorkingSet -Descending
```

### Problem: "Out of memory" errors

**Cause:** Search returning too many results

**Solution:**
```bash
# 1. Limit results:
curl "http://localhost:8000/api/verses?limit=10"

# 2. Use more specific search:
curl "http://localhost:8000/api/verses/search?query=God%20love&limit=5"

# 3. Restart server:
# Kill server (Ctrl+C)
# Restart: python main.py
```

---

## Development Issues

### Problem: "Changes not reflecting after code edit"

**Cause:** Reload is not working or server cache

**Solution:**
```bash
# 1. Kill server
# Press Ctrl+C in terminal

# 2. Restart server
python main.py

# 3. Clear browser cache
# Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

# 4. Check ENV setting
# In .env, make sure:
ENV=development  # For auto-reload

# 5. If still not working, restart Python completely:
ps aux | grep python
# Kill any hanging python processes
```

### Problem: "SQLAlchemy error" with database

**Cause:** Schema mismatch or connection issue

**Solution:**
```bash
# 1. Reset database completely:
psql -U postgres -c "DROP DATABASE scripture_db;"
psql -U postgres -c "CREATE DATABASE scripture_db;"

# 2. Re-run seeding:
python seed_bible.py

# 3. Restart server:
python main.py
```

---

## Getting Help

### Check These Resources:
1. **WALKTHROUGH.md** - Step-by-step setup
2. **TESTING_GUIDE.md** - How to test endpoints
3. **README.md** - Full documentation
4. **FEATURE_ROADMAP.md** - Feature implementation help

### Enable Debug Logging:

In `app/database.py`, change:
```python
engine = create_engine(settings.DATABASE_URL, echo=False)
```

To:
```python
engine = create_engine(settings.DATABASE_URL, echo=True)
```

Now you'll see all SQL queries being executed.

### Check Server Logs:

The server terminal shows all errors. Look for:
- RED text = errors
- YELLOW text = warnings
- BLUE text = info

### Verify Connectivity:

```bash
# Test database connection:
psql -U postgres -d scripture_db -c "SELECT COUNT(*) FROM verse;"

# Test API:
curl http://localhost:8000/health

# Test JSON file:
python -c "import json; print(json.load(open('kjv_with_strongs.json'))['Genesis']['1']['1'])"
```

---

## Emergency Reset

If everything is broken, do a complete reset:

```bash
# 1. Stop server (Ctrl+C)

# 2. Delete database
psql -U postgres -c "DROP DATABASE scripture_db;"

# 3. Recreate database  
psql -U postgres -c "CREATE DATABASE scripture_db;"

# 4. Clear Python cache
rm -rf __pycache__
rm -rf app/__pycache__
rm -rf app/routes/__pycache__

# 5. Reinstall packages
pip install --force-reinstall -r requirements.txt

# 6. Re-seed database
python seed_bible.py

# 7. Restart server
python main.py
```

---

## Known Limitations

1. **Single-threaded database:** Only one write operation at a time
   - Solution: Use multi-threaded app server (Gunicorn)

2. **Large search results:** Searching for common words (like "God") returns 2,000+ verses
   - Solution: Implement pagination, use semantic search

3. **No caching:** Every request hits the database
   - Solution: Add Redis caching

4. **No rate limiting:** Anyone can spam requests
   - Solution: Add FastAPI rate limiting middleware

These are all solvable with additional configuration!

---

You should be able to troubleshoot most issues now. If something weird happens:

1. ✅ Check this troubleshooting guide
2. ✅ Check the error message carefully
3. ✅ Try the emergency reset
4. ✅ Search online for the specific error

Good luck! 🚀
