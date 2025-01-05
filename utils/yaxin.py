# Helper function to handle user data update and state transitions
import asyncio

from aiogram import types

from loader import db


async def calculate_and_send_results(call: types.CallbackQuery):
    scales = {
        "Хавотир мезони": "xavotir",
        "Невротик - депрессия мезони": "nevrotikdep",
        "Астения мезони": "astenik",
        "Истерик тоифадаги жавоб мезони": "isterik",
        "Обсессив-фобик бузилишлар мезони": "obsessivfobik",
        "Вегетатив бузилишлар мезони": "vegetativ",
    }

    # Ma'lumotlarni bir marta yig'ib olish
    result = {
        text: scale_value
        for text, scale_value in zip(
            scales.keys(),
            await asyncio.gather(
                *[
                    db.select_datas_temporary(telegram_id=call.from_user.id, scale_type=scale)
                    for scale in scales.values()
                ]
            ),
        )
    }

    # Ma'lumotlarni birlashtirish
    last_result = "\n".join(f"{text}: {scale}" for text, scale in result.items())

    # Nevrotik holatni aniqlash
    nevrotik_detected = any(number < -1.28 for number in result.values())
    nevrotik_text = "Невротик ҳолат аниқланди!" if nevrotik_detected else "Невротик ҳолат аниқланмади!"

    footer_text = (
        "Мезонлардаги кўрсаткичлар + 1.28 дан юқори бўлса соғломлик даражасини, - 1.28 дан паст бўлса "
        "невротик ҳолат борлигидан далолат беради. Иккисини ўртасидаги кўрсаткич эса нотурғун психик "
        "мослашувчанликни билдиради.\n\nКонсультация учун:\n\n@Hidaya_Med_Clinic_administrator"
        "\n\n+998339513444"
    )

    # Foydalanuvchi ma'lumotlarini olish
    user = await db.select_user(telegram_id=call.from_user.id)
    result_message = (
        f"Тест тури: Яхин, Менделевич | Невротик ҳолатни аниқлаш\n\n"
        f"Исм-шариф: {user['fio']}\nТелефон рақам: {user['phone']}\n\n"
        f"{last_result}\n\n{nevrotik_text}\n\n{footer_text}"
    )

    # Xabarni yangilash
    await call.message.edit_text(text=result_message)
