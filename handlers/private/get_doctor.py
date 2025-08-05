from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.consultation_ikbs import create_sorted_date_inline_keyboard, create_free_time_keyboard, \
    consultation_duration__ikb
from loader import dp, adldb
from services.consultation import generate_workday_text, get_upcoming_work_dates_with_hours, week_days
from services.helper_functions import handle_add_results
from states.user import UserAnketa

data_ = {'yakhin': {'anxiety': 7.81, 'depression': 7.79, 'asthenia': 9.9, 'hysteroid_response': 7.24,
                   'obsessive_phobic': 6.03, 'vegetative': 17.23, 'neurotic_detected': False},
         'eysenc': {'temperament': 'Xolerik', 'extroversion': 15.0, 'neuroticism': 24.0},
         'leongard': {'isteroid': 22, 'pedantic': 22, 'rigid': 18, 'epileptoid': 24, 'gipertim': 24, 'distimic': 15,
                      'danger': 21, 'ciclomistic': 24, 'affectexaltir': 24, 'emotiv': 21}}


@dp.message_handler(F.text == "sasa", state="*")
async def handle_get_doctor(message: types.Message, state: FSMContext):
    await state.update_data(yaxin=data_['yakhin'],
                            ayzenk=data_['eysenc'],
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
    photo_file_id = message.photo[-1].file_id

    if len(data) == 7:
        await handle_add_results(
            state=state, telegram_id=str(message.from_user.id), photo_file_id=photo_file_id, is_patient=True
        )

    elif len(data) == 13:
        await handle_add_results(
            state=state, telegram_id=str(message.from_user.id), photo_file_id=photo_file_id
        )
