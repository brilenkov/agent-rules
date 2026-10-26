---
name: do-it-now
description: >
  Two-minute rule from David Allen GTD: if task takes <2 min, do it NOW, don't defer.
  TRIGGER PROACTIVELY when user mentions a small/quick task — remind "do it now"
  instead of adding to task list. Also triggers on phrases: "потом сделаю",
  "напомни позже", "добавь в задачи", "запиши на потом" — assess if task takes
  <2 min → if yes, suggest doing now. Goal: prevent task list from filling with
  2-min tasks that take longer to schedule than to execute.
---

# Do It Now — 2-minute rule (David Allen GTD)

> "If an action will take less than two minutes, it should be done at the moment
> it's defined." — David Allen, *Getting Things Done*

## Decision matrix

| Task duration | Action |
|---|---|
| < 2 min | ✅ **DO IT NOW** — don't schedule |
| 2-15 min | ⚠️ Schedule for today, do at earliest free slot |
| 15-60 min | 📅 Schedule with `when:: today` + `slot::` |
| > 60 min | 📅 Break into smaller subtasks, schedule each |

## Duration estimates (for common tasks)

- Phone call → 1-2 min
- Reply to message (TГ, WhatsApp) → 1-2 min
- Read short note → 1-2 min
- Fill small form → 1-2 min
- Quick search/lookup → 1-2 min
- Small purchase online → 1-2 min
- Make tea/coffee → 2-3 min
- Tidy desk surface → 2-3 min
- Reply to email → 2-5 min
- Anything involving going somewhere → 15+ min
- Anything requiring preparation → 15+ min
- Anything >1 hour → break down

## When to trigger

1. **User mentions a small task** — assess duration
2. **Phrases indicating defer**:
   - "потом сделаю", "напомни позже", "добавь в задачи", "запиши на потом"
   - "когда-нибудь", "не сейчас", "завтра этим займусь"
3. **Tasks being added to TODO list** — if <2 min, prompt to do now

## Examples

### E1: User says "позвонить в стоматологию"
- Phone call → 1-2 min → AI: "Это займёт 1-2 минуты. Сделай сейчас? Я подожду."
- User: "позже" → AI: "Ок, добавлю в задачи с `when:: сегодня`. Но лучше позвони сейчас."

### E2: User says "разобрать комнату"
- Это много часов → AI: добавлю в 02_areas/money.md как задачу с `when:: 2026-10-25`

### E3: User says "ответить на сообщение Марии"
- Это <2 min → AI: "Это займёт 1 мин. Открой ТГ, напиши, закрой. Не добавляй в TODO."

### E4: User says "купить продукты"
- Это 30-60 мин → AI: добавлю в задачи с `when:: tomorrow` + `slot:: после работы`

### E5: User says "отправить черновик Насте"
- Это 2-3 мин → AI: "Это 2-3 минуты. Сделай сейчас — открой manson_experiment_log.md, скопируй, вставь в WhatsApp."

## Why this matters

- **Task list pollution**: 2-min tasks in TODO = visual noise, decision fatigue
- **Productivity loss**: scheduling 2-min task takes ~30 sec = 25% of task duration
- **Procrastination pattern**: small tasks deferred = guilt pile = paralysis
- **GTD principle**: takes less time to do than to track

## When NOT to apply

- ❌ User explicitly wants to defer ("не сейчас, потом"): respect their choice
- ❌ Task requires specific time/context (e.g., "позвонить в рабочее время")
- ❌ Task requires preparation (e.g., "send email" needs context)
- ❌ User is in a flow state — don't interrupt

## How to remind in chat

When triggered, prepend short message:
```
⏱️ Это займёт ~X мин. Сделай сейчас — не откладывай в TODO.
[task description]
```

If user insists on deferring:
```
Окей, добавлю в задачи: - [ ] (when:: today) (priority:: high) [task]
Но помни — простая задача 1-2 мин, планирование занимает дольше.
```

## Edge cases

| Scenario | Rule |
|---|---|
| "потом" + <2 min | "это займёт 1 мин — точно потом? Можно сделать сейчас." |
| User asks to "напомни" | If <2 min, suggest doing now. Else set reminder. |
| Many 2-min tasks in TODO | "У тебя 5 задач по 1-2 мин. Сделай сейчас за 10 мин." |
| Task 2-3 min (borderline) | Lean toward "do now" — borderline usually quick |

## Related skills

- [[../time-guard/SKILL]] — slot-aware reminders
- [[../daily-note-scaffolder/SKILL]] — daily task list
- [[../worklog-digest/SKILL]] — session summary

## Related files

- `/home/z/my-project/brain/09_meta/Tasks_format.md` — task format
- `/home/z/my-project/brain/06_journal/balance_recovery_plan_Q4.md` — Q4 plan
