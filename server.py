import os
import subprocess
import tempfile
from typing import List

from fastmcp import FastMCP

mcp = FastMCP("ffuf-mcp")

@mcp.tool()
def do_ffuf(url: str, ffuf_args: List[str]) -> str:
    """
    Run ffuf against the given URL with additional ffuf CLI arguments.

    Args:
        url: Target URL to fuzz (passed to ffuf as -u URL)
        ffuf_args: Extra flags/arguments (each entry is passed verbatim to ffuf)
    """
    if not isinstance(ffuf_args, list):
        raise ValueError("ffuf_args must be a list of strings")

    temp_wordlist = None
    args = list(ffuf_args)

    # Provide a tiny default wordlist when none is supplied
    if not any(arg == "-w" or arg.startswith("-w") or arg == "--wordlist" for arg in args):
        fd, path = tempfile.mkstemp(prefix="ffuf_wordlist_", suffix=".txt", text=True)
        with os.fdopen(fd, "w") as f:
            f.write("test\n")
        args += ["-w", path]
        temp_wordlist = path

    # Build the command
    cmd = ["ffuf", "-u", url, *args]

    try:
        # Execute ffuf and capture output
        result = subprocess.run(cmd, capture_output=True, text=True)
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        combined = stdout + stderr

        # Truncate to keep responses manageable for MCP clients
        max_len = 16000
        combined = combined[:max_len]

        if result.returncode != 0:
            return (
                f"ffuf exited with code {result.returncode}.\n"
                f"Command: {' '.join(cmd)}\n\n"
                f"Output (truncated to {max_len} chars):\n{combined}"
            )

        return (
            f"ffuf completed successfully.\n"
            f"Command: {' '.join(cmd)}\n\n"
            f"Output (truncated to {max_len} chars):\n{combined}"
        )
    finally:
        if temp_wordlist and os.path.exists(temp_wordlist):
            os.remove(temp_wordlist)


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        path="/mcp",
    )
