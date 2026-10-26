---
name: time-guard
description: >
  Time-slot guard for the user's daily schedule. TRIGGER PROACTIVELY at the START
  of EVERY response to a user message. Checks the current time against the user's
  schedule (SCHEDULE_2026-10-16_to_30_v4) and the topic of the user's message.
  If the current slot is a "physical-action" slot (walk, exercise, Maxim time,
  meal, liturgy, rehearsal, banya, sleep, Аня) AND the user's message topic is
  NOT schedule/menu/work — prepend a short reminder before answering.
  Example: at 16:10 user asks "что нового у Яны?" → prepend "Сейчас 16:10, слот
  прогулки (16:05-16:30). Это время для прогулки. Отвечу, но потом выходи."
  Exception: if user asks about schedule, menu, or work — respond normally
  without reminder (this is explicitly scheduled planning time).
---

# Time Guard — slot-aware response protocol

> This skill defines when and how to remind the user about schedule transitions
> during AI dialogue. The user's pain: gets "stuck" in chat when the schedule
> says it's time for a walk, training, Maxim, sleep, etc.

## When to trigger

**At the START of EVERY response** to a user message, do this check:

1. Get current time (from chat context or `date` shell command)
2. Look up the current slot in [[../../brain/01_daily/SCHEDULE_2026-10-16_to_30_v4|SCHEDULE v4]]
3. Classify the slot:
   - **OK for AI dialogue** → respond normally, no reminder
   - **Limited dialogue** → brief reminder, then answer
   - **Forbidden dialogue** → strong reminder, brief answer only

## Slot classification (SCHEDULE v4 — 16-30.10.2026)

### ✅ OK for AI dialogue — no reminder

These are slots where AI dialogue is explicitly part of the activity:

| Slot | Time | Activity |
|---|---|---|
| Work morning | 08:30-12:30 (Пн-Пт) | Redmine, tests, doc — AI help OK |
| Work afternoon | 13:15-16:05 (Пн-Пт) | Redmine, support — AI help OK |
| Photo hobby | 16:30-17:30 (Пн-Пт) | Photo processing — AI help OK |
| Photo / free | 12:30-14:30 (Ср) | Photo — AI help OK |
| Planning | 15:30-17:30 (Вс) | Weekly planning — AI help OK |
| Reading + diary | 21:30-22:30 (Пн-Пт) | Brief AI ok (notes) |

### 🟡 Limited dialogue — brief reminder, then answer

These are slots where brief AI dialogue is OK but should not exceed 5-10 min:

| Slot | Time | Activity |
|---|---|---|
| Утр. магия | 07:30-08:00 | Morning routine — brief ok |
| Завтрак | 08:00-08:30 | Eating — brief ok |
| Большой перерыв | 10:05-10:25, 14:05-14:30 | Coffee break — brief ok |
| Ужин лёгкий | 18:30-19:00 | Eating — brief ok |
| Зикр утренний | 07:30-07:45 | 🕉️ — better no phone |
| Зикр вечерний | 21:00-21:10 | 🕉️ — better no phone |
| Финтрек | 21:30-21:40 | Quick log |
| Благодарности | 21:40-21:50 | Quick log |
| Дневник дух | 21:50-22:00 | Quick log |

### 🔴 Forbidden dialogue — strong reminder + brief answer only

These slots require **physical presence** or **non-AI activity**. AI dialogue breaks them:

| Slot | Time | Activity |
|---|---|---|
| Прогулка 30 мин | 16:05-16:30 (Пн-Пт) | **Walk outside**, no phone |
| Отжимания/пресс | 17:30-18:30 (Пн, Ср, Пт, Вс) / 17:30-17:45 (Вт, Чт — ноги) | **Exercise**, no phone |
| Обед с Максимом | 12:05-12:30 (Пн-Пт) | **Be present**, no phone |
| Математика с Макс | 12:30-13:10 (Пн-Пт) | **Be present**, no phone |
| Ужин с Максимом | 19:40-20:30 (Чт) | **Be present** |
| Пятничный ритуал | 18:30-22:30 (Пт) | With Maria — **no phone** |
| «Чашка чая» Марии | 19:30-19:40 (Вт, Чт) | **Be present** with Maria |
| Тренировка Максима | 18:00-19:30 (Вт, Чт, Сб) | Подвезти/забрать — driving |
| Репетиция | 18:30-20:30 (Пн Благовест, Вт Отрада) | **Singing** |
| Золотые голоса | 14:30-16:30 (Сб) / 15:00-17:00 | **Singing** |
| Литургия | 09:00-10:30 (Сб Дарагановка, Вс храм) | **Service** |
| Всенощная | 17:30 (Сб) | **Service** |
| Баня | 19:00-22:00 (Сб) / 19:30-22:30 (Вс) | **Banya**, no phone |
| Аня | 17:30-23:30 (Ср) | **Intimacy**, no phone |
| Honda звонки | 17:00-17:30 (Вт) | Phone calls to dealers |
| Honda визит | 10:00-13:00 (Сб) | Driving to dealers |
| Разбир комнат | 11:00-13:00 (Сб) или 17:30-19:00 (Вс) | **Physical work** |
| Стратегия увольнения | 16:00-16:30 (Чт) | Writing — brief AI ok |
| Рейки | 14:30-15:30 (Ср) / 17:30-18:30 (Вс) | **Practice**, no phone |
| Бесполезная радость | 13:00-14:00 (Сб) | **Joy**, no phone — usually outdoors |
| Финансовый аудит | 15:30-17:00 (Вс) | Review — AI help OK for finance |
| Сон | 22:15-07:30 (Пн-Пт) / 23:00-08:00 (Сб-Вс) | **Sleep**, no phone |

## Reminder protocol

### Format

```
⏰ Сейчас HH:MM — слот «<activity>» (HH:MM-HH:MM).
<one-line advice: что нужно делать физически>.
Отвечу кратко по сути, потом — выходи.
```

### Examples

**Example 1**: at 16:15 user asks "что нового у Яны?" (topic = relationships, not schedule/menu/work)
- Slot: Прогулка 30 мин (16:05-16:30) — 🔴 Forbidden
- Reminder: `⏰ Сейчас 16:15 — слот «Прогулка 30 мин» (16:05-16:30). Нужно выйти из дома, без телефона. Отвечу кратко: <answer>. Потом — выходи на 15 мин.`

**Example 2**: at 16:15 user asks "обнови SCHEDULE v4" (topic = schedule planning)
- Slot: Прогулка 30 мин — 🔴 Forbidden, BUT topic is schedule
- NO reminder (explicit exception: schedule/menu/work topics are OK anytime)

**Example 3**: at 12:15 user asks "что у нас в расписание на завтра?" (topic = schedule)
- Slot: Обед с Максимом (12:05-12:30) — 🔴 Forbidden, BUT topic is schedule
- NO reminder (exception)

**Example 4**: at 09:30 user asks philosophical question
- Slot: Литургия (09:00-10:30) — 🔴 Forbidden
- Reminder: `⏰ Сейчас 09:30 — слот «Литургия» (09:00-10:30). Ты в храме. Коротко: <answer>. Возвращайся к службе.`

**Example 5**: at 14:00 user asks about Manson experiment
- Slot: Work afternoon (13:15-16:05) — ✅ OK
- NO reminder, respond normally

## Exception list (topics that are ALWAYS OK to discuss)

These topics are exempt from reminders regardless of slot:

1. **Schedule** — anything about SCHEDULE, planning, time slots
2. **Menu** — anything about MENU, food, nutrition
3. **Work** — anything about Redmine, tests, code, integration, documentation
4. **Emergency** — anything marked urgent by user ("срочно", "помоги быстро")
5. **Quick confirmations** — user asks a yes/no question, just answer

If user explicitly says "потом" or "после слота" — defer the answer.

## How to actually trigger this skill

This skill is loaded by the assistant at the START of every response. The assistant should:

1. Check `date` to get current time (UTC) and convert to Europe/Moscow (UTC+3)
2. Look up the current slot in SCHEDULE v4 (or daily note if v4 not loaded)
3. Classify slot (OK / Limited / Forbidden)
4. Check user message topic against exception list
5. If slot is Limited or Forbidden AND topic is not in exception list:
   - Prepend the reminder (one-liner format above)
   - Answer briefly (don't dive into deep work)
6. If slot is OK OR topic is in exception list:
   - Respond normally, no reminder

## What if time is between slots?

If the current time doesn't fit any scheduled slot (e.g., 11:00 between work and lunch):
- Default to OK for dialogue (treat as "transition time")
- No reminder

## What if schedule is different from v4?

Always check the **daily note** for today (e.g., `brain/01_daily/2026-10-18.md`)
if it has a ⏰ schedule table — that's the source of truth for today. The SCHEDULE v4
file is the template; daily notes are the actual.

## Reminder intensity

- First reminder: gentle, with one-line answer
- If user continues: stronger reminder ("⚠️ Слот ещё идёт. Сейчас 16:25, осталось 5 мин прогулки.")
- After 3 reminders in same slot: just answer, user clearly chose dialogue over slot
- Never block — always answer, just prepend reminder

## Logging

After a session where reminders were issued, the assistant may add to worklog:
```
- Time-guard reminders issued: N times during slots X, Y, Z
```

This helps the user see how often they're crossing slots.

## Related files

- [[../../brain/01_daily/SCHEDULE_2026-10-16_to_30_v4|📅 SCHEDULE v4]] — current schedule with all slots
- [[../../brain/01_daily/2026-10-17|📅 Today's daily note]] — overrides for today
- [[../../brain/06_journal/balance_recovery_plan_Q4|⚖️ Balance plan]] — source of new slots
- [[../user-environment/SKILL|User environment]] — basic context
