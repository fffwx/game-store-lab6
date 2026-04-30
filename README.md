# 🎮 Game Store - Система покупки цифрових ігор

## 📋 Опис проекту

**Game Store** - це система для купівлі та продажу цифрових ігор, реалізована з використанням архітектури **Controller-Service-Repository** та принципів **SOLID**.

### Реалізовані бізнес-сценарії

| № | Сценарій | Опис |
|---|----------|------|
| 1 | Покупка гри | Користувач купує гру, якщо вона доступна та є достатньо коштів |
| 2 | Повернення гри | Повернення гри протягом 14 днів з поверненням коштів |
| 3 | Пошук ігор | Пошук за назвою, жанром або ціновим діапазоном |
| 4 | Реєстрація | Створення акаунту з бонусом 100 грн |

## 📁 Структура проекту
game_store/
├── src/
│ ├── controllers/ # Контролери (CLI)
│ ├── services/ # Бізнес-логіка
│ ├── repositories/ # Робота з даними
│ ├── models/ # Моделі даних
│ └── dto/ # Об'єкти передачі даних
├── tests/ # Юніт-тести (48 тестів)
├── run.py # Точка входу
└── README.md

text

## 🚀 Запуск програми

```bash
# Перейдіть в папку проекту
cd game_store

# Запустіть програму
python run.py
🧪 Інструкції для запуску тестів
Вимоги
Python 3.8 або вище

Встановлений pip

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
📊 Приклад виводу тестів
text
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
test_find_by_id ... ok
test_find_by_title ... ok
test_find_by_genre ... ok
test_find_by_price_range ... ok
test_find_all_available ... ok
test_update_game ... ok
test_delete_game_soft ... ok
test_clear_repository ... ok
test_auto_increment_id ... ok
test_add_user ... ok
test_find_by_id ... ok
test_find_by_username ... ok
test_find_by_email ... ok
test_username_exists ... ok
test_email_exists ... ok
test_update_user ... ok
test_find_all_only_active ... ok
test_clear_repository ... ok
test_add_purchase ... ok
test_find_by_id ... ok
test_find_by_user ... ok
test_find_by_game ... ok
test_find_user_game_purchase ... ok
test_update_purchase ... ok
test_days_since_purchase ... ok
test_clear_repository ... ok

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

🔧 Перевірка якості коду (лінтинг)
bash
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