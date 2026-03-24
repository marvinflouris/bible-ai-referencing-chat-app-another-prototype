# Scripture AI - API Testing Guide

## Testing the API

Once your server is running (`python main.py`), you can test the API.

---

## Option 1: Swagger UI (Easiest)

Visit: **http://localhost:8000/docs**

Click on each endpoint and click "Try it out" to test directly in the browser.

---

## Option 2: cURL Commands

### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

---

## Verse Endpoints

### 1. List All Verses (Paginated)
```bash
curl "http://localhost:8000/api/verses?skip=0&limit=10"
```

### 2. Search Verses by Text
```bash
curl "http://localhost:8000/api/verses/search?query=God"
```

### 3. Get Specific Verse by ID
```bash
curl http://localhost:8000/api/verses/1
```

Response includes all words with Strong's numbers:
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

### 4. Get Verse by Reference
```bash
curl "http://localhost:8000/api/verses/reference/Genesis/1/1"
```

### 5. Find All Verses with a Strong's Word
```bash
curl "http://localhost:8000/api/verses/strongs/H430"
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

---

## Authentication Endpoints (Once auth is enabled)

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123",
    "password_confirm": "SecurePassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 2. Login User
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123"
  }'
```

Save the `access_token` from the response.

### 3. Get Current User
```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Replace `YOUR_TOKEN_HERE` with the token from login/register.

### 4. Refresh Token
```bash
curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Notes Endpoints (Once auth is enabled)

### 1. Create a Note
```bash
curl -X POST http://localhost:8000/api/notes/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "verse_id": 1,
    "content": "Beautiful passage about creation. The Hebrew word elohim appears here."
  }'
```

### 2. Get My Notes
```bash
curl "http://localhost:8000/api/notes/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Get Notes for Specific Verse
```bash
curl http://localhost:8000/api/notes/verse/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 4. Get Specific Note
```bash
curl http://localhost:8000/api/notes/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 5. Update a Note
```bash
curl -X PUT http://localhost:8000/api/notes/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Updated note with more insights"
  }'
```

### 6. Delete a Note
```bash
curl -X DELETE http://localhost:8000/api/notes/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 7. Search Notes
```bash
curl -X POST http://localhost:8000/api/notes/search \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"query": "creation"}'
```

### 8. Get Note Statistics
```bash
curl http://localhost:8000/api/notes/stats \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Option 3: Python Requests

### Install requests
```bash
pip install requests
```

### Test Script
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Get Genesis 1:1
response = requests.get(f"{BASE_URL}/api/verses/1")
verse = response.json()
print(f"\n{verse['reference']}")
print(f"Text: {verse['text']}\n")

# 2. Print all words with definitions
print("Words with Strong's numbers:")
for word in verse['words']:
    print(f"  [{word['word_index']}] '{word['word_text']}' → {word['strongs_id']}")
    print(f"      {word['transliteration']}: {word['definition']}\n")

# 3. Search for "God"
response = requests.get(f"{BASE_URL}/api/verses/strongs/H430")
god_data = response.json()
print(f"\nStrong's H430 ('{god_data['hebrew_word']}' - {god_data['transliteration']})")
print(f"Definition: {god_data['definition']}")
print(f"Appears in {god_data['occurrences']} verses")
print(f"\nFirst 5 occurrences:")
for verse in god_data['verses'][:5]:
    print(f"  {verse['reference']}: {verse['text']}")
```

---

## Option 4: Postman

1. Download Postman: https://www.postman.com/downloads/
2. Create a new collection
3. Add requests for each endpoint
4. Set `Base URL` variable: `http://localhost:8000`
5. Use `{{Base_URL}}/api/verses` in request URL

### Set Up Bearer Token Variable

1. Create environment variable `token`
2. After login, add to "Tests" tab:
   ```javascript
   if (pm.response.code === 200) {
       pm.environment.set("token", pm.response.json().access_token);
   }
   ```
3. Use in Authorization header: `Bearer {{token}}`

---

## Testing Workflow

### 1. Start with Verse Data
```bash
# Get Genesis 1:1
curl http://localhost:8000/api/verses/1

# Search for "love"
curl "http://localhost:8000/api/verses/search?query=love"

# Find all occurrences of "God" (H430)
curl http://localhost:8000/api/verses/strongs/H430
```

### 2. Test Authentication (After enabling auth)
```bash
# Register
TOKEN=$(curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123",
    "password_confirm": "TestPass123"
  }' | jq -r '.access_token')

# Get user info
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Test Notes (After enabling auth)
```bash
# Create a note
curl -X POST http://localhost:8000/api/notes/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "verse_id": 1,
    "content": "Great verse about creation"
  }'

# Get my notes
curl http://localhost:8000/api/notes/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## Common Issues

### 401 Unauthorized
- **Problem:** Invalid or missing token
- **Solution:** Make sure you include the full token: `Authorization: Bearer eyJ...`

### 404 Not Found
- **Problem:** Verse/verse doesn't exist
- **Solution:** Check the verse_id or reference is correct

### 422 Validation Error
- **Problem:** Invalid request data
- **Solution:** Check the request body matches the schema (check /docs)

### Connection Refused
- **Problem:** Server isn't running
- **Solution:** Run `python main.py` first

---

## Tips for Testing

1. **Use `jq` to format JSON** (install from: https://stedolan.github.io/jq/)
   ```bash
   curl http://localhost:8000/api/verses/1 | jq
   ```

2. **Save token to variable**
   ```bash
   TOKEN="your_token_here"
   curl http://localhost:8000/api/verses \
     -H "Authorization: Bearer $TOKEN"
   ```

3. **Pretty print response**
   ```bash
   curl http://localhost:8000/api/verses/1 | python -m json.tool
   ```

4. **Check only headers**
   ```bash
   curl -I http://localhost:8000/api/verses/1
   ```

---

## Next: Advanced Testing

- Load testing with **Apache JMeter** or **Locust**
- Automated tests with **pytest**
- Integration tests with **FastAPI TestClient**

See: https://fastapi.tiangolo.com/advanced/testing-events/
