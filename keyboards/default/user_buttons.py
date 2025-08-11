from aiogram.types import ReplyKeyboardMarkup

main_dkb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_dkb.row("🧑‍💻 Тестлар | Сўровномалар")
main_dkb.row("🎙 Суҳбат ва лойиҳалар", "📝 Мақолалар")

tests_main_dkb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
tests_main_dkb.row("Яхин Менделевич сўровномаси", "Айзенк | Темперамент аниқлаш")
tests_main_dkb.row("Леонгард сўровномаси", "Саволнома")
tests_main_dkb.row("✍️ Консультацияга ёзилиш")
tests_main_dkb.row("🏡 Бош саҳифа")

interviews_cbuttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
interviews_cbuttons.row("🎙 Суҳбат ва лойиҳалар")
interviews_cbuttons.row("🏡 Бош саҳифа")
