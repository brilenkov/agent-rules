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

## 3.5 Agent coordination protocol (MANDATORY for all MCP-connected agents)

When working with MCP server, use these tools to prevent git conflicts with other agents:

### Before starting work:
```
1. register_activity("your-name", "project-name", ["file1.py", "file2.py"], "task-id")
   → Tells other agents: "I'm working on these files"
   → Returns conflict warning if someone else is on same files

2. check_conflict("project-name", ["file1.py"])
   → Returns JSON: {conflicts: [], recommendation: "proceed"} or {conflicts: [...], recommendation: "wait"}
```

### During long tasks (>5 min):
```
3. heartbeat("your-name")
   → Keeps you active. If no heartbeat for 10 min → auto-removed (others can proceed)
```

### Before git push:
```
4. check_conflict("project-name", ["file1.py"])
   → Verify no new conflicts since you started
```

### After git push:
```
5. unregister_activity("your-name")
   → Frees the files for other agents
```

### Read who's active:
```
Resource: active-agents://
→ Returns list of all active agents + their projects + files + started time
```

### If conflict detected:
- **Option A**: Wait — check again in 5 min (other agent may finish)
- **Option B**: Work on different files (no overlap)
- **Option C**: Ask user "zai-main is working on bot.py. Proceed anyway? (да/нет)"
- **Option D**: Create git branch (for complex multi-file work)

## 3.6 Unique agent identification (MANDATORY)

Each Z.ai chat session MUST identify uniquely:

### At session start — ask user for chat identifier:
```
Agent: "What is this chat's name? (e.g. 'brain-tools', 'aks', 'transcribe')"
User: "brain-tools"
Agent: [Agent Identity]
  🤖 Agent: Z.ai brain-tools
  🎯 Working with: <project>
```

### Git author — push under your chat name:
```bash
git config user.name "Z.ai <chat-name>"
git config user.email "z-ai-<chat-name>@local"
```
Examples:
- `Z.ai brain-tools` — for infrastructure/MCP/agent-rules work
- `Z.ai aks` — for AKS aviation tests
- `Z.ai transcribe` — for audio transcription
- `Z.ai fns-bot` — for FNS receipt bot

### Commit message format (Conventional Commits):
```
<type>(<project>): <description> (fixes #NN)

Types: feat, fix, docs, refactor, test, chore
Examples:
  feat(fns-bot): T-Bank SMS parser (fixes #42)
  fix(mcp-shared): OOM on Render free tier
  docs(agent-rules): SETUP_GUIDE.md
  chore(council-bot): lazy ChromaDB init
```

## 3.7 Task tracking via GitHub Issues (MANDATORY)

Use GitHub Issues for task tracking instead of ad-hoc TODOs.

### Before starting work:
```
1. list_issues("brain-tools", "open", "fns-bot")
   → Check if there's an open issue for your project

2. If no issue exists → create one:
   create_issue("brain-tools",
     title="[fns-bot] bug: TTS race condition",
     body="## What\nTTS plays both browser + z-ai simultaneously\n...",
     labels=["bug", "fns-bot"])

3. Assign to yourself:
   assign_issue("brain-tools", 42, "brilenkov")
```

### During work:
```
4. Register in MCP coordination:
   register_activity("Z.ai brain-tools", "fns-bot", ["bot.py"], "issue-42")

5. Commit with issue reference:
   git commit -m "fix(fns-bot): TTS race condition (fixes #42)"
```

### After push:
```
6. GitHub auto-closes issue #42 (because of 'fixes #42' in commit)
   OR manually: close_issue("brain-tools", 42, "Fixed via commit abc123")

7. unregister_activity("Z.ai brain-tools")
```

### Issue title naming convention:
```
[<project>] <type>: <short description>

Projects: fns-bot, tg-monitor, council-bot, mcp-shared, webrtc,
          marathon-bot, agent-rules, transcribe, aks

Types: bug, feature, enhancement, docs, chore, test, refactor

Examples:
  [fns-bot] bug: TTS race condition
  [council-bot] enhancement: lazy ChromaDB init
  [mcp-shared] feature: GitHub Issues tools
  [agent-rules] docs: SETUP_GUIDE.md
```

### Labels (already created in brain-tools repo):
- **Type labels**: `bug`, `feature`, `enhancement`, `docs`, `chore`, `test`, `refactor`
- **Project labels**: `fns-bot`, `tg-monitor`, `council-bot`, `mcp-shared`, `webrtc`, `marathon-bot`, `agent-rules`, `transcribe`, `aks`

### GitHub Projects (Kanban board):
- Create manually at github.com/brilenkov → Projects → New board
- Add issues from all repos → single view
- Columns: Backlog → In Progress → Review → Done

## 3.8 MCP client setup (MANDATORY for Z.ai agents)

Every Z.ai chat session MUST install MCP client at session start for coordination.

### Setup (run at session start, after AGENT_BOOTSTRAP read):
```bash
# 1. Install MCP SDK
pip install mcp

# 2. Set env vars
export MCP_URL=https://mcp-shared.onrender.com/sse
export MCP_TOKEN=<bearer token from Bitwarden>

# 3. Get the client script (from brain-tools private repo)
cp /home/z/my-project/brain-tools/scripts/mcp_client.py /home/z/my-project/scripts/

# 4. Test connection
python3 scripts/mcp_client.py list-tools
# Should show 20 tools + 6 resources
```

### Coordination workflow (at start of every task):
```bash
# Register: "I'm working on X"
python3 scripts/mcp_client.py register "Z.ai <chat-name>" "<project>" <file1> <file2>

# Check conflicts
python3 scripts/mcp_client.py check "<project>" <file1>

# See who's active
python3 scripts/mcp_client.py active-agents

# Heartbeat (every 5 min for long tasks)
python3 scripts/mcp_client.py heartbeat "Z.ai <chat-name>"

# Unregister after done
python3 scripts/mcp_client.py unregister "Z.ai <chat-name>"
```

### Other useful MCP commands:
```bash
# GitHub Issues
python3 scripts/mcp_client.py issues brain-tools --open --labels fns-bot
python3 scripts/mcp_client.py create-issue brain-tools "[fns-bot] bug: description" "body" bug fns-bot
python3 scripts/mcp_client.py close-issue brain-tools 42 "Fixed"

# Render status
python3 scripts/mcp_client.py status fns-receipt-bot-docker
python3 scripts/mcp_client.py bot-health https://fns-receipt-bot-docker.onrender.com
python3 scripts/mcp_client.py bot-logs https://fns-receipt-bot-docker.onrender.com
python3 scripts/mcp_client.py restart fns-receipt-bot-docker
python3 scripts/mcp_client.py deploy fns-receipt-bot-docker

# Skills
python3 scripts/mcp_client.py find-skill "git push"

# GitHub log
python3 scripts/mcp_client.py github-log brain-tools
```

### Rule: coordination always through MCP when possible
- ✅ Use `mcp_client.py` for register/check/heartbeat/unregister
- ✅ Also use worklog.md (shared filesystem) as backup
- ✅ Also use GitHub Issues for task tracking
- ❌ Don't skip coordination — another agent might be working on same files

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
