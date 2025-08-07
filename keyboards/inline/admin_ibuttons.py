from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def check_patient_datas_ikbs(patient_id):
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(
            text="❌ Рад қилиш", callback_data=f"admin_cancel:{patient_id}"
        )
    )
    return btn


def are_you_sure_markup():
    inline_keyboard = [[
        InlineKeyboardButton(text="❌ No", callback_data='no'),
        InlineKeyboardButton(text="✅ Yes", callback_data='yes')
    ]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard
