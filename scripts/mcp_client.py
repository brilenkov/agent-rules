#!/usr/bin/env python3
"""mcp_client.py — MCP client CLI for Z.ai agents.

Connects to mcp-shared server via SSE, calls tools + reads resources.
Enables coordination between Z.ai sessions (register_activity,
check_conflict, heartbeat, unregister_activity) + GitHub Issues +
Render status + bot health checks.

Setup (at session start):
    pip install mcp                          # install MCP SDK
    export MCP_URL=https://mcp-shared.onrender.com/sse
    export MCP_TOKEN=<bearer token from Bitwarden>

Usage:
    python3 mcp_client.py register Z.ai-brain-tools fns-bot bot.py server.js
    python3 mcp_client.py check fns-bot bot.py
    python3 mcp_client.py unregister Z.ai-brain-tools
    python3 mcp_client.py heartbeat Z.ai-brain-tools
    python3 mcp_client.py active-agents
    python3 mcp_client.py issues brain-tools --open --labels fns-bot
    python3 mcp_client.py status fns-receipt-bot-docker
    python3 mcp_client.py bot-health https://fns-receipt-bot-docker.onrender.com
    python3 mcp_client.py bot-logs https://fns-receipt-bot-docker.onrender.com
    python3 mcp_client.py find-skill "git push"
    python3 mcp_client.py introduce "Z.ai brain-tools" "fns-bot" "issue-42"
    python3 mcp_client.py restart fns-receipt-bot-docker
    python3 mcp_client.py deploy fns-receipt-bot-docker
    python3 mcp_client.py github-log brain-tools
"""
import asyncio
import os
import sys

MCP_URL = os.environ.get("MCP_URL", "https://mcp-shared.onrender.com/sse")
MCP_TOKEN = os.environ.get("MCP_TOKEN", "")


async def call_tool(tool_name: str, arguments: dict) -> str:
    """Connect to MCP server via SSE and call a tool."""
    from mcp import ClientSession
    from mcp.client.sse import sse_client

    headers = {"Authorization": f"Bearer {MCP_TOKEN}"} if MCP_TOKEN else {}

    async with sse_client(MCP_URL, headers=headers) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            if result.content:
                return result.content[0].text
            return "(no result)"


async def read_resource(uri: str) -> str:
    """Read a resource from MCP server."""
    from mcp import ClientSession
    from mcp.client.sse import sse_client

    headers = {"Authorization": f"Bearer {MCP_TOKEN}"} if MCP_TOKEN else {}

    async with sse_client(MCP_URL, headers=headers) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.read_resource(uri)
            if result.contents:
                return result.contents[0].text
            return "(no content)"


async def list_tools() -> str:
    """List all available MCP tools."""
    from mcp import ClientSession
    from mcp.client.sse import sse_client

    headers = {"Authorization": f"Bearer {MCP_TOKEN}"} if MCP_TOKEN else {}

    async with sse_client(MCP_URL, headers=headers) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            lines = [f"MCP tools ({len(tools.tools)}):"]
            for t in tools.tools:
                lines.append(f"  {t.name}: {t.description[:80] if t.description else ''}")
            resources = await session.list_resources()
            lines.append(f"\nMCP resources ({len(resources.resources)}):")
            for r in resources.resources:
                lines.append(f"  {r.uri}: {r.name}")
            return "\n".join(lines)


def usage():
    print(__doc__)
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        usage()

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "register":
        if len(args) < 3:
            print("Usage: mcp_client.py register <agent_name> <project> <file1> [file2] ...")
            sys.exit(1)
        result = asyncio.run(call_tool("register_activity", {
            "agent_name": args[0], "project": args[1], "files": args[2:]
        }))
        print(result)

    elif cmd == "check":
        if len(args) < 2:
            print("Usage: mcp_client.py check <project> <file1> [file2] ...")
            sys.exit(1)
        result = asyncio.run(call_tool("check_conflict", {
            "project": args[0], "files": args[1:]
        }))
        print(result)

    elif cmd == "unregister":
        if len(args) < 1:
            print("Usage: mcp_client.py unregister <agent_name>")
            sys.exit(1)
        result = asyncio.run(call_tool("unregister_activity", {"agent_name": args[0]}))
        print(result)

    elif cmd == "heartbeat":
        if len(args) < 1:
            print("Usage: mcp_client.py heartbeat <agent_name>")
            sys.exit(1)
        result = asyncio.run(call_tool("heartbeat", {"agent_name": args[0]}))
        print(result)

    elif cmd == "active-agents":
        result = asyncio.run(read_resource("active-agents://"))
        print(result)

    elif cmd == "issues":
        if len(args) < 1:
            print("Usage: mcp_client.py issues <repo> [--open|--closed|--all] [--labels x,y]")
            sys.exit(1)
        repo = args[0]
        state = "open"
        labels = ""
        if "--closed" in args: state = "closed"
        elif "--all" in args: state = "all"
        if "--labels" in args:
            idx = args.index("--labels")
            labels = args[idx + 1] if idx + 1 < len(args) else ""
        result = asyncio.run(call_tool("list_issues", {
            "repo": repo, "state": state, "labels": labels
        }))
        print(result)

    elif cmd == "create-issue":
        if len(args) < 3:
            print("Usage: mcp_client.py create-issue <repo> <title> <body> [label1 label2 ...]")
            sys.exit(1)
        repo = args[0]
        title = args[1]
        body = args[2] if len(args) > 2 else ""
        labels = args[3:] if len(args) > 3 else []
        result = asyncio.run(call_tool("create_issue", {
            "repo": repo, "title": title, "body": body, "labels": labels
        }))
        print(result)

    elif cmd == "close-issue":
        if len(args) < 2:
            print("Usage: mcp_client.py close-issue <repo> <number> [comment]")
            sys.exit(1)
        repo = args[0]
        num = int(args[1])
        comment = args[2] if len(args) > 2 else ""
        result = asyncio.run(call_tool("close_issue", {
            "repo": repo, "issue_number": num, "comment": comment
        }))
        print(result)

    elif cmd == "status":
        if len(args) < 1:
            print("Usage: mcp_client.py status <service_name>")
            sys.exit(1)
        result = asyncio.run(call_tool("render_status", {"service_name": args[0]}))
        print(result)

    elif cmd == "bot-health":
        if len(args) < 1:
            print("Usage: mcp_client.py bot-health <url>")
            sys.exit(1)
        result = asyncio.run(call_tool("bot_health", {"bot_url": args[0]}))
        print(result)

    elif cmd == "bot-logs":
        if len(args) < 1:
            print("Usage: mcp_client.py bot-logs <url>")
            sys.exit(1)
        result = asyncio.run(call_tool("bot_logs", {"bot_url": args[0]}))
        print(result)

    elif cmd == "restart":
        if len(args) < 1:
            print("Usage: mcp_client.py restart <service_name>")
            sys.exit(1)
        result = asyncio.run(call_tool("render_restart", {"service_name": args[0]}))
        print(result)

    elif cmd == "deploy":
        service = args[0] if args else ""
        result = asyncio.run(call_tool("render_deploy", {"service_name": service}))
        print(result)

    elif cmd == "find-skill":
        if len(args) < 1:
            print("Usage: mcp_client.py find-skill <query>")
            sys.exit(1)
        result = asyncio.run(call_tool("find_skill", {"query": args[0]}))
        print(result)

    elif cmd == "github-log":
        repo = args[0] if args else "brain-tools"
        result = asyncio.run(call_tool("github_log", {"repo": repo}))
        print(result)

    elif cmd == "introduce":
        if len(args) < 2:
            print("Usage: mcp_client.py introduce <role> <project> [task_id]")
            sys.exit(1)
        result = asyncio.run(call_tool("introduce_agent", {
            "role": args[0], "project": args[1],
            "task_id": args[2] if len(args) > 2 else ""
        }))
        print(result)

    elif cmd == "list-tools":
        result = asyncio.run(list_tools())
        print(result)

    elif cmd == "health":
        # Read shared-state resource
        result = asyncio.run(read_resource("shared-state://"))
        print(result)

    else:
        print(f"Unknown command: {cmd}")
        usage()


if __name__ == "__main__":
    main()
