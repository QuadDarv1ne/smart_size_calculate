import json

def calculate_sizes(chest: int, waist: int, hips: int, height: int):
    """
    Рассчитывает размеры одежды по параметрам.
    :param chest: Обхват груди (в см)
    :param waist: Обхват талии (в см)
    :param hips: Обхват бедер (в см)
    :param height: Рост (в см)
    :return: Словарь размеров
    """
    # Российские размеры
    ru_size = (chest - 4) // 2  # Примерная формула

    # Международные размеры
    intl_size = ""
    if ru_size <= 40:
        intl_size = "XS"
    elif ru_size <= 42:
        intl_size = "S"
    elif ru_size <= 46:
        intl_size = "M"
    elif ru_size <= 50:
        intl_size = "L"
    elif ru_size <= 54:
        intl_size = "XL"
    else:
        intl_size = "XXL"

    # Европейские размеры
    eu_size = ru_size + 6

    # Американские размеры
    us_size = ru_size - 34

    # Британские размеры
    uk_size = us_size

    # Ростовые категории
    height_category = ""
    if height < 160:
        height_category = "Petite"
    elif height > 190:
        height_category = "Tall"
    else:
        height_category = "Regular"

    return {
        "RU": ru_size,
        "International": intl_size,
        "EU": eu_size,
        "US": us_size,
        "UK": uk_size,
        "Height Category": height_category
    }

def display_sizes(sizes):
    """
    Выводит размеры в удобной форме.
    :param sizes: Словарь с размерами
    """
    print("Ваши размеры:")
    for key, value in sizes.items():
        print(f"{key}: {value}")

def load_user_data_from_json(filename):
    """
    Загружает данные пользователя из JSON файла.
    :param filename: Имя файла
    :return: Словарь с параметрами пользователя
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Убедитесь, что файл существует.")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка чтения файла {filename}. Проверьте его содержимое.")
        return None

def main():
    print("Добро пожаловать в калькулятор размеров!")

    # Загружаем данные из файла
    user_data = load_user_data_from_json("user_data.json")

    if user_data:
        print("Данные успешно загружены:")
        for key, value in user_data.items():
            print(f"{key}: {value} см")

        # Расчет размеров
        sizes = calculate_sizes(
            chest=user_data.get("chest", 0),
            waist=user_data.get("waist", 0),
            hips=user_data.get("hips", 0),
            height=user_data.get("height", 0)
        )

        # Вывод результатов
        display_sizes(sizes)

        # Сохранение результатов в файл
        save_sizes_to_json(sizes, "sizes_report.json")
    else:
        print("Не удалось загрузить данные пользователя. Завершение программы.")

def save_sizes_to_json(sizes, filename):
    """
    Сохраняет размеры в JSON файл.
    :param sizes: Словарь с размерами
    :param filename: Имя файла
    """
    try:
        with open(filename, 'w') as f:
            json.dump(sizes, f, ensure_ascii=False, indent=4)
        print(f"Результаты сохранены в файл {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении в файл {filename}: {e}")

if __name__ == "__main__":
    main()
