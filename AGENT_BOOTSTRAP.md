# AGENT BOOTSTRAP (Public) — rules for AI assistants working with Alexey Brilenkov

> **This is a PUBLIC sanitized version.** No personal info, no secrets, no tokens.
> For full personal context (project details, dating, health, etc.) — use MCP server.
>
> **MCP server**: `https://mcp-shared.onrender.com/sse`
> **Bearer token**: NOT included here. Ask Alexey to paste it in your chat.
> **Token tiers**: A (read-only resources) / B (write tools: append_worklog, git_confirm)

---

## 0. Who is this for

Any AI assistant (Z.ai, Cursor, Claude Code, Cline, ChatGPT, DeepSeek, Qwen, Grok, Gemini, etc.)
that works with Alexey Brilenkov on his projects.

## 1. Critical rules (MANDATORY)

1. **NO FORCE PUSH**: `git push --force` FORBIDDEN. Use `--force-with-lease` only when necessary.

2. **NO DELETE**: Never delete files/services/databases without explicit user confirmation.

3. **GIT AFTER EACH STEP**: After each subtask (3+ file modifications) — git commit + push.
   Before push — show what's being pushed, wait for user "да" (or auto-push with announcement).

4. **NO INVENTED DATA**: Don't make up dates/names/phones. If unknown — say "не знаю, уточни".

5. **CHAT STABILITY**: Decompose tasks to ≤3 file modifications per response. If 2+ tool_calls fail in a row — STOP.

6. **WORKLOG MANDATORY**: After each subtask, append to worklog.md (via MCP tool `append_worklog` or manually).

7. **BOT ACCESS CONTROL**: Every TG bot must have `ALLOWED_TG_USER_IDS` env var (whitelist).

8. **NO SUBMODULES**: brain-tools is single source of truth for rules, but NOT a git submodule. Clone or WebFetch when needed.

## 2. Agent Identity Protocol (MANDATORY for ALL agents)

### At session start — introduce yourself:
```
[Agent Identity]
🤖 Agent: <your name — e.g. "ChatGPT-4o" or "Cursor assistant">
🎯 Working with: <project if known, or "general">
📚 Context: this public AGENT_BOOTSTRAP (sanitized version)
```

### Before git push/pull/commit (3+ files) — confirm with user:
```
[Git Operation Confirmation]
📤 About to push:
  - repo: <name>
  - branch: <branch>
  - commits: <count>
  - files: <list>
Подтверждаешь push? (да/нет)
```
STOP and wait for "да". NEVER silent push.

### Auto-push (after 3+ modifications) — announce, don't ask:
```
[Auto-Push — git-after-each-step rule]
📤 Auto-pushing: <count> commits to <branch>
```

### Project context switch — announce:
```
[Context Switch]
🔄 Switching: <prev> → <new>
📁 Reading: project-<new>/SKILL.md via MCP
✅ Done. Now in <new> context.
```

## 3. MCP server (for full personal context)

- **URL**: `https://mcp-shared.onrender.com/sse`
- **Auth**: Bearer token (ask Alexey to paste in chat)
- **Token tiers**:
  - **Tier A** (read-only): read resources (full AGENT_BOOTSTRAP, skills, worklog)
  - **Tier B** (write): + tools (append_worklog, git_confirm, render_status)

### Resources available via MCP:
- `shared-state://` — live coordination file (SHARED_STATE.md)
- `skill-list://` — list of all available skills
- `skill://{name}` — specific skill SKILL.md content
- (planned) `brain-tools://agent-bootstrap-private` — full AGENT_BOOTSTRAP with personal context
- (planned) `brain-tools://worklog?limit=N` — worklog tail

### Tools available via MCP:
- `scheduler_status()` — check scheduler-bot health on Render
- (planned) `introduce_agent(role, project, task_id)` — generate identity intro
- (planned) `find_skill(query)` — search skills by keywords
- (planned) `git_confirm(operation, repo, branch, files)` — format confirmation
- (planned) `append_worklog(task_id, agent, summary)` — append to worklog (Tier B)
- (planned) `render_status(service_name)` — query Render API

## 4. How to get full context (per AI type)

### Tool-enabled AI (Cursor, Claude Code, Cline):
1. `git clone https://github.com/brilenkov/agent-rules.git`
2. Open in your IDE — auto-reads `.cursorrules` / `CLAUDE.md` / `.clinerules` (symlinks → this file)
3. Configure MCP client with URL + bearer token (ask Alexey)
4. Now you have: public rules + MCP-gated personal context

### Chat-only AI (ChatGPT, DeepSeek, Qwen, Grok, Gemini web):
1. User pastes this URL → you WebFetch it → read rules
2. Introduce yourself per Identity Protocol
3. For project context — ask user for MCP bearer token
4. Call MCP server with token (if your platform supports HTTP/MCP)

### Z.ai main agent:
- Has full filesystem access to private brain-tools repo
- Reads full AGENT_BOOTSTRAP.md (with personal context)
- Has Skill tool (136 skills available)
- Tier B MCP token in env vars

## 5. Subagent delegation (for parent agents)

When delegating to a subagent via Task tool, parent MUST inject rules into subagent prompt.
Use `subagent-prompt-template.md` from `agent-skills/` directory.

Key rules to inject:
1. Subagent introduces itself at start
2. Subagent NEVER silent push/pull — returns commit info to parent
3. Parent shows user confirmation prompt → user says "да" → parent pushes
4. Subagent appends to worklog after subtask
5. Subagent returns final report to parent

⚠️ Subagent gets ONLY what parent puts in prompt. Subagent does NOT see filesystem, skills, or worklog directly.

## 6. Cross-platform config files (symlinks)

All AI tool config files in this repo are symlinks to AGENT_BOOTSTRAP.md:

| File | AI Tool |
|------|---------|
| `.cursorrules` | Cursor |
| `CLAUDE.md` | Claude Code |
| `.clinerules` | Cline |
| `AGENTS.md` | OpenAI Codex CLI / Aider |
| `GEMINI.md` | Gemini Code Assist |
| `.windsurfrules` | Windsurf |
| `CONVENTIONS.md` | Aider (alt) |
| `.continuerules` | Continue.dev |
| `.aider.rules` | Aider (alt 2) |
| `.codeiumrules` | Codeium |
| `.codyrules` | Sourcegraph Cody |
| `.amazonq-project.md` | Amazon Q Developer |
| `.github/copilot-instructions.md` | GitHub Copilot Chat |

## 7. Available skills (generic, no personal info)

~20 generic agent-skills in `agent-skills/` directory. For personal project skills (dating, health, finance, etc.) — use MCP server with bearer token.

## 8. When things go wrong

### Chat broke (HTTP 400, tool_call error):
1. STOP — don't make more tool_calls
2. If you have filesystem: run `python /home/z/my-project/scripts/session-export.py`
3. Tell user: "start new chat, here's the summary"

### Git push rejected (parallel work):
1. `git fetch origin`
2. `git pull --rebase origin main` (NOT `git pull` without rebase)
3. Resolve conflicts
4. `git rebase --continue`
5. `git push origin main`

### MCP server not responding:
1. Check `https://mcp-shared.onrender.com/health`
2. If down — Render free tier might be sleeping (cold start ~30s)
3. Retry with longer timeout

---

**Version**: 1.0 — 2026-10-26
**Full version**: Available via MCP resource `brain-tools://agent-bootstrap-private` (requires Tier A+ token)
**Source**: https://github.com/brilenkov/agent-rules/blob/main/AGENT_BOOTSTRAP.md
