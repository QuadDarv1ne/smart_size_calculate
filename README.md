# smart_size_calculate

**Smart Size Calculate** – это умный калькулятор размеров одежды, который помогает рассчитать `российские`, `международные`, `европейские`, `американские` и `британские` размеры на основе параметров тела.

![dupley_maxim_igorevich](img/DupleyMI.jpg)

### 🔧 Функционал

**Поддержка расчета основных типов размеров:**
1. `Российских (РФ)`
2. `Международных (XS, S, M, L, XL, XXL)`
3. `Европейских (EU)`
4. `Американских (US)`
5. `Британских (UK)`

**Учет ростовых категорий:**
1. `Petite (для низкого роста)`
2. `Regular (средний рост)`
3. `Tall (для высокого роста)`

Загрузка данных из JSON-файла.

Сохранение результатов в JSON-отчёт.

Полная обработка ошибок для гладкой работы.

### 📚 Как использовать

#### 🔧 1. Установка

**Клонируйте репозиторий:**
```bash
git clone https://github.com/your-username/smart_size_calculate.git
```

**Перейдите в папку проекта:**
```bash
cd smart_size_calculate
```
Убедитесь, что у вас установлен `Python 3.7+`

#### 🔄 2. Подготовка данных

Создайте JSON-файл с параметрами пользователя.

**Пример структуры файла:**
```json
{
    "chest": 92,
    "waist": 74,
    "hips": 98,
    "height": 175
}
```
Сохраните файл с именем user_data.json в корневую папку проекта.

#### ⚙️ 3. Запуск программы

**Запустите приложение:**
```bash
python smart_size_calculate.py
```
Программа автоматически загрузит данные из файла `user_data.json`, рассчитает размеры и сохранит результаты в файл `sizes_report.json`

### 📊 Пример результата

**После выполнения программа выведет что-то подобное:**

```
Добро пожаловать в калькулятор размеров.
Данные успешно загружены:
chest: 92 см
waist: 74 см
hips: 98 см
height: 175 см

Ваши размеры:
RU: 44
International: M
EU: 50
US: 10
UK: 10
Height Category: Regular

Результаты сохранены в файл sizes_report.json.
```

---

### 🚀 Будущие улучшения

1. Добавление расчёта детских размеров.
2. Визуализация данных через веб-интерфейс (`Flask/Django`)
3. Интеграция с базами данных клиентов.
4. Локализация программы на разные языки.

---

### 📄 Лицензия ✅

[Этот проект лицензирован под лицензией MIT](LICENCE)

Для получения дополнительной информации ознакомьтесь с файлом `LICENSE`

---

💼 **Автор:** Дуплей Максим Игоревич

📲 **Telegram:** @quadd4rv1n7

📅 **Дата:** 27.01.2025

▶️ **Версия 1.0**

```
※ Предложения по сотрудничеству можете присылать на почту ※
📧 maksimqwe42@mail.ru
```
