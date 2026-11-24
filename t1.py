# завдання 1. обробка виключень: try/except/else/finally та контекстний менеджер

import json
import os


def prepare_test_files():
    #створюємо тестові файли через контекстний менеджер with
    valid_data = {"host": "127.0.0.1", "port": 8080, "timeout": 30}
    with open("valid_config.json", "w", encoding="utf-8") as f:
        json.dump(valid_data, f)

    with open("broken_config.json", "w", encoding="utf-8") as f:
        f.write("{host: 127.0.0.1, port: }")  # некоректний json


def scenario_1_read_file(filepath: str):
    #сценарій 1: базова конструкція try/except + контекстний менеджер with
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"  [успіх] файл '{filepath}' прочитано, розмір: {len(content)} байт")
    except FileNotFoundError:
        print(f"  [помилка] файл '{filepath}' не знайдено на диску")


def scenario_2_parse_config(filepath: str):
    #сценарій 2: повна конструкція try/except/else/finally
    data = None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        host = data["host"]
        port = data["port"]
    except json.JSONDecodeError as e:
        print(f"  [помилка] некоректний синтаксис json у '{filepath}': {e.msg}")
    except KeyError as e:
        print(f"  [помилка] у конфігурації відсутній обов'язковий ключ: {e}")
    else:
        print(f"  [else / успіх] конфігурацію завантажено: сервер {host}:{port}")
    finally:
        print(f"  [finally] завершено спробу обробки файлу '{filepath}'")


def scenario_3_calculate_port_offset(port_value, offset):
    #сценарій 3: перехоплення кількох типів виключень одним блоком except (Type1, Type2)
    try:
        port_num = int(port_value)
        result = port_num + offset
        print(f"  [успіх] розрахований порт: {result}")
    except (ValueError, TypeError) as e:
        print(f"  [помилка] неможливо обчислити порт ({type(e).__name__}): {e}")


def cleanup_test_files():
    for filename in ("valid_config.json", "broken_config.json"):
        if os.path.exists(filename):
            os.remove(filename)


def main():
    prepare_test_files()

    print("=== сценарій 1: try/except + контекстний менеджер with ===")
    print("запуск 1 (успішний шлях):")
    scenario_1_read_file("valid_config.json")
    print("запуск 2 (шлях із помилкою):")
    scenario_1_read_file("missing_config.json")

    print("\n=== сценарій 2: try/except/else/finally ===")
    print("запуск 1 (успішний шлях):")
    scenario_2_parse_config("valid_config.json")
    print("запуск 2 (шлях із помилкою json):")
    scenario_2_parse_config("broken_config.json")

    print("\n=== сценарій 3: перехоплення кількох типів except (ValueError, TypeError) ===")
    print("запуск 1 (успішний шлях):")
    scenario_3_calculate_port_offset("8080", 10)
    print("запуск 2 (шлях із помилкою ValueError):")
    scenario_3_calculate_port_offset("not_a_port", 10)
    print("запуск 3 (шлях із помилкою TypeError):")
    scenario_3_calculate_port_offset(None, 10)

    cleanup_test_files()


if __name__ == "__main__":
    main()