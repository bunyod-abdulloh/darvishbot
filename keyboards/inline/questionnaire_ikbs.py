from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def symptom_keyboard(symptom_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    
    kb.add(
        InlineKeyboardButton("Ҳа", callback_data=f"symptom:{symptom_id}:yes"),
        InlineKeyboardButton("Йўқ", callback_data=f"symptom:{symptom_id}:no")
    )
    if symptom_id > 1:
        kb.add(InlineKeyboardButton("Орқага", callback_data=f"back:{symptom_id - 1}"))
    return kb
