from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.user_ibuttons import confirm_reenter_ibtn, marital_status_ikb, absence_children_ikb
from loader import dp, adldb
from states.user import UserAnketa


@dp.callback_query_handler(F.data == "consultation_test", state="*")
async def handle_consultation_test(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0)
    data = await state.get_data()

    if len(data) < 3:
        await call.message.answer(
            text="Консультацияга ёзилиш учун барча тестларни ишлашингиз лозим!"
        )
        return

    patient = await adldb.get_patient(telegram_id=str(1234567))

    if patient:
        full_name = patient[3]
        gender = patient[9]
        age = patient[7]
        marital_status = patient[5]
        absence_children = patient[6]
        work = patient[8]

        await call.message.answer(
            text=f"Маълумотларингиз сақланган\n\n"
                 f"Исм шариф: {full_name}\n"
                 f"Жинс: {gender}\n"
                 f"Ёш: {age}\n"
                 f"Оилавий ҳолат: {marital_status}\n"
                 f"Фарзандлар: {absence_children}\n"
                 f"Иш соҳаси: {work}\n\n"
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
        pass

    if call.data == "re-enter":
        pass


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
    data = await state.get_data()

    eysenc = data['eysenc_state']
    yakhin = data['yakhin_state']
    leo = data['leo_state']

    # Patient jadvaliga user ma'lumotlarini qo'shish
    patient_id = await adldb.add_patient(
        telegram_id=message.from_user.id, name=data['user_full_name'], phone=message.text,
        marital_status=data['marital_status'], absence_children=data['absence_children'], work=data['work'],
        result_eeg=data['eeg_result']
    )

    await adldb.add_to_tt_eysenc(
        patient_id=patient_id, temperament=eysenc['temperament'], extraversion=eysenc['extroversion'],
        neuroticism=eysenc['neuroticism']
    )

    await adldb.add_to_tt_yakhin(
        patient_id=patient_id, neurotic_detected=yakhin['neurotic_detected'], anxiety=yakhin['anxiety'],
        depression=yakhin['depression'], asthenia=yakhin['asthenia'], hysteroid_response=yakhin['hysteroid_response'],
        obsessive_phobic=yakhin['obsessive_phobic'], vegetative=yakhin['vegetative']
    )

    await adldb.add_tt_leonhard(
        patient_id=patient_id, hysteroid=leo['isteroid'], pedantic=leo['pedantic'], rigid=leo['rigid'],
        epileptoid=leo['epileptoid'], hyperthymic=leo['gipertim'], dysthymic=leo['distimic'],
        anxious=leo['danger'], cyclothymic=leo['ciclomistic'], affective=leo['affectexaltir'], emotive=leo['emotiv']
    )
    await message.answer(
        text="Tamam"
    )


@dp.message_handler(F.text == "salom", state="*")
async def handle_sample(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data)
