# import os
from datetime import datetime

from aiogram import types
# from docx import Document

# from data.config import ADMINS, ADMIN_GROUP
from keyboards.inline.user_ibuttons import ayzenktemp_ikb, test_link_ibutton
from loader import db, bot


async def ayztemplastquestion(question_id: int, call: types.CallbackQuery):
    if question_id == 57:
        await handle_end_of_test(call=call)
    else:
        all_questions = await db.select_questions_ayztemp()
        try:
            await call.message.edit_text(
                text=f"{all_questions[question_id]['question_number']} / {len(all_questions)}\n\n"
                     f"{all_questions[question_id]['question']}",
                reply_markup=ayzenktemp_ikb(testdb=all_questions[question_id])
            )
        except Exception as err:
            await call.answer(
                text=f"{err}", show_alert=True
            )


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
        yes_sum = await db.select_sum_ayztemptemp(telegram_id=call.from_user.id, scale_type=scale, column="yes")
        no_sum = await db.select_sum_ayztemptemp(telegram_id=call.from_user.id, scale_type=scale, column="no_")

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
        temperament = f"Темперамент: Холерик\n\nЭкстраверсия - интроверсия: {extroversion} балл\n\nНейротизм: {neuroticism} балл"
    elif extroversion > 12 > neuroticism:
        temperament = f"Темперамент: Сангвиник\n\nЭкстраверсия - интроверсия: {extroversion} балл\n\nНейротизм: {neuroticism} балл"
    elif extroversion < 12 > neuroticism:
        temperament = f"Темперамент: Флегматик\n\nЭкстраверсия - интроверсия: {extroversion} балл\n\nНейротизм: {neuroticism} балл"
    else:
        temperament = f"Темперамент: Меланхолик\n\nЭкстраверсия - интроверсия: {extroversion} балл\n\nНейротизм: {neuroticism} балл"

    return extroversion, neuroticism, temperament


async def handle_end_of_test(call: types.CallbackQuery):
    """
    Handle end of the test and generate the result.
    """

    scales = await calculate_scales(call)
    extroversion, neuroticism, temperament = await generate_temperament(scales)

    if 12 in (extroversion, neuroticism):
        await call.message.edit_text(
            text="Кўрсаткичларингиз иккита темпераментга тўғри келиб қолди, сўровномага қайта жавоб беришингиз лозим!"
        )
    elif scales['yolgon'] > 4:
        await call.message.edit_text(
            text="Ёлғон мезони бўйича натижангиз 4 баллдан ошиб кетди! Сўровномага қайта жавоб беришингиз лозим!"
        )
    else:
        user = await db.select_user(telegram_id=call.from_user.id)

        current_date = datetime.now()
        formatted_date = current_date.strftime("%d.%m.%Y")

        await call.message.edit_text(
            text=f"Сўровнома якунланди!\n\nТест тури: Айзенк | Шахсият сўровномаси\n\nСана: {formatted_date}\n"
                 f"Ф.И.О: {user['fio']}\nТелефон рақам: {user['phone']}\n\n{temperament}",
            reply_markup=test_link_ibutton(
                link="https://telegra.ph/Ajzenk-SHahsiyat-s%D1%9Erovnomasiga-izo%D2%B3-07-20")
        )
        # await convert_to_docx(
        #     text=f"Сана: {formatted_date}\n\nТест тури: Айзенк | Шахсият сўровномаси\n\n"
        #          f"Ф.И.О: {user['fio']}\nТелефон рақам: {user['phone']}\n\n{temperament}",
        #     filename=f"{call.from_user.id}", current_date=formatted_date)
        await db.delete_ayztemptemp(telegram_id=call.from_user.id)


# Define a helper function to handle "yes" and "no" cases
async def handle_response(response_type, question_id, call: types.CallbackQuery):
    column = "yes" if response_type == "yes" else "no_"
    get_scale = await db.get_ayzscales_by_value(value=question_id, column=column)

    if get_scale:
        get_question = await db.select_check_ayztemptemp(
            telegram_id=call.from_user.id, question_number=question_id
        )

        if get_question is None:
            add_method = (
                db.add_ayztemptempyes if response_type == "yes" else db.add_ayztemptempno
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
