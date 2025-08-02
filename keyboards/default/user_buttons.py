from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_dkb = ReplyKeyboardMarkup(
    keyboard=
    [
        [
            KeyboardButton(text="🧑‍💻 Тестлар | Сўровномалар")
        ],
        [
            KeyboardButton(text="🎙 Суҳбат ва лойиҳалар"),
            KeyboardButton(text="📝 Мақолалар")
        ],
        [
            KeyboardButton(
                text="✍️ Консультацияга ёзилиш"
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

tests_main_dkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Яхин Менделевич сўровномаси"),
            KeyboardButton(text="Айзенк | Темперамент аниқлаш")
        ],
        [
            KeyboardButton(text="Леонгард сўровномаси")
        ],
        [
            KeyboardButton(text="🏡 Бош саҳифа")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

interviews_cbuttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎙 Суҳбат ва лойиҳалар")
        ],
        [
            KeyboardButton(text="🏡 Бош саҳифа")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


def sign_up_consultation_dkb():
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.add()
