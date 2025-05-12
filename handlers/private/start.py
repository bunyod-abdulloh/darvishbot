from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from magic_filter import F

from keyboards.default.user_buttons import main_dkb
from loader import dp, udb
from services.error_service import notify_exception_to_admin


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Assalomu alaykum!\n\nBotimizga xush kelibsiz!!!",
                         reply_markup=main_dkb)

    try:
        await udb.add_user(telegram_id=message.from_user.id)
    except Exception as err:
        await notify_exception_to_admin(err=err)


@dp.message_handler(F.text == "🏡 Bosh sahifa", state="*")
async def main_page_handle(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text=message.text, reply_markup=main_dkb
    )
