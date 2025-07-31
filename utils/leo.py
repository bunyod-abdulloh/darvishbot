from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.user_ibuttons import leotest_ikb, sign_up_to_consultation
from loader import leodb, stdb
from services.error_service import notify_exception_to_admin


async def leo_result(call: types.CallbackQuery):
    scales = {
        "Намойишкор(истероид)": "isteroid",
        "Педантик": "pedantic",
        "Бир жойда қотиб қолган(ригид)": "rigid",
        "Тез қўзғалувчан(эпилептоид)": "epileptoid",
        "Гипертим": "gipertim",
        "Дистимик": "distimic",
        "Хавотирли ва қўрқувчи": "danger",
        "Циклотим": "ciclomistic",
        "Аффектив - экзальтир": "affectexaltir",
        "Эмотив": "emotiv"
    }

    scale_multipliers = {
        "isteroid": 2,
        "pedantic": 2,
        "rigid": 2,
        "epileptoid": 3,
        "gipertim": 3,
        "distimic": 3,
        "danger": 3,
        "ciclomistic": 3,
        "affectexaltir": 6,
        "emotiv": 3
    }

    # Maksimal balllar belgilab olinadi
    max_scores = {
        "isteroid": 22,
        "pedantic": 22,
        "rigid": 18,
        "epileptoid": 24,
        "gipertim": 24,
        "distimic": 15,
        "danger": 21,
        "ciclomistic": 24,
        "affectexaltir": 24,
        "emotiv": 21
    }

    results = {}
    leo_state = {}

    for scale in scales.values():
        scale_data = await leodb.get_sums_leotemp(telegram_id=call.from_user.id, scale_type=scale)
        if scale_data:
            results[scale] = (scale_data['total_yes'] + scale_data['total_no']) * scale_multipliers[scale]

    result_text = f"Сўровнома якунланди!\n\nТест тури: Леонгард | Характерологик сўровнома\n\n"

    for key, value in scales.items():
        leo_state[value] = results.get(value)
        result_text += f"{key} тоифа: {results.get(value, 'No data')} балл\n"

    result_text += "\nСўровнома ва шкалаларга таъриф қуйидаги ҳаволада:\n\n" \
                   f"https://telegra.ph/K-Leongardning-harakterologik-s%D1%9Erovnomasi-07-25"

    await call.message.answer(text=result_text, reply_markup=sign_up_to_consultation())
    await leodb.delete_leotemp(telegram_id=call.from_user.id)

    # Eng yuqori ballni topamiz
    dominant_type = str()

    if results:
        dominant_type = max(results, key=lambda k: results[k] / max_scores.get(k, 1))

    # Foydalanuvchining umumiy natijasini statistika uchun bazaga yozamiz
    await stdb.set_test_result(telegram_id=call.from_user.id, test_type="Leongard", result=dominant_type)

    return leo_state


async def handle_answer(call: types.CallbackQuery, question_id: int, is_yes: bool, state: FSMContext):
    try:
        all_questions = await leodb.select_questions_leo()
        scale_type = await leodb.get_yes_leoscales(yes=question_id) if is_yes else await leodb.get_no_leoscales(
            no_=question_id)

        if scale_type:
            get_question = await leodb.select_check_leotemp(telegram_id=call.from_user.id, question_number=question_id)
            if get_question is None:
                await leodb.add_leotemp(
                    telegram_id=call.from_user.id, scale_type=scale_type['scale_type'], question_number=question_id,
                    yes=1 if is_yes else 0
                )

        if question_id == 88:
            leo_state = await leo_result(call=call)
            await state.update_data(
                leo_state=leo_state
            )
        else:
            await call.message.edit_text(
                text=f"{all_questions[question_id]['question_number']} / {len(all_questions)}"
                     f"\n\n{all_questions[question_id]['question']}",
                reply_markup=leotest_ikb(all_questions[question_id])
            )
    except Exception as err:
        await call.answer(text=f"{err}", show_alert=True)
        await notify_exception_to_admin(err=err)
