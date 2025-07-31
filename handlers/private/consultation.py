from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.user_ibuttons import confirm_reenter_ibtn, marital_status_ikb, absence_children_ikb
from loader import dp, adldb
from services.helper_functions import handle_add_results
from states.user import UserAnketa


@dp.callback_query_handler(F.data == "consultation_test", state="*")
async def handle_consultation_test(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0)
    data = await state.get_data()
    tests = ['ayzenk', 'leongard', 'yaxin']

    missing = [t for t in tests if t not in data]
    if missing:
        missing_text = "\n".join(f"{i + 1}. {t.capitalize()}" for i, t in enumerate(missing))
        await call.message.answer(text=f"Консультацияга ёзилиш учун барча тестларни ишлашингиз лозим!\n\n"
                                       f"Қуйидаги тестлар ишланмади:\n\n{missing_text}")
        return

    patient = await adldb.get_patient(telegram_id=str(call.from_user.id))

    if patient:
        full_name = patient[3]
        gender = patient[4]
        age = patient[5]
        marital_status = patient[7]
        absence_children = patient[8]
        work = patient[9]
        result_eeg = patient[10]
        phone = patient[6]

        patient_dict = {
            "male": "Эркак",
            "female": "Аёл",
            "married": "Турмуш қурган",
            "unmarried": "Турмуш қурмаган",
            "yes": "Бор",
            "no": "Йўқ"
        }
        await call.message.answer(
            text=f"Маълумотларингиз сақланган\n\n"
                 f"1. Исм шариф: {full_name}\n"
                 f"2. Жинс: {patient_dict[gender]}\n"
                 f"3. Ёш: {age}\n"
                 f"4. Оилавий ҳолат: {patient_dict[marital_status]}\n"
                 f"5. Фарзандлар: {patient_dict[absence_children]}\n"
                 f"6. Иш соҳаси: {work}\n"
                 f"7. ЭЭГ натижаси: {result_eeg}\n"
                 f"8. Телефон рақам: {phone}\n\n"
                 f"Барчаси тўғри бўлса <b>Тасдиқлаш</b> тугмасини, тўғри бўлмаса <b>Қайта киритиш</b> тугмасини босинг",
            reply_markup=confirm_reenter_ibtn()
        )
    else:
        await call.message.answer(
            text="Исм шарифингизни киритинг.\n\n<b>Намуна: Тешабоева Гавҳар Дарвишовна</b>"
        )
        await UserAnketa.FULL_NAME.set()


@dp.callback_query_handler(F.data == "confirm", state="*")
@dp.callback_query_handler(F.data == "re-enter", state="*")
async def handle_confirm_reenter(call: types.CallbackQuery, state: FSMContext):
    if call.data == "confirm":
        await handle_add_results(
            state=state, telegram_id=str(call.from_user.id), is_patient=True
        )
        await call.message.answer(
            text="Tamam"
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


@dp.callback_query_handler(F.data == "married", state="*")
@dp.callback_query_handler(F.data == "unmarried")
async def handle_marital_status(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(marital_status=call.data)
    await call.message.edit_text(
        text="Фарзандларингиз борми?", reply_markup=absence_children_ikb())


@dp.callback_query_handler(F.data == "yes_absence_children", state="*")
@dp.callback_query_handler(F.data == "no_absence_children", state="*")
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
        text="Tamam"
    )


@dp.message_handler(F.text == "salom", state="*")
async def handle_sample(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data)
