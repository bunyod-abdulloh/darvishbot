from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.default.user_buttons import tests_main_dkb
from keyboards.inline.consultation_ikbs import select_gender_btn
from loader import dp, udb
from services.helper_functions import handle_tests_main
from states.user import UserAnketa


@dp.message_handler(F.text == "🧑‍💻 Тестлар | Сўровномалар", state="*")
async def tests_main_hr(message: types.Message, state: FSMContext):
    await handle_tests_main(event=message, state=state)


@dp.message_handler(state=UserAnketa.GET_AGE, content_types=types.ContentType.TEXT)
async def handle_get_age(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(user_age=int(message.text))
        await message.answer(
            text="Жинсингизни танланг", reply_markup=select_gender_btn()
        )
    else:
        await message.answer(
            text="Фақат намунадагидек киритилиши лозим!"
        )


@dp.callback_query_handler(F.data.startswith("test_"), state="*")
async def handle_gender(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0)
    gender = call.data.split("_")[1]
    age = (await state.get_data()).get("user_age")
    await call.message.answer(
        text="🧑‍💻 Тестлар | Сўровномалар", reply_markup=tests_main_dkb
    )
    
    await udb.update_user_info(
        telegram_id=str(call.from_user.id), age=age, gender=gender
    )
    await state.finish()
