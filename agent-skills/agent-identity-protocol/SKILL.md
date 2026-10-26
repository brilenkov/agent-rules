---
name: agent-identity-protocol
description: >
  MANDATORY for ALL AI agents (Z.ai main, Cursor, chat-only assistants, telethon userbots, etc).
  Every agent MUST introduce themselves at the start of each session/response and explicitly
  confirm git push/pull operations before executing.
  
  Trigger PROACTIVELY at:
  - First message of every new chat session
  - When user asks "who are you" / "кто ты" / "с чем работаем"
  - Before ANY git push, git pull, git commit operation
  - When switching project context (e.g. "работаем с tg-monitor" → "switch to council-bot")
  - After completing a subtask (3+ file modifications)
  
  This skill ensures multi-agent coordination, prevents silent git operations, and gives
  user visibility into which agent made which changes.

  Also triggers when user says: "представься", "кто ты", "что ты умеешь", "agent identity",
  "представление агента", "подтверди пуш", "confirm git push".
---

# agent-identity-protocol

> **MANDATORY behavior** for every AI agent working with Алексей's projects.
> Solves 3 problems:
> 1. User doesn't know which agent (Z.ai / Cursor / chat-only / subagent) is responding
> 2. Silent git push/pull creates confusion when parallel agents work
> 3. Project context switching is invisible to user

## When to introduce yourself

### Always — at start of session (after reading AGENT_BOOTSTRAP.md)

```
[Agent Identity]
🤖 Agent: <name> (e.g. "Z.ai main agent" / "Cursor assistant" / "Subagent for X")
🎯 Working with: <current project> (e.g. "fns-receipt-bot" / "tg-monitor" / "council-bot")
📚 Context: AGENT_BOOTSTRAP.md + project-<name>/SKILL.md loaded
📍 Worklog: last entry from <date> (Task ID <X>)

Готов работать. Что делаем?
```

### When switching project context

User: "работаем с tg-monitor" / "switch to raw-to-lightroom" / "continue with council-bot"

Agent response BEFORE doing the work:
```
[Context Switch]
🔄 Switching: <previous project> → <new project>
📁 Loading: agent-skills/project-<new>/SKILL.md
✅ Done. Now in <new project> context.
```

### When user asks "who are you" / "кто ты"

Show identity + current project + active skill set:
```
[Agent Identity]
🤖 Agent: <name>
🎯 Working with: <project>
📚 Active skills: <list of triggered skills in this session>
🛠 Stack: <Python/Node/CLI/etc>
📍 Worklog: <last entry>
🔗 GitHub: github.com/brilenkov/<repo>

Что хочешь узнать подробнее?
```

## When to confirm git operations

### BEFORE git push (mandatory)

Before running `git push origin <branch>`:

```
[Git Operation Confirmation]
📤 About to push:
  - repo: <name>
  - branch: <branch>
  - commits: <count> commits to push
  - files changed: <list of files>
  - commit messages: <list>

Подтверждаешь push? (да/нет)
```

**STOP and wait for user "да"**. Do NOT push silently. Even if user said "закоммить" — show what will be pushed first.

Exception: `git-after-each-step` rule (commit + push after 3+ file modifications) — push can proceed automatically but MUST be announced:
```
[Auto-Push — git-after-each-step rule]
📤 Auto-pushing: <count> commits to <branch>
   Files: <list>
   Reason: subtask completed (3+ modifications)
```

### BEFORE git pull (mandatory)

Before running `git pull` or `git pull --rebase`:

```
[Git Operation Confirmation]
📥 About to pull:
  - repo: <name>
  - branch: <branch>
  - method: pull --rebase (default — preserves linear history)

Подтверждаешь pull? (да/нет)
```

### BEFORE git commit (semi-mandatory)

For commits — show what's being committed:

```
[Git Commit Preview]
💾 Files to commit:
  - <file1> (modified, +N lines -M lines)
  - <file2> (new file)
  - ...

📝 Commit message:
<commit message>

Подтверждаешь commit? (да/нет)
```

For minor commits (<3 files, single-line change) — can proceed silently but announce:
```
[Auto-Commit]
💾 Committed: <short message>
```

### NEVER silent git operations

Forbidden patterns:
```bash
# ❌ BAD — silent push, user doesn't know what happened
git push origin main

# ❌ BAD — silent force push
git push --force  # also violates no-force-push skill

# ✅ GOOD — announced + confirmed
[Git Operation Confirmation]
📤 About to push...
Подтверждаешь push? (да/нет)
# (user confirms)
git push origin main
[Pushed ✅]
```

## Format examples

### Example 1: Session start

User: "почини council-bot"

Agent (Z.ai main):
```
[Agent Identity]
🤖 Agent: Z.ai main agent (GLM-4)
🎯 Working with: project-council-bot (context loaded from agent-skills/project-council-bot/SKILL.md)
📚 Active skills: agent-bootstrap, agent-identity-protocol, project-council-bot, git-after-each-step
📍 Worklog: last entry Task ID fns-bot-v1.9.0 (2026-10-26)

Понял задачу — council-bot лежит. Что именно: OOM на Render, /health issue, или другое?
```

### Example 2: Git push with confirmation

User: "закоммить и запушь фиксы"

Agent:
```
[Git Operation Confirmation]
📤 About to push to brain-tools/main:
  - commits: 3 commits since last push
  - files changed:
    - bots/fns-receipt-bot/bot.py (+245 -12)
    - bots/therapist-voice-bot/webrtc/server.js (+89 -45)
    - bots/life_council_bot_v2/.../src/bot.py (+12 -25)

📝 Latest commit message:
  feat: TTS race fix + voice dropdown + Phase 0 prompt + access token

Подтверждаешь push? (да/нет)
```

User: "да"

Agent:
```
[Pushing...]
$ git push origin main

✅ Pushed. Live on Render (auto-deploy triggered).
```

### Example 3: Project context switch

User: "switch to tg-monitor, разберись с bulk import"

Agent:
```
[Context Switch]
🔄 Switching: fns-receipt-bot → tg-monitor
📁 Loading: agent-skills/project-tg-monitor/SKILL.md
✅ Done. Now in tg-monitor context.

[Agent Identity]
🤖 Agent: Z.ai main agent (still same)
🎯 Working with: project-tg-monitor
📚 Active skills: + project-tg-monitor, role-classifier
📍 TODOs: bulk import всех 38 контактов активных в 2026

Что именно: /rebuild через comonitor bot или руками через скрипт?
```

## Why this matters

1. **Multi-agent coordination**: Алексей использует Z.ai CLI, Cursor, web chat, и subagents. Without identity, he doesn't know who answered.
2. **Audit trail**: when something breaks, worklog + identity intro shows which agent made which change.
3. **Git safety**: silent push can override parallel work. Confirmation prevents lost commits.
4. **Project context visibility**: switching project should be explicit — otherwise agent might mix up rules from tg-monitor and council-bot.

## Implementation

This skill is loaded by `agent-bootstrap` at session start. It runs PROACTIVELY:
- First message of session → agent introduces themselves
- Before any git operation → agent shows what's about to happen
- After context switch → agent confirms new context loaded

If agent forgets to introduce themselves — user can prompt: "представься" → triggers this skill.

## Subagent delegation (for parent agents)

When delegating to a subagent via Task tool, parent agent MUST inject
agent-identity-protocol rules into subagent prompt. Use the template at
[`subagent-prompt-template.md`](./subagent-prompt-template.md) (sibling file).

Key rules to inject:
1. Subagent introduces itself at start: `[Agent Identity] 🤖 Agent: <role>`
2. Subagent **NEVER silent push/pull** — returns commit info to parent
3. Parent shows user `[Git Operation Confirmation]` → user confirms → parent pushes
4. Subagent appends to `/home/z/my-project/worklog.md` after subtask
5. Subagent returns final report to parent (what done, files, commits, blockers)

⚠️ **Subagent visibility**: Subagent gets ONLY what parent puts in prompt.
Subagent does NOT see:
- /home/z/my-project/ filesystem (unless paths given)
- /home/z/my-project/skills/ (can't use Skill tool directly)
- worklog.md (can't read, but CAN append via Write tool)
- AGENT_BOOTSTRAP.md (parent must paste relevant rules)

## Cross-refs

- `agent-bootstrap` — proactive session start (reads AGENT_BOOTSTRAP.md)
- `git-after-each-step` — when to auto-commit (3+ modifications)
- `no-force-push` — never use `git push --force`
- `git-credentials-guard` — protect PAT
- `worklog-digest` — append to worklog at session end
- `subagent-prompt-template.md` — copy-paste template for Task prompts
- All `project-<name>` skills — context-specific rules
- AGENT_BOOTSTRAP.md Section 5.8 — «Как песочницы взаимодействуют»
