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


### Deploy as container

Build container image:
```
sudo docker build . -t invokeed/teacher-assistant-api
```

Pass Env:

create .env file when running as container 

```
DB_USER=<user>
DB_PASSWORD=<pass>
DB_HOST=localhost # Or the actual host if not local
DB_NAME=teaching_db
DB_PORT=5432
```

Launch container:

```bash
sudo docker stop teacher-assistant-api

sudo docker run --rm --name teacher-assistant-api -d \
  --env-file .env \
  -v $(pwd)/secret.yaml:/app/secret.yaml \
  -p 5000:5000 \
  invokeed/teacher-assistant-api
```

Specify Gemini key:

Create secret.yaml to host the Gemini API key

```
GEMINI_API_KEY: "KEY"
```

Other helpful commands:

```bash
sudo docker ps
sudo docker logs -f teacher-assistant-api
```
