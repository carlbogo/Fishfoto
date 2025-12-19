# Fishfoto

This project is fully containerized and runs using Docker.
You do not need to install Python, Node.js, or any other dependencies locally.

1. Install prerequisites
Make sure the following tools are installed on your system:
- Docker
- Docker Compose (included with Docker Desktop)

Verify installation:
'docker --version'
'docker compose version'

2. Clone the repository
'git clone https://github.com/carlbogo/Fishfoto.git'
'cd Fishfoto'

3. Build and start the containers
From the project root:
'docker compose up --build'

This will:
- Build the backend (FastAPI) image
- Build the frontend (nginx) image
- Start both services
- Create a shared Docker network

4. Open the application
Once the containers are running, open your browser:
- Frontend UI:
http://localhost:3000
- Backend API docs (FastAPI):
http://localhost:8000/docs

6. Stop the application
Press Ctrl + C in the terminal, then stop and remove containers:
'docker compose down'

Notes
- The frontend is served via nginx
- API requests are proxied internally to the backend
- Docker is required to run this project locally
- The browser only communicates with localhost
