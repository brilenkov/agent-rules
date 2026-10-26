# agent-rules — Public AI assistant rules for Alexey Brilenkov

Public sanitized version of AGENT_BOOTSTRAP.md for any AI assistant
(Cursor, Claude Code, Cline, ChatGPT, DeepSeek, Qwen, Grok, Gemini, etc.)

## Quick start

### For tool-enabled AI (Cursor, Claude Code, etc.)
```bash
git clone https://github.com/brilenkov/agent-rules.git
# Open in your IDE — auto-reads .cursorrules / CLAUDE.md / .clinerules
```

### For chat-only AI (ChatGPT, DeepSeek, etc.)
```
WebFetch https://github.com/brilenkov/agent-rules/blob/main/AGENT_BOOTSTRAP.md
```

### For MCP-aware AI (Claude Desktop, Cursor with MCP, Continue.dev)
1. Read AGENT_BOOTSTRAP.md (this repo)
2. Configure MCP server: `https://mcp-shared.onrender.com/sse`
3. Ask Alexey for bearer token

## What's here

- `AGENT_BOOTSTRAP.md` — public sanitized rules (no personal info, no secrets)
- `agent-skills/` — ~20 generic agent skills (no personal info)
- `MCP_PHASES.md` — 3-tier architecture implementation plan
- `MCP_CROSS_PLATFORM_SUPPORT.md` — coverage map (which AI tool uses what)
- `.cursorrules`, `CLAUDE.md`, `.clinerules`, etc. — symlinks to AGENT_BOOTSTRAP.md

## What's NOT here (private — via MCP server)

- Personal context (name, age, family, dating status)
- Project-specific skills (project-dating, project-maria, audit-*, etc.)
- Bot tokens, API keys, session strings
- Render service details

Access these via MCP server with bearer token. Ask Alexey.
