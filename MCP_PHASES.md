# MCP_PHASES.md — 3-tier architecture implementation plan

> **Created**: 2026-10-26
> **Status**: Plan document. Phase 0 (this file) done. Phases 1-6 to be implemented.
> **Related**:
> - Existing mcp-shared server: https://github.com/brilenkov/brain-tools/tree/main/bots/mcp-shared (FastMCP, SSE transport, Bearer auth — already deployed on Render)
> - MCP_CROSS_PLATFORM_SUPPORT.md (coverage map)
> - MCP_SERVER_DESIGN.md (original design — superseded by this file)

---

## 🎯 Architecture summary (3 tiers)

```
┌─────────────────────────────────────────────────────────────────┐
│  Tier 1: PUBLIC sanitized AGENT_BOOTSTRAP.md                   │
│  ─────────────────────────────────────────────                  │
│  New public repo: github.com/brilenkov/agent-rules             │
│  - Sections 0, 5, 5.5-5.9, 10, 11, 12 (rules + protocols)     │
│  - Generic agent-skills (no personal info: agent-bootstrap,    │
│    agent-identity-protocol, do-not-delete, no-force-push, etc.) │
│  - MCP server URL (https://mcp-shared.onrender.com/sse)         │
│  - "Ask user for bearer token" instruction                     │
│  NO: names, ages, dating, tokens, paths, secrets               │
└─────────────────────────────────────────────────────────────────┘
                          ↑
                          │ WebFetch (any AI, no auth)
                          │
┌─────────────────────────────────────────────────────────────────┐
│  Tier 2: mcp-shared MCP server (gated by bearer token)         │
│  ─────────────────────────────────────────────                  │
│  https://mcp-shared.onrender.com/sse (ALREADY LIVE)             │
│  - Server has PAT to brain-tools (private repo)                 │
│  - Clients never see PAT — only bearer token                   │
│  - Exposes: resources (full AGENT_BOOTSTRAP, skills), tools    │
│  - Token tiers (TODO — add multi-token support):               │
│    * Tier A (read-only, rate-limited): resources               │
│    * Tier B (write tools): append_worklog, git_confirm         │
└─────────────────────────────────────────────────────────────────┘
                          ↑
                          │ Bearer token (manually pasted per AI, from Bitwarden)
                          │ NOT in any public file
                          │
┌─────────────────────────────────────────────────────────────────┐
│  Tier 3: PRIVATE brain-tools repo (current)                    │
│  ─────────────────────────────────────────────                  │
│  github.com/brilenkov/brain-tools (PRIVATE)                    │
│  - Full AGENT_BOOTSTRAP.md (after Phase 1 — secrets removed)   │
│  - All 58 agent-skills (incl. project-dating, project-maria)   │
│  - .git-credentials, .render-credentials                        │
│  - Bot code, scripts, sites                                      │
│  Access: PAT required (only Z.ai main + mcp-shared server)     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Phase-by-phase implementation

### Phase 0: Save this plan (DONE — this file)
- **Who**: Z.ai main agent (me)
- **Status**: ✅ done
- **Action**: created MCP_PHASES.md, committed to brain-tools

### Phase 1: URGENT sanitize AGENT_BOOTSTRAP.md (in private brain-tools)
**Why urgent**: AGENT_BOOTSTRAP.md currently contains REAL TOKEN VALUES:
- `COMONITOR_BOT_TOKEN = 8888173059:AAEvP9VLClJemimeav0akH9b-MzgPg5PCk0`
- `Telegram API_ID/HASH = 27644518 / 2a58808d4d9b12672ed290a07ba863bf`
- Paths to session strings

Even though brain-tools is private — anyone with PAT access (or in future anyone with read access if we accidentally leak PAT) sees these tokens. Move all token VALUES to Render env vars only; AGENT_BOOTSTRAP.md should only mention ENV VAR NAMES.

**Who does what**:
- ✅ **Me**: Edit AGENT_BOOTSTRAP.md Section 4 — replace token values with env var names
- ✅ **Me**: Commit + push to private brain-tools

**Files affected**: AGENT_BOOTSTRAP.md only

**Estimated time**: 5 minutes

---

### Phase 2: Create public repo `brilenkov/agent-rules`
**Why**: For Tier 1 sanitized bootstrap — any AI can WebFetch without PAT.

**Who does what**:
- ✅ **Me**: Create public repo via GitHub API (PAT has `repo` scope — can create repos)
- ✅ **Me**: Create sanitized AGENT_BOOTSTRAP.md (Tier 1 content only)
- ✅ **Me**: Copy generic agent-skills (15-20 skills, no project-dating/maria/audit-*)
- ✅ **Me**: Create symlinks (.cursorrules, CLAUDE.md, .clinerules, AGENTS.md, GEMINI.md, etc.)
- ✅ **Me**: Commit + push to new public repo
- (Optional) **User**: verify on github.com/brilenkov/agent-rules that no sensitive info leaked

**Files to create in public repo**:
```
agent-rules/
├── AGENT_BOOTSTRAP.md           ← sanitized, ~250 lines (no personal/secrets)
├── .cursorrules → AGENT_BOOTSTRAP.md
├── CLAUDE.md → AGENT_BOOTSTRAP.md
├── .clinerules → AGENT_BOOTSTRAP.md
├── AGENTS.md → AGENT_BOOTSTRAP.md
├── GEMINI.md → AGENT_BOOTSTRAP.md
├── .windsurfrules → AGENT_BOOTSTRAP.md
├── CONVENTIONS.md → AGENT_BOOTSTRAP.md
├── .continuerules → AGENT_BOOTSTRAP.md
├── .aider.rules → AGENT_BOOTSTRAP.md
├── .codeiumrules → AGENT_BOOTSTRAP.md
├── .codyrules → AGENT_BOOTSTRAP.md
├── .amazonq-project.md → AGENT_BOOTSTRAP.md
├── .github/copilot-instructions.md → AGENT_BOOTSTRAP.md
├── README.md                    ← explains purpose + how to use
├── MCP_PHASES.md                ← this file (public copy, no implementation secrets)
├── MCP_CROSS_PLATFORM_SUPPORT.md ← coverage map (public)
└── agent-skills/                ← ~20 generic skills (no personal ones)
    ├── agent-bootstrap/SKILL.md
    ├── agent-identity-protocol/SKILL.md
    ├── subagent-prompt-template.md
    ├── do-not-delete/SKILL.md
    ├── no-force-push/SKILL.md
    ├── git-after-each-step/SKILL.md
    ├── git-credentials-guard/SKILL.md
    ├── chat-stability-guard/SKILL.md
    ├── time-guard/SKILL.md
    ├── worklog-digest/SKILL.md
    ├── session-summary-export/SKILL.md
    ├── schedule-change-guard/SKILL.md
    ├── tg-bot-access-control/SKILL.md
    ├── telegram-bot-development/SKILL.md
    ├── telegram-kb/SKILL.md
    ├── bot-test-suite/SKILL.md
    ├── debug-status/SKILL.md
    ├── do-it-now/SKILL.md
    ├── skill-creator/SKILL.md
    ├── skill-gap-analyzer/SKILL.md
    └── safe-reseed-policy/SKILL.md
```

**Skills NOT in public repo** (have personal info):
- ❌ project-dating (Victoria 44, Анна, Яна)
- ❌ project-maria, project-maria-3d-store, project-maxim
- ❌ project-tg-monitor, project-council-bot, project-marathon-bot (mention Render service IDs)
- ❌ audit-finance, audit-health, audit-physical, audit-relationships, audit-self-education, audit-spiritual (have personal info)
- ❌ project-aks (production security-sensitive)
- ❌ project-transcribe (mentions saved sohbets)
- ❌ avito-outreach-tracker (mentions real Avito contacts)
- ❌ bo-rag-query, bo-sohbet-kb (mention Борис Олегович by name)
- ❌ course-document-generator, course-materials-source-of-truth, glossary-guard (course-specific personal)
- ❌ facilitator-reports-workflow (mentions marathon bot users)
- ❌ fns-receipt-bot (mentions FNS API details)
- ❌ finance-tracker (mentions money transactions)
- ❌ new-contact-processor (mentions brain-vault contacts)
- ❌ role-classifier (mentions contact names)
- ❌ schedule-google-sync, schedule-google-sync-bidirectional (mention calendar IDs)
- ❌ task-goals-projects-organizer (mentions personal goals)
- ❌ vk-scout-update (mentions VK scraping)
- ❌ wfolio-reference-rebuild (mentions photographer names)

**Estimated time**: 30 minutes

---

### Phase 3: Extend mcp-shared server with new resources/tools
**Why**: mcp-shared already exists (FastMCP, SSE, Bearer auth, deployed on Render). Need to add:
- `brain-tools://agent-bootstrap-public` → sanitized Tier 1 version
- `brain-tools://agent-bootstrap-private` → full Tier 3 version (requires Tier B token)
- `brain-tools://user-context` → personal info (Tier B)
- `brain-tools://skills/{name}` → existing — extend to include personal skills (Tier B)
- `brain-tools://worklog?limit=N` → worklog tail (Tier B)
- `brain-tools://projects` → list of project-* skills (Tier A names, Tier B content)

New tools:
- `introduce_agent(role, project, task_id)` — generate identity intro text
- `find_skill(query)` — search skills by trigger keywords
- `git_confirm(operation, repo, branch, files, commits)` — format confirmation prompt
- `append_worklog(task_id, agent, summary)` — append to worklog.md (Tier B)
- `render_status(service_name)` — query Render API
- `project_switch(from, to)` — return new project context

**Who does what**:
- ✅ **Me**: Edit `bots/mcp-shared/server.py` — add new resources/tools
- ✅ **Me**: Commit + push to brain-tools
- ✅ **Render auto-deploys** mcp-shared on push

**Files affected**: bots/mcp-shared/server.py, possibly bots/mcp-shared/README.md

**Estimated time**: 1 hour

---

### Phase 4: Multi-token support in mcp-shared
**Why**: Currently single `MCP_BEARER_TOKEN` env var. Need Tier A (read-only) + Tier B (write) tokens, individually revocable.

**Implementation**:
- Add env var `MCP_TOKENS_JSON` on Render: JSON map of token → permissions
  ```json
  {
    "mcp_zai_main_b_2026_10_27": {"tier": "B", "rate": 1000, "expires": null},
    "mcp_cursor_a_2026_10_27": {"tier": "A", "rate": 100, "expires": null},
    "mcp_chatgpt_temp_2026_10_27": {"tier": "A", "rate": 50, "expires": "2026-10-28T00:00:00Z"}
  }
  ```
- Modify auth middleware in server.py: parse Bearer, look up in MCP_TOKENS_JSON, check tier + rate + expiry
- Keep `MCP_BEARER_TOKEN` for backward compat (treat as Tier B admin)

**Who does what**:
- ✅ **Me**: Edit server.py — add token validation middleware
- ✅ **Me**: Commit + push (auto-deploy)
- ✅ **User**: Generate tokens via script, add to Bitwarden, set as MCP_TOKENS_JSON env var on Render

**Files affected**: bots/mcp-shared/server.py

**Estimated time**: 1 hour

---

### Phase 5: Bitwarden + token distribution workflow
**Why**: Tokens must NOT be in any public file. User stores them in Bitwarden vault, pastes per-AI session.

**Who does what**:
- ❌ **User (manual)**: Create Bitwarden vault "AI agent tokens"
- ❌ **User**: For each new AI session, generate token via script, save to Bitwarden, paste in chat
- ✅ **Me**: Write `scripts/generate_mcp_token.py` — generates random token, suggests env var update
- ✅ **Me**: Document workflow in `agent-rules/README.md` (public) — "How to request token from Алексей"

**Files affected**: scripts/generate_mcp_token.py (new)

**Estimated time**: 30 minutes

---

### Phase 6: Connect AI clients to MCP
**Why**: Configure each AI tool to use mcp-shared.

**Who does what**:
- ❌ **User (manual)**: For each AI tool (Cursor, Claude Desktop, Continue.dev):
  1. Get bearer token from Bitwarden
  2. Configure MCP client (per tool's docs)
  3. Test connection
- ✅ **Me**: Provide configuration snippets per tool in `agent-rules/README.md`
- ✅ **Me**: For Cursor — `.cursor/mcp.json` template
- ✅ **Me**: For Claude Desktop — `claude_desktop_config.json` template
- ✅ **Me**: For Continue.dev — `.continue/config.yaml` template

**Files affected**: agent-rules/README.md, agent-rules/mcp-config-templates/

**Estimated time**: 30 min (me) + 30 min (user per tool)

---

## 📊 Summary: what I do vs what user does

| Phase | What | Who | Status |
|-------|------|-----|--------|
| 0 | Save this plan to git | Me | ✅ done |
| 1 | Sanitize AGENT_BOOTSTRAP.md (remove token VALUES) | Me | pending |
| 2 | Create public `brilenkov/agent-rules` repo + sanitized content | Me (via GitHub API) | pending |
| 3 | Extend mcp-shared server (resources/tools) | Me | pending |
| 4 | Multi-token support in mcp-shared | Me | pending |
| 5 | Bitwarden vault setup | User (manual) | pending |
| 5 | Token generation script | Me | pending |
| 6 | Connect AI clients (Cursor, Claude Desktop, etc.) | User (per tool, with my templates) | pending |
| 6 | Provide MCP config templates per tool | Me | pending |

**Total my work**: ~3-4 hours (Phases 0-4, 5-script, 6-templates)
**Total user work**: ~1 hour (Bitwarden setup + per-AI client configuration)

---

## 🔐 Security checklist

- [ ] **Phase 1**: Remove `COMONITOR_BOT_TOKEN` value from AGENT_BOOTSTRAP.md
- [ ] **Phase 1**: Remove Telegram `API_ID`/`API_HASH` values
- [ ] **Phase 1**: Replace paths to session strings with "see env var"
- [ ] **Phase 2**: Verify no personal info in public `agent-rules` repo before push
- [ ] **Phase 2**: Audit each agent-skill for personal info before copying to public
- [ ] **Phase 4**: Token validation middleware tested
- [ ] **Phase 4**: Tokens stored in Bitwarden (NOT in any git repo)
- [ ] **Phase 4**: Render env var `MCP_TOKENS_JSON` set (sync:false)
- [ ] **Phase 6**: Each AI tool configured with individual token (not shared)

---

## 🎯 After all 6 phases — final state

| AI Tool | Bootstrap source | MCP token | Tier |
|---------|-----------------|-----------|------|
| **Z.ai main** (this) | brain-tools AGENT_BOOTSTRAP.md (private, full) | mcp_zai_main_b_* (Tier B) | 3 + 2 |
| **Cursor** (user's PC) | agent-rules AGENT_BOOTSTRAP.md (public, sanitized) | mcp_cursor_a_* (Tier A) | 1 + 2 |
| **Claude Code** (user's PC) | same | mcp_claude_a_* (Tier A) | 1 + 2 |
| **ChatGPT (web)** | WebFetch agent-rules URL | mcp_chatgpt_temp_* (24h Tier A) | 1 + 2 |
| **DeepSeek web** | same | mcp_deepseek_temp_* | 1 + 2 |
| **Qwen web** | same | mcp_qwen_temp_* | 1 + 2 |
| **Grok web** | same | mcp_grok_temp_* | 1 + 2 |
| **Gemini web** | same | mcp_gemini_temp_* | 1 + 2 |
| **Z.ai subagents** | Parent injects subagent-prompt-template.md | inherits parent's Tier B | 2 (limited) |

**Result**: ANY AI can:
1. Read Tier 1 public rules (no auth)
2. With bearer token — access Tier 2 MCP resources (full AGENT_BOOTSTRAP, all skills, worklog)
3. With Tier B token — call write tools (append_worklog, git_confirm)
4. NEVER sees PAT, never sees other AI's tokens

---

**Version**: 1.0 — 2026-10-26
**Author**: Z.ai main agent (per agent-identity-protocol)
**Implementation**: starting after user confirms direction
