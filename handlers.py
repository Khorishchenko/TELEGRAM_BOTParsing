from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogram import flags
from aiogram.fsm.context import FSMContext
# from states import Gen
from aiogram.types.callback_query import CallbackQuery  # Вот этого.

router = Router()

import utils
import kb
import text

import config
import logging
import asyncio
from datetime import datetime
from stopgame import StopGame
from main import db, bot


# Ініціалізуємо парсер
sg = StopGame( 'lastkey.txt' )


@router.message( Command( "start" ) )
@router.message( Command( "menu" ) )
@router.message( F.text == "◀️ Выйти в меню" )
async def menu( msg: Message ):
	asyncio.create_task( scheduled( 10 ) )
	await msg.answer( text.hello )
	await msg.answer( text.greet.format( name=msg.from_user.full_name ), reply_markup=kb.menu )


# Команда активації 
# @dp.message_handler(commands=['subscribe'])
@router.callback_query( F.data == "subscribe" )
async def subscribe( message: types.Message ):
	if( not db.subscriber_exists( message.from_user.id ) ):
		# Якщо користувача немає в основі, додаємо його
		db.add_subscriber( message.from_user.id )
	else:
		# якщо він вже є, то просто оновлюємо йому статус передплати
		db.update_subscription( message.from_user.id, True )
	
	await message.answer( text.subscribe )


# Команда отписки
# @dp.message_handler(commands=['unsubscribe'])
@router.callback_query(F.data == "unsubscribe")
async def unsubscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# Якщо користувача немає в базі, додаємо його з неактивною передплатою (запам'ятовуємо)
		db.add_subscriber(message.from_user.id, False)
		await message.answer(text.subscribeTrue)
	else:
		# якщо він вже є, то просто оновлюємо йому статус передплати
		db.update_subscription(message.from_user.id, False)
		await message.answer(text.unsubscribe)


# # перевіряємо наявність нових ігор та робимо розсилки
print("Bot started working!!!")  # Повідомлення про початок роботи бота

async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        # перевірка наявності нових ігор
        booles = False
        new_games = []

        if booles:
            # scraper  = sg.new_games()
            scraper  = sg.parse_div()
        else:
            new_games = sg.new_games()

        print("Checking for new games...")

        if new_games:
            print("New games found!")
            new_games.reverse()
            for ng in new_games:
                nfo = sg.game_info(ng)

                print(f"Sending info about new game: {nfo['title']}")
                print(nfo)

                subscriptions = db.get_subscriptions()

                # with open(sg.download_image(nfo['image']), 'rb') as photo:
                for s in subscriptions:
                        await bot.send_photo(
                            s[1],
                            nfo['image'],
                            caption = f"<b>{nfo['title']}</b>\n" + "Оценка: " + nfo['score'] + "\n" + f"<i>{nfo['excerpt']}</i>" + "\n\n" + f"<a href='{nfo['link']}'>Посилання</a>",
                            disable_notification = True
                        )
                # sg.update_lastkey(nfo['id'])
                print(f"Info about {nfo['title']} sent successfully!")
        else:
            print("No new games found.")

        if scraper:
            subscribers = db.get_subscriptions()

            for str in scraper:
                # Пройдіться по списку підписників і відправте кожному повідомлення
                for subscriber in subscribers:
                    user_id = subscriber[1]  # Першим елементом у кортежі є user_id
                    await bot.send_message(user_id, str)  # str ваше повідомлення