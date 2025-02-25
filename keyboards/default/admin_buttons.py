from aiogram.types import ReplyKeyboardMarkup

admin_main_btns = ReplyKeyboardMarkup(resize_keyboard=True)
admin_main_btns.row("Foydalanuvchilar soni")
admin_main_btns.row("Yaxin tozalash", "Leo tozalash")
admin_main_btns.row("Ayzenk tozalash")
admin_main_btns.row("✅ Oddiy post yuborish")
admin_main_btns.row("🎞 Mediagroup post yuborish")
admin_main_btns.row("🏡 Bosh sahifa")
