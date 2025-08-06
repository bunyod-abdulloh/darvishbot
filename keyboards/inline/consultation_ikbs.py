from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_free_time_keyboard(start_str: str, end_str: str, busy_times: list[str]) -> InlineKeyboardMarkup:
    start = datetime.strptime(start_str, "%H:%M")
    end = datetime.strptime(end_str, "%H:%M")

    busy_set = set(busy_times)

    keyboard = InlineKeyboardMarkup(row_width=3)

    current = start
    while current < end:
        time_str = current.strftime("%H:%M")
        if time_str not in busy_set:
            keyboard.insert(
                InlineKeyboardButton(
                    text=time_str,
                    callback_data=f"select_time-{time_str}"
                )
            )
        current += timedelta(minutes=30)
    keyboard.add(
        InlineKeyboardButton(
            text="⬅️ Ортга", callback_data="consultation_back:3"
        )
    )
    return keyboard


def sign_up_to_consultation():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(InlineKeyboardButton(
        text="✍️ Консультацияга ёзилиш", callback_data=f"heaved_on_consultation"))
    return btn


def select_gender_btn():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.row(
        InlineKeyboardButton(text="👱‍♂️ Эркак", callback_data="test_male"),
        InlineKeyboardButton(text="👩‍🦰 Аёл", callback_data="test_female")
    )
    return btn


def confirm_reenter_ibtn():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.row(
        InlineKeyboardButton(
            text="1", callback_data="edit_fullname"
        ),
        InlineKeyboardButton(
            text="2", callback_data="edit_gender"
        ),
        InlineKeyboardButton(
            text="3", callback_data="edit_age"
        ),
        InlineKeyboardButton(
            text="4", callback_data="edit_marital_status"
        )
    )
    btn.row(
        InlineKeyboardButton(
            text="5", callback_data="edit_absence_children"
        ),
        InlineKeyboardButton(
            text="6", callback_data="edit_work"
        ),
        InlineKeyboardButton(
            text="7", callback_data="edit_eeg"
        ),
        InlineKeyboardButton(
            text="8", callback_data="edit_phone"
        )
    )
    btn.row(
        InlineKeyboardButton(
            text="❌ Бекор қилиш", callback_data="cancel_consultation"
        ),
        InlineKeyboardButton(
            text="✅ Тасдиқлаш", callback_data="confirm"
        )
    )
    return btn


def marital_status_ikb():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton(
            text="💍 Турмуш қурган", callback_data="married"
        )
    )
    btn.add(
        InlineKeyboardButton(
            text="💐 Турмуш қурмаган", callback_data="unmarried"
        )
    )
    return btn


def absence_children_ikb():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.row(
        InlineKeyboardButton(
            text="👶 Бор", callback_data="has_child_yes"
        ),
        InlineKeyboardButton(
            text="🚫👶 Йўқ", callback_data="has_child_no"
        )
    )
    return btn


def consultation_duration__ikb():
    btn = InlineKeyboardMarkup(row_width=2)
    durations = ['10', '20', '30']

    for duration in durations:
        btn.insert(
            InlineKeyboardButton(
                text=f"⏱️ {duration} дақиқа", callback_data=f"duration_{duration}"
            )
        )
    btn.add(
        InlineKeyboardButton(
            text="⬅️ Ортга", callback_data="consultation_back:1"
        )
    )
    return btn


def show_consultation_dates_keyboard(dates_by_day: dict[str, dict[str, list[str]]]) -> InlineKeyboardMarkup:
    all_dates = []

    # Barcha sanalarni yig‘ish va datetime formatga aylantirib saqlash

    for key, value in dates_by_day.items():
        for date_str in value['dates']:
            all_dates.append((key, date_str, value['time'], datetime.strptime(date_str, "%d-%m-%Y")))

    # Sana bo‘yicha sortlash
    all_dates.sort(key=lambda x: x[3])

    # Inline tugmalar yaratish
    keyboard = InlineKeyboardMarkup(row_width=2)

    for key, date_str, time, _ in all_dates:
        keyboard.insert(
            InlineKeyboardButton(
                text=date_str,
                callback_data=f"date_{key}_{date_str}_{time}"
            )
        )
    keyboard.add(
        InlineKeyboardButton(
            text="⬅️ Ортга", callback_data="consultation_back:2"
        )
    )
    return keyboard
