# import os

from aiogram import types
from aiogram.dispatcher import FSMContext

# from data.config import ADMINS, ADMIN_GROUP
from keyboards.inline.user_ibuttons import ayzenktemp_ikb, sign_up_to_consultation
from loader import stdb, ayzdb
from services.error_service import notify_exception_to_admin
from services.helper_functions import check_user_test


# from docx import Document


async def ayztemplastquestion(question_id: int, call: types.CallbackQuery, state: FSMContext):

    if question_id == 57:
        await handle_end_of_test(call=call, state=state)
    else:
        all_questions = await ayzdb.select_questions_ayztemp()
        try:
            await call.message.edit_text(
                text=f"{all_questions[question_id]['question_number']} / {len(all_questions)}\n\n"
                     f"{all_questions[question_id]['question']}",
                reply_markup=ayzenktemp_ikb(testdb=all_questions[question_id])
            )
        except Exception as err:
            await call.answer(text=f"{err}", show_alert=True)
            await notify_exception_to_admin(err=err)


async def calculate_scales(call: types.CallbackQuery):
    """
    Calculation of the sum of the scales for the user.
    """
    scales = {
        "yolgon": 0,
        "extra-intro": 0,
        "neyrotizm": 0,
    }

    for scale in scales.keys():
        yes_sum = await ayzdb.select_sum_ayztemptemp(telegram_id=call.from_user.id, scale_type=scale, column="yes")
        no_sum = await ayzdb.select_sum_ayztemptemp(telegram_id=call.from_user.id, scale_type=scale, column="no_")

        if yes_sum['sum']:
            scales[scale] += yes_sum['sum']
        if no_sum['sum']:
            scales[scale] += no_sum['sum']
    return scales


async def generate_temperament(scales):
    """
    Generate temperament description based on extroversion and neuroticism.
    """
    extroversion = float(scales["extra-intro"])
    neuroticism = float(scales["neyrotizm"])

    if extroversion > 12 < neuroticism:
        text = f"Темперамент: Холерик\n\nЭкстраверсия - интроверсия: {extroversion} балл\n\nНейротизм: {neuroticism} балл"
        temperament = "Холерик"
    elif extroversion > 12 > neuroticism:
        text = f"Темперамент: Сангвиник\n\nЭкстраверсия - интроверсия: {extroversion} балл\n\nНейротизм: {neuroticism} балл"
        temperament = "Сангвиник"
    elif extroversion < 12 > neuroticism:
        text = f"Темперамент: Флегматик\n\nЭкстраверсия - интроверсия: {extroversion} балл\n\nНейротизм: {neuroticism} балл"
        temperament = "Флегматик"
    else:
        text = f"Темперамент: Меланхолик\n\nЭкстраверсия - интроверсия: {extroversion} балл\n\nНейротизм: {neuroticism} балл"
        temperament = "Меланхолик"

    return extroversion, neuroticism, text, temperament


async def handle_end_of_test(call: types.CallbackQuery, state: FSMContext):
    """
    Handle end of the test and generate the result.
    """
    scales = await calculate_scales(call)
    extroversion, neuroticism, text, temperament = await generate_temperament(scales)

    if 12 in (extroversion, neuroticism):
        await call.message.edit_text(
            text="Кўрсаткичларингиз иккита темпераментга тўғри келиб қолди, сўровномага қайта жавоб беришингиз лозим!"
        )
    elif scales['yolgon'] > 4:
        await call.message.edit_text(
            text="Ёлғон мезони бўйича натижангиз 4 баллдан ошиб кетди! Сўровномага қайта жавоб беришингиз лозим!"
        )
    else:

        if not await check_user_test(call=call):
            return

        await call.message.answer(
            text=f"Сўровнома якунланди!\n\nТест тури: Айзенк | Шахсият сўровномаси\n"
                 f"\n\n{text}\n\n<a href='https://telegra.ph/Ajzenk-SHahsiyat-s%D1%9Erovnomasiga-izo%D2%B3-07-20'>Кўрсатмалар</a>",
            reply_markup=sign_up_to_consultation()
        )

        await ayzdb.delete_ayztemptemp(telegram_id=call.from_user.id)

        temperament_map = {
            'Холерик': 'Xolerik',
            'Флегматик': 'Flegmatik',
            'Сангвиник': 'Sangvinik',
            'Меланхолик': 'Melanxolik'
        }

        eysenc_state = {"temperament": temperament_map[temperament],
                        "extroversion": extroversion,
                        "neuroticism": neuroticism}

        await state.update_data(ayzenk=eysenc_state)

        temperament_result = temperament_map.get(temperament)

        await stdb.set_test_result(
            telegram_id=call.from_user.id, test_type="Ayzenk", result=temperament_result
        )
        # await convert_to_docx(
        #     text=f"Сана: {formatted_date}\n\nТест тури: Айзенк | Шахсият сўровномаси\n\n"
        #          f"Ф.И.О: {user['fio']}\nТелефон рақам: {user['phone']}\n\n{temperament}",
        #     filename=f"{call.from_user.id}", current_date=formatted_date)



# Define a helper function to handle "yes" and "no" cases
async def handle_response(response_type, question_id, call: types.CallbackQuery):
    column = "yes" if response_type == "yes" else "no_"
    get_scale = await ayzdb.get_ayzscales_by_value(value=question_id, column=column)

    if get_scale:
        get_question = await ayzdb.select_check_ayztemptemp(
            telegram_id=call.from_user.id, question_number=question_id
        )

        if get_question is None:
            add_method = (
                ayzdb.add_ayztemptempyes if response_type == "yes" else ayzdb.add_ayztemptempno
            )
            await add_method(
                telegram_id=call.from_user.id,
                scale_type=get_scale['scale_type'],
                question_number=question_id,
                **({"yes": 1} if response_type == "yes" else {"no_": 1})
            )


# async def convert_to_docx(text, filename, current_date):
#     doc = Document()
#
#     doc.add_paragraph(text=text)
#
#     # Faylni saqlash
#     doc.save(f"{filename}.docx")
#
#     file_path = os.path.abspath(f"{filename}.docx")
#
#     try:
#         await bot.send_document(
#             chat_id=ADMINS[0],
#             document=types.InputFile(f"{file_path}"),
#             caption=f"#ayzenk\n\nСана: {current_date}")
#     except Exception as e:
#         await bot.send_message(
#             chat_id=ADMIN_GROUP, text=f"Xatolik: {e} Sana: {current_date}"
#         )
#     os.remove(file_path)
