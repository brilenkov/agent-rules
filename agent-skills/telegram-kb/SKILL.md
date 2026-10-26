---
name: telegram-kb
description: >
  Knowledge base for Telegram bot development. TRIGGER when user asks about:
  Telegram bots, TG API, aiogram, pyTelegramBotAPI, telethon, Telegram Stars,
  parse_mode, formatting, FSM, inline keyboards, bot architecture, payments,
  bot testing, or any TG-related development question. Also triggers on
  "тг бот", "телеграм бот", "как сделать бота", "aiogram", "telethon".
  Loads the knowledge base from brain/04_references/telegram_kb.md and
  provides relevant code examples, patterns, and links.
---

# Telegram KB — skill for TG bot development questions

> Loads the knowledge base when user asks about Telegram bot development.

## When to trigger

- "как сделать бота" / "how to make a bot"
- "aiogram" / "telebot" / "pyTelegramBotAPI" / "telethon"
- "Telegram Stars" / "оплата в боте"
- "parse_mode" / "форматирование сообщений"
- "FSM" / "inline keyboard" / "кнопки"
- "тг бот" / "телеграм бот"
- Any code question involving `aiogram`, `telebot`, `telegram` Python libraries

## What to do

1. Read `/home/z/my-project/brain/04_references/telegram_kb.md` (the knowledge base)
2. Also check relevant files in `alexenur_marathon_bot/` for code examples
3. Check `brain/05_projects/marafon_stiranie/13_tg_bot_architecture.md` for architecture
4. Answer with relevant code patterns, links, and best practices from the KB
5. If user asks about new topic not in KB → search web → add to KB → answer

## Knowledge base location

- **Main KB**: `brain/04_references/telegram_kb.md`
- **Architecture**: `brain/05_projects/marafon_stiranie/13_tg_bot_architecture.md`
- **Bot code**: `alexenur_marathon_bot/app/` (bot.py, handlers/, keyboards/)
- **Telethon tests**: `alexenur_marathon_bot/scripts/telethon_login.py`
- **Tests**: `alexenur_marathon_bot/tests/` (66 tests: 46 unit + 20 integration)

## Topics covered in KB

| Topic | Section in KB |
|---|---|
| aiogram 3.x setup | 📚 Библиотеки → aiogram |
| pyTelegramBotAPI | 📚 Библиотеки → pyTelegramBotAPI |
| Telethon (testing) | 📚 Библиотеки → Telethon |
| Telegram Stars payments | 💰 Telegram Stars |
| Promocodes | 💰 Telegram Stars → Промокоды |
| HTML formatting | 📝 Форматирование → HTML |
| MarkdownV2 | 📝 Форматирование → MarkdownV2 |
| Long messages (>4000) | 📝 Форматирование → Разделение |
| Bot architecture | 🏗 Архитектура alexenur_marathon_bot |
| Data models | 🏗 Архитектура → Модели данных |
| Scheduler (cron) | 🏗 Архитектура → Scheduler |
| Proxy (bypass blocks) | 🏗 Архитектура → Прокси |
| Google Drive integration | 🔌 Интеграции → Google Drive |
| OpenAI integration | 🔌 Интеграции → OpenAI |
| Telethon testing | 🧪 Тестирование |
| .env variables | 🔑 Переменные окружения |

## Updating the KB

When user provides a new article or finding:
1. Read the article (WebFetch)
2. Extract key technical details
3. Append to the relevant section in `telegram_kb.md`
4. Add source link to "🔗 Источники" section
5. Commit to brain repo

## Related skills

- [[../time-guard/SKILL]] — time slot reminders
- [[../do-it-now/SKILL]] — 2-minute rule
- [[../daily-note-scaffolder/SKILL]] — daily notes

## Related files

- `brain/04_references/telegram_kb.md` — main knowledge base
- `alexenur_marathon_bot/README.md` — bot project README
- `alexenur_marathon_bot/app/bot.py` — bot initialization
- `brain/05_projects/marafon_stiranie/13_tg_bot_architecture.md` — architecture doc
