from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from handlers.private.get_doctor import data_
from keyboards.inline.consultation_ikbs import marital_status_ikb, absence_children_ikb, consultation_duration__ikb
from loader import dp
from services.consultation import check_patient_datas, show_consultation_dates_menu
from states.user import UserAnketa


@dp.message_handler(F.text == "✍️ Консультацияга ёзилиш", state="*")
async def handle_sign_up_consultation(message: types.Message, state: FSMContext):
    await check_patient_datas(event=message, state=state)


@dp.callback_query_handler(F.data.startswith("consultation_back:"), state="*")
async def handle_back_buttons(call: types.CallbackQuery, state: FSMContext):
    level = int(call.data.split(":")[1])
    print(level)
    levels = {
        1: lambda: check_patient_datas(event=call, state=state),
        2: lambda: call.message.edit_text(
            text="Консультация давомийлигини танланг",
            reply_markup=consultation_duration__ikb()
        ),
        3: lambda: show_consultation_dates_menu(call=call)
    }
    await call.answer()
    await levels[level]()


@dp.message_handler(F.text == "sa", state="*")
async def sempler(message: types.Message, state: FSMContext):
    await state.update_data(yakhin=data_['yakhin'],
                            eysenc=data_['eysenc'],
                            leonhard=data_['leongard'])
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="Konsultasiya", callback_data="heaved_on_consultation"
        )
    )
    await message.answer(text=message.text, reply_markup=keyboard)


@dp.callback_query_handler(F.data == "heaved_on_consultation", state="*")
async def handle_consultation_test(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0)
    await check_patient_datas(event=call, state=state)


@dp.callback_query_handler(F.data == "cancel_consultation", state="*")
async def handle_cancel_consultation(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        text="Барча тестларингиз натижалари бекор қилинди!"
    )


@dp.callback_query_handler(F.data.in_(("re-enter", "confirm")), state="*")
async def handle_confirm_reenter(call: types.CallbackQuery):
    if call.data == "confirm":
        await call.message.edit_text(
            text="Консультация давомийлигини танланг", reply_markup=consultation_duration__ikb()
        )
        # await handle_consultation_date_sv(event=call)

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
    if message.text.startswith("+") and message.text[1:].isdigit():
        await state.update_data(phone=message.text)
        await message.answer(
            text="Консультация давомийлигини танланг", reply_markup=consultation_duration__ikb()
        )
    else:
        await message.answer(text="Телефон рақамингизни юборинг\n\n<b>Намуна: +998971234567</b>")
