---
name: agent-bootstrap
description: PROACTIVE session start skill. Reads AGENT_BOOTSTRAP.md + worklog.md + latest context_recovery file. Trigger at FIRST user message of every new session/chat. Also triggers when user says "продолжай", "восстанови контекст", "давай дальше", "что уже сделано", "статус". Solves the problem of every new chat starting from zero context.
---

# agent-bootstrap

Proactive skill — должен активироваться в начале каждой новой сессии/чата с AI-ассистентом.

## Когда активировать

**PROACTIVE** — агент САМ активирует в начале сессии, без явного триггера:
- Первый user message в новом чате
- Длинная пауза (>30 мин после последнего ответа агента)
- Юзер сказал "продолжай" / "восстанови контекст" / "давай дальше"
- Юзер спросил "что уже сделано" / "статус" / "на чём мы"

## Что делать (workflow)

### Шаг 1. Прочитать AGENT_BOOTSTRAP.md

```bash
# Если AGENT_BOOTSTRAP.md не существует локально — склонировать brain-tools
if [ ! -f /home/z/my-project/AGENT_BOOTSTRAP.md ]; then
    git clone https://github.com/brilenkov/brain-tools.git /tmp/bt-bootstrap
    cp /tmp/bt-bootstrap/AGENT_BOOTSTRAP.md /home/z/my-project/
    cp -r /tmp/bt-bootstrap/agent-skills/* /home/z/my-project/skills/
fi
cat /home/z/my-project/AGENT_BOOTSTRAP.md
```

В файле: список репо, путей, токенов, текущие активные сервисы на Render, 10 критичных правил, текущие активные проекты.

### Шаг 2. Прочитать worklog.md

```bash
tail -200 /home/z/my-project/worklog.md
```

Worklog — единый multi-agent лог. Последние 200 строк покажут что сделали в этой и параллельных сессиях.

### Шаг 3. Найти последний context_recovery

```bash
ls /tmp/brain-vault/06_journal/context_recovery_*.md 2>/dev/null | tail -3
# Если есть — прочитать последний
latest=$(ls /tmp/brain-vault/06_journal/context_recovery_*.md 2>/dev/null | tail -1)
[ -n "$latest" ] && cat "$latest"
```

Context recovery — для переноса контекста между чатами. Если юзер сказал "продолжай" — там последняя задача.

### Шаг 4. Проверить git состояние

```bash
cd /home/z/my-project/brain-tools && git log --oneline -10
git status
# Если есть unstaged changes от прошлой сессии — спасти через stash или commit
```

### Шаг 5. Сформировать ответ юзеру

После чтения контекста — КРАТКО (≤5 строк) резюмируй что уже сделано + что сейчас в работе + какой следующий шаг. Затем — переходи к запросу юзера.

Пример:
```
✅ Прочитал AGENT_BOOTSTRAP + worklog + context_recovery_2026-10-26.md.

Сделано:
- tg-monitor bot задеплоен на Render (live) ✅
- Access control + role classifier реализованы

В работе:
- Patch существующих ботов с ALLOWED_TG_USER_IDS

Что дальше:
- marathon-bot middleware
- fns-receipt-bot middleware

Твой запрос: <echo>
```

## КРИТИЧНО

### Никогда не пропускай шаги 1-3

Даже если юзер дал конкретную задачу ("создай X") — сначала прочитай контекст. Иначе:
- Будешь дублировать чужую работу
- Используешь устаревший токен/путь
- Нарушишь критичное правило (например no-force-push)

### Если контекста нет — создай минимальный

Если worklog.md пуст и AGENT_BOOTSTRAP.md не существует:
```
"Не нашёл AGENT_BOOTSTRAP/worklog. Создаю сейчас. Опиши задачу — продолжу."
```
Затем:
1. Склонируй brain-tools репо
2. Скопируй AGENT_BOOTSTRAP.md в /home/z/my-project/
3. Скопируй agent-skills/* в /home/z/my-project/skills/
4. Создай пустой worklog.md
5. Продолжай с задачей юзера

### Не загружай ВСЕ скилы сразу

В brain-tools/agent-skills/ ~15 скилов. Загружай только те что РЕЛЕВАНТНЫ текущему запросу юзера. Для общего контекста достаточно AGENT_BOOTSTRAP + worklog + context_recovery.

## Связанные скилы

- `chat-stability-guard` — правила декомпозиции + incremental commits
- `session-summary-export` — генерация context_recovery файла
- `worklog-digest` — append в worklog.md
- `git-after-each-step` — коммитить после каждой подзадачи
- `git-credentials-guard` — проверить PAT перед git ops

## Ссылки

- AGENT_BOOTSTRAP.md: https://github.com/brilenkov/brain-tools/blob/main/AGENT_BOOTSTRAP.md
- Этот скил: https://github.com/brilenkov/brain-tools/blob/main/agent-skills/agent-bootstrap/SKILL.md
