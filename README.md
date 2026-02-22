# DM API Tests

## Overview

Test suites are split by domain and markers:

- `smoke` for critical and quick checks
- `regression` for extended checks

## Project Structure

```text
.
|- .github/workflows/
|  |- api-tests-ci.yml
|  |- api-tests-nightly.yml
|  |- api-tests-reusable.yml
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

- `api-tests-reusable.yml`: matrix run for each domain and suite (`smoke`, `regression`) with `pytest -n 3`.
- `api-tests-ci.yml`: reusable launch for `push` to `main`, `pull_request`, and manual run.
- `api-tests-nightly.yml`: daily schedule at `06:00 UTC` (equals `09:00` Turkey, TRT `UTC+3`) and manual run.

Reporting:

- each matrix job uploads its own Allure results artifact
- final merge job combines all artifacts and publishes one merged Allure HTML report artifact
