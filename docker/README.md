# Docker Guide

## Description

* `docker-compose.yml`: contains all the services needed both for dev and deploy.

## Services

### chat-server

Contains all the logic for chatbot's conversation/chatting, user-query/bot response verify to the chatbot website。

### mcp-server

Write AI agent invoke in the [MCP](https://modelcontextprotocol.io/overview) method. Contains the logic of how AI bot answer human queries.

### dozzle

A log monitor to easily monitor all logs of the docker containers.
