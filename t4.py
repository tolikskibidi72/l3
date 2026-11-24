# завдання 4. демонстрація інтроспекції: __name__, __doc__, __annotations__ та help()

import config_manager.core.validator as validator_module
from config_manager import ConfigValidationError, load_json_config, validate_config


def main() -> None:
    print("=== 1. інтроспекція модуля ===")
    print(f"__name__: {validator_module.__name__}")
    print(f"__doc__:  {validator_module.__doc__}")

    print("\n=== 2. інтроспекція функцій (__name__, __annotations__, __doc__) ===")
    for func in (validate_config, load_json_config):
        print(f"функція: {func.__name__}")
        print(f"  __annotations__: {func.__annotations__}")
        first_line_doc = func.__doc__.splitlines()[0] if func.__doc__ else ""
        print(f"  __doc__ (перший рядок): {first_line_doc}")

    print("\n=== 3. виклик help(validate_config) ===")
    help(validate_config)

    print("=== 4. виклик help(ConfigValidationError) ===")
    help(ConfigValidationError)


if __name__ == "__main__":
    main()