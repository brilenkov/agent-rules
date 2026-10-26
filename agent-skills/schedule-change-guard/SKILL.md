---
name: schedule-change-guard
description: >
  GUARD for the user's daily schedule (SCHEDULE_*.md in brain/01_daily/).
  Prevents accidental modifications — schedule is updated ONLY when user
  explicitly requests it with a confirmation pattern.
  TRIGGER when user says: "измени расписание", "поменяй расписание",
  "перенеси слот", "поставь X на Y время", "удали слот", "добавь слот",
  "обнови SCHEDULE", "move training to", "schedule change", "edit schedule".
  ALWAYS: (1) read current SCHEDULE file, (2) show diff before applying,
  (3) ask "Подтверждаешь? (да/нет)", (4) only on "да" — write + backup old +
  log to brain/09_meta/schedule_changes.log + commit to git.
  NEVER change schedule silently. NEVER change as side-effect of another task.
---

# schedule-change-guard — protects user's daily schedule from accidental edits

> Schedule is the most sensitive file in the vault — wrong slot = missed
> rehearsal / missed Maxim / lost workout. All changes go through this skill.

## When to trigger

EXPLICIT triggers:
- "измени расписание" / "поменяй расписание" / "обнови SCHEDULE"
- "перенеси слот" / "перемести X на Y"
- "поставь репетицию на 18:00"
- "удали слот <name>" / "добавь слот <name> <time>"
- "schedule change" / "edit schedule" / "update schedule"
- "время поменялось" / "репетиция теперь в 18"

DO NOT trigger for:
- Casual mentions ("у меня в 18 репетиция")
- Questions ("когда репетиция?")
- Asking for the schedule (just show, no edit)

## Hard rules (NEVER violate)

1. NO SILENT EDITS
2. NO SIDE-EFFECT EDITS — even if I see "this slot looks wrong" — DO NOT fix without asking
3. ALWAYS BACKUP → `brain/01_daily/.archive/SCHEDULE_YYYY-MM-DD_v_OLD.md`
4. ALWAYS DIFF — show what changes BEFORE applying
5. ALWAYS ASK CONFIRMATION — "Подтверждаешь? (да/нет)". Only on "да" → apply.
6. ALWAYS LOG → `brain/09_meta/schedule_changes.log`
7. ALWAYS COMMIT → git with descriptive message

## Procedure

### Step 1: Locate current schedule
```bash
ls /home/z/my-project/brain/01_daily/SCHEDULE_*.md
```

### Step 2: Show diff
```
== ПРОЕКТ ИЗМЕНЕНИЯ ==
Файл: SCHEDULE_2026-10-16_to_30_v4.md

БЫЛО:
  18:30-20:30 | Репетиция (Пн Благовест, Вт Отрада)

СТАНЕТ:
  18:00-20:30 | Репетиция (Пн Благовест, Вт Отрада)

Подтверждаешь? (да/нет)
```

### Step 3: Backup
```bash
mkdir -p /home/z/my-project/brain/01_daily/.archive
cp SCHEDULE_*.md .archive/SCHEDULE_$(date +%Y%m%d_%H%M%S)_OLD.md
```

### Step 4: Apply edit (only on "да")
Use `Edit` tool with exact text replacement.

### Step 5: Log
Append to `/home/z/my-project/brain/09_meta/schedule_changes.log`:
```
2026-10-19T17:00:00 | user=Алексей | file=SCHEDULE_v4.md | change="Репетиция 18:30→18:00" | confirmed=yes | backup=.archive/..._OLD.md
```

### Step 6: Update dependent files (ASK FIRST)
- `skills/time-guard/SKILL.md`
- `brain/04_references/skills_cheatsheet.md`

### Step 7: Git commit + push
```bash
cd /home/z/my-project/brain && git add -A && git commit -m "chore(schedule): <change>"
git push origin main
```

### Step 8: Confirm to user
Show file, change, backup path, log entry, commit hash.

## Forbidden patterns

❌ Reading SCHEDULE, noticing "ошибка", fixing without asking
❌ Adding a new slot "because it makes sense"
❌ Reordering slots "for clarity"
❌ Changing filename v4→v5 without asking
❌ Bulk-replacing time strings without context

## Audit log

`brain/09_meta/schedule_changes.log` accumulates all changes. Read to answer "when did X change?":
```bash
grep "Репетиция" /home/z/my-project/brain/09_meta/schedule_changes.log
```

## Example user requests

✅ "измени расписание: репетиция в 18:00, а не 18:30"
✅ "перенеси тренировку на 17:00"
✅ "удали слот Хонда звонки — не актуально"
✅ "добавь слот: чтение 21:00-21:30 Пн-Пт"

❌ "у меня в 18 репетиция" — no trigger
❌ "когда репетиция?" — no trigger
❌ "покажи расписание" — no trigger (read-only)

## Files referenced

- `/home/z/my-project/brain/01_daily/SCHEDULE_*.md` — current schedule
- `/home/z/my-project/brain/01_daily/.archive/` — backups
- `/home/z/my-project/brain/09_meta/schedule_changes.log` — audit log
- `/home/z/my-project/skills/time-guard/SKILL.md` — slot table for reminders
- `/home/z/my-project/brain/04_references/skills_cheatsheet.md` — cheatsheet
