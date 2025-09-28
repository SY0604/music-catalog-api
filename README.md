# **MusicCatalog API 🎵**

A comprehensive music catalog management system built with FastAPI and powered by MongoDB.
This RESTful API enables users to manage their music collection with automated metadata enrichment.

## 📋 **For Supervisor Evaluation**

**⚠️ IMPORTANT: This project works best when run LOCALLY (not Docker)**

**Recommended Local Setup (3 minutes):**

**Step 1: Start MongoDB**
```bash
docker run -d --name local_mongo -p 27017:27017 mongo:7.0
```

**Step 2: Install Dependencies**
```bash
pip install fastapi uvicorn motor pymongo aiohttp python-dotenv
```

**Step 3: Start API Server**
```bash
uvicorn src.server:application --host 0.0.0.0 --port 8000 --reload
```

**Step 4: Run Demo (Optional)**
```bash
python local_demo.py
```

**Step 5: Access API Documentation**
```
http://localhost:8000/docs
```

## **🧪 Quick Testing Examples**

**Add a track:**
```bash
curl -X POST "http://localhost:8000/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Bohemian Rhapsody", "artist": "Queen"}'
```

**PowerShell (Windows):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/" -Method Post -ContentType "application/json" -Body '{"title": "Bohemian Rhapsody", "artist": "Queen"}'
```

**Search tracks:**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"search_terms": ["Queen"]}'
```

**PowerShell (Windows):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/search" -Method Post -ContentType "application/json" -Body '{"search_terms": ["Queen"]}'
```

**Expected Response:**
```json
{
  "id": "68d7a5fdf0b2905748e5b199",
  "title": "Thunderstruck",
  "artist": "AC/DC",
  "release_date": "1990-09-24",
  "external_link": "https://genius.com/AC-DC-thunderstruck-lyrics"
}
```

## **✨ Key Features:**

- 🚀 **FastAPI** with async support and auto-generated docs
- 🗄️ **MongoDB** integration with text search indexing  
- 🌐 **External APIs** - Genius, Spotify, LRCLib integration
- 🔧 **CRUD Operations** with comprehensive error handling
- 📊 **Metadata Enrichment** from multiple sources
- 🏗️ **Clean Architecture** with separation of concerns

## **🔧 Prerequisites:**

- Docker Engine
- Docker Compose

## **🚀 Quick Start Guide**

1) Clone this repository:

```bash
git clone https://github.com/yourusername/musiccatalog-api.git
cd musiccatalog-api
```

2) Launch the application stack:
```bash
docker-compose up --build
```

The API server will be accessible at:

http://localhost:8000

## **📚 API Usage Examples**

### 🎵 **Interactive API Documentation**

![API Documentation](Screenshot%202025-09-27%20152650.png)

![Add Track Example](Screenshot%202025-09-27%20152841.png)


![Search Example](Screenshot%202025-09-27%20153021.png)

### 💻 **Command Line Examples**

**Add a track:**
```bash
curl -X POST "http://localhost:8000/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Bohemian Rhapsody", "artist": "Queen"}'
```

**Search tracks:**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"search_terms": ["Queen", "rock"]}'
```

**Get track with lyrics:**
```bash
curl -X GET "http://localhost:8000/{track_id}?page=1&size=10"
```

### 📊 **Sample API Responses**

**Track Addition Response:**
```json
{
  "id": "68d7a5fdf0b2905748e5b199",
  "title": "Thunderstruck",
  "artist": "AC/DC", 
  "release_date": "1990-09-24",
  "external_link": "https://genius.com/AC-DC-thunderstruck-lyrics"
}
```

**Search Response:**
```json
[
  {
    "id": "68d7a48ef0b2905748e5b182",
    "title": "Hotel California",
    "artist": "Eagles",
    "release_date": "1976-12-08"
  }
]
```

## **📖 API Documentation**

Interactive Swagger UI: http://localhost:8000/docs

Alternative ReDoc Interface: http://localhost:8000/redoc

## **🏗️ Architecture Overview**

```
src/
├── handlers/        # HTTP request handlers (API endpoints)
├── business/        # Core business logic implementation
├── data/           # Data access layer (MongoDB operations)
├── config/         # Application configuration and settings
├── database/       # Database connection management
├── integrations/   # External API client implementations
└── server.py       # FastAPI application bootstrap
```

## **🎯 Core Functionality**

- **Track Management**: Add, retrieve, update, and remove music tracks
- **Metadata Enrichment**: Automatic enhancement with release dates, lyrics, and external links
- **Advanced Search**: Full-text search across titles, artists, and lyrics content
- **Multi-Source Integration**: Combines data from Genius, Spotify, and LRCLib APIs
- **Pagination Support**: Efficient handling of large lyric content
- **Data Validation**: Robust input validation using Pydantic schemas
