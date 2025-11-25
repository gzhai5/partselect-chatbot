# partselect-chatbot

## 📝 Introduction

This repository aims to develop a e-commerce chatbot tailored for the PartSelect website. The goal is to reduce the workload of handling repetitive customer inquiries and to support sales efforts by engaging with potential new customers.

## ⚙️ Tech Stacks
* Frontend: [Next.js](https://nextjs.org/)
* Backend:
    - [FastAPI](https://fastapi.tiangolo.com/)
    - [FastMCP](https://gofastmcp.com/getting-started/welcome)
* Databases:
    - [MongoDB](https://www.mongodb.com/)
* Log Monitor: [Dozzle](https://dozzle.dev/)

## 🚧 Current stage

The project has already been devloped to have basic sturcture and features, but requires more tests...

## 🛠️ Local build

This project uses [Docker Compose](https://docs.docker.com/compose/) for local development.  
The configuration file is located at [docker/docker-compose.yml](docker/docker-compose.yml), and a high-level explanation of each container service is available in the [Docker README](docker/README.md).

### 🔐 Environment Setup

Obtain the required environment variable files (for simplicity, all env files are combined) from the author (or insert yours) and place it at:

- `chat-server/.env`
- `client/.env.local`
- `mcp-server/.env`

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

### 💻 Start the Frontend
Install the frontend dependencies:

```bash
cd client
npm i
```

Then run the development server:

```bash
npm run dev
```

Once started, the chatbot will be available at http://localhost:3000.
