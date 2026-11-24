"""Точка входу для запуску пакету командою python -m config_manager."""

import json
import os

# форма імпорту 1: абсолютний імпорт цілого модуля
import config_manager.utils.logger

# форма імпорту 2: вибірковий абсолютний імпорт конкретних імен
from config_manager.core.exceptions import ConfigError
from config_manager.core.validator import validate_config
from config_manager.utils.loader import load_json_config


def run_demo() -> None:
    """Запускає демонстрацію роботи пакету, імпортів та обмеження __all__.

    Returns:
        None: Результати виводяться безпосередньо в консоль.
    """
    sample_file = "demo_server_config.json"
    with open(sample_file, "w", encoding="utf-8") as f:
        json.dump({"host": "127.0.0.1", "port": 8080}, f)

    try:
        print("=== 1. робота пакету config_manager ===")
        config_manager.utils.logger.log_event("info", f"завантаження '{sample_file}'")
        raw = load_json_config(sample_file)
        valid = validate_config(raw, allowed_hosts=["127.0.0.1", "localhost"])
        config_manager.utils.logger.log_event("info", f"конфігурація валідна: {valid}")

        print("\n=== 2. перевірка обробки помилки через пакет ===")
        try:
            validate_config({"host": "127.0.0.1", "port": 70000})
        except ConfigError as e:
            config_manager.utils.logger.log_event("error", str(e))

        print("\n=== 3. демонстрація обмеження експорту через __all__ ===")
        namespace: dict[str, object] = {}
        exec("from config_manager import *", namespace)
        exported_names = sorted(k for k in namespace if not k.startswith("__"))
        print(f"  імена, імпортовані через 'from config_manager import *': {exported_names}")
        print(f"  чи потрапила внутрішня змінна INTERNAL_SECRET: {'INTERNAL_SECRET' in namespace}")
    finally:
        if os.path.exists(sample_file):
            os.remove(sample_file)


if __name__ == "__main__":
    run_demo()