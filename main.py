import json
from pathlib import Path
from enum import Enum
import logging

# Проверка наличия rich
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress
    from rich import print
    rich_installed = True
except ImportError:
    rich_installed = False
    print("Модуль 'rich' не найден. Вывод будет менее наглядным. Установите 'rich' через: pip install rich")

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Константы размеров (вынесены в словарь)
SIZE_LIMITS = {
    "XS": 40,
    "S": 42,
    "M": 46,
    "L": 50,
    "XL": 54,
}

# Категории роста
HEIGHT_CATEGORIES = {
    150: "Very Petite",
    160: "Petite",
    190: "Tall",
    200: "Very Tall"
}

# Enum для ключей словаря размеров
class SizeType(Enum):
    INTERNATIONAL = "1️⃣  International"
    RU = "2️⃣  RU"
    EU = "3️⃣  EU"
    US = "4️⃣  US"
    UK = "5️⃣  UK"
    HEIGHT_CATEGORY = "6️⃣  Height Category"

def calculate_sizes(chest: int, waist: int, hips: int, height: int) -> dict:
    """
    Рассчитывает размеры одежды по параметрам.

    Args:
        chest: 🎽 Обхват груди (в см)
        waist: 📏 Обхват талии (в см)
        hips: 🍑 Обхват бедер (в см)
        height: 🧍 Рост (в см)

    Returns:
        Словарь размеров с ключами типа SizeType.
    Raises:
        ValueError: Если параметры не являются неотрицательными целыми числами.
    """
    if not all(isinstance(arg, int) and arg >= 0 for arg in [chest, waist, hips, height]):
        raise ValueError("Размеры и рост должны быть неотрицательными целыми числами.")
    
    russian_size = (chest - 4) // 2
    intl_size = get_intl_size(russian_size)
    eu_size = russian_size + 6
    us_size = russian_size - 34
    uk_size = us_size
    height_category = get_height_category(height)

    return {
        SizeType.INTERNATIONAL: intl_size,
        SizeType.RU: russian_size,
        SizeType.EU: eu_size,
        SizeType.US: us_size,
        SizeType.UK: uk_size,
        SizeType.HEIGHT_CATEGORY: height_category,
    }

def get_intl_size(ru_size: int) -> str:
    """
    Определяет международный размер на основе российского размера.

    Args:
        ru_size: Российский размер.

    Returns:
        Международный размер (строка).
    """
    if ru_size <= SIZE_LIMITS["XS"]:
        return "XS"
    elif ru_size <= SIZE_LIMITS["S"]:
        return "S"
    elif ru_size <= SIZE_LIMITS["M"]:
        return "M"
    elif ru_size <= SIZE_LIMITS["L"]:
        return "L"
    elif ru_size <= SIZE_LIMITS["XL"]:
        return "XL"
    else:
        return "XXL"


def get_height_category(height: int) -> str:
    """
    Определяет категорию роста на основе роста человека.

    Args:
        height: Рост человека (в см).

    Returns:
        Категория роста (строка).
    """
    sorted_heights = sorted(HEIGHT_CATEGORIES.keys())
    
    if height < sorted_heights[0]:
        return HEIGHT_CATEGORIES[sorted_heights[0]]
    for i in range(len(sorted_heights) - 1):
        if sorted_heights[i] <= height < sorted_heights[i+1]:
           return "Regular"
    return HEIGHT_CATEGORIES[sorted_heights[-1]]

def display_sizes(sizes: dict, console:Console):
    """
    Выводит размеры в удобной форме.

    Args:
         sizes: Словарь с размерами, где ключи типа SizeType.
         console: Rich Console для вывода.
    """
    console.print("\n[bold blue]✨ Ваши размеры:[/bold blue]")
    for key, value in sizes.items():
         console.print(f"[green]{key.value}:[/green] [cyan]{value}[/cyan]")

def load_user_data_from_json(filename: str, console: Console) -> dict | None:
    """
    Загружает данные пользователя из JSON файла.

    Args:
        filename: Имя файла.
        console: Rich Console для вывода.

    Returns:
        Словарь с параметрами пользователя или None при ошибке.
    """
    file_path = Path(filename)

    if not file_path.exists():
        console.print(f"[bold red]❌ Ошибка:[/bold red] Файл {filename} не найден. Убедитесь, что файл существует.")
        logging.error(f"Файл {filename} не найден. Убедитесь, что файл существует.")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            # Проверка наличия всех нужных полей
            if not all(key in data for key in ["chest", "waist", "hips", "height"]):
                console.print("[bold red]❌ Ошибка:[/bold red] В файле отсутствуют обязательные поля (chest, waist, hips, height).")
                logging.error("Ошибка: В файле отсутствуют обязательные поля (chest, waist, hips, height).")
                return None

            # Проверка, что все значения являются числами
            if not all(isinstance(value, (int, float)) for value in data.values()):
                console.print("[bold red]❌ Ошибка:[/bold red] Значения в файле должны быть целыми числами. Пожалуйста, проверьте данные.")
                logging.error("Ошибка: Значения в файле должны быть целыми числами. Пожалуйста, проверьте данные.")
                return None
            
            #Дополнительная валидация
            if not validate_user_data(data, console):
                return None

            return data
    except json.JSONDecodeError:
        console.print(f"[bold red]❌ Ошибка:[/bold red] Ошибка чтения файла {filename}. Проверьте его содержимое или формат JSON.")
        logging.error(f"Ошибка чтения файла {filename}. Проверьте его содержимое или формат JSON.")
        return None
    except Exception as e:
      console.print(f"[bold red]❌ Ошибка:[/bold red] Произошла ошибка при чтении файла {filename}: {e}")
      logging.error(f"Произошла ошибка при чтении файла {filename}: {e}")
      return None
    
def validate_user_data(data:dict, console:Console) -> bool:
    """
    Дополнительная валидация данных пользователя
    Args:
        data: Словарь с данными пользователя
        console: Rich Console для вывода.
    Returns:
         True если валидация успешна, иначе False
    """
    try:
        if not (0 < data["chest"] < 250 and 0 < data["waist"] < 200 and 0 < data["hips"] < 250 and 50 < data["height"] < 250):
             console.print("[bold red]❌ Ошибка:[/bold red] Данные пользователя выходят за разумные пределы.")
             logging.error("Ошибка: Данные пользователя выходят за разумные пределы.")
             return False
    except (TypeError, KeyError) as e:
        console.print(f"[bold red]❌ Ошибка валидации данных:[/bold red] {e}")
        logging.error(f"Ошибка валидации данных: {e}")
        return False
    return True

def main():
    if rich_installed:
        console = Console()
        console.print("[bold magenta]✨ Добро пожаловать в калькулятор размеров 👋[/bold magenta]")
    else:
        console = None
        print("Добро пожаловать в калькулятор размеров 👋\n")
    
    # Загружаем данные из файла
    if console:
        user_data = load_user_data_from_json("user_data.json", console)
    else:
       user_data = load_user_data_from_json("user_data.json", None)
    
    if not user_data:
        if console:
           user_data = input_user_data(console) #Запрашиваем данные пользователя, если не удалось загрузить из файла
        else:
            user_data = input_user_data(None)

    
    if user_data:
        if console:
            table = Table(title="[bold green]✅ Данные успешно загружены[/bold green]")
            table.add_column("Параметр", style="cyan")
            table.add_column("Значение", style="magenta")
            for key, value in user_data.items():
                table.add_row(key, f"{value} см")
            console.print(table)
            logging.info("Данные успешно загружены.")
        else:
            print("Данные успешно загружены:")
            for key, value in user_data.items():
                print(f"{key}: {value} см")


        # Расчет размеров
        try:
            with Progress(transient=True) as progress:
                 task_id = progress.add_task("[bold blue]🔄 Расчет размеров...[/bold blue]", total=1)
                 sizes = calculate_sizes(
                    chest=int(user_data["chest"]),
                    waist=int(user_data["waist"]),
                    hips=int(user_data["hips"]),
                    height=int(user_data["height"]),
                    )
                 progress.update(task_id, advance=1)

            # Вывод результатов
            if console:
                display_sizes(sizes, console)
            else:
                display_sizes(sizes)
            
            # Опциональное сохранение в файл
            if console and input("\nСохранить результаты в файл? (y/n): ").lower() == "y":
                 save_sizes_to_json(sizes, "sizes_report.json", console)
            elif not console and input("\nСохранить результаты в файл? (y/n): ").lower() == "y":
                 save_sizes_to_json(sizes, "sizes_report.json", None)
            else:
                 if console:
                    console.print("\n[bold blue]📝 Результаты не сохранены.[/bold blue]")
                 else:
                    print("\nРезультаты не сохранены.")
        except ValueError as ve:
            if console:
               console.print(f"[bold red]❌ Ошибка валидации данных:[/bold red] {ve}")
            else:
                print(f"Ошибка валидации данных: {ve}")
            logging.error(f"Ошибка валидации данных: {ve}")
        except Exception as e:
             if console:
                console.print(f"[bold red]❌ Произошла ошибка при расчёте размеров:[/bold red] {e}")
             else:
                 print(f"Произошла ошибка при расчёте размеров: {e}")
             logging.error(f"Произошла ошибка при расчёте размеров: {e}")
    else:
       if console:
           console.print("[bold red]❌ Не удалось загрузить данные пользователя. Завершение программы.[/bold red]")
       else:
           print("Не удалось загрузить данные пользователя. Завершение программы.")


def save_sizes_to_json(sizes: dict, filename: str, console: Console):
    """
    Сохраняет размеры в JSON файл.

    Args:
        sizes: Словарь с размерами, где ключи типа SizeType.
        filename: Имя файла.
        console: Rich Console для вывода.
    """
    file_path = Path(filename)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            # Преобразуем ключи Enum в строки для сохранения в JSON
            sizes_to_save = {key.value: value for key, value in sizes.items()}
            json.dump(sizes_to_save, f, ensure_ascii=False, indent=4)
        if console:
             console.print(f"[bold green]✅ Результаты сохранены в файл {filename}[/bold green]")
        else:
             print(f"Результаты сохранены в файл {filename}")
        logging.info(f"Результаты сохранены в файл {filename}")
    except Exception as e:
        if console:
           console.print(f"[bold red]❌ Ошибка при сохранении в файл {filename}:[/bold red] {e}")
        else:
            print(f"Ошибка при сохранении в файл {filename}: {e}")
        logging.error(f"Ошибка при сохранении в файл {filename}: {e}")

def input_user_data(console: Console) -> dict:
    """
    Запрашивает данные пользователя с клавиатуры.
    Args:
         console: Rich Console для вывода.
    Returns:
        Словарь с данными пользователя.
    """
    if console:
        console.print("Пожалуйста, введите ваши данные:")
    else:
         print("Пожалуйста, введите ваши данные:")
    while True:
        try:
           if console:
              chest = int(console.input("[cyan]Обхват груди (см):[/cyan] "))
              waist = int(console.input("[cyan]Обхват талии (см):[/cyan] "))
              hips = int(console.input("[cyan]Обхват бедер (см):[/cyan] "))
              height = int(console.input("[cyan]Рост (см):[/cyan] "))
           else:
              chest = int(input("Обхват груди (см): "))
              waist = int(input("Обхват талии (см): "))
              hips = int(input("Обхват бедер (см): "))
              height = int(input("Рост (см): "))

           data = {
            "chest": chest,
            "waist": waist,
            "hips": hips,
            "height": height
            }
           if validate_user_data(data, console):
              return data
           else:
                if console:
                  console.print("[bold red]❌ Пожалуйста, проверьте введенные данные и попробуйте еще раз.[/bold red]")
                else:
                    print("Пожалуйста, проверьте введенные данные и попробуйте еще раз.")
        except ValueError:
           if console:
              console.print("[bold red]❌ Ошибка: Пожалуйста, введите целые числа.[/bold red]")
           else:
                print("Ошибка: Пожалуйста, введите целые числа.")
        except Exception as e:
           logging.error(f"Произошла ошибка ввода данных: {e}")
           if console:
               console.print(f"[bold red]❌ Произошла ошибка ввода данных:[/bold red] {e}")
           else:
               print(f"Произошла ошибка ввода данных: {e}")

if __name__ == "__main__":
    main()
