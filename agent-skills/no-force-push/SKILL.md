# No Force Push — Git Safety Guard

**CRITICAL RULE:** NEVER use `git push --force`. ALWAYS use `git push --force-with-lease` instead.

## TRIGGER

Активируется когда:
- User упоминает "force push", "push --force", "затереть remote"
- Команда `git push -f` или `git push --force` встречается в скрипте
- Перед любым push проверяем — не является ли он force

## Что делает

1. **Блокирует** `git push --force` — заменяет на `git push --force-with-lease`
2. Если `--force-with-lease` fails (remote обновился) — показывает diff и просит подтверждение
3. Логирует все push операции в `brain/09_meta/git_pushes.log`

## Почему это критично

Force push **удаляет коммиты** на remote которые отсутствуют в локальном repo:
- Другие разработчики потеряют свою работу
- CI/CD pipelines сломаются
- Невозможно откатить — коммиты физически исчезают из remote history
- Восстановление возможно только через reflog (только на машине где были коммиты)

## Что использовать вместо

```bash
# ❌ ЗАПРЕЩЕНО:
git push --force origin main

# ✅ БЕЗОПАСНО:
git push --force-with-lease origin main

# --force-with-lease проверяет что remote не изменился с момента
# последнего fetch. Если кто-то запушил новые коммиты — push ОТКАЖЕТСЯ.
```

## Если нужно перезаписать remote (rebase scenario)

```bash
# 1. Fetch latest
git fetch origin

# 2. Check if remote has new commits we don't have
git log origin/main..HEAD  # our commits
git log HEAD..origin/main  # their commits

# 3. If no conflicts — push with lease
git push --force-with-lease origin main

# 4. If remote has commits we don't have — merge first
git pull --rebase origin main
git push origin main  # normal push, no force needed
```

## Recovery от force push

Если кто-то сделал force push и удалил коммиты:

```bash
# 1. Check reflog for lost commits
git reflog --oneline | head -20

# 2. Find the commit before force push
git log --all --oneline | grep "your-commit-message"

# 3. Restore specific files from that commit
git checkout <commit-hash> -- path/to/files/

# 4. Commit restored files
git add path/to/files/
git commit -m "Restore: files deleted by force push"
git push origin main
```

## Tags

`git` `safety` `force-push` `critical` `guard`
