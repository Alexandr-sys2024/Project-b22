import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from polygon import RESTClient

from config import TOKEN, POLYGON_API_KEY

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Инициализация клиента Polygon
client = RESTClient(api_key=POLYGON_API_KEY)

# Обработчик команды /start
@dp.message(Command(commands=['start']))
async def cmd_start(message: types.Message):
    logging.info(f"Получена команда /start от {message.from_user.id}")
    await message.reply("Привет! Я бот, который предоставляет информацию о компаниях. Используйте /company, чтобы узнать данные по тикеру компании.")

#@dp.message()
#async def handle_unknown_command(message: types.Message):
#    await message.reply("Неизвестная команда. Используйте /start или /company.")


# Обработчик команды /company
@dp.message(Command(commands=['company']))
async def get_company_details(message: Message):
    await message.reply("Введите тикер компании (например, AAPL):")

    @dp.message(lambda msg: True)
    async def fetch_details(msg: Message):
        ticker = msg.text.strip()
        try:
            # Запрос к Polygon API
            details = client.get_ticker_details(ticker)

            # Форматируем адрес
            address = ", ".join(filter(None, [
                details.address.address1,
                details.address.city,
                details.address.state,
                details.address.postal_code
            ]))

            # Формируем ответ
            response_message = (
                f"Информация о компании {details.name} ({details.ticker}):\n\n"
                f"Адрес: {address}\n"
                f"Рыночная капитализация: ${details.market_cap:,.2f}\n"
                f"Биржа: {details.primary_exchange}\n"
                f"Тип актива: {details.type}\n"
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