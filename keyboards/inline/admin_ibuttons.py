from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def check_patient_datas_ikbs(patient_id):
    btn = InlineKeyboardMarkup()
    btn.add(
        InlineKeyboardButton(
            text="Рад қилиш", callback_data=f"admin_cancel:{patient_id}"
        ),
        InlineKeyboardButton(
            text="Тасдиқлаш", callback_data=f"admin_check:{patient_id}"
        )
    )
    return btn
