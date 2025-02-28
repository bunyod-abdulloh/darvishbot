import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from magic_filter import F

from keyboards.default.user_buttons import main_dkb
from loader import dp, udb


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Assalomu alaykum!\n\nBotimizga xush kelibsiz!!!",
                         reply_markup=main_dkb)

    try:
        await udb.add_user(telegram_id=message.from_user.id)
    except asyncpg.exceptions.UniqueViolationError:
        pass
    except Exception as e:
        await message.answer(text=f"{e}")
        pass
    await state.finish()


@dp.message_handler(F.text == "🏡 Bosh sahifa")
async def main_page_handle(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text=message.text, reply_markup=main_dkb
    )
