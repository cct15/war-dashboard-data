FROM python:3.11-slim
WORKDIR /app
COPY mcp_server/server.py .
ENTRYPOINT ["python", "server.py"]
