# Flask Teaching App

This Flask application allows teachers to upload lecture recordings, analyze them using an LLM, and retrieve useful educational content.

## Prerequisites
- Docker & Docker Compose installed
- Python 3.8+

## Setup and Running

### Start PostgreSQL using Docker Compose
```sh
docker-compose up -d
```
This will start a PostgreSQL container and create a `teaching_db` database.

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Start the Flask App
```sh
python app.py
```

### API Endpoints
- `POST /upload` - Upload an audio recording
- `GET /audio/<id>` - Stream an audio file
- `GET /news?subject=<subject>` - Fetch relevant news
- `GET /quiz?subject=<subject>` - Retrieve a quiz
- `GET /articles?subject=<subject>` - Fetch articles
- `GET /stats/<teacher_id>` - Get performance statistics

### Stop Services
```sh
docker-compose down
```

### Next Steps

- Host in Heroku
- Extract any configs to envs
- Link to Gemini for a few routes

