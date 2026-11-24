"""Модуль валідації параметрів серверної конфігурації."""

from typing import Any, Optional

# відносний імпорт у межах одного підпакету
from .exceptions import ConfigValidationError


def validate_config(data: dict[str, Any], allowed_hosts: Optional[list[str]] = None) -> dict[str, Any]:
    """Перевіряє коректність обов'язкових полів конфігурації.

    Args:
        data (dict[str, Any]): Словник із параметрами конфігурації.
        allowed_hosts (Optional[list[str]]): Необов'язковий список дозволених хостів.

    Returns:
        dict[str, Any]: Перевірений словник конфігурації.

    Raises:
        ConfigValidationError: Якщо поле host або port має невірний тип чи значення.
    """
    host = data.get("host")
    if not isinstance(host, str) or not host.strip():
        raise ConfigValidationError("host", host, "хост має бути непорожнім рядком")

    if allowed_hosts is not None and host not in allowed_hosts:
        raise ConfigValidationError("host", host, f"хост не входить до списку дозволених: {allowed_hosts}")

    port = data.get("port")
    if not isinstance(port, int) or isinstance(port, bool) or not (1 <= port <= 65535):
        raise ConfigValidationError("port", port, "порт має бути цілим числом від 1 до 65535")

    return data