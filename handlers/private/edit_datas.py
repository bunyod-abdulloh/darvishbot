from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp, adldb
from states.user import UserAnketa, UserEditDatas


@dp.callback_query_handler(F.data == "edit_fullname", state="*")
async def handle_edit_fullname(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        text="Исм шарифингизни киритинг"
    )
    await UserEditDatas.EDIT_FULLNAME.set()


@dp.message_handler(state=UserEditDatas.EDIT_FULLNAME, content_types=types.ContentType.TEXT)
async def handle_set_fullname(message: types.Message, state: FSMContext):
    await adldb.set_fullname(
        fullname=message.text, telegram_id=str(message.from_user.id)
    )
    await message.answer(
        text="Исм шариф ўзгартирилди!"
    )

