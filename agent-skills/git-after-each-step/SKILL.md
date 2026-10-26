---
name: git-after-each-step
description: CRITICAL rule — commit + push to GitHub after every subtask (3+ file modifications). Triggers proactive when agent has done 3+ Write/Edit operations OR after completing a subtask. Solves problem of session breakage causing loss of unfinished work. Trigger phrases: "закоммить", "push в гит", "после шага", "git commit", "сохрани наработки", "session может упасть".
---

# git-after-each-step

КРИТИЧНОЕ правило — после каждой подзадачи (>=3 file modifications) немедленно git commit + push.

## Проблема

AI сессия может упасть в любой момент:
- HTTP 400 (tool_call corruption)
- Content moderation block
- Context limit reached
- Network timeout
- User accidentally closes tab

Если за сессию сделано 10+ правок и они НЕ закоммичены — ВСЯ работа теряется.
Юзер сохраняет mhtml страницы чтобы восстановить — это плохо.

## Решение

После КАЖДОЙ подзадачи которая включает >=3 file modifications:

1. `git add <modified files>`
2. `git commit -m "<subtask description> — chat <short_id>"`
3. `git push origin <branch>`

## Критерии "подзадача завершена"

Подзадача завершена если выполнено ЛЮБОЕ из:
- 3+ файлов отредактированы через Write/Edit
- Создан новый файл (Write new file)
- Удалены файлы (через Bash rm)
- Запущен long-running script (Bash long output)
- Изменён env var на Render
- Создан новый сервис
- Создан новый skill

## Workflow

```bash
# После 3+ правок:

cd /home/z/my-project/brain-tools

# 1. Проверить что изменилось
git status
# staged + unstaged changes должны быть видны

# 2. Добавить конкретные файлы (НЕ git add -A — может попасть мусор)
git add bots/tg-monitor/monitor.py
git add agent-skills/tg-bot-access-control/SKILL.md

# 3. Commit с описательным сообщением
git commit -m "feat(tg-monitor): access control + role classifier — chat abc123"

# 4. Push
git push origin main

# 5. Если rejected (parallel push):
git fetch origin
git pull --rebase origin main  # НЕ git pull (merge commit!)
# Resolve conflicts:
# git checkout --theirs <file>  # мои изменения (rebase context)
# git checkout --ours <file>    # origin/main (rebase context)
git rebase --continue
git push origin main
```

## Что НЕ делать

### НЕ копить 20 правок в один коммит

Плохо:
```
(Writes 20 files)
git add -A
git commit -m "many changes"
git push
```

Если что-то упало в середине — теряешь всё.

Хорошо:
```
(Writes 3 files)
git add file1 file2 file3
git commit -m "feat(bot): access control middleware"
git push

(Writes 3 more files)
git add file4 file5 file6
git commit -m "feat(bot): role classifier"
git push

...
```

### НЕ откладывать push "потом"

Если коммит сделан но не запушен — он на локальной машине. Если среда упадёт (env reset, container restart) — коммит потерян.

ВСЕГДА push сразу после commit.

### НЕ force push

`git push --force` FORBIDDEN. Только `--force-with-lease` если РЕАЛЬНО необходимо (см. no-force-push skill).

## Исключения (когда НЕ коммитить)

- Тестовый запуск (ad-hoc experiments, потом удалишь)
- Temporary files в `/tmp/` — эти и так исчезнут
- Files в `.gitignore` — session strings, .env, credentials
- Work-in-progress который компилируется но ломает тесты

В этих случаях — stash:
```bash
git stash push -m "WIP access control middleware"
# Продолжить позже
git stash pop
```

## Commit message format

```
<type>(<scope>): <subject> — chat <short_chat_id>

<body>

<footer>
```

Types:
- `feat` — новая фича
- `fix` — баг фикс
- `refactor` — рефакторинг без изменения поведения
- `docs` — документация
- `chore` — рутина (зависимости, конфиг)
- `test` — тесты
- `skill` — создание/обновление skill

Scopes (примеры):
- `tg-monitor`
- `tg-monitor-cli`
- `marathon-bot`
- `fns-bot`
- `agent-bootstrap`

Examples:
```
feat(tg-monitor): access control via ALLOWED_TG_USER_IDS — chat cead99bf

- Added AccessControlMiddleware in app/middleware/access.py
- Registered in Dispatcher (message + callback_query)
- Fails-safe: bot crashes if env var not set (no public bot)

Ref: agent-skills/tg-bot-access-control/SKILL.md
```

```
skill(role-classifier): auto-classify contact roles with user audit

- 6 roles: dating/family/colleagues/business/friends/other
- Heuristic markers in config.py ROLE_MARKERS
- LLM fallback if confidence < 50%
- Inline keyboard audit via comonitor bot

Closes #N
```

## Связанные скилы

- `no-force-push` — запрет `--force`
- `git-credentials-guard` — проверка PAT перед git ops
- `chat-stability-guard` — правило 5 (incremental commits)
- `worklog-digest` — append в worklog.md после сессии
- `session-summary-export` — экспорт если сессия всё-таки упала
- `agent-bootstrap` — чтение контекста в начале сессии

## Ссылка

- Этот скил: https://github.com/brilenkov/brain-tools/blob/main/agent-skills/git-after-each-step/SKILL.md
