---
name: tg-bot-access-control
description: SECURITY rule — all Telegram bots MUST enforce ALLOWED_TG_USER_IDS env var. Every bot handler checks user_id against allowlist BEFORE responding. Triggers when developing/modifying any Telegram bot (aiogram, telethon, pyTelegramBotAPI, node-telegram-bot-api). Also triggers on questions like "как ограничить бота", "публичный бот", "кто может писать боту", "ALLOWED_TG_USER_IDS", "bot access control", "whitelist".
---

# tg-bot-access-control

КРИТИЧНОЕ правило — каждый TG бот должен проверять user_id перед ответом.

## Проблема

По умолчанию Telegram Bot API — публичный. Любой человек в мире может:
- Найти бота через поиск по username
- Написать `/start` → бот ответит
- Использовать команды бота (читать данные, триггерить действия)
- Если бот связан с БД — читать чужие данные
- Если бот может git push — пушить от имени юзера
- Если бот имеет PAT / tokens в env — злоумышленник может их украсть

## Решение

Каждый TG бот ДОЛЖЕН иметь:

1. **`ALLOWED_TG_USER_IDS` env var** — список user_id через запятую
2. **Middleware / handler** который проверяет `user_id` BEFORE обработкой
3. **Default = пусто** → если env не задан, бот НЕ запускается (fail-safe)

## Допущенные user_id для юзера @alexenur

| Username | TG User ID | Назначение |
|----------|-------------|-----------|
| `@alexenur` | 791785023 | основной аккаунт Алексея |
| `@tgnamel` | 6035309393 | запасной аккаунт Алексея |

`ALLOWED_TG_USER_IDS=791785023,6035309393` — стандартный env var для всех ботов Алексея.

## Паттерн для aiogram 3.x (Python)

Создать `app/middleware/access.py`:

```python
"""Access control middleware — проверяет user_id перед обработкой."""
import os
import sys
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery


class AccessControlMiddleware(BaseMiddleware):
    """Проверяет user_id в ALLOWED_TG_USER_IDS BEFORE обработкой."""
    
    def __init__(self):
        allowed_str = os.environ.get("ALLOWED_TG_USER_IDS", "")
        self.allowed_ids = [
            int(uid.strip())
            for uid in allowed_str.split(",")
            if uid.strip()
        ]
        if not self.allowed_ids:
            raise RuntimeError(
                "ALLOWED_TG_USER_IDS env var не задан — бот НЕ может стартовать "
                "(security: без whitelist бот публичный)"
            )
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        # Получаем user_id из event
        user = None
        if isinstance(event, (Message, CallbackQuery)):
            user = event.from_user
        
        if not user:
            return  # нет user — не обрабатываем
        
        if user.id not in self.allowed_ids:
            # Логируем попытку — НЕ отвечаем (не раскрываем что бот существует)
            print(
                f"[ACCESS DENIED] user_id={user.id} username=@{user.username} "
                f"tried to use bot — not in allowlist {self.allowed_ids}",
                file=sys.stderr,
            )
            return
        
        return await handler(event, data)
```

Зарегистрировать в `app/__main__.py` или `app/bot.py`:

```python
from aiogram import Dispatcher
from app.middleware.access import AccessControlMiddleware

dp = Dispatcher()
dp.message.middleware(AccessControlMiddleware())
dp.callback_query.middleware(AccessControlMiddleware())
```

## Паттерн для pyTelegramBotAPI (telebot)

```python
import telebot
import os
import sys

bot = telebot.TeleBot(os.environ["BOT_TOKEN"])
ALLOWED_IDS = [
    int(uid.strip())
    for uid in os.environ.get("ALLOWED_TG_USER_IDS", "").split(",")
    if uid.strip()
]
if not ALLOWED_IDS:
    raise RuntimeError("ALLOWED_TG_USER_IDS not set — bot cannot start")

@bot.message_handler(func=lambda m: m.from_user.id not in ALLOWED_IDS)
def deny_unauthorized(message):
    """Логируем попытку — НЕ отвечаем."""
    print(
        f"[ACCESS DENIED] user_id={message.from_user.id} "
        f"username=@{message.from_user.username}",
        file=sys.stderr,
    )

@bot.message_handler(func=lambda m: m.from_user.id in ALLOWED_IDS)
def handle_authorized(message):
    # Реальная обработка
    pass
```

## Паттерн для node-telegram-bot-api (Node.js)

```javascript
const TelegramBot = require('node-telegram-bot-api');
const token = process.env.BOT_TOKEN;
const bot = new TelegramBot(token, { polling: true });

const allowedIds = (process.env.ALLOWED_TG_USER_IDS || '')
    .split(',')
    .map(id => parseInt(id.trim()))
    .filter(id => !isNaN(id));

if (allowedIds.length === 0) {
    console.error('FATAL: ALLOWED_TG_USER_IDS not set — bot cannot start');
    process.exit(1);
}

// Access control — первая проверка во всех handlers
bot.on('message', (msg) => {
    if (!allowedIds.includes(msg.from.id)) {
        console.error(`[ACCESS DENIED] user_id=${msg.from.id} username=@${msg.from.username}`);
        return;  // silently ignore
    }
    // Реальная обработка
});

bot.on('callback_query', (query) => {
    if (!allowedIds.includes(query.from.id)) {
        console.error(`[ACCESS DENIED callback] user_id=${query.from.id}`);
        return;
    }
    // Реальная обработка
});
```

## Паттерн для raw HTTP polling (Python)

```python
import os, json, urllib.request

ALLOWED_IDS = [
    int(uid.strip())
    for uid in os.environ.get("ALLOWED_TG_USER_IDS", "").split(",")
    if uid.strip()
]

def handle_update(update):
    msg = update.get("message") or update.get("callback_query", {}).get("message")
    if not msg:
        return
    user_id = msg["from"]["id"]
    if user_id not in ALLOWED_IDS:
        print(f"[ACCESS DENIED] user_id={user_id}", file=sys.stderr)
        return
    # Реальная обработка
```

## Render env vars (для всех ботов Алексея)

В `render.yaml` каждого бота ДОЛЖНО быть:

```yaml
envVars:
  - key: ALLOWED_TG_USER_IDS
    value: "791785023,6035309393"  # @alexenur + @tgnamel
```

НЕ `sync: false` — это не секрет (public ID). Бот без этого env var НЕ стартует (security fail-safe).

## Существующие боты — аудит (октябрь 2026)

| Бот | Стек | ALLOWED_TG_USER_IDS | Что починить |
|-----|------|---------------------|--------------|
| tg-monitor | Python (raw polling) | ✅ enforce | OK |
| alexenur-marathon-bot | Python + aiogram 3.x | TODO | добавить middleware |
| alexenur-marathon-test-bot (staging) | тот же код | тот же фикс | OK after marathon-bot patch |
| fns-receipt-bot | Python (raw) | TODO | добавить проверку |
| scheduler-bot | Node.js (node-telegram-bot-api) | TODO | добавить в handler |
| therapist-voice-bot | Node.js | TODO | добавить в handler |
| life_council_bot_v2 | Python | TODO | проверить стек |
| alexenur-github-bot | проверяет user_id в notify_user.py | OK | OK |
| marafon-bot (legacy) | Python | нет | удалить (legacy) |

## Что делать если env не задан

**FAIL-SAFE**: бот НЕ запускается. Ошибка в логи:
```
FATAL: ALLOWED_TG_USER_IDS env var не задан.
Бот не может стартовать — без whitelist он публичный (security risk).
Установи env var: ALLOWED_TG_USER_IDS=791785023,6035309393
```

Это лучше чем запустить публичный бот по ошибке.

## Связанные скилы

- `bot-access-info` — single source of truth для marathon_bot окружения
- `telegram-bot-development` — общие правила разработки TG ботов
- `telegram-kb` — knowledge base по TG API

## Ссылка

- Этот скил: https://github.com/brilenkov/brain-tools/blob/main/agent-skills/tg-bot-access-control/SKILL.md
