---
name: git-credentials-guard
description: >
  GUARD for GitHub PAT (Personal Access Token) — prevents accidental deletion
  of /home/z/my-project/.git-credentials file. Verifies token works before any
  git operation. Restores from known good state if file is missing/invalid.
  TRIGGER proactively at session start AND on any git operation (push/pull/clone).
  Also triggers when user mentions: "PAT потерялся", "креденшиалы пропали",
  "git push не работает", "credential helper", "не могу запушить",
  "restore PAT", "проверь PAT".
  NEVER logs the token value. NEVER prints the token to stdout/worklog.
  If token is invalid/expired — instruct user to create new PAT at
  https://github.com/settings/tokens and paste it.
---

# git-credentials-guard — protect GitHub PAT from accidental deletion

> PAT (Personal Access Token) is the most critical credential. Losing it
> breaks all git push operations. This skill ensures PAT is always present,
> valid, and never accidentally deleted.

## When to trigger

### Proactive (auto)
1. **At session start** — verify `.git-credentials` exists and is non-empty
2. **Before any `git push` / `git pull` / `git clone`** — verify credentials

### Explicit triggers (user request)
- «PAT потерялся», «креденшиалы пропали», «credential helper»
- «git push не работает», «не могу запушить»
- «restore PAT», «проверь PAT»
- «восстановь токен», «почему теряется PAT»

## Hard rules

1. **NEVER print token value** — not in chat, not in worklog, not in any file other than `.git-credentials`
2. **NEVER commit `.git-credentials` to git** — already in .gitignore of all repos
3. **NEVER log full token** — only log SHA256 hash + first/last 4 chars for identification
4. **NEVER include token in error messages** — when reporting errors, use `<TOKEN>` placeholder
5. **ALWAYS verify token** before declaring it "valid" — run `git ls-remote` on a known repo
6. **ALWAYS restore from backup** if backup exists and main file is missing
7. **ALWAYS instruct user to rotate token** if any sign of compromise

## Where things live

| File | Purpose | Permissions |
|---|---|---|
| `/home/z/my-project/.git-credentials` | Active PAT (used by git credential helper) | `600` (only owner rw) |
| `/home/z/my-project/.git-credentials.backup` | Last known good PAT | `600` |
| `/home/z/my-project/.git-credentials.hash` | SHA256 hash of last verified token | `644` |
| `/home/z/my-project/worklog.md` | Append-only audit log (no token value!) | `644` |

## Procedure — at session start

```bash
# 1. Check credentials file exists
CRED=/home/z/my-project/.git-credentials
ls -la "$CRED" 2>/dev/null

if [ ! -f "$CRED" ] || [ ! -s "$CRED" ]; then
    echo "⚠️ .git-credentials missing or empty"
    # Try to restore from backup
    if [ -f /home/z/my-project/.git-credentials.backup ] && [ -s /home/z/my-project/.git-credentials.backup ]; then
        cp /home/z/my-project/.git-credentials.backup "$CRED"
        chmod 600 "$CRED"
        echo "✅ Restored from backup"
    else
        echo "❌ No backup. Ask user for new PAT"
        # Don't proceed with git operations
        return 1
    fi
fi

# 2. Configure git to use credential helper
git config --global credential.helper 'store --file=/home/z/my-project/.git-credentials'
git config --global user.name "Alexey Brilenkov"
git config --global user.email "brilenkov@users.noreply.github.com"

# 3. Verify token works (without exposing value)
git ls-remote https://github.com/brilenkov/brain.git HEAD 2>&1 | head -3
if [ $? -eq 0 ]; then
    echo "✅ PAT verified"
    # Save backup + hash
    cp "$CRED" /home/z/my-project/.git-credentials.backup
    chmod 600 /home/z/my-project/.git-credentials.backup
    # Compute hash (NOT the token value)
    sha256sum "$CRED" | awk '{print $1}' > /home/z/my-project/.git-credentials.hash
else
    echo "❌ PAT invalid or expired"
fi
```

## Procedure — before every git push

Run quick check:

```bash
if [ ! -f /home/z/my-project/.git-credentials ] || [ ! -s /home/z/my-project/.git-credentials ]; then
    echo "❌ Cannot push: .git-credentials missing. Ask user: 'PAT потерялся — дай новый'"
    return 1
fi
```

If missing — DO NOT proceed with push. Ask user for PAT.

## How to add a new PAT (when user provides one)

User says: «вот PAT: ghp_xxxxx...»

1. Write to file (NEVER echo back):

```bash
cat > /home/z/my-project/.git-credentials << 'EOF'
https://brilenkov:USER_PROVIDED_PAT@github.com
EOF
chmod 600 /home/z/my-project/.git-credentials
```

2. Configure git:

```bash
git config --global credential.helper 'store --file=/home/z/my-project/.git-credentials'
git config --global user.name "Alexey Brilenkov"
git config --global user.email "brilenkov@users.noreply.github.com"
```

3. Verify:

```bash
git ls-remote https://github.com/brilenkov/brain.git HEAD 2>&1 | head -3
```

4. If verification succeeds:
   - Create backup: `cp .git-credentials .git-credentials.backup`
   - Compute hash: `sha256sum .git-credentials | awk '{print $1}' > .git-credentials.hash`
   - Log to worklog (WITHOUT token value):
     ```
     2026-10-19T15:00 | git-credentials-guard | PAT updated | hash=abc123... | verified=yes
     ```
   - Tell user: "✅ PAT сохранён, верифицирован, бэкап создан"

5. If verification fails:
   - DO NOT save backup
   - Tell user: "❌ PAT не работает. Проверь: scope (нужен `repo`), срок действия, корректность вставки"

## Why PAT might "disappear"

Common causes (skill guards against all):

| Cause | Solution |
|---|---|
| Container/sandbox restart | Restore from `.git-credentials.backup` |
| Accidental `rm` by another agent | Restore from `.git-credentials.backup` |
| Wrong file permissions | `chmod 600 .git-credentials` |
| `git config --global` reset | Re-run `git config --global credential.helper 'store --file=/home/z/my-project/.git-credentials'` |
| Token expired (90 days default) | User creates new PAT at https://github.com/settings/tokens |
| Token revoked by user | User creates new PAT |

## Audit logging

When this skill runs, append to `/home/z/my-project/worklog.md`:

```
---
Task ID: git-credentials-guard-<action>
Agent: <agent>
Task: <verify/restore/update>

Work Log:
- checked .git-credentials: exists|missing|empty
- backup: available|missing
- git ls-remote brain: success|failed
- action taken: <restored_from_backup|asked_user_for_new_pat|verified_ok|updated_pat>
- token hash (first 8 chars): abc12345

Stage Summary:
- credentials status: ok|invalid|missing
- next step: <push to github|wait for user PAT|...>
```

**NEVER log:**
- Token value
- File contents of `.git-credentials`
- Full hash (only first 8 chars)

## User-facing message templates

### When PAT is valid
```
✅ PAT verified (hash: abc12345...)
- File: /home/z/my-project/.git-credentials (mode 600)
- Backup: /home/z/my-project/.git-credentials.backup
- Configured: credential.helper, user.name, user.email
- Test: git ls-remote brain → success
```

### When PAT is missing (need from user)
```
❌ .git-credentials file is missing or empty.

To fix:
1. Go to https://github.com/settings/tokens (login as brilenkov)
2. Generate new token (classic) → scope: repo
3. Copy token (starts with ghp_)
4. Tell me: "вот PAT: ghp_xxxxx..."

I'll save it to /home/z/my-project/.git-credentials, configure git, verify,
create backup.
```

### When PAT is invalid
```
❌ PAT is invalid or expired.

Test result: git ls-remote https://github.com/brilenkov/brain.git → "Authentication failed"

Possible causes:
- Token expired (default 90 days)
- Token revoked
- Scope missing (need `repo`)

Solution: create new PAT at https://github.com/settings/tokens
```

## Forbidden patterns

❌ Echo token value to stdout/chat
❌ Write token to worklog or any markdown file
❌ Commit `.git-credentials` to git
❌ Pass token as command-line argument (visible in process list)
❌ Use token in URLs that get logged

## Related skills

- `debug-status` — show git state (without token)
- `schedule-change-guard` — pattern for protected file changes
- `bot-access-info` — for TG bot tokens (different repo)

## Files referenced

- `/home/z/my-project/.git-credentials` — active PAT (NEVER in git)
- `/home/z/my-project/.git-credentials.backup` — backup PAT
- `/home/z/my-project/.git-credentials.hash` — SHA256 hash for identification
- `/home/z/my-project/worklog.md` — audit log (token value NEVER logged)
- `/home/z/my-project/brain/.gitignore` — must contain `.git-credentials`
- `/home/z/my-project/brain-tools/.gitignore` — must contain `.git-credentials`
