"""Підпакет core: доменні виключення та валідація конфігурації."""

from .exceptions import (
    ConfigError,
    ConfigNotFoundError,
    ConfigParseError,
    ConfigValidationError,
)
from .validator import validate_config

__all__ = [
    "ConfigError",
    "ConfigNotFoundError",
    "ConfigParseError",
    "ConfigValidationError",
    "validate_config",
]