from __future__ import annotations

from contextlib import contextmanager

import allure


@contextmanager
def step(title: str):
    with allure.step(title):
        yield


def masked_env(env_var_name: str, parameter_name: str | None = None) -> None:
    allure.dynamic.parameter(
        parameter_name or env_var_name.lower(),
        f"env.{env_var_name}",
        mode=allure.parameter_mode.MASKED,
    )


def hidden_env(env_var_name: str, parameter_name: str | None = None) -> None:
    allure.dynamic.parameter(
        parameter_name or env_var_name.lower(),
        f"env.{env_var_name}",
        mode=allure.parameter_mode.HIDDEN,
    )
