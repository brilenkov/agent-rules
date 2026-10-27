# PROMPT FOR NEW AGENT — вставь в начало нового чата с Z.ai

> Скопируй текст ниже, замени плейсхолдеры, вставь в новый чат.
> Токены (PAT, MCP_TOKEN) НЕ в этом файле — получи у Alexey или из Bitwarden.

---

```
Это чат: <НАЗВАНИЕ ЧАТА>

Перед началом — прочитай правила:
WebFetch https://github.com/brilenkov/agent-rules/blob/main/AGENT_BOOTSTRAP.md

Репозитории (private, кроме agent-rules):
- brilenkov/brain-tools — боты, скрипты, mcp-shared
- brilenkov/brain — Obsidian vault
- brilenkov/AKS — авиа-тесты (production)
- brilenkov/transcribe — 133 сохбета → текст
- brilenkov/agent-rules — PUBLIC rules (этот файл)

GitHub PAT (из Bitwarden, vault "GitHub"):
export PAT=<PAT_ИЗ_BITWARDEN>
git clone https://brilenkov:${PAT}@github.com/brilenkov/brain-tools.git /home/z/my-project/brain-tools

После чтения AGENT_BOOTSTRAP:

1. MCP КЛИЕНТ (из public repo, без PAT):
   pip install mcp
   export MCP_URL=https://mcp-shared.onrender.com/sse
   export MCP_TOKEN=<MCP_TOKEN_ИЗ_BITWARDEN>
   mkdir -p scripts
   curl -o scripts/mcp_client.py https://raw.githubusercontent.com/brilenkov/agent-rules/main/scripts/mcp_client.py
   python3 scripts/mcp_client.py list-tools

2. ИДЕНТИФИКАЦИЯ:
   cd /home/z/my-project/brain-tools
   git config user.name "Z.ai <НАЗВАНИЕ ЧАТА>"
   git config user.email "z-ai-<НАЗВАНИЕ>@local"
   Представься: [Agent Identity]

3. КООРДИНАЦИЯ:
   python3 scripts/mcp_client.py register "Z.ai-<НАЗВАНИЕ>" "<project>" <files>
   python3 scripts/mcp_client.py active-agents

4. ISSUES:
   python3 scripts/mcp_client.py issues brain-tools --open

5. ПЕРЕД PUSH:
   python3 scripts/mcp_client.py check "<project>" <files>
   git commit -m "<type>(<project>): <desc> (fixes #NN)

   Co-authored-by: Z.ai <НАЗВАНИЕ> <z-ai-<НАЗВАНИЕ>@local>"
   git push origin main

6. ПОСЛЕ PUSH:
   python3 scripts/mcp_client.py unregister "Z.ai-<НАЗВАНИЕ>"

7. NO FORCE PUSH
8. ВСЕГДА добавляй Co-authored-by в commit (MANDATORY)

Что делаем?
```

## Плейсхолдеры

| Что | Где взять | Пример |
|---|---|---|
| НАЗВАНИЕ ЧАТА | Название вкладки | brain-tools, aks |
| PAT_ИЗ_BITWARDEN | Bitwarden → "GitHub" | ghp_xxx |
| MCP_TOKEN_ИЗ_BITWARDEN | Bitwarden → "MCP token" | mcp_zai_main_b_xxx |
| project | Что делаешь | fns-bot |
| files | Какие файлы | bot.py |
