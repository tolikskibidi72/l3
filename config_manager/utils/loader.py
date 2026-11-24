"""Модуль завантаження JSON-конфігурацій із файлової системи."""

import json
from typing import Any

# відносний імпорт із сусіднього підпакету
from ..core.exceptions import ConfigNotFoundError, ConfigParseError


def load_json_config(filepath: str) -> dict[str, Any]:
    """Зчитує та розбирає JSON-файл конфігурації.

    Args:
        filepath (str): Шлях до файлу конфігурації.

    Returns:
        dict[str, Any]: Словник із розібраними даними.

    Raises:
        ConfigNotFoundError: Якщо файл не знайдено на диску.
        ConfigParseError: Якщо файл містить некоректний JSON.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ConfigNotFoundError(filepath) from e
    except json.JSONDecodeError as e:
        raise ConfigParseError(filepath, e.lineno, e.msg) from e