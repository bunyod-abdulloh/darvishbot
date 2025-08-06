from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.user_ibuttons import select_gender_btn
from loader import dp
from services.error_service import notify_exception_to_admin
from states.user import UserAnketa


@dp.callback_query_handler(F.data == "heaved_on_consultation", state="*")
async def handle_sign_up_consultation(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Тўлиқ исм-шарифингизни киритинг:\n\n<b>(Намуна: Тешабоева Гавҳар Дарвишовна)</b>"
    )
    await UserAnketa.add_fullname.set()


@dp.message_handler(state=UserAnketa.add_fullname)
async def add_fullname_handle(message: types.Message, state: FSMContext):
    try:
        if "'" in message.text:
            user_data = message.text.replace("'", "`")
        else:
            user_data = message.text

        await state.update_data(user_full_name=user_data)

        await message.answer(text="Телефон рақамингизни киритинг:\n\n<b>(Намуна: +998991234567</b>")
        await UserAnketa.add_phone.set()
    except Exception as err:
        await message.answer(text=f"Хатолик: {err}")
        await notify_exception_to_admin(err=err)


@dp.message_handler(state=UserAnketa.add_phone)
async def add_phone_handle(message: types.Message, state: FSMContext):
    await state.update_data(user_phone=message.text)
    await message.answer(
        text="Жинсингизни танланг", reply_markup=select_gender_btn()
    )


@dp.callback_query_handler(F.data.in_(["male", "female"]), state="*")
async def handle_gender(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0)
    await state.update_data(user_gender=call.data)
    await call.message.edit_text(
        text="Manzilingizni kiriting"
    )
