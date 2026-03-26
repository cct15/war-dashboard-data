FROM python:3.11-slim
LABEL io.modelcontextprotocol.server.name="io.github.cct15/war-dashboard-data"
WORKDIR /app
COPY mcp_server/server.py .
ENTRYPOINT ["python", "server.py"]
