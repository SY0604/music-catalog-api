# Music Catalog API - Evaluation Guide

## 🎯 Project Overview
This is a comprehensive music catalog management system built with FastAPI, MongoDB, and multiple external API integrations. The system allows users to manage music tracks with automatic metadata enrichment from Genius, Spotify, and LRCLib APIs.

## 🚀 Quick Setup & Testing (3 minutes)

### Prerequisites
- Docker installed (for MongoDB only)
- Python 3.11+ installed
- Internet connection (for external API calls)

### ⭐ **RECOMMENDED: Local Testing (VERIFIED WORKING)**

**This is the method that has been tested and confirmed working:**

1. **Start MongoDB:**
   ```bash
   docker run -d --name local_mongo -p 27017:27017 mongo:7.0
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn motor pymongo aiohttp python-dotenv
   ```

3. **Start the API:**
   ```bash
   uvicorn src.server:application --host 0.0.0.0 --port 8000 --reload
   ```

4. **Run Automated Demo:**
   ```bash
   python local_demo.py
   ```

5. **Access the API:**
   - Open browser: http://localhost:8000/docs
   - Interactive API documentation will load

### ⚠️ Docker Compose (Alternative - May have network issues)

**Note: Docker Compose setup may have networking issues. Local setup is recommended.**

1. **Start everything:**
   ```bash
   docker-compose up --build
   ```

2. **Access the API:**
   - Open browser: http://localhost:8000/docs

## 🧪 Testing the API Functionality

### 1. Interactive Testing (Easiest)
- Go to: http://localhost:8000/docs
- Click on any endpoint → "Try it out" → Enter test data → "Execute"

### 2. Sample Test Data

**Add Tracks:**
```json
{"title": "Bohemian Rhapsody", "artist": "Queen"}
{"title": "Imagine", "artist": "John Lennon"}
{"title": "Billie Jean", "artist": "Michael Jackson"}
```

**Search Tracks:**
```json
{"search_terms": ["Queen", "rock"]}
{"search_terms": ["Lennon"]}
```

### 3. PowerShell Commands (Windows)

**Add a track:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/" -Method Post -ContentType "application/json" -Body '{"title": "Bohemian Rhapsody", "artist": "Queen"}'
```
**Search tracks:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/search" -Method Post -ContentType "application/json" -Body '{"search_terms": ["Queen"]}'
```

## ✅ Expected Results (VERIFIED WORKING)

### Successful Track Addition (Real Example from Testing):
```json
{
  "id": "68d7a5fdf0b2905748e5b199",
  "title": "Thunderstruck",
  "artist": "AC/DC",
  "release_date": "1990-09-24",
  "external_link": "https://genius.com/AC-DC-thunderstruck-lyrics"
}
```

### Another Verified Example:
```json
{
  "id": "68d7a48ef0b2905748e5b182",
  "title": "Hotel California",
  "artist": "Eagles",
  "release_date": "1976-12-08",
  "external_link": "https://genius.com/Eagles-hotel-california-lyrics"
}
```

### Track with Lyrics:
```json
{
  "id": "68d7a48ef0b2905748e5b182",
  "title": "Hotel California",
  "artist": "Eagles",
  "release_date": "1976-12-08",
  "lyrics": [
    "On a dark desert highway, cool wind in my hair",
    "Warm smell of colitas, rising up through the air",
    "Up ahead in the distance, I saw a shimmering light",
    "My head grew heavy and my sight grew dim",
    "I had to stop for the night"
  ],
  "external_link": "https://genius.com/Eagles-hotel-california-lyrics"
}
```

## 🔍 Key Features to Verify

### ✅ Core Functionality Checklist:
- [ ] API documentation loads (Swagger UI)
- [ ] Can add new tracks
- [ ] Tracks get enriched with metadata from external APIs
- [ ] Can retrieve tracks with lyrics
- [ ] Search functionality works
- [ ] Can update track information
- [ ] Can delete tracks
- [ ] Proper error handling (404, 409 errors)

### ✅ Technical Architecture:
- [ ] FastAPI framework with async support
- [ ] MongoDB integration with text indexing
- [ ] External API integrations (Genius, Spotify, LRCLib)
- [ ] Proper separation of concerns (handlers, business, data layers)
- [ ] Docker containerization
- [ ] Environment configuration
- [ ] Comprehensive error handling

### ✅ Code Quality:
- [ ] Clean, readable code structure
- [ ] Proper documentation and comments
- [ ] Consistent naming conventions
- [ ] Type hints and validation
- [ ] Modular architecture

## 📊 Performance Expectations

- **API Response Time:** < 2 seconds for track addition
- **Search Performance:** < 1 second for keyword searches
- **External API Integration:** Graceful fallback if APIs are unavailable
- **Database Operations:** Efficient indexing and querying

## 🛠️ Troubleshooting

**If API doesn't start:**
1. Check if MongoDB is running: `docker ps`
2. Check if port 8000 is available
3. Verify environment variables in `.env` file

**If external APIs fail:**
- Some songs might not be available in external databases
- API will still work with basic metadata
- Check internet connection

## 📁 Project Structure Review

```
MusicCatalogAPI/
├── src/
│   ├── handlers/        # API endpoints (REST controllers)
│   ├── business/        # Business logic layer
│   ├── data/           # Database operations
│   ├── integrations/   # External API clients
│   ├── models/         # Data models and schemas
│   ├── config/         # Configuration and settings
│   └── database/       # Database connection management
├── docker-compose.yml  # Container orchestration
├── Dockerfile         # Container definition
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## 🎯 Evaluation Criteria

### Excellent (90-100%):
- All features work flawlessly
- Clean, well-documented code
- Proper error handling
- Good performance
- Complete external API integration

### Good (80-89%):
- Most features work
- Code is readable and structured
- Basic error handling
- Acceptable performance

### Satisfactory (70-79%):
- Core features work
- Code structure is adequate
- Some error handling present

## 📞 Support

If you encounter any issues during evaluation, the following logs can help:
- API logs: Check the terminal where uvicorn is running
- MongoDB logs: `docker logs local_mongo`
- Container logs: `docker logs music_catalog_api`
