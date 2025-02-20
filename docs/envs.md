sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev


mkvirtualenv -p $(which python3.10) teacher-assistant-api
