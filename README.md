# 🎮 Game Store - Система покупки цифрових ігор

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![CI/CD](https://github.com/YOUR_USERNAME/game-store-lab6/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/game-store-lab6/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/tests-48%20passed-brightgreen.svg)]()
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Опис проекту

**Game Store** - це система для купівлі та продажу цифрових ігор, реалізована з використанням архітектури **Controller-Service-Repository** та принципів **SOLID**.

### Реалізовані бізнес-сценарії

| № | Сценарій | Опис |
|---|----------|------|
| 1 | Покупка гри | Користувач купує гру, якщо вона доступна та є достатньо коштів |
| 2 | Повернення гри | Повернення гри протягом 14 днів з поверненням коштів |
| 3 | Пошук ігор | Пошук за назвою, жанром або ціновим діапазоном |
| 4 | Реєстрація | Створення акаунту з бонусом 100 грн |

---

## 📁 Структура проекту
game_store/
├── .github/workflows/
│ └── ci.yml # CI/CD pipeline (GitHub Actions)
├── src/
│ ├── controllers/ # Контролери (CLI)
│ ├── services/ # Бізнес-логіка
│ ├── repositories/ # Робота з даними
│ ├── models/ # Моделі даних
│ └── dto/ # Об'єкти передачі даних
├── tests/ # Юніт-тести (48 тестів)
├── Dockerfile # Docker образ для додатку
├── Dockerfile.test # Docker образ для тестів
├── docker-compose.yaml # Багатоконтейнерний запуск
├── requirements.txt # Залежності Python
├── run.py # Точка входу
└── README.md # Документація

---

## 🐳 Запуск через Docker (рекомендований)

### Передумови
- Встановлений Docker та Docker Compose

### Крок 1: Клонування репозиторію

```bash
git clone https://github.com/fffwx/game-store-lab6.git
cd game-store-lab6
Крок 2: Побудова Docker образів
bash
# Побудова образу для додатку
docker build -f Dockerfile -t game-store-app .

# Побудова образу для тестів
docker build -f Dockerfile.test -t game-store-test .
Крок 3: Запуск тестів в Docker
bash
# Запуск тестів
docker run --rm game-store-test
Крок 4: Запуск додатку в Docker
bash
# Інтерактивний режим
docker run -it --rm game-store-app
Крок 5: Запуск через Docker Compose
bash
# Запуск всіх сервісів
docker-compose up

# Запуск тільки тестів
docker-compose run tests
🖥️ Локальний запуск (без Docker)
Вимоги
Python 3.8 або вище

Встановлений pip

Крок 1: Створення віртуального середовища
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Крок 2: Встановлення залежностей
bash
pip install -r requirements.txt
Крок 3: Запуск програми
bash
python run.py
🧪 Інструкції для запуску тестів
Крок 1: Встановлення залежностей
bash
pip install pytest
Крок 2: Запуск всіх тестів
bash
# Через unittest (стандартний)
python -m unittest discover tests -v

# Через pytest
pytest tests/ -v
Крок 3: Запуск окремих тестів
bash
# Тести сервісу (21 тест)
python tests/test_game_store_service.py -v

# Тести репозиторіїв (27 тестів)
python tests/test_repositories.py -v

# Запуск конкретного тесту
python -m unittest tests.test_game_store_service.TestGameStoreService.test_01_purchase_game_success
Крок 4: Запуск з деталізацією
bash
# З детальним виводом
python -m unittest discover tests -v --buffer

# Зберегти результати у файл
python -m unittest discover tests -v > test_results.txt
 Приклад виводу тестів
bash
$ python -m unittest discover tests -v

test_01_purchase_game_success ... ok
test_02_purchase_game_insufficient_funds ... ok
test_03_purchase_game_already_owned ... ok
test_04_purchase_game_nonexistent_user ... ok
test_05_purchase_game_nonexistent_game ... ok
test_06_purchase_unavailable_game ... ok
test_07_return_game_success ... ok
test_08_return_game_not_purchased ... ok
test_09_return_game_expired ... ok
test_10_return_game_wrong_user ... ok
test_11_search_by_title_success ... ok
test_12_search_by_genre_success ... ok
test_13_search_by_price_range ... ok
test_14_search_not_found ... ok
test_15_register_user_success ... ok
test_16_register_user_duplicate_username ... ok
test_17_register_user_duplicate_email ... ok
test_18_register_user_weak_password ... ok
test_19_add_funds_success ... ok
test_20_add_funds_negative_amount ... ok
test_21_get_top_games ... ok

test_add_game ... ok
test_auto_increment_id ... ok
test_clear_repository ... ok
test_delete_game_soft ... ok
test_find_all_available ... ok
test_find_by_genre ... ok
test_find_by_id ... ok
test_find_by_price_range ... ok
test_find_by_title ... ok
test_update_game ... ok
test_add_purchase ... ok
test_clear_repository ... ok
test_days_since_purchase ... ok
test_find_by_game ... ok
test_find_by_id ... ok
test_find_by_user ... ok
test_find_user_game_purchase ... ok
test_update_purchase ... ok
test_add_user ... ok
test_clear_repository ... ok
test_email_exists ... ok
test_find_all_only_active ... ok
test_find_by_email ... ok
test_find_by_id ... ok
test_find_by_username ... ok
test_update_user ... ok
test_username_exists ... ok

----------------------------------------------------------------------
Ran 48 tests in 0.089s

OK ✅
📊 Результати тестування
Компонент	Кількість тестів	Статус
GameStoreService	21	✅ Всі пройдено
GameRepository	10	✅ Всі пройдено
UserRepository	9	✅ Всі пройдено
PurchaseRepository	8	✅ Всі пройдено
ВСЬОГО	48	✅ 100% пройдено
🏗️ Пояснення логіки тестів
Позитивні сценарії (що має працювати)
purchase_game_success - перевіряє, що користувач з достатнім балансом може купити гру

return_game_success - перевіряє повернення гри протягом 14 днів

search_by_title_success - перевіряє пошук гри за назвою

register_user_success - перевіряє реєстрацію нового користувача

Негативні сценарії (що має ВИДАВАТИ ПОМИЛКУ)
purchase_game_insufficient_funds - недостатньо коштів → помилка

purchase_game_already_owned - гра вже куплена → помилка

return_game_not_purchased - повернення некупленої гри → помилка

return_game_expired - повернення після 14 днів → помилка

register_user_duplicate_username - дублікат username → помилка

register_user_weak_password - короткий пароль → помилка

🔧 Змінні середовища
Змінна	Опис	За замовчуванням
ENVIRONMENT	Середовище запуску	development
REGISTRATION_BONUS	Бонус при реєстрації (грн)	100
RETURN_DAYS_LIMIT	Термін повернення (днів)	14
DEBUG	Режим налагодження	True
LOG_LEVEL	Рівень логування	INFO
🔧 Перевірка якості коду (лінтинг)
# Встановлення інструментів
pip install flake8 pylint black isort

# Перевірка стилю коду
flake8 src/ --max-line-length=120 --statistics

# Перевірка якості коду
pylint src/ --fail-under=8

# Автоматичне форматування
black src/ tests/

# Сортування імпортів
isort src/ tests/
🚀 CI/CD Pipeline (GitHub Actions)
Статус конвеєра:
https://github.com/fffwx/game-store-lab6/actions/workflows/ci.yml/badge.svg

Що автоматизується:
Лінтинг - перевірка стилю коду (flake8, black, isort)

Тестування - запуск 48 юніт-тестів

Docker build - збірка Docker образу

Docker test - тестування контейнера

Перегляд статусу:
Перейдіть на вкладку Actions у вашому GitHub репозиторії.

📝 Приклад використання програми
$ python run.py

🎮 Ласкаво просимо до Game Store!

============================================================
🎮 GAME STORE - Магазин цифрових ігор 🎮
============================================================
1. 🛒 Покупка гри
2. ↩️  Повернення гри
3. 🔍 Пошук ігор
4. 👤 Реєстрація нового користувача
5. 📋 Список всіх ігор
6. 👤 Інформація про користувача
7. 💰 Поповнити баланс
8. 🏆 Топ ігор за рейтингом
0. 🚪 Вихід
============================================================

Виберіть опцію: 5

📋 ДОСТУПНІ ІГРИ:
============================================================
🎮 ID: 1 | Cyberpunk 2077
   Жанр: rpg | Ціна: 299.99₴ | ⭐ 4.5
--------------------------------------------------
🎮 ID: 2 | The Witcher 3
   Жанр: rpg | Ціна: 199.99₴ | ⭐ 4.9
--------------------------------------------------
🎮 ID: 3 | Stardew Valley
   Жанр: simulation | Ціна: 79.99₴ | ⭐ 4.8
--------------------------------------------------
