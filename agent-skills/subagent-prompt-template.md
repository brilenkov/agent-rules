# Subagent Prompt Template

> Copy-paste этот блок в начало каждого Task prompt при делегировании subagent'у.
> Гарантирует что subagent следует agent-identity-protocol, не делает silent
> git push/pull, пишет в worklog после подзадачи.

## Шаблон для вставки в Task prompt

```text
SUBAGENT INSTRUCTIONS — follow strictly:

1. IDENTITY: At start, introduce yourself per agent-identity-protocol:
   [Agent Identity]
   🤖 Agent: <Subagent role> (e.g. "Subagent for fns-bot code review")
   🎯 Working with: <project name>
   📍 Task ID: <provided by parent>

2. CONTEXT BOUNDARIES — you DON'T see:
   - /home/z/my-project/ filesystem (unless paths explicitly given below)
   - /home/z/my-project/skills/ — can't use Skill tool directly
   - worklog.md — can't read it; but MUST append to it after subtask
   - AGENT_BOOTSTRAP.md — can't read it; rules in this prompt suffice

3. BEFORE GIT OPS — NEVER silent push/pull:
   - git push — STOP, return commit info to parent. Parent asks user "да".
   - git pull --rebase — STOP, return what conflicts might exist.
   - git commit (3+ files) — show diff summary first.
   - git reset --hard / git rm — NEVER without explicit parent approval.
   Auto-push allowed ONLY after 3+ file modifications (git-after-each-step
   rule) BUT with announcement:
   [Auto-Push — git-after-each-step rule]
   📤 Auto-pushing: <count> commits to <branch>
      Files: <list>
      Reason: subtask completed (3+ modifications)

4. WORKLOG — after subtask complete, append to /home/z/my-project/worklog.md
   using Write tool (NOT Edit — append):
   ---
   Task ID: <provided by parent>
   Agent: <Subagent role>
   Task: <what you did>
   
   Work Log:
   - <step 1>
   - <step 2>
   
   Stage Summary:
   - <key results>
   - <files produced>

5. REPORT BACK — at end, return to parent:
   - What was done (concise summary)
   - Files produced/modified (paths)
   - Git commits made (hashes + messages)
   - Any blockers / TODO for parent

6. PROJECT-SPECIFIC RULES:
   <parent inserts project-specific rules here, e.g.:
   - "Bot uses ALLOWED_TG_USER_IDS env var, never make it public"
   - "Telegram bot can't send messages from user account"
   - "Brain vault contains medical info, redact PII in logs">

7. SKILLS REFERENCE (if subagent has Skill tool access):
   - Skill(command="agent-identity-protocol") — full identity rules
   - Skill(command="git-after-each-step") — auto-commit rules
   - Skill(command="no-force-push") — never use --force
   - Skill(command="do-not-delete") — never delete without confirmation
   - Skill(command="project-<name>") — project-specific context

8. NO SUBMODULES — brain-tools is single source of truth, but NOT a submodule.
   If you need AGENT_BOOTSTRAP.md or agent-skills/, ask parent to copy content
   into your prompt or use WebFetch on GitHub URL:
   https://github.com/brilenkov/brain-tools/blob/main/AGENT_BOOTSTRAP.md

---

TASK-SPECIFIC INSTRUCTIONS:

<Task ID>: <provided by parent>
<Working with>: <project name>
<Steps>:
1. <step 1>
2. <step 2>
...
<Files to modify>: <list>
<Expected outcome>: <description>
```

## Пример использования

```python
Task(
    description="Fix TTS bug in webrtc",
    subagent_type="general-purpose",
    prompt="""
SUBAGENT INSTRUCTIONS — follow strictly:

1. IDENTITY: ...
2. CONTEXT BOUNDARIES — ...
3. BEFORE GIT OPS — ...
4. WORKLOG — ...
5. REPORT BACK — ...
6. PROJECT-SPECIFIC RULES:
   - Therapist-voice-bot uses WRTC_ACCESS_TOKEN env var (Render)
   - Server.js + public/index.html are the main files
   - Bot is read-only for user, but voice therapist is interactive
   
7. SKILLS REFERENCE:
   - Skill(command="project-council-bot") — no wait, wrong project
   - Actually no project skill exists for therapist-voice-bot yet

8. NO SUBMODULES — brain-tools is single source...

---

TASK-SPECIFIC INSTRUCTIONS:

Task ID: webrtc-tts-fix-v2
Working with: therapist-voice-bot/webrtc
Steps:
1. Read /home/z/my-project/brain-tools/bots/therapist-voice-bot/webrtc/server.js
2. Find the TTS race condition (browser speechSynthesis starts before z-ai MP3)
3. Fix: try z-ai TTS first, only emit therapist_text with has_audio=true if
   z-ai succeeded. Otherwise emit therapist_text with has_audio=false (browser
   uses speechSynthesis).
4. Update public/index.html to handle new {text, has_audio} object format
5. Test by reading the code (no live test possible)
6. Commit + push to brain-tools main (after user confirmation via parent)

Files to modify:
- /home/z/my-project/brain-tools/bots/therapist-voice-bot/webrtc/server.js
- /home/z/my-project/brain-tools/bots/therapist-voice-bot/webrtc/public/index.html

Expected outcome: TTS plays only z-ai MP3 (no Google fallback competing).
"""
)
```

## Anti-patterns (что НЕ делать в subagent prompt)

❌ BAD:
```
Fix the TTS bug. Push to git when done.
```
(No identity, no worklog requirement, no push confirmation, no paths, no project rules)

✅ GOOD:
```
[Full SUBAGENT INSTRUCTIONS block from above]
TASK-SPECIFIC INSTRUCTIONS:
Task ID: ...
Working with: ...
Files to modify: <explicit paths>
Steps: <numbered list>
```

## Когда НЕ использовать subagent

Subagents не подходят для:
- Tasks требующих full conversation context (subagent не видит историю чата)
- Tasks требующих Skill tool (subagent не имеет того же набора skills)
- Tasks где нужно подтверждение user'а в реальном времени (subagent не может напрямую общаться с user'ом — только через parent)
- Tasks с высокой вариативностью (subagent не может адаптироваться на лету)

Используй subagent для:
- Чистых, well-defined задач (write a function, fix a specific bug, parse a file)
- Tasks где нужен параллелизм (2 subagent'а параллельно — один пишет код, другой пишет тесты)
- Tasks где контекст полностью передаваем в текстовом prompt'е
