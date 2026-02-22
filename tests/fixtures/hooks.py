from __future__ import annotations

import json
from pathlib import Path

import pytest

FAILED_FIXTURE_STATUSES = {"failed", "broken"}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def _get_allure_results_dir(config: pytest.Config) -> Path | None:
    for option_name in ("alluredir", "--alluredir"):
        try:
            value = config.getoption(option_name)
        except Exception:
            continue
        if value:
            return Path(value)
    return None


def _filter_fixture_blocks(container_path: Path) -> None:
    try:
        data = json.loads(container_path.read_text(encoding="utf-8"))
    except Exception:
        return

    changed = False
    for section in ("befores", "afters"):
        blocks = data.get(section)
        if not isinstance(blocks, list):
            continue
        filtered_blocks = [block for block in blocks if block.get("status") in FAILED_FIXTURE_STATUSES]
        if len(filtered_blocks) != len(blocks):
            data[section] = filtered_blocks
            changed = True

    if changed:
        container_path.write_text(json.dumps(data), encoding="utf-8")


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    _ = exitstatus
    results_dir = _get_allure_results_dir(session.config)
    if not results_dir or not results_dir.exists():
        return

    for container_path in results_dir.glob("*-container.json"):
        _filter_fixture_blocks(container_path)
