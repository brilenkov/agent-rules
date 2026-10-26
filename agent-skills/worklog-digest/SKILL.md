---
name: worklog-digest
description: >
  Summarize what was done in the current session by reading worklog.md tail.
  TRIGGER PROACTIVELY at session end (heuristic: long pause >10 min after last
  assistant action OR explicit "bye" / "конец" / "спасибо" / "до завтра").
  Also triggers on explicit: "сводка", "summary", "что сделали", "итог сессии",
  "digest", "что было сделано".
  Output: brief 3-7 bullet summary in chat + optional append to worklog.md as final entry.
---

# Worklog Digest — session summary

> At session end, reads worklog.md tail and produces a brief summary of what
> was accomplished in this session. Helps user see session value + start
> next session with context.

## When to trigger

1. **Explicit request**: "сводка", "summary", "что сделали за сессию", "итог", "digest"
2. **Session end heuristic**:
   - User says "bye" / "конец" / "спасибо" / "до завтра" / "всё"
   - Long pause (>10 min) after last assistant message
   - User starts new unrelated topic (suggests previous work is done)
3. **Pre-shutdown**: if user mentions restarting/closing session

## Workflow

### Step 1: Read worklog.md

```python
worklog_path = "/home/z/my-project/worklog.md"
content = Path(worklog_path).read_text(encoding="utf-8")
```

### Step 2: Identify this session's entries

Session = all entries added since the start of the current conversation.

Heuristics:
- Look for `Task ID:` lines after the last `---` separator before this session
- Or use timestamps if available
- Or use chat context: identify entries that match topics discussed in this session

### Step 3: Group by Task ID prefix

Each worklog entry has `Task ID: <id>`. Group entries by prefix:
- `banya-17.10` → relations work (Yana)
- `cold-outreach-*` → photography outreach
- `vk-scout-*` → VK scout tool
- `brain-tools-*` → repo management
- `balance-plan-*` → life wheel
- `schedule-v4-*` → schedule updates
- `daily-note-scaffolder-*` → this skill
- etc.

### Step 4: Count artifacts produced

For each group, count:
- Files created
- Files updated
- Commits to brain repo
- Commits to brain-tools repo
- Skills invoked/created

### Step 5: Build summary

Format (3-7 bullets):

```
📋 **Сессия сводка** ({date}, {duration_estimate}min)

**Создано файлов**: N
- `path/to/file1.md` — purpose
- `path/to/file2.md` — purpose

**Обновлено**: M файлов в brain/, K файлов в brain-tools/

**Skills созданы/использованы**:
- ✨ daily-note-scaffolder (new)
- ⏰ time-guard (used N times)
- ...

**Коммиты**:
- brain repo: X commits → {commit_hash}
- brain-tools repo: Y commits → {commit_hash}

**Главные темы сессии**:
1. {topic 1 — e.g., "Manson experiment с Яной 17.10"}
2. {topic 2 — e.g., "VK scout tool + cold outreach strategy"}
3. {topic 3 — e.g., "Расписание v4 + balance recovery plan"}

**Следующие шаги** (из worklog "Stage Summary"):
- {next step 1}
- {next step 2}
- {next step 3}

📊 **Time-guard reminders за сессию**: N (в слотах X, Y, Z)
```

### Step 6: Optional — append to worklog as final entry

If session was long (>30 min) and produced significant work:

```python
# Append digest as final entry
with open(worklog_path, "a", encoding="utf-8") as f:
    f.write("\n---\n")
    f.write(f"Task ID: digest-{date}\n")
    f.write(f"Agent: Z.ai (main)\n")
    f.write(f"Task: Session summary digest\n\n")
    f.write(f"Work Log:\n{bullets}\n\n")
    f.write(f"Stage Summary:\n{next_steps}\n")
```

### Step 7: Output to chat

Print the summary in chat. Keep it concise — 3-7 bullets max, ~200-400 words.

## What NOT to include

- ❌ Don't dump full file contents
- ❌ Don't repeat worklog verbatim — summarize
- ❌ Don't include Z.ai internal thoughts / reasoning
- ❌ Don't include PAT or any secrets

## What to include

- ✅ Concrete file paths (so user can find artifacts)
- ✅ Commit hashes (so user can find on GitHub)
- ✅ Quantitative counts (N files, M commits, K reminders)
- ✅ Next steps from worklog Stage Summary sections
- ✅ Topic-level overview (not full detail)

## Edge cases

- **First session ever**: no worklog.md → just say "Это первая сессия, worklog пустой. Все изменения в этой сессии — старт."
- **Very short session** (<5 min, 1-2 tool calls): just say "Короткая сессия, сделано: {1-2 вещи}."
- **Long session** (>2 hours): produce full digest + suggest splitting work into worklog entries

## Related skills

- [[../daily-note-scaffolder/SKILL]] — creates daily note, where session digest can be referenced
- [[../time-guard/SKILL]] — counts reminders issued during session

## Related files

- `/home/z/my-project/worklog.md` — source
- `/home/z/my-project/brain/01_daily/{today}.md` — may receive digest reference in "Работа с brain" section
