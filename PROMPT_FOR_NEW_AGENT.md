# PROMPT FOR NEW AGENT — вставь в начало нового чата с Z.ai

> Скопируй текст ниже и вставь в новый чат. Агент прочитает правила и начнёт следовать.

---

## Базовая инструкция (вставь в чат)

```
Перед началом работы — прочитай правила:
WebFetch https://github.com/brilenkov/agent-rules/blob/main/AGENT_BOOTSTRAP.md

Это чат: <НАЗВАНИЕ ЧАТА> (например: "brain-tools", "aks", "transcribe", "fns-bot")

Репозитории (все private, кроме agent-rules):
- brilenkov/brain-tools — боты, скрипты, agent-skills, mcp-shared (INFRA)
- brilenkov/brain — Obsidian vault: daily notes, контакты, БО сохбеты
- brilenkov/AKS — боевые тесты авиа-аппаратуры (ID-114, MK-114, MU-114, SOVA-1)
- brilenkov/transcribe — 133 сохбета → текст через ElevenLabs
- brilenkov/agent-rules — PUBLIC sanitized rules для всех AI

После чтения правил:
1. Идентифицируй себя: это чат "<НАЗВАНИЕ ЧАТА>"
   git config user.name "Z.ai <НАЗВАНИЕ ЧАТА>"
   git config user.email "z-ai-<НАЗВАНИЕ ЧАТА>@local"
   Представься: [Agent Identity] 🤖 Agent: Z.ai <НАЗВАНИЕ ЧАТА>

2. Перед стартом — проверь GitHub Issues:
   MCP: list_issues("<repo>", "open", "<project-label>")
   Или: WebFetch https://github.com/brilenkov/<repo>/issues

3. Нет issue → создай:
   MCP: create_issue("<repo>", "[<project>] <type>: <description>", body, ["<type>","<project>"])
   Title format: [project] type: description
   Labels: type (bug/feature/...) + project (fns-bot/tg-monitor/...)

4. Перед git push (3+ файлов) — подтверди с пользователем
5. Commit format: <type>(<project>): <description> (fixes #NN)
6. После push — GitHub auto-closes issue (если 'fixes #NN' в commit)
7. Не используй git push --force

8. Координация через MCP (если настроен):
   register_activity("Z.ai <chat>", "<project>", ["<files>"], "issue-NN")
   check_conflict("<project>", ["<files>"])
   heartbeat("Z.ai <chat>") каждые 5 мин
   unregister_activity("Z.ai <chat>") после push

MCP server: https://mcp-shared.onrender.com/sse
Bearer token: <из Bitwarden>

Что делаем?
```

## Если MCP не настроен

Убери пункты 2 (list_issues через MCP), 3 (create_issue через MCP), 8 (координация).
Используй WebFetch GitHub URLs вместо MCP tools.

## Замени <НАЗВАНИЕ ЧАТА>

Перед вставкой в чат — замени `<НАЗВАНИЕ ЧАТА>` на реальное название:
- "brain-tools" — для infrastructure/MCP/agent-rules
- "aks" — для авиационных тестов
- "transcribe" — для транскрибации сохбетов
- "fns-bot" — для FNS receipt bot
- "tg-monitor" — для monitoring bot
- "council-bot" — для council bot
