---
name: do-not-delete
description: NEVER delete or suggest deleting files, services, databases, or configurations without explicit user confirmation. Activate when considering DELETE operations, git rm, DROP TABLE, render API DELETE, or any destructive action. Triggers on 'delete', 'удалить', 'drop', 'remove', 'rm', 'destroy', 'cleanup', 'очистить'.
---

# Skill: Do Not Delete

> ⚠ Этот skill активируется когда я собираюсь что-то удалить.
> Правило: НИКОГДА не удалять без явного подтверждения пользователя.

## Принцип

1. **НЕ удалять** файлы, сервисы, БД, конфигурации без явного «да, удали» от пользователя
2. **НЕ предлагать** удаление как решение проблемы
3. **НЕ делать** `git rm`, `DROP TABLE`, `DELETE FROM`, `render API DELETE` без подтверждения
4. **НЕ чистить** `node_modules/`, `__pycache__/`, логи — если не просят
5. **НЕ сбрасывать** БД, не пересоздавать таблицы без backup

## Что делать вместо удаления

| Вместо | Делай |
|--------|-------|
| Удалить файл | Переименовать в `.bak` |
| Удалить сервис | Приостановить (suspend) |
| DROP TABLE | `CREATE TABLE ..._old AS SELECT *` |
| `git rm` | `git mv file file.bak` |
| Удалить env | Закомментировать с `# DELETED:` |
| Очистить логи | Архивировать в `.log.gz` |

## Render API — правила

- `DELETE /v1/services/{id}` — НИКОГДА без явного подтверждения
- `POST .../deploys` с clearCache — OK
- `PATCH` — OK (обновление)
- `GET` — OK (чтение)

## Приватные файлы (НЕ удалять, НЕ gitignore)

- `.render-credentials` — Render API ключ
- `.env` — переменные окружения
- `credentials/*.json` — Google OAuth credentials
- `skills/*/SKILL.md` — скиллы

## Файлы которые МОЖНО удалять (без подтверждения)

- `__pycache__/`, `.pytest_cache/`, `*.pyc`
- `node_modules/` (есть package-lock.json)
- `/tmp/*`
