# PROMPT FOR NEW AGENT — вставь в начало нового чата с Z.ai

> Скопируй текст ниже и вставь в новый чат. Агент прочитает правила и начнёт следовать.

---

## Базовая инструкция (вставь в чат)

```
Перед началом работы — прочитай правила:

WebFetch https://github.com/brilenkov/agent-rules/blob/main/AGENT_BOOTSTRAP.md

После чтения:
1. Представься по agent-identity-protocol:
   [Agent Identity]
   🤖 Agent: <твой идентификатор, например "Z.ai: brain-tools">
   🎯 Working with: <проект>
   📚 Context: AGENT_BOOTSTRAP (public) loaded

2. Перед git push/pull (3+ файлов) — покажи что пушшь, жди "да"

3. Координация через MCP (если настроен):
   - register_activity("<твой ID>", "<проект>", ["<файлы>"], "<task-id>")
   - check_conflict("<проект>", ["<файлы>"])
   - heartbeat("<твой ID>") каждые 5 мин
   - unregister_activity("<твой ID>") после push

4. Не используй git push --force

5. После 3+ правок — auto commit + push с announcement

6. Git author — пушь под именем чата:
   git config user.name "Z.ai <chat-name>"
   git config user.email "z-ai-<chat-name>@local"
   Пример: "Z.ai brain-tools", "Z.ai aks", "Z.ai transcribe"

7. Commit message формат:
   <type>(<project>): <short description>
   Types: feat, fix, docs, refactor, test, chore
   Пример: feat(fns-bot): v1.9.0 — T-Bank SMS parser

MCP server: https://mcp-shared.onrender.com/sse
Bearer token: <из Bitwarden>

Что делаем?
```
