---
name: session-summary-export
description: Generate context recovery file when chat breaks or session ends. TRIGGER proactive at session end (long pause >10 min OR explicit "bye"/"конец"/"спасибо"/"до завтра"). Also triggers on explicit request "сохрани контекст", "session summary", "сделай экспорт", "чат сломался", "восстанови в новом чате". Replaces the MHTML-save-and-upload workaround.
---

# session-summary-export

Executable skill для экспорта контекста текущей сессии в файл. Заменяет ручной mhtml-save + upload workaround.

## Когда активировать

**PROACTIVE** (сам агент в конце сессии):
- Длинная пауза >10 мин после последнего действия агента
- Юзер сказал "bye" / "конец" / "спасибо" / "до завтра" / "всё"
- Сессия близка к context limit
- Перед риском chat breakage (большой multi-tool-call)

**EXPLICIT** (юзер попросил):
- "сохрани контекст"
- "session summary"
- "сделай экспорт сессии"
- "чат сломался, сохрани наработки"
- "восстанови в новом чате"

## Что делать

1. Запустить CLI:
```bash
python /home/z/my-project/scripts/session-export.py
# Или с флагами:
python /home/z/my-project/scripts/session-export.py --task-id <id> --upload-comonitor
```

Если `session-export.py` не существует локально:
```bash
git clone https://github.com/brilenkov/brain-tools.git /tmp/bt-bootstrap
mkdir -p /home/z/my-project/scripts
cp /tmp/bt-bootstrap/scripts/session-export.py /home/z/my-project/scripts/
```

2. CLI сделает:
   - Прочитает `/home/z/my-project/worklog.md` — найдёт последний Task ID
   - Прочитает последние git log'и в brain-tools
   - Найдёт все unstaged changes
   - Проверит активные сервисы на Render через `tg-monitor-cli.py status`
   - Сформирует markdown summary в `/tmp/brain-vault/06_journal/context_recovery_<timestamp>.md`

3. Агент дополнит summary:
   - Текущий запрос юзера (последний)
   - Что сделано в этой сессии
   - Что pending (что ещё надо сделать)
   - Ключевые решения
   - Файлы/коммиты которые надо сохранить
   - Следующий шаг

4. Скажет юзеру:
```
✅ Context recovery сохранён:
/tmp/brain-vault/06_journal/context_recovery_2026-10-26_14-32.md

В новом чате напиши:
"Прочитай /tmp/brain-vault/06_journal/context_recovery_2026-10-26_14-32.md и продолжи"
```

## Format context_recovery файла

```markdown
# Context Recovery — <YYYY-MM-DD HH:MM MSK>

## Session meta
- Chat ID: <short>
- Started: <approximate time>
- Ended: <now>
- Worklog Task ID: <last>
- User request (last): "<exact text>"

## What was done this session

### Completed
- <action 1>
- <action 2>

### In progress (NOT finished)
- <action X> — stopped at step N of M

## Files modified (this session only)

| File | Repo | Commit | Status |
|------|------|--------|--------|
| /path/to/file | brain | abc1234 | committed + pushed |
| /path/to/another | brain-tools | (uncommitted) | staged, NOT pushed |

## Git state
- brain-tools: HEAD = <hash>, branch=main, dirty=<yes/no>
- Unpushed commits: <list>

## Render services state
- tg-monitor: <status> (URL: ...)
- alexenur-marathon-bot: <status>

## Next steps (PRIORITY ORDER)
1. <most important next action>
2. <second>

## How to continue in new chat
В новом чате пошли это:
"Прочитай /tmp/brain-vault/06_journal/context_recovery_2026-10-26_14-32.md и продолжи с шага: <specify>"
```

## Если CLI недоступен

Если `/home/z/my-project/scripts/session-export.py` не существует — агент должен:
1. Склонировать brain-tools: `git clone https://github.com/brilenkov/brain-tools.git /tmp/bt`
2. Скопировать: `cp /tmp/bt/scripts/session-export.py /home/z/my-project/scripts/`
3. Запустить CLI

ИЛИ написать summary вручную через Write tool в `/tmp/brain-vault/06_journal/context_recovery_<timestamp>.md`.

## Связанные скилы

- `agent-bootstrap` — обратный процесс (чтение context_recovery в новом чате)
- `chat-stability-guard` — правило 7 (Context Recovery Protocol)
- `worklog-digest` — append в worklog.md
- `git-after-each-step` — чтобы незакоммиченных наработок не было

## Ссылка

- Этот скил: https://github.com/brilenkov/brain-tools/blob/main/agent-skills/session-summary-export/SKILL.md
- CLI скрипт: https://github.com/brilenkov/brain-tools/blob/main/scripts/session-export.py
