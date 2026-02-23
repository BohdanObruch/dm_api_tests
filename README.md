# DM API Tests

## Overview

Test suites are split by domain and markers:

- `smoke` for critical and quick checks
- `regression` for extended checks

## Project Structure

```text
.
|- .github/actions/
|  |- setup/action.yml
|  |- publish-allure-pages/action.yml
|- .github/workflows/
|  |- all_tests_report.yml
|  |- run-account-tests.yml
|  |- run-common-tests.yml
|  |- run-community-tests.yml
|  |- run-forum-tests.yml
|  |- run-game-tests.yml
|  |- run-messaging-tests.yml
|- docs/
|  |- test_plan_by_swagger.md
|  |- test_coverage_gap.md
|- src/api/
|  |- controllers/
|  |- models/
|- tests/
|  |- api/
|  |  |- account/
|  |  |- common/
|  |  |- community/
|  |  |- forum/
|  |  |- game/
|  |  |- messaging/
|  |- fixtures/
|- pyproject.toml
```

## Coverage By Swagger Blocks

- `account`: registration/login/account profile/password/email flows, positive + negative auth/body cases.
- `common`: search endpoint with roundtrip/pagination/empty/invalid-query scenarios.
- `community`: polls/reviews/users/uploads baseline coverage, including unauthorized and invalid input checks.
- `forum`: fora/topics/comments coverage with CRUD and likes, including not-found and validation scenarios.
- `game`: covered baseline for lists and key entities (`game`, `attribute schema`, `room`, `post`, `comment`,
  `character`), but still partial vs full swagger scope.
- `messaging`: chat/dialogues/messages read scenarios, not-found checks, auth-negative cases, and invalid payload checks
  for chat post.

Detailed gap analysis against full plan: `docs/test_coverage_gap.md`.

## Requirements

- Python `>=3.14`
- `uv` (recommended)

## Setup

```bash
uv sync
```

## Configuration

Create `.env`:

```env
BASE_URL=http://your-api-host
MAIL_HOG_URL=http://your-mailhog-host
```

## Local Run

```bash
# all tests
uv run pytest

# smoke only
uv run pytest -m smoke

# regression only
uv run pytest -m regression
```

## GitHub Actions

Workflows:

- `run-account-tests.yml`
- `run-common-tests.yml`
- `run-community-tests.yml`
- `run-forum-tests.yml`
- `run-game-tests.yml`
- `run-messaging-tests.yml`
  each workflow runs matrix suites (`smoke`, `regression`) and uploads Allure artifacts in format
  `<domain>-<suite>-allure-results`.
- `all_tests_report.yml` runs on `push` to `main`, `pull_request`, schedule (`06:40 UTC`), and manual запуск.
  It triggers all six domain workflows, then publishes one merged Allure report to GitHub Pages.

Reporting:

- setup duplication is moved to composite action `./.github/actions/setup`
- Allure aggregation + deploy logic is moved to composite action `./.github/actions/publish-allure-pages`
- final `publish-report` job merges all domain/suite artifacts into one Allure report and deploys it to GitHub Pages
