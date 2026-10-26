---
name: bot-test-suite
description: Regression testing protocol for alexenur_marathon_bot. Activate before deploy, after code changes, or when user asks 'прогони тесты', 'регрессия', 'проверь всё'. Triggers: 'тесты', 'регрессия', 'test suite', 'run tests', 'проверь тесты', 'smoke', 'coverage'.
---

# Skill: Bot Test Suite — Regression Protocol

> v3.10.2 — categorized test markers for selective/regression runs.

## Quick commands

```bash
cd /home/z/my-project/brain-tools/bots/alexenur_marathon_bot
PY=/home/z/.venv/bin/python3

# SMOKE (fast, critical path — ~4s)
$PY -m pytest tests/ --ignore=tests/integration/ -m smoke -q

# REPORT FLOW (save_report PENDING/APPROVED, reject)
$PY -m pytest tests/ --ignore=tests/integration/ -m report_flow -q

# COURSE CONTENT (solo→соло, из 92, theory in day 1)
$PY -m pytest tests/ --ignore=tests/integration/ -m course_content -q

# JOURNEY (end-to-end: join→report→approve→progress)
$PY -m pytest tests/ --ignore=tests/integration/ -m journey -q

# EDGE CASES (double approve, reject already rejected)
$PY -m pytest tests/ --ignore=tests/integration/ -m edge_cases -q

# SERVICES (version, user, settings, messages)
$PY -m pytest tests/ --ignore=tests/integration/ -m services -q

# WEB ENDPOINTS (/health, /logs, /admin)
$PY -m pytest tests/integration/test_web_endpoints.py -m web -q

# FULL REGRESSION (all unit + integration, no live — ~6s)
$PY -m pytest tests/ --ignore=tests/integration/test_telethon_live.py \
  --ignore=tests/integration/test_telethon_real.py \
  --ignore=tests/integration/test_full_flows.py \
  --ignore=tests/integration/test_handler_direct.py \
  -m "not live" --tb=line -q

# LIVE TELEGRAM (real messages — ~2min)
$PY -m pytest tests/integration/test_telethon_live.py -m live -v -s

# COVERAGE REPORT
$PY -m pytest tests/ \
  --ignore=tests/integration/test_telethon_live.py \
  --ignore=tests/integration/test_telethon_real.py \
  --ignore=tests/integration/test_full_flows.py \
  --ignore=tests/integration/test_handler_direct.py \
  --cov=app --cov-report=term -q
```

## Test categories

| Marker | Tests | Runtime | When to run |
|---|---|---|---|
| `smoke` | 9 | ~4s | Before EVERY deploy |
| `report_flow` | 3 | ~1s | After changes to save_report, approve, reject |
| `course_content` | 5 | ~1s | After changes to week_*.md files |
| `journey` | 4 | ~1s | After changes to handlers or services |
| `edge_cases` | 3 | ~1s | After changes to report flow |
| `services` | 11 | ~1s | After changes to version, user, settings |
| `web` | ~10 | ~1s | After changes to __main__.py endpoints |
| `live` | 10 | ~2min | After deploy — verify live bot works |
| `not live` | 86 | ~6s | Full regression (no Telegram) |

## Regression protocol

### Before deploy:
1. `smoke` — must pass (critical path)
2. `report_flow` — if save_report changed
3. `course_content` — if materials changed
4. `not live` — full regression (~6s)
5. If any FAIL → fix before deploy

### After deploy:
1. `/health` → check `{"status":"ok"}`
2. `live` — Telethon tests (~2min)
3. If live FAIL → check logs `/admin/logs`

### After reseed:
1. `course_content` — verify content quality
2. `smoke` — verify critical path

## Test files

| File | Markers | Tests |
|---|---|---|
| `test_services.py` | smoke, services | ~15 |
| `test_report_flow.py` | smoke, report_flow, facilitator | 7 |
| `test_course_cards.py` | smoke, course_content | 11 |
| `test_user_journey.py` | smoke, journey | 5 |
| `test_edge_cases.py` | smoke, edge_cases | 6 |
| `test_services_coverage.py` | services | 15 |
| `test_web_endpoints.py` | web, smoke | ~10 |
| `test_seed.py` | — | ~3 |
| `test_models.py` | models | ~5 |
| `test_config.py` | config | ~3 |
| `test_handlers.py` | — | ~10 |
| `test_db_helpers.py` | — | ~5 |
| `test_telethon_live.py` | live | 10 |

**Total: 120 tests (110 unit + 10 live)**

## Coverage (v3.10.1)

```
TOTAL: 6756 statements, 5227 missed, 1529 covered = 23%
```

| File | Coverage |
|---|---|
| models.py | 96% |
| parse_weeks.py | 92% |
| user.py | 84% |
| course.py | 72% |
| settings.py | 69% |
| report.py | 60% |
| version.py | 55% |
| subscription.py | 51% |
| messages.py | 39% |
| seed.py | 42% |
| handlers/* | <10% |
| scheduler.py | 10% |
