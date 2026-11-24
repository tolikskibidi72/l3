"""Пакет config_manager для завантаження та валідації JSON-конфігурацій."""

from .core import (
    ConfigError,
    ConfigNotFoundError,
    ConfigParseError,
    ConfigValidationError,
    validate_config,
)
from .utils import load_json_config

# внутрішня змінна, яка НЕ входить у __all__
INTERNAL_SECRET = "hidden_value"

__all__ = [
    "ConfigError",
    "ConfigNotFoundError",
    "ConfigParseError",
    "ConfigValidationError",
    "load_json_config",
    "validate_config",
]