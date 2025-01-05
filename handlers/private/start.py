import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.user_buttons import main_dkb
from loader import dp, db


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Assalomu alaykum!\n\nBotimizga xush kelibsiz!!!",
                         reply_markup=main_dkb)

    try:
        await db.add_user(telegram_id=message.from_user.id)
    except asyncpg.exceptions.UniqueViolationError:
        pass
    except Exception as e:
        await message.answer(text=f"{e}")
        pass
    await state.finish()
