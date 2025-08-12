from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def check_patient_datas_ikbs(patient_telegram):
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(
            text="❌ Рад қилиш", callback_data=f"admin_cancel:{patient_telegram}"
        )
    )
    return btn


def patient_message_ikbs(telegram_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            text="Хабар юбориш", callback_data=f"admin_message:{telegram_id}"
        )
    )
    return kb


def are_you_sure_markup():
    inline_keyboard = [[
        InlineKeyboardButton(text="❌ No", callback_data='no'),
        InlineKeyboardButton(text="✅ Yes", callback_data='yes')
    ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard
