from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text="📝 Підписатись ", callback_data="subscribe"),
    InlineKeyboardButton(text="🖼 Відписатись", callback_data="unsubscribe")],
    [InlineKeyboardButton(text="🔎 Допомога", callback_data="help")]          # функціонал не реалізований.
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Вийти у меню")]], resize_keyboard=True)