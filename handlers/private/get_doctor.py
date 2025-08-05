from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from keyboards.inline.admin_ibuttons import check_patient_datas_ikbs
from keyboards.inline.consultation_ikbs import create_sorted_date_inline_keyboard, create_free_time_keyboard, \
    consultation_duration__ikb
from loader import dp, adldb, bot
from services.consultation import generate_workday_text, get_upcoming_work_dates_with_hours, week_days, patient_dict
from services.helper_functions import handle_add_results
from states.user import UserAnketa

data_ = {'yaxin': {'anxiety': 7.81, 'depression': 7.79, 'asthenia': 9.9, 'hysteroid_response': 7.24,
                   'obsessive_phobic': 6.03, 'vegetative': 17.23, 'neurotic_detected': False},
         'ayzenk': {'temperament': 'Xolerik', 'extroversion': 15.0, 'neuroticism': 24.0},
         'leongard': {'isteroid': 22, 'pedantic': 22, 'rigid': 18, 'epileptoid': 24, 'gipertim': 24, 'distimic': 15,
                      'danger': 21, 'ciclomistic': 24, 'affectexaltir': 24, 'emotiv': 21}}


@dp.message_handler(F.text == "sasa", state="*")
async def handle_get_doctor(message: types.Message, state: FSMContext):
    await state.update_data(yaxin=data_['yaxin'],
                            ayzenk=data_['ayzenk'],
                            leongard=data_['leongard'])

    await message.answer(
        text="Консультация давомийлигини танланг", reply_markup=consultation_duration__ikb()
    )


@dp.callback_query_handler(F.data.startswith("duration_"), state="*")
async def handle_consultation_duration(call: types.CallbackQuery, state: FSMContext):
    duration = call.data.split("_")[1]
    await state.update_data(
        consultation_duration=duration
    )

    doctor = await adldb.get_doctor_work_days()

    text = generate_workday_text(doctor)

    dates_by_day = get_upcoming_work_dates_with_hours(doctor)

    keyboard = create_sorted_date_inline_keyboard(dates_by_day=dates_by_day)

    await call.message.edit_text(text=text, reply_markup=keyboard)


@dp.callback_query_handler(F.data.startswith("date_"), state="*")
async def handle_choose_date(call: types.CallbackQuery, state: FSMContext):
    _, day_code, date_str, time_range = call.data.split("_")

    start_time, end_time = time_range.split("-")
    busy_times = []

    formatted_date = datetime.strptime(date_str, "%d-%m-%Y").date()

    doctor_time = await adldb.get_doctor_time(
        formatted_date=formatted_date
    )

    for time in doctor_time:
        busy_times.append(time['appointment_time'])

    keyboard = create_free_time_keyboard(start_str=start_time, end_str=end_time, busy_times=busy_times)

    if len(keyboard['inline_keyboard']) == 1:
        await call.answer(
            text="Бу санада қабул тўлган!", show_alert=True
        )
        return

    await call.answer()
    await call.message.edit_text(
        f"📅 Сана: {date_str} | {week_days[day_code]}\n\n🕒 Иш вақти: {start_time} - {end_time}\n\n"
        f"Керакли вақтни танланг", reply_markup=keyboard
    )
    await state.update_data(
        consultation_date=date_str, consultation_day=day_code
    )


@dp.callback_query_handler(F.data == "consultation_back1", state="*")
async def handle_back_consultation(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(data)


@dp.callback_query_handler(F.data.startswith("select_time-"), state="*")
async def handle_select_time(call: types.CallbackQuery, state: FSMContext):
    time = call.data.split("-")[1]
    await state.update_data(consultation_time=time)
    await call.message.edit_text(
        text="Тўлов чеки расмини юборинг"
    )
    await UserAnketa.PAYMENT.set()


@dp.message_handler(state=UserAnketa.PAYMENT, content_types=types.ContentType.PHOTO)
async def handle_consultation_chek(message: types.Message, state: FSMContext):

    data = await state.get_data()
    print(f"{data}\n\n{len(data)}")

    if len(data) == 7:
        await handle_add_results(
            state=state, telegram_id=str(message.from_user.id), is_patient=True
        )

    elif len(data) == 13:
        await handle_add_results(
            state=state, telegram_id=str(message.from_user.id)
        )


@dp.message_handler(F.text == "ada", state="*")
async def handle_ada(message: types.Message, state: FSMContext):
    data = await state.get_data()
    file_id = "AgACAgIAAxkBAAJXQGiQKFBf73yomJN77kQCQgABz7NtUgACvPcxG-WngUiX8ISh8aug4QEAAwIAA3kAAzYE"
    print(f"{data}\n\n{len(data)}")

    if len(data) == 7:
        patient = await adldb.get_patient(telegram_id=str(message.from_user.id))

        patient_id = patient['id']
        full_name = patient[3]
        gender = patient_dict[patient[4]]
        age = int(patient[5])
        marital_status = patient_dict[patient[7]]
        absence_children = patient_dict[patient[8]]
        work = patient[9]
        result_eeg = patient[10]
        phone = patient[6]
        consultation_date = data.get("consultation_date")
        consultation_day = week_days[data.get("consultation_day")]
        consultation_time = data.get("consultation_time")
        consultation_duration = data.get("consultation_duration")

        await bot.send_photo(
            chat_id=ADMINS[0],
            photo=file_id,
            caption=f"<b>Янги бемор маълумотлари қабул қилинди!</b>\n\n"
                    f"<b>Исм шарифи:</b> {full_name}\n"
                    f"<b>Жинси:</b> {gender}\n"
                    f"<b>Ёши:</b> {age}\n"
                    f"<b>Оилавий ҳолати:</b> {marital_status}\n"
                    f"<b>Фарзандлари:</b> {absence_children}\n"
                    f"<b>Иш соҳаси:</b> {work}\n"
                    f"<b>ЭЭГ натижаси:</b> {result_eeg}\n"
                    f"<b>Телефон рақами:</b> {phone}\n"
                    f"<b>Телеграм ID:</b> <code>{message.from_user.id}</code>\n"
                    f"<b>Телеграм username:</b>  @{message.from_user.username}\n"
                    f"<b>Консультация санаси:</b> {consultation_date} | {consultation_day} | {consultation_time}\n"
                    f"<b>Давомийлиги:</b> {consultation_duration} дақиқа\n\n"
                    f"<b>Тестлар натижасини CRMдан кўришингиз мумкин!</b>", reply_markup=check_patient_datas_ikbs(
                patient_id=patient['id'])
        )



    elif len(data) == 13:
        await handle_add_results(
            state=state, telegram_id=str(message.from_user.id)
        )
        pass

    else:
        await message.answer(
            text="Маълумотлар тўлиқ киритилмади!"
        )
