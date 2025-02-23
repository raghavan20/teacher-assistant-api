# Flask Teaching Assistance App

This Flask application allows teachers to upload lecture recordings, analyze them using an LLM, and retrieve useful educational content.

## Prerequisites
- Docker & Docker Compose installed
- Python 3.10

```
mkvirtualenv -p $(which python3.11) teacher-assistant-api
```

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


### Stop Services
```sh
docker-compose down
```

### Additional commands

```commandline
sudo docker build . -t invokeed/teacher-assistant-api


sudo docker run --rm --name teacher-assistant-api -d --env-file .env  -p 5000:5000  invokeed/teacher-assistant-api

sudo docker stop teacher-assistant-api

sudo docker ps
sudo docker logs -f teacher-assistant-api
```

### Next Steps

- Host with Railway
- Extract any configs to envs
- Link to Gemini for a few routes

