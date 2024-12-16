import logging
import pandas as pd
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile  # Импортируем FSInputFile для работы с локальными файлами
from aiogram.filters import Command
from polygon import RESTClient
from config import TOKEN, POLYGON_API_KEY

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и клиента Polygon
bot = Bot(token=TOKEN)
dp = Dispatcher()
client = RESTClient(api_key=POLYGON_API_KEY)

@dp.message(Command(commands=["chart"]))
async def get_historical_chart(message: Message):
    await message.reply("Введите тикер компании (например, AAPL):")

    @dp.message(lambda msg: True)
    async def fetch_chart(msg: Message):
        ticker = msg.text.strip().upper()  # Приводим тикер к верхнему регистру
        try:
            # Запрос исторических данных
            aggs = client.list_aggs(
                ticker=ticker,
                multiplier=1,
                timespan="day",
                from_="2024-01-01",
                to="2024-12-12"
            )

            # Создание DataFrame
            data = pd.DataFrame([{
                "date": pd.to_datetime(agg.timestamp, unit='ms'),
                "close": agg.close
            } for agg in aggs])

            # Построение графика
            plt.figure(figsize=(10, 5))
            plt.plot(data["date"], data["close"], label=f"{ticker} (Закрытие)")
            plt.title(f"Исторические данные {ticker}")
            plt.xlabel("Дата")
            plt.ylabel("Цена закрытия")
            plt.legend()
            plt.grid()

            # Сохранение графика
            chart_path = f"{ticker}_chart.png"
            plt.savefig(chart_path)
            plt.close()

            # Отправка графика пользователю
            photo = FSInputFile(chart_path)  # Используем FSInputFile для отправки локального файла
            await msg.reply_photo(photo=photo)
        except Exception as e:
            await msg.reply(f"Ошибка при запросе данных: {e}")

# Главная функция
import asyncio

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())