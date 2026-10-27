# PROMPT FOR NEW AGENT — вставь в начало нового чата с Z.ai

> Скопируй текст ниже и вставь в новый чат. Агент прочитает правила и начнёт следовать.

---

## Базовая инструкция (вставь в чат)

```
Это чат: <НАЗВАНИЕ ЧАТА>

Перед началом работы — прочитай правила:
WebFetch https://github.com/brilenkov/agent-rules/blob/main/AGENT_BOOTSTRAP.md

Репозитории:
- brilenkov/brain-tools — боты, скрипты, agent-skills, mcp-shared (INFRA)
- brilenkov/brain — Obsidian vault: daily notes, контакты, БО сохбеты
- brilenkov/AKS — боевые тесты авиа-аппаратуры (production!)
- brilenkov/transcribe — 133 сохбета → текст через ElevenLabs
- brilenkov/agent-rules — PUBLIC rules (this file)

После чтения AGENT_BOOTSTRAP:

1. УСТАНОВИ MCP КЛИЕНТ (обязательно!):
   pip install mcp
   export MCP_URL=https://mcp-shared.onrender.com/sse
   export MCP_TOKEN=<bearer token из Bitwarden>
   cp /home/z/my-project/brain-tools/scripts/mcp_client.py /home/z/my-project/scripts/
   python3 scripts/mcp_client.py list-tools
   # должно показать 20 tools + 6 resources

2. ИДЕНТИФИЦИРУЙ СЕБЯ:
   git config user.name "Z.ai <НАЗВАНИЕ ЧАТА>"
   git config user.email "z-ai-<НАЗВАНИЕ ЧАТА>@local"
   Представься: [Agent Identity] 🤖 Agent: Z.ai <НАЗВАНИЕ ЧАТА>

3. ЗАРЕГИСТРИРУЙСЯ В КООРДИНАЦИИ:
   python3 scripts/mcp_client.py register "Z.ai <НАЗВАНИЕ ЧАТА>" "<project>" <files>
   python3 scripts/mcp_client.py active-agents
   # видишь кто ещё работает

4. ПРОВЕРЬ GITHUB ISSUES:
   python3 scripts/mcp_client.py issues brain-tools --open
   # возьми существующую задачу или создай новую

5. ПЕРЕД GIT PUSH:
   python3 scripts/mcp_client.py check "<project>" <files>
   # проверь конфликты
   Подтверди с пользователем: [Git Operation Confirmation]
   git commit -m "<type>(<project>): <desc> (fixes #NN)"
   git push origin main

6. ПОСЛЕ PUSH:
   python3 scripts/mcp_client.py unregister "Z.ai <НАЗВАНИЕ ЧАТА>"
   # освободи файлы для других агентов

7. НЕ ИСПОЛЬЗУЙ git push --force

Bearer token для MCP: <вставь из Bitwarden>

Что делаем?
```

## Замени <НАЗВАНИЕ ЧАТА>

Примеры названий: brain-tools, aks, transcribe, fns-bot, tg-monitor, council-bot
