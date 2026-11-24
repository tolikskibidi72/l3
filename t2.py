# завдання 2. ієрархія власних виключень, ланцюжки (raise ... from) та повторне піднесення

import json
import os


#---ієрархія власних виключень---

class ConfigError(Exception):
    # базовий клас помилок конфігурації
    def __init__(self, message: str, code: str = "config_error"):
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


class ConfigNotFoundError(ConfigError):
    #помилка доступу: файл конфігурації не знайдено
    def __init__(self, filepath: str):
        self.filepath = filepath
        super().__init__(f"файл '{filepath}' не знайдено", code="not_found")

    def __str__(self) -> str:
        return f"[{self.code}] не вдалося відкрити ресурс '{self.filepath}'"


class ConfigParseError(ConfigError):
    #помилка парсингу json
    def __init__(self, filepath: str, line: int, details: str):
        self.filepath = filepath
        self.line = line
        self.details = details
        super().__init__(f"помилка синтаксису у '{filepath}'", code="parse_error")

    def __str__(self) -> str:
        return f"[{self.code}] файл '{self.filepath}', рядок {self.line}: {self.details}"


class ConfigValidationError(ConfigError):
    # помилка бізнес-логіки/валідації полів
    def __init__(self, field: str, value, reason: str):
        self.field = field
        self.value = value
        self.reason = reason
        super().__init__(f"некоректне поле '{field}'", code="validation_error")

    def __str__(self) -> str:
        return f"[{self.code}] поле '{self.field}' (значення={self.value!r}): {self.reason}"


# ---сервісні функції ---

def load_config(filepath: str) -> dict:
    #завантаження файлу з формуванням ланцюжка виключень (raise ... from)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ConfigNotFoundError(filepath) from e
    except json.JSONDecodeError as e:
        raise ConfigParseError(filepath, e.lineno, e.msg) from e


def validate_config(data: dict) -> dict:
    # перевірка значень полів конфігурації
    host = data.get("host")
    if not isinstance(host, str) or not host.strip():
        raise ConfigValidationError("host", host, "хост має бути непорожнім рядком")

    port = data.get("port")
    if not isinstance(port, int) or not (1 <= port <= 65535):
        raise ConfigValidationError("port", port, "порт має бути цілим числом від 1 до 65535")

    return data


def load_and_log_config(filepath: str) -> dict:
    # демонстрація повторного піднесення (raise без аргументів) після логування
    try:
        raw = load_config(filepath)
        return validate_config(raw)
    except ConfigError as e:
        print(f"  [журнал] зафіксовано помилку конфігурації: {e}")
        raise


#--- допоміжні функції для тестів ---

def prepare_files():
    with open("broken_t2.json", "w", encoding="utf-8") as f:
        f.write('{"host": "127.0.0.1", "port": }')

    with open("invalid_port.json", "w", encoding="utf-8") as f:
        json.dump({"host": "127.0.0.1", "port": 99999}, f)


def cleanup_files():
    for name in ("broken_t2.json", "invalid_port.json"):
        if os.path.exists(name):
            os.remove(name)


def main():
    prepare_files()

    print("=== 1. перехоплення ConfigNotFoundError та ланцюжок __cause__ ===")
    try:
        load_config("no_such_file.json")
    except ConfigNotFoundError as e:
        print(f"  перехоплено: {e}")
        print(f"  атрибут filepath: {e.filepath}")
        print(f"  первинна причина (__cause__): {type(e.__cause__).__name__} -> {e.__cause__}")

    print("\n=== 2. перехоплення ConfigParseError та ланцюжок __cause__ ===")
    try:
        load_config("broken_t2.json")
    except ConfigParseError as e:
        print(f"  перехоплено: {e}")
        print(f"  рядок помилки: {e.line}")
        print(f"  первинна причина (__cause__): {type(e.__cause__).__name__} -> {e.__cause__}")

    print("\n=== 3. перехоплення ConfigValidationError ===")
    try:
        data = load_config("invalid_port.json")
        validate_config(data)
    except ConfigValidationError as e:
        print(f"  перехоплено: {e}")
        print(f"  проблемне поле: {e.field}, значення: {e.value}")

    print("\n=== 4. повторне піднесення (raise) та перехоплення базовим ConfigError ===")
    try:
        load_and_log_config("invalid_port.json")
    except ConfigError as e:
        print(f"  зовнішній обробник отримав базовий ConfigError ({type(e).__name__}): {e}")

    cleanup_files()


if __name__ == "__main__":
    main()