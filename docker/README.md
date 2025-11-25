# Docker Guide

## Description

* `docker-compose-test.yml`: WIP!, contains an auto testing service set by docker to evaluate MCP server or other servers' performance.
* `docker-compose.yml`: contains all the services needed both for dev and deploy.

## Services

### chat-server

Contains all the logic for chatbot's conversation/chatting, metrics collection, and authentication to the chatbot website。

### rag-server

Do the RAG techniques to the knowledge base.

### mcp-server

Write AI agent invoke in the [MCP](https://modelcontextprotocol.io/overview) method. Contains the logic of how AI bot answer human queries.

### dashboard-server

Handle the backend logic of all dashboard-related data CRUD.

### etcd, minio, milvus

In-memory docker-based Milvus vector database for storing vectors for RAG queries.

### cron-job-runner

Container to run cron jobs. Currently it only runs vectorizing S3 files at every 1AM.

### dozzle

A log monitor to easily monitor all logs of the docker containers.

### mongo

Main database for storing all data.

### scrape-server

Server to handle web scraping-related services.