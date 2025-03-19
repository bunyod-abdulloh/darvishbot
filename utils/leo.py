from aiogram import types

from keyboards.inline.user_ibuttons import leotest_ikb
from loader import db, udb


async def leo_result(call: types.CallbackQuery):
    scales = {"Намойишкор(истероид)": "isteroid", "Педантик": "pedantic",
              "Бир жойда қотиб қолган(ригид)": "rigid", "Тез қўзғалувчан(эпилептоид)": "epileptoid",
              "Гипертим": "gipertim", "Дистимик": "distimic", "Хавотирли ва қўрқувчи": "danger",
              "Циклотим": "ciclomistic", "Аффектив - экзальтир": "affectexaltir",
              "Эмотив": "emotiv"}
    scale_multipliers = {"isteroid": 2, "pedantic": 2, "rigid": 2, "epileptoid": 3, "gipertim": 3, "distimic": 3,
                         "danger": 3, "ciclomistic": 3, "affectexaltir": 6, "emotiv": 3}

    results = {}

    for scale in scales.values():
        scale_data = await db.get_sums_leotemp(telegram_id=call.from_user.id, scale_type=scale)
        if scale_data:
            results[scale] = (scale_data['total_yes'] + scale_data['total_no']) * scale_multipliers[scale]

    user = await udb.select_user(telegram_id=call.from_user.id)
    result_text = f"Сўровнома якунланди!\n\nТест тури: Леонгард | Характерологик сўровнома\n\n" \
                  f"Ф.И.О: {user['fio']}\n\nТелефон рақам: {user['phone']}\n\n"

    for key, value in scales.items():
        result_text += f"{key} тоифа: {results.get(value, 'No data')} балл\n"

    result_text += "\nСўровнома ва шкалаларга таъриф қуйидаги ҳаволада:\n\n" \
                   f"https://telegra.ph/K-Leongardning-harakterologik-s%D1%9Erovnomasi-07-25"

    await call.message.edit_text(result_text)
    await db.delete_leotemp(telegram_id=call.from_user.id)


async def handle_answer(call: types.CallbackQuery, question_id: int, is_yes: bool):
    try:
        all_questions = await db.select_questions_leo()
        scale_type = await db.get_yes_leoscales(yes=question_id) if is_yes else await db.get_no_leoscales(
            no_=question_id)

        if scale_type:
            get_question = await db.select_check_leotemp(telegram_id=call.from_user.id, question_number=question_id)
            if get_question is None:
                await db.add_leotemp(
                    telegram_id=call.from_user.id, scale_type=scale_type['scale_type'], question_number=question_id,
                    yes=1 if is_yes else 0
                )

        if question_id == 88:
            await leo_result(call)
        else:
            await call.message.edit_text(
                text=f"{all_questions[question_id]['question_number']} / {len(all_questions)}"
                     f"\n\n{all_questions[question_id]['question']}",
                reply_markup=leotest_ikb(all_questions[question_id])
            )
    except Exception as err:
        await call.answer(text=f"{err}")
