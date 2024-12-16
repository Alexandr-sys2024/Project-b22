import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from polygon import RESTClient
from config import TOKEN, POLYGON_API_KEY

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и клиента Polygon
bot = Bot(token=TOKEN)
dp = Dispatcher()
client = RESTClient(api_key=POLYGON_API_KEY)

@dp.message(Command(commands=["yesterday"]))
async def get_yesterday_trades(message: Message):
    await message.reply("Введите тикер компании (например, AAPL):")

    @dp.message(lambda msg: True)
    async def fetch_trades(msg: Message):
        ticker = msg.text.strip()
        try:
            # Запрос данных о вчерашних торгах
            aggs = client.get_previous_close_agg(ticker)

            for agg in aggs:
                response_message = (
                    f"Информация о вчерашних торгах для {agg.ticker}:\n\n"
                    f"Закрытие: ${agg.close:,.2f}\n"
                    f"Максимум: ${agg.high:,.2f}\n"
                    f"Минимум: ${agg.low:,.2f}\n"
                    f"Открытие: ${agg.open:,.2f}\n"
                    f"Объем: {agg.volume:,}\n"
                )
                await msg.reply(response_message)
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