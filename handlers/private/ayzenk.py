from aiogram import types
from aiogram.dispatcher import FSMContext

from magic_filter import F

from keyboards.default.user_buttons import tests_main_dkb
from keyboards.inline.user_ibuttons import ayzenktemp_ikb, start_test
from loader import db, dp
from services.error_service import notify_exception_to_admin
from utils.all_functions import warning_text
from utils.ayzenk import ayztemplastquestion, handle_response


@dp.message_handler(F.text == "Ayzenk | Temperament aniqlash", state="*")
async def temperament_router(message: types.Message, state: FSMContext):
    await state.finish()
    await db.delete_ayztemptemp(
        telegram_id=message.from_user.id
    )

    await message.answer(
        text="Айзенкнинг <b>Шахсият сўровномаси</b> 57 та саволдан иборат. Жавоблар 3 та мезон"
             "(интроверсия/экстраверсия, нейротизм ва ёлғон)лар асосида таҳлил қилиниб натижа чиқарилади. Сўровнома "
             "Сиздаги доминант темпераментни аниқлашга ёрдам беради. Саволларнинг 24 таси шахснинг интроверт ёки "
             "экстраверт эканлигини аниқлашга, 24 таси шахснинг ҳиссий барқарор ёки барқарор эмаслигини "
             "аниқлаш(нейротизм)га ва қолган 9 таси сўровнома тўлдирувчи шахснинг сўровномага муносабатини аниқлашга "
             "қаратилган."
             "\n\nСиз саволларни ўқиб, уларга жавоб беришингиз лозим. Уларга “Ҳа” ёки “Йўқ” деб жавоб беринг, "
             "ҳаёлингизга келган биринчи жавобни ёзинг, улар устида узоқ ўйлаб ўтирманг, чунки жавобни аниқлашга "
             "дастлабки реакциянгиз муҳим. Тўғри ва нотўғри жавобнинг ўзи йўқ, бу ерда бор-йўғи шахсингиз аниқланади "
             "холос."
             "\n\nСўровнома якунлангач, интроверт ёки экстраверт эканлигингиз, нейротизм даражаси ва қайси темперамент "
             "доминант эканлиги кўрсатилади."
             "\n\n<b><i>Эслатма:\n\nЁлғон мезони бўйича кўрсаткичингиз 4 баллдан ошиб кетса ёки "
             "натижа сифатида иккита темперамент чиқарилса сўровномани қайта ишлашингиз лозим!\n\n"
             "</i></b>",
        reply_markup=start_test(
            callback="ayztemp"
        )
    )


# Handler for starting the test
@dp.callback_query_handler(F.data == "ayztemp")
async def ayztemp_go(call: types.CallbackQuery):
    await db.delete_ayztemptemp(telegram_id=call.from_user.id)
    all_questions = await db.select_questions_ayztemp()

    await call.message.edit_text(
        text=f"{warning_text}\n\n{all_questions[0]['question_number']} / {len(all_questions)}\n\n"
             f"{all_questions[0]['question']}",
        reply_markup=ayzenktemp_ikb(testdb=all_questions[0])
    )


@dp.callback_query_handler(F.data.startswith("ayztemp:yes:"))
@dp.callback_query_handler(F.data.startswith("ayztemp:no:"))
async def ayztemp_answer(call: types.CallbackQuery):
    try:
        question_id = int(call.data.split(":")[2])
        await call.answer(cache_time=0)
        # Determine the response type and process it
        if "yes" in call.data:
            await handle_response("yes", question_id, call)
        elif "no" in call.data:
            await handle_response("no", question_id, call)

        # Move to the next question or finish the test
        await ayztemplastquestion(question_id, call)

    except Exception as err:
        await notify_exception_to_admin(err=err)


@dp.callback_query_handler(F.data.startswith("ayztempback"))
async def ayzback_callback(call: types.CallbackQuery):
    question_id = int(call.data.split(":")[1])

    if question_id == 0:
        await call.message.delete()
        await call.message.answer(text="🧑‍💻 Testlar | So'rovnomalar", reply_markup=tests_main_dkb)
    else:
        await db.back_user_ayztemptemp(telegram_id=call.from_user.id, question_number=question_id)
        all_questions = await db.select_questions_ayztemp()

        await call.message.edit_text(
            text=f"{all_questions[question_id - 1]['question_number']} / {len(all_questions)}\n\n{all_questions[question_id - 1]['question']}",
            reply_markup=ayzenktemp_ikb(testdb=all_questions[question_id - 1])
        )
