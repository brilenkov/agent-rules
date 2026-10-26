# Chat Stability Guard

GUARD for Z.ai chat stability — prevents chat breakage, tool_call corruption, content moderation triggers, and context loss. Ensures agent works incrementally and preserves recoverable context.

TRIGGER: proactive at session start AND before any multi-step task. Also triggers when user says "чат сломался", "опять ошибка", "иногда выдает ошибку", "почему не отвечает", "chat broke", "chat stopped responding".

## Rules

### 1. Tool Call Integrity (CRITICAL)

**Problem**: Z.ai GLM-5.2 sometimes emits tool_calls missing required fields (`type`, `id`, `function.name`). Once saved to chat history, every subsequent API call includes the broken tool_call → upstream returns HTTP 400 with code 1214 `工具类型不能为空` ("tool type cannot be empty"). Chat becomes permanently broken.

**Rules**:
- Before emitting any tool_call, mentally verify: `id` ✅, `type` ✅ (must be `"function"`), `function.name` ✅, `function.arguments` ✅ (valid JSON string).
- If a tool_call fails with `is_error: true` or `status: "error"`, **do NOT retry the same call**. Inspect the error, fix the call structure, then retry with a corrected version.
- If you see `upstream returned status 400` with `工具类型不能为空` in any assistant message — **STOP immediately**. The chat is broken. Tell the user to start a new chat and use the context recovery file.
- Prefer `Bash` with simple commands over complex multi-tool calls when possible. Fewer tool_calls = fewer chances for corruption.

### 2. Content Moderation Awareness

**Problem**: Z.ai has a content moderation layer. Themes involving sex-for-money, commercial sex work, explicit sexual content descriptions, and certain politically sensitive topics trigger moderation. The chat receives a `Content Security Warning` and stops responding.

**Rules**:
- If the user discusses relationships that involve commercial sex themes (sponsorship, paid encounters, MЖМ with payment), **do not reproduce or quote explicit content**. Respond abstractly: "Понял ситуацию. Тема закрыта/поляризована. Переходим к задаче X."
- Do NOT paste voice message transcripts that contain explicit sexual content into your response. Summarize neutrally.
- If you receive a `Content Security Warning` — acknowledge it briefly, abstract the conversation to neutral terms, and redirect to the actual task.
- Keep all relationship/therapy discussions at a clinical/analytical level, not a descriptive one.

### 3. Subtask Decomposition (CRITICAL)

**Problem**: Large multi-file tasks (e.g., birthdays_all.md dataview + 8 file renames + 5 date format fixes + 4 merges) create long tool_call chains. Each tool_call is a risk point. If one breaks, the entire chain fails and the chat may become unusable.

**Rules**:
- Break any task involving >3 file modifications into subtasks of ≤3 files each.
- Complete one subtask → verify → commit to git → then start the next.
- Never batch more than 3 Write/Edit/Bash operations in a single response. Spread across multiple responses.
- If a subtask fails, the previous subtasks are already committed — context is preserved.

### 4. File Verification Before Complex Operations

**Problem**: Running `grep` or `find` on non-existent paths, or parsing files with unexpected encoding, can produce tool_call errors that corrupt chat history.

**Rules**:
- Before running `grep`/`find`/`Read` on a file, first verify it exists: `ls -la <path>` or `test -f <path>`.
- Before parsing MHTML/HTML files, check file size and encoding first.
- If a file doesn't exist, don't retry — tell the user and ask for the correct path.

### 5. Incremental Commits

**Problem**: If a chat breaks after 5 tasks are done but before the commit, all work is lost.

**Rules**:
- After completing each subtask that modifies brain-vault files, immediately commit with a descriptive message.
- Commit format: `<subtask description> — chat <chat_id_short>`
- Push to remote after every 2-3 commits.

### 6. No Invented Data

**Problem**: Agent sometimes invents birthdays, dates, times, names, and other factual data that then gets saved to the brain-vault as if real.

**Rules**:
- NEVER invent dates (birthdays, appointments, deadlines). Only use dates from brain-vault files or explicit user statements.
- NEVER invent names, phone numbers, addresses, or credentials.
- If data is missing, say "не найдено в brain-vault, уточните" — don't fill the gap.
- If you previously invented data and it was saved — flag it for correction at the next opportunity.

### 7. Context Recovery Protocol

**Problem**: When a chat breaks, the next agent starts from zero. All context about what was done, what's pending, and key decisions is lost.

**Rules**:
- After completing a significant task (a commit, a session, a subtask), append a summary entry to `brain/06_journal/context_recovery_<date>.md`.
- Format:
  ```markdown
  ## <timestamp> — <task name>
  **Chat ID**: <short>
  **Status**: completed | in-progress | blocked
  **Commits**: <hash> → <repo>
  **Files**: <list>
  **Decisions**: <key decisions>
  **Next**: <what to do next>
  ```
- At the start of a new chat, if the user says "восстанови контекст" or "продолжай", read the latest `context_recovery_*.md` file first.
- Keep the recovery file concise — 1-2 lines per task, not full paragraphs.

### 8. Error Detection and Early Warning

**Problem**: Chat breakage often starts with a single failed tool_call. If detected early, the user can start a new chat before more damage is done.

**Rules**:
- If you see `Oops, something went wrong. Please refresh the page or try again later.` in your own previous responses — the chat is already breaking. Warn the user immediately.
- If you receive `upstream returned status 400` or `工具类型不能为空` — the chat IS broken. Do not attempt further work. Tell the user to start a new chat.
- If 2+ consecutive tool_calls fail with different errors — pause and tell the user, don't keep trying.
- If you notice your responses are getting shorter or you're losing context — save what you can to the recovery file and warn the user.

### 9. New Chat Handoff

When starting a new chat (after breakage or proactively), provide this starter prompt template to the user:

```
Прочитай brain/06_journal/context_recovery_<latest_date>.md — там последний статус.
Я Алексей, работаем над brain-vault.
Последние коммиты: <hash> (brain), <hash> (brain-tools).
Продолжаем с задачи: <specific task from recovery file>.
```

Keep it short. One task per chat start. Don't try to do everything at once.
