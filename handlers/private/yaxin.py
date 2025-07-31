from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.default.user_buttons import tests_main_dkb
from keyboards.inline.user_ibuttons import start_test, test_ibuttons
from loader import dp, yxndb
from services.error_service import notify_exception_to_admin
from utils.all_functions import warning_text
from utils.yaxin import calculate_and_send_results


@dp.message_handler(F.text == "Яхин Менделевич сўровномаси", state="*")
async def test_command(message: types.Message):
    await yxndb.delete_user_yaxintemporary(telegram_id=message.from_user.id)
    await message.answer(
        text="Ушбу клиник сўровнома невротик ҳолатларнинг асосий синдромларини аниқлашга ёрдам беради. Клиник сўровнома "
             "натижалари қуйидаги 6 та мезон бўйича аниқланиб таҳлил қилинади:"
             "\n\n1) Хавотир мезони \n2) Невротик депрессия мезони \n3) Астения мезони \n4) Истерик тоифадаги жавоб "
             "мезони \n5) Обсессив - фобик бузилишлар мезони \n6) Вегетатив бузилишлар мезони \n\nЙўриқнома:"
             "\n\nХозирги ҳолатингизни тасвирловчи 68 та саволлар тўпламига қуйидаги 5 та жавобдан бирини танлаб жавоб "
             "беришингиз лозим:\n\n• Ҳеч қачон \n• Камдан - кам \n• Баъзида \n• Тез - тез \n• Доим \n\nСўровнома "
             "якунлангач ҳар бир мезон бўйича кўрсаткичларингиз тақдим этилади.",
        reply_markup=start_test(callback="yaxintest")
    )


@dp.callback_query_handler(F.data == "yaxintest", state="*")
async def start_test_yaxin(call: types.CallbackQuery):
    all_questions = await yxndb.select_all_yaxin()
    await call.message.edit_text(
        text=f"{warning_text}\n\n{all_questions[0]['id']} / {len(all_questions)}\n\n{all_questions[0]['question']}",
        reply_markup=test_ibuttons(testdb=all_questions[0])
    )


@dp.callback_query_handler(F.data.startswith("point_"), state="*")
async def test_callback(call: types.CallbackQuery, state: FSMContext):
    column_name, scale_type, question_number = call.data.split(":")
    question_number = int(question_number)

    await call.answer(cache_time=0)

    all_questions = await yxndb.select_all_yaxin()
    scale_parts = scale_type.split("-")

    # Handle multi-scale responses
    for scale in (scale_parts if len(scale_parts) > 1 else [scale_type]):
        point = await yxndb.select_question_scale(scale_type=scale, question_number=question_number)

        await yxndb.add_yaxin_temporary(
            telegram_id=call.from_user.id, scale_type=scale, question_number=question_number,
            test_type="nevroz_yaxin", answer=point[column_name]
        )

    if all_questions[-1]['id'] == question_number:
        await calculate_and_send_results(call=call, state=state)
    else:
        try:
            await call.message.edit_text(
                text=f"{all_questions[question_number]['id']} / {len(all_questions)}"
                     f"\n\n{all_questions[question_number]['question']}",
                reply_markup=test_ibuttons(testdb=all_questions[question_number])
            )
        except Exception as err:
            await call.answer(text=f"Xatolik: {err}", show_alert=True)
            await notify_exception_to_admin(err=err)


@dp.callback_query_handler(F.data.startswith("yaxinback:"), state="*")
async def test_back_callback(call: types.CallbackQuery):
    question_number = int(call.data.split(":")[1])

    if question_number == 0:
        await call.message.delete()
        await call.message.answer(text="🧑‍💻 Тестлар | Сўровномалар", reply_markup=tests_main_dkb)
    else:
        await yxndb.back_yaxintemporary(telegram_id=call.from_user.id, question_number=question_number)
        all_questions = await yxndb.select_all_yaxin()
        await call.message.edit_text(
            text=f"{all_questions[question_number - 1]['id']} / {len(all_questions)}"
                 f"\n\n{all_questions[question_number - 1]['question']}",
            reply_markup=test_ibuttons(testdb=all_questions[question_number - 1])
        )
