from aiogram.types import ReplyKeyboardMarkup

bot_main_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
bot_main_buttons.row("Foydalanuvchilar soni")
bot_main_buttons.row("✅ Oddiy post yuborish")
bot_main_buttons.row("🎞 Mediagroup post yuborish")
bot_main_buttons.row("🏡 Bosh sahifa")
