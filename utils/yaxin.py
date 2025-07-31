# Helper function to handle user data update and state transitions
import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.user_ibuttons import sign_up_to_consultation
from loader import yxndb, stdb


async def calculate_and_send_results(call: types.CallbackQuery, state: FSMContext):
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
                    yxndb.select_datas_temporary(telegram_id=call.from_user.id, scale_type=scale)
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
        "мослашувчанликни билдиради."
    )

    result_message = (
        f"Тест тури: Яхин, Менделевич | Невротик ҳолатни аниқлаш\n\n"        
        f"{last_result}\n\n{nevrotik_text}\n\n{footer_text}"
    )

    # Xabarni yangilash
    await call.message.answer(text=result_message, reply_markup=sign_up_to_consultation())

    await yxndb.delete_user_yaxintemporary(telegram_id=call.from_user.id)

    yakhin_stt = {
        "anxiety": float(list(result.values())[0]),
        "depression": float(list(result.values())[1]),
        "asthenia": float(list(result.values())[2]),
        "hysteroid_response": float(list(result.values())[3]),
        "obsessive_phobic": float(list(result.values())[4]),
        "vegetative": float(list(result.values())[5]),
        "neurotic_detected": nevrotik_detected
    }

    await state.update_data(yaxin=yakhin_stt)

    await stdb.set_test_result(
        telegram_id=str(call.from_user.id), test_type="Yaxin", result=f"{nevrotik_detected}"
    )
