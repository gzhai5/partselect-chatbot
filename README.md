# milea-chatbot

## 📝 Introduction

This repository aims to develop a general-purpose chatbot tailored for the winery industry. The goal is to reduce the workload of handling repetitive customer inquiries and to support sales efforts by engaging with potential new customers.

## ⚙️ Tech Stacks
* Frontend: [Next.js](https://nextjs.org/)
* Backend: [FastAPI](https://fastapi.tiangolo.com/)
* Databases:
    - [MongoDB](https://www.mongodb.com/)
    - [Milvus](https://milvus.io/)
* Log Monitor: [Dozzle](https://dozzle.dev/)

## 🚧 Current stage

The project has reached MVP stage, but requires more tests...

## 🛠️ Local build

This project uses [Docker Compose](https://docs.docker.com/compose/) for local development.  
The configuration file is located at [docker/docker-compose.yml](docker/docker-compose.yml), and a high-level explanation of each container service is available in the [Docker README](docker/README.md).

### 🔐 Environment Setup

Obtain the required environment variable files (for simplicity, all env files are combined) from a team member and place it at:

- `env/.env`
- `cron-job-runner/params.py`
- `mcp-server/app/params.py`

### ⚙️ Prerequisites

Ensure your system has the following installed:

- [Docker](https://docs.docker.com/engine/install/)
- [Node.js and npm](https://nodejs.org/en/download)

### 🚀 Start All Services

Navigate to the `/docker` directory and run:

```bash
docker compose up --build
```

(Optional) To verify that all Docker containers are running properly:
```bash
docker ps -a
```

### 📥 Inject Vector Data into Milvus
Since Milvus uses local storage, the vector database may initially be empty. But there's a cron job that will do the job every 1am to pull every markdownfiles from S3, vectorize them, inject into the Milvus.

### 💻 Start the Frontend
Install the frontend dependencies:

```bash
cd chatbot-client
npm i
```

Then run the development server:

```bash
npm run dev
```

Once started, the chatbot will be available at http://localhost:3000.
