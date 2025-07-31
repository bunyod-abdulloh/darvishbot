import os

import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.articlesjson import articlesjs
from data.suhbatloyihajson import suhbats
from filters.admins import IsBotAdminFilter
from loader import dp, db, bot, yxndb, leodb, ayzdb
from services.batch import process_users_in_batches
from services.helper_functions import users_data
from states.admin_states import AdminState


@dp.message_handler(F.text == "addprojects")
async def add_projects_handler(message: types.Message):
    c = 0
    for project in suhbats:
        c += 1
        await db.add_projects(
            category=project['category'],
            subcategory=project['subcategory'],
            sequence=project['sequence'],
            file_type=project['file_type'],
            file_id=project['file_id'],
            caption=project['caption']
        )
    await message.answer(
        text=f"{c} ta material qo'shildi"
    )


@dp.message_handler(F.text == "addarticles")
async def add_articles_handler(message: types.Message):
    c = 0
    for article in articlesjs:
        c += 1
        await db.add_articles(
            file_name=article['file_name'],
            link=article['link']
        )
    await message.answer(
        text=f"{c} ta maqola qo'shildi"
    )


async def download_and_save_file(file_id: str, save_path: str):
    file_info = await bot.get_file(file_id)
    f_path = os.path.join(save_path, file_info.file_path)
    os.makedirs(os.path.dirname(f_path), exist_ok=True)

    await bot.download_file(file_info.file_path, f_path)

    return f_path


@dp.message_handler(F.text == "yaxinquestions", IsBotAdminFilter())
async def add_yaxquest_handler(message: types.Message):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await AdminState.yaxinquestions.set()


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=AdminState.yaxinquestions)
async def add_yaxin_quests(message: types.Message, state: FSMContext):
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        await yxndb.add_questions_yaxin(
            scale_type=row[0],
            question=row[1],
            a=row[2],
            b=row[3],
            c=row[4],
            d=row[5],
            e=row[6]
        )
        c += 1

    await message.answer(
        text=f"Jami {c} ta savollar qo'shildi"
    )
    await state.finish()
    os.remove(f_path)


@dp.message_handler(F.text == "yaxinscales", IsBotAdminFilter())
async def add_yaxscales_handler(message: types.Message):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await AdminState.yaxinscales.set()


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=AdminState.yaxinscales)
async def add_yaxscales_state(message: types.Message, state: FSMContext):
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        await yxndb.add_yaxin_scales(
            scale_type=row[0],
            question_number=row[1],
            point_one=row[2],
            point_two=row[3],
            point_three=row[4],
            point_four=row[5],
            point_five=row[6]
        )
        c += 1
    await message.answer(
        text=f"Jami {c} ta savollar qo'shildi"
    )
    await state.finish()
    os.remove(f_path)


@dp.message_handler(F.text == "leoquestions", IsBotAdminFilter())
async def add_leoquest_handler(message: types.Message):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await AdminState.leoquestions.set()


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=AdminState.leoquestions)
async def add_leoquest_state(message: types.Message, state: FSMContext):
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        await leodb.add_leoquestions(
            question_number=row[0],
            question=row[1]
        )
        c += 1
    await message.answer(
        text=f"Jami {c} ta savollar qo'shildi"
    )
    await state.finish()
    os.remove(f_path)


@dp.message_handler(F.text == "leoscales", IsBotAdminFilter())
async def add_leoscales_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await state.set_state(AdminState.leoscales)


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=AdminState.leoscales)
async def add_leoscales_state(message: types.Message, state: FSMContext):
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        await leodb.add_leoscales(
            scale_type=row[0],
            yes=row[1],
            no_=row[2]
        )
        c += 1
    await message.answer(
        text=f"Jami {c} ta savollar qo'shildi"
    )
    await state.finish()
    os.remove(f_path)


@dp.message_handler(F.text == "ayzquestion")
async def add_ayzquestion_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await state.set_state(AdminState.ayzquestions)


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=AdminState.ayzquestions)
async def add_ayzquestion_state(message: types.Message, state: FSMContext):
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        await ayzdb.add_ayztempquestion(
            question_number=row[0],
            question=row[1]
        )
        c += 1
    await message.answer(
        text=f"Jami {c} ta savollar qo'shildi"
    )
    await state.finish()
    os.remove(f_path)


@dp.message_handler(F.text == "ayzscales")
async def add_ayzscales_handler(message: types.Message, state: FSMContext):
    await message.answer(
        text="Test qo'shish uchun Excel faylni yuboring"
    )
    await state.set_state(AdminState.ayzscales)


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=AdminState.ayzscales)
async def add_ayzscales_state(message: types.Message, state: FSMContext):
    f_path = await download_and_save_file(
        file_id=message.document.file_id, save_path="downloads/"
    )
    df = pd.read_excel(f_path, sheet_name=0)
    c = 0
    for row in df.values:
        await ayzdb.add_ayztempscales(
            scale_type=row[0],
            yes=row[1],
            no_=row[2]
        )
        c += 1
    await message.answer(
        text=f"Jami {c} ta savollar qo'shildi"
    )
    await state.finish()
    os.remove(f_path)


def alert_message(text: str):
    matn = f"Jarayon {text}!"
    return matn


@dp.message_handler(IsBotAdminFilter(), F.text == "add_users", state="*")
async def handle_add_users(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=alert_message(text="boshlandi"))
    await process_users_in_batches(users=users_data)
    await message.answer(text=alert_message(text="tugadi"))
