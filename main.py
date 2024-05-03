# Єхо Бот
# logging.basicConfig(level=logging.INFO)
 
# bot = Bot(token=config.API_TOKEN)
# dp = Dispatcher(bot)

# from aiogram import types
# async def echo(message: types.Message):
#     await message.answer(message.text)
# dp.register_message_handler(echo)

# # запускаємо лонг поллінг
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)


import config

from dbSQliter import SQLighter

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware


# Ініціалізуємо бота
bot = Bot(token=config.API_TOKEN, parse_mode=ParseMode.HTML)

# Ініціалізуємо диспетчера з пам'яттю
dp = Dispatcher(storage=MemoryStorage())

# Ініціалізуємо з'єднання з БД
db = SQLighter('db.db')

from handlers import router
from stopgame import StopGame

async def main():
    # Стартуємо бота з роутером
    dp.include_router(router)
    
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    # Налаштовуємо рівень логування
    logging.basicConfig(level=logging.INFO)
    # Створюємо новий цикл asyncio
    loop = asyncio.get_event_loop()
    # Запускаємо основну функцію
    loop.run_until_complete(main())