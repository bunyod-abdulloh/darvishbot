from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.articlesjson import articlesjs
from data.suhbatloyihajson import suhbats
from filters.admins import IsBotAdminFilter
from loader import dp
from services.batch import process_users_in_batches, process_articles_in_batches, process_suhbats_in_batches
from services.helper_functions import users_data


def alert_message(text: str):
    matn = f"Jarayon {text}!"
    return matn


@dp.message_handler(IsBotAdminFilter(), F.text == "add_users", state="*")
async def handle_add_users(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=alert_message(text="boshlandi"))
    await process_users_in_batches(users=users_data)
    await message.answer(text=alert_message(text="tugadi"))


@dp.message_handler(IsBotAdminFilter(), F.text == "add_articles", state="*")
async def handle_add_articles(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=alert_message(text="boshlandi"))
    await process_articles_in_batches(articles=articlesjs)
    await message.answer(text=alert_message(text="tugadi"))


@dp.message_handler(IsBotAdminFilter(), F.text == "add_iq", state="*")
async def handle_add_iq(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=alert_message(text="boshlandi"))
    pass
    await message.answer(text=alert_message(text="tugadi"))


@dp.message_handler(IsBotAdminFilter(), F.text == "add_suhbats", state="*")
async def handle_add_suhbats(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=alert_message(text="boshlandi"))
    await process_suhbats_in_batches(suhbats=suhbats)
    await message.answer(text=alert_message(text="tugadi"))
