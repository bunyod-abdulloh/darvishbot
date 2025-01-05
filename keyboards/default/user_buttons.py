from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_dkb = ReplyKeyboardMarkup(
    keyboard=
    [
        [
            KeyboardButton(text="🧑‍💻 Testlar | So'rovnomalar")
        ],
        [
            KeyboardButton(text="🎙 Suhbat va loyihalar"),
            KeyboardButton(text="📝 Maqolalar")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

tests_main_dkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yaxin Mendelevich so'rovnomasi"),
            KeyboardButton(text="Ayzenk | Temperament aniqlash")
        ],
        [
            KeyboardButton(text="Leongard so'rovnomasi")
        ],
        [
            KeyboardButton(text="🏡 Bosh sahifa")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

interviews_cbuttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎙 Suhbat va loyihalar")
        ],
        [
            KeyboardButton(text="🏡 Bosh sahifa")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
