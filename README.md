# ffuflosa – FFUF MCP server for Render

This repository packages **ffuf** as a Model Context Protocol (MCP) server using Python **FastMCP** with an SSE transport, ready for deployment on Render.

## Tool
- `do_ffuf(url: str, ffuf_args: List[str])` – runs `ffuf -u <url>` with additional CLI arguments and returns combined stdout/stderr (truncated to 16k chars).

## Running locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```
The server listens on `0.0.0.0:${PORT:-8000}` at path `/mcp`.

## Docker
Render will auto-detect the included `Dockerfile`.
To build/run manually:
```bash
docker build -t ffuflosa .
docker run -p 8000:8000 -e PORT=8000 ffuflosa
```

## MCP client configuration (example)
```
"mcpServers": {
  "ffuflosa": {
    "url": "https://<your-render-service>.onrender.com/mcp"
  }
}
```
