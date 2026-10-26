---
name: debug-status
description: >
  Debug mode — show what skills are available, which were used in the current
  session, current task context, and active RAG/KB pipelines.
  TRIGGER when user says: дебаг, debug, статус, status, какой скил, что запущено,
  активные скилы, чё запущено, контекст, что в работе, debug status, show skills.
  Toggle ON/OFF. When ON, agent prefixes every reply with a small "[debug]" block
  showing active skill, context source, and step.
---

# debug-status — show running skills, context, and session state

> Activated by keywords: "дебаг", "debug", "статус", "какой скил", "что запущено".
> Toggle mode: ON/OFF. When ON, prefix every reply with a compact debug block.

## When to trigger

- "дебаг" / "debug" / "debug status"
- "статус" / "status"
- "какой скил сейчас" / "что запущено"
- "активные скилы" / "какие скилы есть"
- "контекст" (when asking about active context)
- "что в работе" / "покажи скилы" / "чё запущено"

Turn OFF debug when user says:
- "дебаг выкл" / "debug off" / "без дебага" / "выключи дебаг"

## What it shows

### 1. Active skills in this session
Read `/home/z/my-project/worklog.md` — show tasks from current session.

### 2. All available skills
List from `/home/z/my-project/skills/*/SKILL.md` — grouped by category:
- BO / knowledge: bo-sohbet-kb, bo-rag-query
- Time / workflow: time-guard, daily-note-scaffolder, do-it-now, worklog-digest, skill-gap-analyzer, schedule-change-guard
- Dev / KB: telegram-kb, telegram-bot-development, fullstack-dev, render-deploy-watchdog
- Documents: docx, pdf, xlsx, pptx, charts
- AI / media: LLM, VLM, ASR, TTS, image-generation/edit/search, video-understand, agent-browser
- Meta: debug-status, skill-creator, skill-finder-cn, git-credentials-guard

### 3. Current context
- Last user message (truncated)
- Last task in worklog
- Active RAG pipeline (ChromaDB stats)
- TODO items

### 4. Pipeline / debug info
- ChromaDB path + count
- ONNX model path + dim
- KB files path
- z-ai CLI path
- Git status (brain + brain-tools)

## Output format

When debug ON, every reply starts with:
```
[debug] skills: <active> | ctx: <brief> | step: <todo>
---
```

When user triggers debug, show full report.

## How to read state

### Active skills in session
```bash
tail -50 /home/z/my-project/worklog.md 2>/dev/null | grep -E "^Task ID:|Agent:|Task:" | tail -20
```

### Available skills
```bash
ls /home/z/my-project/skills/
```

### ChromaDB stats
```bash
cd /home/z/my-project/brain-tools/bo-rag && python3 load_rag.py --stats 2>&1 | tail -10
```

### Git credentials status
```bash
ls -la /home/z/my-project/.git-credentials /home/z/my-project/.git-credentials.backup 2>&1
```

### Git status
```bash
cd /home/z/my-project/brain && git status --short | head -10
cd /home/z/my-project/brain-tools && git status --short | head -10
```

## Related skills

- `git-credentials-guard` — PAT verification
- `schedule-change-guard` — schedule audit log
- `skill-gap-analyzer` — quarterly skills audit
