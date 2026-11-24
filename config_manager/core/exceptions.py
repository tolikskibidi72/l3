"""Модуль ієрархії власних виключень для роботи з конфігураціями."""

from typing import Any


class ConfigError(Exception):
    """Базовий клас усіх помилок пакету config_manager.

    Args:
        message (str): Текстовий опис помилки.
        code (str): Короткий код помилки.
    """

    def __init__(self, message: str, code: str = "config_error") -> None:
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        """Повертає форматоване представлення помилки.

        Returns:
            str: Рядок із кодом та текстом помилки.
        """
        return f"[{self.code}] {self.message}"


class ConfigNotFoundError(ConfigError):
    """Виключення, що піднімається при відсутності файлу конфігурації.

    Args:
        filepath (str): Шлях до відсутнього файлу.
    """

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        super().__init__(f"файл '{filepath}' не знайдено", code="not_found")

    def __str__(self) -> str:
        """Повертає текстовий опис помилки доступу до файлу.

        Returns:
            str: Повідомлення зі шляхом до ресурсу.
        """
        return f"[{self.code}] не вдалося відкрити ресурс '{self.filepath}'"


class ConfigParseError(ConfigError):
    """Виключення, що піднімається при помилці парсингу JSON.

    Args:
        filepath (str): Шлях до пошкодженого файлу.
        line (int): Номер рядка з помилкою.
        details (str): Деталі синтаксичної помилки.
    """

    def __init__(self, filepath: str, line: int, details: str) -> None:
        self.filepath = filepath
        self.line = line
        self.details = details
        super().__init__(f"помилка синтаксису у '{filepath}'", code="parse_error")

    def __str__(self) -> str:
        """Повертає текстовий опис помилки парсингу.

        Returns:
            str: Повідомлення з файлом, номером рядка та деталями.
        """
        return f"[{self.code}] файл '{self.filepath}', рядок {self.line}: {self.details}"


class ConfigValidationError(ConfigError):
    """Виключення, що піднімається при некоректних значеннях полів конфігурації.

    Args:
        field (str): Назва проблемного поля.
        value (Any): Передане некоректне значення.
        reason (str): Пояснення причини відхилення.
    """

    def __init__(self, field: str, value: Any, reason: str) -> None:
        self.field = field
        self.value = value
        self.reason = reason
        super().__init__(f"некоректне поле '{field}'", code="validation_error")

    def __str__(self) -> str:
        """Повертає текстовий опис помилки валідації.

        Returns:
            str: Повідомлення з назвою поля, значенням та причиною.
        """
        return f"[{self.code}] поле '{self.field}' (значення={self.value!r}): {self.reason}"