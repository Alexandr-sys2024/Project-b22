import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp

from config import TOKEN, POLYGON_API_KEY  # Импортируем необходимые переменные

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Определение состояний для FSM
class CompanyForm(StatesGroup):
    waiting_for_company_name = State()

# Функция для получения данных с API Polygon
async def fetch_stock_data(ticker, start_date, end_date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?apiKey={POLYGON_API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if 'results' in data:
                    return data['results']
                else:
                    return "Нет данных по указанному тикеру."
            else:
                return f"Ошибка API: {response.status}"

# Обработчик команды /start
@dp.message(Command(commands=['start']))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.reply("Привет! Введите название компании для получения данных:")
    await state.set_state(CompanyForm.waiting_for_company_name)

# Обработчик текстового сообщения, который срабатывает, когда бот ждёт название компании
@dp.message(StateFilter(CompanyForm.waiting_for_company_name))
async def process_company_name(message: types.Message, state: FSMContext):
    company_name = message.text.strip()
    if company_name:
        await message.reply(f"Вы ввели название компании: {company_name}. Получаем данные...")

        # Пример вызова функции для получения данных
        data = await fetch_stock_data(company_name, "2024-12-01", "2024-12-12")

        # Формирование ответа с данными
        if isinstance(data, list):
            response_message = f"Данные по {company_name}:\n"
            for entry in data:
                response_message += f"Дата: {entry['t']}, Открытие: {entry['o']}, Закрытие: {entry['c']}, Объем: {entry['v']}\n"
            await message.reply(response_message)
        else:
            await message.reply(data)  # Если возникла ошибка или нет данных
    else:
        await message.reply("Пожалуйста, введите название компании.")

    # Заканчиваем состояние
    await state.clear()



async def main() -> None:

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == '__main__':
        import asyncio

        asyncio.run(main())