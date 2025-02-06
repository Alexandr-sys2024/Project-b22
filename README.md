# Project-b22

## 📌 Описание проекта

**Project-b22** – это инструмент для анализа фондового рынка, который позволяет пользователям получать данные о компаниях и визуализировать историческую информацию об акциях.

Основные цели проекта:
- Предоставление актуальных данных о капитализации и рыночных показателях.
- Анализ торгов за предыдущие дни.
- Визуализация исторических данных для удобного анализа тенденций.
- Улучшенная обработка ошибок и информативные сообщения.
- Гибкая настройка диапазона дат для исторических данных.
- Расширенные графики с дополнительными аналитическими возможностями.

## 🚀 Функционал

- 🔎 **Получение информации о компании** по тикеру (названию акций на бирже).
- 📊 **Данные о вчерашних торгах** (открытие, максимум, минимум, закрытие).
- 📈 **Графики исторических данных** с возможностью выбора диапазона дат.
- 📉 **Анализ трендов** с использованием скользящих средних и других индикаторов.

## 🛠 Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone <repo-url>
   cd Project-b22
   
## Создайте виртуальное окружение и установите зависимости
   ```bash
python -m venv venv
source venv/bin/activate  # Для macOS/Linux
venv\Scripts\activate     # Для Windows
pip install -r requirements.txt

##  Структура проекта

Project-b22/
├── capitalization.py     # Скрипт для работы с капитализацией
├── config.py             # Конфигурационный файл с API-ключами
├── historical_chart.py   # Визуализация исторических данных
├── polygon_utils.py      # Взаимодействие с API Polygon.io
├── requirements.txt      # Список зависимостей
├── yeasterday_trades.py  # Данные о вчерашних торгах
└── historical_data/      # Папка с историческими данными

## 📌 Использование

## Запустите приложение
   ```bash
python main.py

## Выберите тикер акции для анализа .
1. Используйте интерфейс для выполнения следующих действий :
2. Получение информации о компании.
3. Просмотр данных о вчерашних торгах.
4. Построение графиков для анализа исторических данных.
5. Выбор кастомного диапазона дат.
6. Анализ трендов с использованием индикаторов.
🔑 API и конфигурация
Для работы с Polygon.io API требуется API-ключ.
Добавьте свой API-ключ в config.py:
API_KEY = "your_polygon_api_key"

## 📚 Полезные ресурсы
Документация Polygon.io
Документация Python
Документация Matplotlib (визуализация)
Основы анализа данных в Pandas
👨‍💻 Автор
[Александр] – [Контактная информация]

📜 Лицензия
Этот проект распространяется под лицензией MIT License .