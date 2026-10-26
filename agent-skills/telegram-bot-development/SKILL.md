---
name: telegram-bot-development
description: Use when developing, modifying, or formatting Telegram bot features — payment (Stars/XTR, YooKassa), message formatting (HTML, Markdown, Rich Messages Bot API 10.1), inline keyboards, callbacks, FSM, error handling, aiogram 3.x patterns. Triggers on requests mentioning Telegram bots, aiogram, message formatting, payments in bot, send_invoice, refund_star_payment, parse_mode, callback_data, tg-bot, тг-бот, телеграм-бот.
---

# Skill: Telegram Bot Development Knowledge Base

> Этот skill автоматически активируется при работе с Telegram-ботами.
> В контексте: aiogram 3.x, Bot API 10.1+, Stars (XTR), Rich Messages,
> HTML/Markdown formatting, payments, refund, error handling.

## Когда активировать

Любой запрос, связанный с:
- Созданием/модификацией Telegram-бота
- Форматированием сообщений (`parse_mode`, HTML, Markdown, Rich Messages)
- Платежами в боте (Stars, YooKassa, refund)
- Inline-кнопками, callback_query, FSM
- Обработкой ошибок (`telegram_message_too_long`, `PROVIDER_ACCOUNT_INVALID`, etc.)
- aiogram 3.x best practices

## База знаний — что читать

Перед началом любой работы над TG-ботом — открыть соответствующую статью:

### 📱 Оплата через Telegram Stars (XTR)

| Статья | Где лежит | Что покрывает |
|--------|-----------|---------------|
| Stars на aiogram 3.7+ | `brain-tools/alexenur_marathon_bot/docs/telegram_stars_articles/article_1_habr_821415.md` | `LabeledPrice`, `send_invoice`, `pre_checkout_query`, `refund_star_payment`, `paysupport` |
| Stars на pyTelegramBotAPI | `brain-tools/alexenur_marathon_bot/docs/telegram_stars_articles/article_2_habr_969080.md` | `send_invoice` с `currency=XTR`, `provider_token=""`, payload-идентификация |

**Ключевые правила Stars:**
1. `currency` = `"XTR"` (строго)
2. `provider_token` = `""` (пустая строка)
3. `prices` = один `LabeledPrice` (не несколько)
4. **Подключение Stars через @BotFather обязательно** → иначе `PROVIDER_ACCOUNT_INVALID`
5. Refund: `bot.refund_star_payment(user_id, telegram_payment_charge_id)` — до 1 года
6. `pre_checkout_query` надо ответить в течение 10 сек (иначе авто-отмена)

### 📝 Форматирование сообщений (Rich Messages, Bot API 10.1)

| Статья | Где лежит | Что покрывает |
|--------|-----------|---------------|
| Bot API 10.1 Rich Messages | `brain-tools/docs/telegram_kb/article_3_bot_api_10_1_rich_messages.md` | Rich Messages = 32K символов, нативные таблицы, чек-листы, `<details>`, LaTeX, `<tg-collage>`, `<tg-map>`, стриминг AI, Guard Bots |
| Примеры Rich Messages | `brain-tools/docs/telegram_kb/article_4_rich_messages_examples.md` | `InputRichMessage(html=...)`, `message.answer_rich(...)`, aiogram >=3.29.1, полный HTML-пример заказа с таблицей + details + mark |
| Справочник HTML-тегов (Regular Messages) | `brain/09_meta/TELEGRAM_FORMATTING.md` | `<b>`, `<i>`, `<code>`, `<pre>`, `<blockquote>`, `<a>`, `<tg-spoiler>`, ограничения, таблицы через `<pre>` workaround |

**Когда что:**
- Regular Messages (обычные) → лимит 4096 символов, простое HTML-форматирование
- Rich Messages (новые, Bot API 10.1+) → лимит 32768, нативные таблицы, формулы, медиа
- Rich Messages требуют aiogram >=3.29.1 + `message.answer_rich(InputRichMessage(html=...))`

## Главные правила при работе с TG-ботами

### 1. Форматирование

- **HTML по умолчанию** (`parse_mode=ParseMode.HTML` в `DefaultBotProperties`)
- **MarkdownV2 НЕ использовать** — ломается на эмодзи и кавычках, требует слишком много экранирования
- **Rich Messages** — только если задание длиннее 4096 символов или нужны нативные таблицы
- **Таблицы** в Regular Messages → `<pre>` с выравниванием пробелами (Telegram не поддерживает `<table>`)
- **Длинные сообщения** → chunking по границам `\n\n` (не больше 3500 на часть, запас под клавиатуру)
- **Эмодзи в кнопках** — добавлять, но умеренно (1 на кнопку, не больше 3 на экран)

### 2. Оплата (Stars)

- **Обязательно** подключить Stars в @BotFather: `/mybots` → выбрать бота → `Payments` → `Telegram Stars` → `Connect`
- Без этого — `PROVIDER_ACCOUNT_INVALID` (бот возвращает ошибку при `send_invoice`)
- **Fallback** — если Stars не подключены, показывать ручную оплату с реквизитами карты (env `MANUAL_PAYMENT_CARD`)
- **pre_checkout_query** — отвечать сразу `query.answer(ok=True)`, иначе авто-отмена через 10 сек
- **successful_payment** — фильтр `F.successful_payment` (НЕ `F.successful_payment is not None` — MagicFilter всегда truthy)
- **refund** — `bot.refund_star_payment(user_id, charge_id)`, работает до 1 года

### 3. Inline-кнопки и callback

- `callback_data` ≤ 64 байт — компактно, без словарей
- Для контекстных данных — кодировать ID + действие: `course:active`, `course:send_now`, `payment:menu`
- **После `edit_or_send_long`** (chunking) — исходное сообщение удалено, повторный `edit_text` упадёт. Для «Назад к заданию» — вызывать `cb_send_now`, не `cb_active_course`
- **Кнопка «В меню»** — на каждом экране, callback `menu:main`
- **Primary action первой** в `main_menu_kb` — правило Фиттса, попадает под большой палец

### 4. FSM (Finite State Machine)

- **MemoryStorage** — только dev. На проде — `RedisStorage` (переживает рестарт)
- На Render free — перезапуск каждые 15 мин → MemoryStorage теряет всё. Подключить PostgreSQL addon (`DATABASE_URL`) и Redis addon

### 5. Error handling

- `try/except Exception` — НЕ ловит `asyncio.CancelledError` (его re-raise)
- Различать:
  - `sqlalchemy.OperationalError` → «БД временно недоступна», alert админу
  - `aiogram.exceptions.TelegramRetryAfter` → wait & retry
  - `aiogram.exceptions.TelegramAPIError` → логировать + сообщить юзеру
  - `telegram_message_too_long` → chunking через `send_long_message`
- **Fallback handlers**: universal `@router.message(F.text.startswith("/"))` → «Команда не распознана. /help» — закрывает silent failure

### 6. Health-check и деплой

- **Health endpoint** — `GET /health` возвращает `{"status":"ok", "db":"ok", "scheduler":"running"}`, не просто `200 OK`
- **Pre-deploy backup** — `render.yaml` → `preDeploy` hook → `python -m app.services.backup pre_deploy` (non-fatal)
- **Persistent storage** — SQLite in-container НЕ persistent на Render free. Подключить Postgres addon, `DATABASE_URL` env

### 7. Stars-специфичные баги и решения

| Симптом | Причина | Решение |
|---------|---------|---------|
| `PROVIDER_ACCOUNT_INVALID` | Stars не подключены в @BotFather | Подключить через `/mybots` → `Payments` → `Telegram Stars` → `Connect` |
| `Bad Request: PRICE_LABELS_INVALID` | `prices` содержит > 1 элемента | Для Stars оставить один `LabeledPrice` |
| `Bad Request: CURRENCY_XTR_NOT_SUPPORTED` | `currency` ≠ `"XTR"` | Строго `"XTR"` (регистрозависимо) |
| `Bad Request: PAYLOAD_INVALID` | payload > 127 байт | Сократить payload |
| `pre_checkout_query` не приходит | handler не зарегистрирован | `@router.pre_checkout_query()` без фильтра |
| `F.successful_payment is not None` → TypeError | MagicFilter всегда truthy | Использовать `F.successful_payment` без `is not None` |

## Где этот skill используется

Применяется к репозиториям:
- `brain-tools/alexenur_marathon_bot/` — основной бот (v2.3.2+)
- `brain-tools/marafon_bot/` — legacy-версия (v2.0.0)
- `brain-tools/life_council_bot_v2/` — советник-бот
- Любой новый TG-бот, который разрабатывается

## Ссылки

- Официальная дока: https://core.telegram.org/bots/api
- Stars: https://core.telegram.org/bots/payments-stars
- Rich Messages (Bot API 10.1): https://core.telegram.org/bots/api#rich-messages
- aiogram docs: https://docs.aiogram.dev/
- Статьи в KB: `brain-tools/docs/telegram_kb/`
