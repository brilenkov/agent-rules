---
name: safe-reseed-policy
description: Activate when user asks about reseeding course, course content updates, daily_tasks changes, or when working with seed.py / parse_weeks.py. CRITICAL safety rules for protecting participant progress during course content updates. Triggers: 'reseed', 'пересидировать', 'сидировать', 'course materials', 'daily_tasks', 'course content', 'seed.py', 'force_reseed', 'participations progress', 'progress loss'.
---

# Skill: Safe Reseed Policy

> v3.7.1 (2026-10-22): Created after CRITICAL incident — `seed_stiranie_if_empty`
> deleted course on bot restart → CASCADE wiped participations + reports.
> Lost 50+ reports of 2 participants (Render free PG has no auto-backup).
>
> Этот скилл защищает прогресс участников при обновлении контента курса.

## 🎯 Главное правило

**НИКОГДА** не вызывать `await session.delete(course)` автоматически (не в
ручной admin-команде). CASCADE FK `participations.course_id` и
`reports.course_id` (ondelete="CASCADE") удалит ВСЕ связанные данные.

## 📋 Архитектура FK (что удаляется cascade)

```
courses.id
    ↓ ondelete=CASCADE
    ├── participations.course_id (FK CASCADE)
    │       ↓ ondelete=CASCADE
    │       └── reports.user_id (FK CASCADE — но reports нет FK на participation_id, только на user_id)
    │           ↓ но reports.course_id (FK CASCADE) → также удалится
    └── daily_tasks.course_id (FK CASCADE)
```

**Если удалить course** → CASCADE удалит:
- ALL `daily_tasks` WHERE course_id = X (это ОК, мы хотим их обновить)
- ALL `participations` WHERE course_id = X (❌ прогресс участников потерян)
- ALL `reports` WHERE course_id = X (❌ все отчёты потеряны)

## 🛡️ Safe reseed — что безопасно

### ✅ Safe: `force_reseed_stiranie` (v3.7.0+)

Код в `app/seed.py`:
```python
async def force_reseed_stiranie() -> None:
    # НЕ удаляет course
    course_id = existing.id
    # DELETE только daily_tasks
    await session.execute(
        delete(DailyTask).where(DailyTask.course_id == course_id)
    )
    # INSERT new daily_tasks
    for task_data in tasks_data:
        session.add(DailyTask(**kwargs))
    # Update course fields
    existing.duration_days = max_day
    existing.finishes_at = datetime.utcnow() + timedelta(days=max_day)
    # Clamp participations.current_day if > max_day
    parts = (await session.execute(
        select(Participation).where(
            Participation.course_id == course_id,
            Participation.current_day > max_day,
        )
    )).scalars().all()
    for p in parts:
        p.current_day = max_day  # clamp
```

**Что сохраняется:**
- `course.id` (не меняется) → participations FK остаётся валидным
- `participations` (текущий день, completed_days, streak) — только clamp
- `reports` — все отчёты остаются (FK на user_id + course_id + day_number)

### ❌ Forbidden: auto-delete in startup

```python
# ❌ НИКОГДА ТАК НЕ ДЕЛАТЬ в setup_scheduler / on_startup
if existing and tasks_count != expected_count:
    await session.delete(existing)  # CASCADE wipes participations + reports
```

Это сработает при перезапуске бота → потеря данных.

## 📐 When to reseed

| Сценарий | Что делать |
|---|---|
| Обновил markdown файлы в `course_materials/stiranie/weeks/` | `/reseed_stiranie` (вызовет force_reseed_stiranie — безопасно) |
| Удалил дубликат week файла | `/reseed_stiranie` |
| Изменил структуру курса (12 недель → 14) | `/reseed_stiranie` + clamp participations |
| Хочу поправить текст одного задания | `/admin_edit_task <id>` (НЕ reseed) |
| Новый курс с нуля | `/reseed_stiranie` — создаст новый course.id (старый остаётся) |

## 🔍 Pre-deploy check (mandatory)

Перед каждым deploy который трогает `app/seed.py`:

```bash
# Найти все session.delete(course) в коде
grep -rn "session.delete.*Course\|session.delete.*existing" app/seed.py
# Если есть вне force_reseed_stiranie (который НЕ должен удалять course) — STOP
```

Только `force_reseed_stiranie` имеет право вызывать delete-операции на daily_tasks.
Никогда на courses напрямую.

## 🚨 Recovery protocol (если прогресс потерян)

Если инцидент произошёл:

1. **Проверить auto-backup** (если настроен в scheduler.py 03:00):
   ```python
   from app.services.backup import backup_db
   # Render free PG: backup вернёт None (нет pg_dump)
   # Render paid PG: backup в /tmp/*.sql
   ```

2. **Render Dashboard → Postgres → Backups** (только paid plan):
   - Manual snapshot если есть
   - Восстановить через restore

3. **Восстановить participations вручную** (если знаешь значения):
   ```sql
   INSERT INTO participations (user_id, course_id, joined_at, current_day, completed_days, streak, is_finished, facilitator_tg_id)
   VALUES (1, NEW_COURSE_ID, NOW(), 12, 11, 11, FALSE, NULL);
   ```
   Источники значений: логи бота (/admin/logs), бот-уведомления в Telegram,
   /admin_db?action=table&table=participations (если ещё что-то осталось).

4. **Reports — утерянные** восстановлению НЕ подлежат если нет backup.
   Можно создать заглушки:
   ```sql
   INSERT INTO reports (user_id, course_id, day_number, type, content, status, submitted_at)
   VALUES (1, NEW_COURSE_ID, 1, 'text', '[восстановлено из памяти]', 'approved', NOW());
   ```

## 📦 Auto-backup setup (recommended)

В `app/scheduler.py` уже есть `_auto_backup` cron в 03:00 MSK.

**Что нужно для работы:**
1. Render paid Postgres plan ($7/мес) — для pg_dump support
2. Папка `/tmp/backups` с правами на запись (Docker container)
3. `pg_dump` доступен в container

**Render free PG** — backup НЕ работает (нет pg_dump permissions на shared instance).
Если критично — переходи на paid plan.

## 📚 История инцидентов

- **2026-10-22 v3.7.0** — `seed_stiranie_if_empty` delete existing course при
  tasks_count (100) != expected (92) после удаления дублей markdown.
  CASCADE удалил 2 participations + 50+ reports.
  v3.7.1: hotfix — `seed_stiranie_if_empty` больше НИКОГДА не удаляет курс.

## 🛠️ File structure

- `app/seed.py` — `seed_stiranie_if_empty()` (auto on startup) +
  `force_reseed_stiranie()` (manual via `/reseed_stiranie`)
- `app/handlers/admin.py:reseed_stiranie` — admin command (calls force_reseed)
- `app/parse_weeks.py` — `parse_all_weeks()` returns list[dict] from markdown
- `course_materials/stiranie/weeks/*.md` — source of truth (markdown files)

## 🔗 Related skills

- `render-deploy-watchdog` — pre-deploy checks for safety
- `facilitator-reports-workflow` — workflow with participant data (must be preserved)
- `do-not-delete` — general no-delete rules (this skill extends for courses)

## 📝 Pre-deploy checklist

Before deploying changes to `app/seed.py`:
- [ ] `grep -rn "session.delete.*Course" app/seed.py` — должно быть 0 matches
- [ ] `grep -rn "session.delete.*existing" app/seed.py` — должно быть 0 matches
- [ ] force_reseed_stiranie имеет только `delete(DailyTask)` НЕ `delete(Course)`
- [ ] seed_stiranie_if_empty НЕ имеет delete при tasks_count mismatch
- [ ] Тест `tests/test_seed.py` проходит
- [ ] После deploy — проверить через `/admin/logs` что нет WARNING про course deletion

## 🚀 Quick test after reseed

After running `/reseed_stiranie`:

1. `/admin/logs` — должен видеть:
   ```
   🔄 Пересидирование курса «Стирание» (id=N) — только задания
   🗑 Удалено старых заданий: 100
   ✅ Курс «Стирание» пересидирован: 92 заданий (max day=92)
   ```
2. SQL check:
   ```sql
   SELECT count(*) FROM daily_tasks WHERE course_id = N; -- 92
   SELECT count(*) FROM participations WHERE course_id = N; -- unchanged
   SELECT count(*) FROM reports WHERE course_id = N; -- unchanged
   ```
3. User perspective — `/start` → «📋 Активный курс» → видит тот же день что раньше
