"""Модуль простого журналювання подій конфігурації."""

from datetime import datetime


def log_event(level: str, message: str) -> str:
    """Формує та виводить у консоль запис журналу.

    Args:
        level (str): Рівень повідомлення (наприклад, info або error).
        message (str): Текст події.

    Returns:
        str: Сформований рядок журналу.

    Raises:
        ValueError: Якщо текст повідомлення порожній.
    """
    if not message.strip():
        raise ValueError("повідомлення журналу не може бути порожнім")
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{level.lower()} {timestamp}] {message}"
    print(f"  {entry}")
    return entry