# SETUP GUIDE — для каждого AI tool

> Пошаговая инструкция как подключить каждый AI к Alexey Brilenkov's MCP server + rules.
> Public file — safe to share. No tokens here.

---

## 🔑 Что нужно заранее

1. **MCP server URL**: `https://mcp-shared.onrender.com/sse`
2. **Bearer token** — получить у Alexey (хранится в Bitwarden, vault "AI agent tokens")
3. **Public rules repo**: `https://github.com/brilenkov/agent-rules`

Token tiers:
- **Tier A** (read-only): может читать resources (AGENT_BOOTSTRAP, skills, worklog)
- **Tier B** (read+write): может вызывать tools (append_worklog, git_confirm, render_status)

---

## 🖱 Cursor (на твоей машине)

### Шаг 1: Clone public rules repo

```bash
# Windows (PowerShell)
cd D:\
git clone https://github.com/brilenkov/agent-rules.git

# Mac/Linux
cd ~/projects
git clone https://github.com/brilenkov/agent-rules.git
```

### Шаг 2: Configure MCP

```bash
# В проекте где ты работаешь (или глобально):
mkdir -p .cursor
```

Создай файл `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "brilenkov-shared": {
      "url": "https://mcp-shared.onrender.com/sse",
      "headers": {
        "Authorization": "Bearer ТВОЙ_ТОКЕН_ИЗ_BITWARDEN"
      }
    }
  }
}
```

Заменить `ТВОЙ_ТОКЕН_ИЗ_BITWARDEN` на token из Bitwarden (например `mcp_cursor_a_1636f7417b0244406b192596`).

### Шаг 3: Restart Cursor

```
Ctrl+Shift+P → "Developer: Reload Window"
```

### Шаг 4: Проверка

В Cursor напиши:
```
Проверь статус scheduler-bot через MCP
```

Cursor должен вызвать MCP tool `scheduler_status()` и вернуть результат.

### Шаг 5: Cursor auto-reads rules

При открытии проекта Cursor читает `.cursorrules`. Если хочешь чтобы Cursor видел правила Alexey:

```bash
# В корне твоего проекта:
ln -s /path/to/agent-rules/AGENT_BOOTSTRAP.md .cursorrules
```

Или просто скопируй `.cursorrules` из agent-rules repo.

---

## 🖥 Claude Desktop (на твоей машине)

### Шаг 1: Clone public rules repo (same as Cursor Step 1)

### Шаг 2: Configure MCP

Создай/открой файл:

**Mac:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

Добавь:

```json
{
  "mcpServers": {
    "brilenkov-shared": {
      "type": "sse",
      "url": "https://mcp-shared.onrender.com/sse",
      "headers": {
        "Authorization": "Bearer ТВОЙ_ТОКЕН_ИЗ_BITWARDEN"
      }
    }
  }
}
```

### Шаг 3: Restart Claude Desktop

Полностью закрой и открой Claude Desktop.

### Шаг 4: Проверка

Напиши в Claude Desktop:
```
Read resource agent-bootstrap-public:// from MCP server
```

Claude должен получить sanitized AGENT_BOOTSTRAP.md.

---

## 💬 ChatGPT / DeepSeek / Qwen / Grok / Gemini (web chat)

### Шаг 1: Дай AI правила

Вставь в чат:

```
Я работаю с Alexey Brilenkov. Прочитай правила:
WebFetch https://github.com/brilenkov/agent-rules/blob/main/AGENT_BOOTSTRAP.md
```

AI прочитает sanitized правила (no personal info, no tokens).

### Шаг 2: Для MCP access (если AI поддерживает HTTP/MCP)

```
MCP server для полного контекста:
- URL: https://mcp-shared.onrender.com/sse
- Bearer token: <вставь токен из Bitwarden>
- Token tier: A (read-only) или B (read+write)
```

Если AI не поддерживает MCP (ChatGPT web, DeepSeek web, Qwen web, Grok web):

### Шаг 3 (fallback без MCP): Вставь нужный skill вручную

```
Прочитай skill для проекта:
WebFetch https://github.com/brilenkov/agent-rules/blob/main/agent-skills/agent-identity-protocol/SKILL.md
```

Или для конкретного skill:
```
WebFetch https://github.com/brilenkov/brain-tools/blob/main/agent-skills/<skill-name>/SKILL.md
```
(нужен GitHub login для private brain-tools repo)

### Шаг 4: Проверка

```
Представься по agent-identity-protocol
```

AI должен ответить:
```
[Agent Identity]
🤖 Agent: ChatGPT-4o (или DeepSeek-V3, Qwen, etc.)
🎯 Working with: <project>
📚 Context: public AGENT_BOOTSTRAP loaded
```

---

## 📋 Cline (VS Code extension)

### Шаг 1: Clone public rules repo (same as Cursor Step 1)

### Шаг 2: Configure MCP

В VS Code settings → Cline → MCP Servers:

```json
{
  "mcpServers": {
    "brilenkov-shared": {
      "url": "https://mcp-shared.onrender.com/sse",
      "headers": {
        "Authorization": "Bearer ТВОЙ_ТОКЕН_ИЗ_BITWARDEN"
      }
    }
  }
}
```

Или создай `.clinerules` в корне проекта (symlink to AGENT_BOOTSTRAP.md).

### Шаг 3: Restart VS Code

---

## 📋 Continue.dev

### Шаг 1: Configure MCP

В `~/.continue/config.yaml` (или `.continue/config.yaml` в проекте):

```yaml
mcpServers:
  brilenkov-shared:
    url: https://mcp-shared.onrender.com/sse
    headers:
      Authorization: "Bearer ТВОЙ_ТОКЕН_ИЗ_BITWARDEN"
```

### Шаг 2: Restart Continue.dev

---

## 📋 OpenAI Codex CLI / Aider / другие AGENTS.md readers

### Шаг 1: Clone rules

```bash
git clone https://github.com/brilenkov/agent-rules.git ~/agent-rules
```

### Шаг 2: Symlink AGENTS.md

```bash
# В корне твоего проекта:
ln -s ~/agent-rules/AGENT_BOOTSTRAP.md AGENTS.md
# Codex CLI / Aider auto-read AGENTS.md at startup
```

### Шаг 3: MCP (если поддерживается)

Codex CLI и Aider пока НЕ поддерживают MCP. Используй:
- AGENTS.md (rules) — auto-loaded
- Manual WebFetch для specific skills
- Запрос к Alexey для paste конкретного контекста

---

## 🧪 Проверка для всех

После настройки любой AI должен:

1. ✅ Представляться: `[Agent Identity] 🤖 Agent: <name>...`
2. ✅ Перед git push: `[Git Operation Confirmation] 📤 About to push...`
3. ✅ Использовать MCP tools (если настроен): `find_skill("git")`, `render_status()`
4. ✅ Читать MCP resources (если настроен): `agent-bootstrap://`, `skill://{name}`

---

## 🔄 Генерация нового токена (для нового AI)

```bash
cd /home/z/my-project/brain-tools
python3 scripts/generate_mcp_token.py --tier A --name "deepseek-temp" --expires 24h
```

Выведет:
- Новый token
- JSON fragment для MCP_TOKENS_JSON (добавить на Render)
- Инструкции для Bitwarden
- Cursor .cursor/mcp.json template

---

## ⚠️ Безопасность

- ❌ НИКОГДА не коммить bearer token в git
- ❌ НИКОГДА не вставляй token в AGENT_BOOTSTRAP.md
- ✅ Храни tokens в Bitwarden (vault "AI agent tokens")
- ✅ Используй Tier A (read-only) для временных сессий
- ✅ Используй `--expires 24h` для временных токенов
- ✅ Отзывай токены через удаление из MCP_TOKENS_JSON на Render
