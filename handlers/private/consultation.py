from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.consultation_ikbs import marital_status_ikb, absence_children_ikb
from loader import dp
from services.helper_functions import handle_add_results, check_patient_datas
from states.user import UserAnketa


@dp.message_handler(F.text == "✍️ Консультацияга ёзилиш", state="*")
async def handle_sign_up_consultation(message: types.Message, state: FSMContext):
    await check_patient_datas(event=message, state=state)


@dp.callback_query_handler(F.data == "consultation_test", state="*")
async def handle_consultation_test(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0)
    await check_patient_datas(event=call, state=state)


@dp.callback_query_handler(F.data == "confirm", state="*")
@dp.callback_query_handler(F.data == "re-enter", state="*")
async def handle_confirm_reenter(call: types.CallbackQuery, state: FSMContext):
    if call.data == "confirm":
        await handle_add_results(
            state=state, telegram_id=str(call.from_user.id), is_patient=True
        )
        await call.message.answer(
            text="Маълумотлар қабул қилинди!"
        )

    if call.data == "re-enter":
        await call.message.answer(
            text="Исм шарифингизни киритинг.\n\n<b>Намуна: Тешабоева Гавҳар Дарвишовна</b>"
        )
        await UserAnketa.FULL_NAME.set()


@dp.message_handler(state=UserAnketa.FULL_NAME, content_types=types.ContentType.TEXT)
async def handle_get_fullname(message: types.Message, state: FSMContext):
    await state.update_data(user_full_name=message.text)
    await message.answer(
        text="Оилавий ҳолатингиз", reply_markup=marital_status_ikb()
    )
    await UserAnketa.MARITAL_STATUS.set()


@dp.callback_query_handler(state=UserAnketa.MARITAL_STATUS)
async def handle_marital_status(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(marital_status=call.data)
    await call.message.edit_text(
        text="Фарзандларингиз борми?", reply_markup=absence_children_ikb())
    await UserAnketa.ABSENCE_CHILDREN.set()


@dp.callback_query_handler(state=UserAnketa.ABSENCE_CHILDREN)
async def handle_absence_children(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(absence_children=call.data.split("_")[0])
    await call.message.edit_text(
        text="Иш соҳангизни киритинг"
    )
    await UserAnketa.WORK.set()


@dp.message_handler(state=UserAnketa.WORK, content_types=types.ContentType.TEXT)
async def handle_work(message: types.Message, state: FSMContext):
    await state.update_data(work=message.text)
    await message.answer(text="ЭЭГ текшируви натижасини юборинг\n\n<b>(матн кўринишида)</b>")
    await UserAnketa.EEG.set()


@dp.message_handler(state=UserAnketa.EEG, content_types=types.ContentType.TEXT)
async def handle_eeg_result(message: types.Message, state: FSMContext):
    await state.update_data(eeg_result=message.text)
    await message.answer(text="Телефон рақамингизни юборинг\n\n<b>Намуна: +998971234567</b>")
    await UserAnketa.PHONE.set()


@dp.message_handler(state=UserAnketa.PHONE, content_types=types.ContentType.TEXT)
async def handle_phone_number(message: types.Message, state: FSMContext):
    await handle_add_results(
        state=state, telegram_id=str(message.from_user.id), phone=message.text
    )
    await message.answer(
        text="Маълумотлар қабул қилинди!"
    )
