# MCP Cross-Platform AI Support — Coverage Map

> **Created**: 2026-10-26
> **Status**: Phase 1 complete (symlinks + chat-only + MCP design). MCP server implementation pending.
> **Single source of truth**: `AGENT_BOOTSTRAP.md` (in this repo, 519+ lines)

---

## 📋 Что сделано

3 фазы cross-platform AI support:

### ✅ Phase 1: Symlinks для AI tools (13 файлов)
В brain-tools root созданы symlinks на популярные config-файлы. Каждый AI tool
автоматически читает свой config при открытии репо, который указывает на
`AGENT_BOOTSTRAP.md` → AI сразу видит все правила.

### ✅ Phase 2: Chat-only fallback (`AGENT_BOOTSTRAP_CHAT_ONLY.md`)
Minimal version (~150 lines) для AIs без filesystem доступа (ChatGPT, Claude
web, DeepSeek, Qwen, Grok, Gemini web). User вставляет URL в чат → AI через
WebFetch читает правила.

### ✅ Phase 3: MCP server design (`MCP_SERVER_DESIGN.md`)
Дизайн-документ для единого MCP-сервера (planned, not implemented):
- HTTP MCP server на Render
- Exposes resources (AGENT_BOOTSTRAP, 58 skills, worklog, Render status)
- Exposes tools (introduce_agent, find_skill, git_confirm, append_worklog,
  render_status, session_start, project_switch)
- Exposes prompts (subagent_template, session_start, git_push_confirmation)
- Implementation: FastMCP Python (~150 lines)

---

## 📁 Структура brain-tools после изменений

```
brain-tools/
├── AGENT_BOOTSTRAP.md                            ← full rules (519+75 lines, single source of truth)
├── AGENT_BOOTSTRAP_CHAT_ONLY.md                  ← minimal version (150 lines) для chat-only AIs
├── MCP_SERVER_DESIGN.md                         ← MCP design doc (280 lines, not implemented)
├── MCP_CROSS_PLATFORM_SUPPORT.md                 ← ЭТОТ ФАЙЛ — coverage map + summary
│
├── .cursorrules → AGENT_BOOTSTRAP.md             ← Cursor
├── CLAUDE.md → AGENT_BOOTSTRAP.md                ← Claude Code
├── .clinerules → AGENT_BOOTSTRAP.md              ← Cline
├── AGENTS.md → AGENT_BOOTSTRAP.md                ← OpenAI Codex CLI / Aider
├── GEMINI.md → AGENT_BOOTSTRAP.md                ← Gemini Code Assist
├── .windsurfrules → AGENT_BOOTSTRAP.md           ← Windsurf (Codeium IDE)
├── CONVENTIONS.md → AGENT_BOOTSTRAP.md           ← Aider (alternative)
├── .continuerules → AGENT_BOOTSTRAP.md           ← Continue.dev
├── .aider.rules → AGENT_BOOTSTRAP.md             ← Aider (alternative 2)
├── .codeiumrules → AGENT_BOOTSTRAP.md             ← Codeium
├── .codyrules → AGENT_BOOTSTRAP.md               ← Sourcegraph Cody
├── .amazonq-project.md → AGENT_BOOTSTRAP.md      ← Amazon Q Developer
├── .github/copilot-instructions.md → AGENT_BOOTSTRAP.md ← GitHub Copilot Chat
│
└── agent-skills/                                  ← 58 user-custom skills (in git)
    ├── agent-bootstrap/SKILL.md                   ← proactive session start
    ├── agent-identity-protocol/SKILL.md           ← MANDATORY identity + git confirmation
    ├── subagent-prompt-template.md                ← copy-paste template for Task prompts
    ├── project-council-bot/SKILL.md               ← council-bot context
    ├── project-tg-monitor/SKILL.md                ← tg-monitor context
    ├── audit-finance/SKILL.md                     ← 6 audit-* skills
    ├── audit-health/SKILL.md
    ├── audit-physical/SKILL.md
    ├── audit-relationships/SKILL.md
    ├── audit-self-education/SKILL.md
    ├── audit-spiritual/SKILL.md
    ├── avito-outreach-tracker/SKILL.md            ← TFP outreach
    ├── bo-rag-query/SKILL.md                      ← RAG по БО сохбетам
    ├── bo-sohbet-kb/SKILL.md                      ← БО knowledge base
    ├── bot-access-info/SKILL.md                   ← marathon_bot env info
    ├── bot-test-suite/SKILL.md                    ← regression testing
    ├── chat-stability-guard/SKILL.md              ← prevent chat breakage
    ├── course-document-generator/SKILL.md         ← FULL_COURSE.md pipeline
    ├── course-materials-source-of-truth/SKILL.md
    ├── daily-note-scaffolder/SKILL.md
    ├── debug-status/SKILL.md
    ├── do-it-now/SKILL.md                         ← GTD 2-min rule
    ├── do-not-delete/SKILL.md                     ← never delete without confirm
    ├── facilitator-reports-workflow/SKILL.md
    ├── finance-tracker/SKILL.md                  ← money transactions
    ├── fns-receipt-bot/SKILL.md                   ← FNS receipts bot skill
    ├── git-after-each-step/SKILL.md               ← auto-commit after 3+ mods
    ├── git-credentials-guard/SKILL.md             ← protect PAT
    ├── glossary-guard/SKILL.md                   ← course terminology
    ├── new-contact-processor/SKILL.md
    ├── no-force-push/SKILL.md                     ← never --force
    ├── project-aks/SKILL.md                       ← 14 project-* skills
    ├── project-council-bot/SKILL.md
    ├── project-dating/SKILL.md
    ├── project-lr-plugin/SKILL.md
    ├── project-marathon-bot/SKILL.md
    ├── project-maria-3d-store/SKILL.md
    ├── project-maria/SKILL.md
    ├── project-maxim/SKILL.md
    ├── project-photography/SKILL.md
    ├── project-raw-to-lightroom/SKILL.md
    ├── project-redmine-setup/SKILL.md
    ├── project-schedule/SKILL.md
    ├── project-stiranie/SKILL.md
    ├── project-tg-monitor/SKILL.md
    ├── project-transcribe/SKILL.md
    ├── role-classifier/SKILL.md
    ├── safe-reseed-policy/SKILL.md
    ├── schedule-change-guard/SKILL.md
    ├── schedule-google-sync-bidirectional/SKILL.md
    ├── schedule-google-sync/SKILL.md
    ├── session-summary-export/SKILL.md
    ├── task-goals-projects-organizer/SKILL.md
    ├── task-review/SKILL.md
    ├── telegram-bot-development/SKILL.md
    ├── telegram-kb/SKILL.md
    ├── tg-bot-access-control/SKILL.md
    ├── tg-monitor/SKILL.md
    ├── time-guard/SKILL.md
    ├── vk-scout-update/SKILL.md
    ├── wfolio-reference-rebuild/SKILL.md
    └── worklog-digest/SKILL.md
```

---

## 🗺️ Карта покрытия AI tools

| AI Tool | Как подхватит правила | Status | Setup |
|---------|----------------------|--------|-------|
| **Cursor** | `.cursorrules` symlink → AGENT_BOOTSTRAP.md | ✅ | `git clone brain-tools` + open in Cursor |
| **Claude Code** | `CLAUDE.md` symlink | ✅ | `git clone brain-tools` + open in Claude Code |
| **Cline** | `.clinerules` symlink | ✅ | `git clone brain-tools` + open in Cline |
| **OpenAI Codex CLI** | `AGENTS.md` symlink | ✅ | `git clone brain-tools` + run `codex` |
| **Aider** | `AGENTS.md` OR `CONVENTIONS.md` OR `.aider.rules` | ✅ | `git clone brain-tools` + `aider` |
| **Gemini Code Assist** | `GEMINI.md` symlink | ✅ | `git clone brain-tools` + open in Gemini |
| **Windsurf (Codeium IDE)** | `.windsurfrules` symlink | ✅ | `git clone brain-tools` + open in Windsurf |
| **Continue.dev** | `.continuerules` symlink | ✅ | `git clone brain-tools` + Continue.dev reads |
| **Codeium** | `.codeiumrules` symlink | ✅ | `git clone brain-tools` + open in Codeium |
| **Sourcegraph Cody** | `.codyrules` symlink | ✅ | `git clone brain-tools` + open in Cody |
| **Amazon Q Developer** | `.amazonq-project.md` symlink | ✅ | `git clone brain-tools` + open in Amazon Q |
| **GitHub Copilot Chat** | `.github/copilot-instructions.md` symlink | ✅ | `git clone brain-tools` + open in Copilot Chat |
| **Z.ai main (этот)** | `Skill` tool + `/home/z/my-project/skills/` (136 skills) | ✅ | runtime copy on this machine |
| **Z.ai subagents** | Parent injects subagent-prompt-template.md | ✅ | Parent includes template in Task prompt |
| **ChatGPT (web)** | User pastes `AGENT_BOOTSTRAP_CHAT_ONLY.md` URL | ✅ manual | WebFetch GitHub URL |
| **Claude web** | User pastes URL | ✅ manual | WebFetch GitHub URL |
| **DeepSeek web** | User pastes URL | ✅ manual | WebFetch GitHub URL |
| **Qwen web** | User pastes URL | ✅ manual | WebFetch GitHub URL |
| **Grok web** | User pastes URL | ✅ manual | WebFetch GitHub URL |
| **Gemini web** | User pastes URL | ✅ manual | WebFetch GitHub URL |
| **Future MCP-aware AI** | `https://brain-tools-mcp.onrender.com/mcp` (when built) | ⏳ planned | Configure MCP URL in client |

---

## 🎯 3 уровня покрытия

### Level 1: Tool-enabled AIs (Cursor, Claude Code, Cline, Codex CLI, Aider, etc.)
- Открывают brain-tools репо → auto-reads свой config file (symlink → AGENT_BOOTSTRAP.md)
- Получают все 519+ строк правил сразу
- **Update propagation**: `git pull` в brain-tools → fresh rules

### Level 2: Chat-only AIs (ChatGPT, Claude web, DeepSeek, Qwen, Grok, Gemini web)
- User вставляет URL: `https://github.com/brilenkov/brain-tools/blob/main/AGENT_BOOTSTRAP_CHAT_ONLY.md`
- AI через WebFetch читает minimal version (~150 lines)
- Понимает user context + identity protocol + critical rules
- Если нужно больше — WebFetch full `AGENT_BOOTSTRAP.md`

### Level 3: MCP-aware AIs (Future — Claude Desktop, Cursor with MCP, Continue.dev with MCP)
- Configure MCP server URL: `https://brain-tools-mcp.onrender.com/mcp` (planned)
- Получают rules + callable tools (find_skill, append_worklog, render_status, etc.)
- Always fresh (server reads git на каждый запрос)
- Cross-machine (HTTP transport)

---

## 📊 Comparison: current symlinks vs MCP

| Aspect | Current (symlinks + git clone) | With MCP server |
|--------|--------------------------------|------------------|
| Setup per machine | `git clone brain-tools` (777MB) | None — just configure URL |
| Setup per AI tool | 13+ symlinks in repo | 1 URL in MCP config |
| Update propagation | `git pull` on each machine | Automatic (server reads fresh) |
| Chat-only AIs (Qwen, DeepSeek, Grok) | ❌ Manual paste URL | ✅ HTTP MCP if supported |
| Callable tools (find_skill, append_worklog) | ❌ Not available | ✅ Yes |
| Render service status | Manual API call | ✅ Via render_status tool |
| Cross-platform | Per-tool config | Standard MCP protocol |

---

## 📋 Migration plan (когда MCP будет готов)

1. **Phase 1** (done now): Keep symlinks for backward compat (Cursor/Claude/Cline still use them)
2. **Phase 2** (TODO): Build MCP server (FastMCP, ~150 lines Python), deploy on Render
3. **Phase 3** (TODO): Configure Cursor + Claude Desktop + Continue.dev to use MCP URL
4. **Phase 4** (TODO): Document in AGENT_BOOTSTRAP.md Section 5.9 how to use MCP
5. **Phase 5** (optional, later): Once MCP stable, remove symlinks (less files to maintain)
6. **Phase 6** (future): Add MCP tools for Render deploy trigger, GitHub PR creation, etc.

---

## 🔗 Quick reference

| Resource | URL / Path |
|----------|-----------|
| AGENT_BOOTSTRAP.md (full) | https://github.com/brilenkov/brain-tools/blob/main/AGENT_BOOTSTRAP.md |
| AGENT_BOOTSTRAP_CHAT_ONLY.md (minimal) | https://github.com/brilenkov/brain-tools/blob/main/AGENT_BOOTSTRAP_CHAT_ONLY.md |
| MCP_SERVER_DESIGN.md (design) | https://github.com/brilenkov/brain-tools/blob/main/MCP_SERVER_DESIGN.md |
| THIS file (coverage map) | https://github.com/brilenkov/brain-tools/blob/main/MCP_CROSS_PLATFORM_SUPPORT.md |
| Agent skills (58) | https://github.com/brilenkov/brain-tools/tree/main/agent-skills |
| Subagent template | https://github.com/brilenkov/brain-tools/blob/main/agent-skills/subagent-prompt-template.md |

---

## 🚧 Limitations / TODO

1. **MCP server not implemented yet** — design only (see MCP_SERVER_DESIGN.md)
2. **Render free tier HTTP MCP** — might be slow (cold start ~30s)
3. **Authentication** — MCP server should require API key (don't expose worklog/skills publicly)
4. **Z.ai support** — Z.ai doesn't yet support MCP. Until then, symlinks + Skill tool stay.
5. **ChatGPT/Qwen/DeepSeek/Grok web** — these don't yet support MCP. They use `AGENT_BOOTSTRAP_CHAT_ONLY.md` (paste manually)
6. **Worklog writes from chat-only** — MCP tool `append_worklog` requires MCP support. Chat-only AIs use parent (Z.ai main) to write.

---

**Version**: 1.0 — 2026-10-26
**Pushed at**: see git log of this file
**Author**: Z.ai main agent (per agent-identity-protocol)
