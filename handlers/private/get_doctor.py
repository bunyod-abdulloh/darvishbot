from datetime import datetime

from aiogram import types
from magic_filter import F

from keyboards.inline.consultation_ikbs import create_sorted_date_inline_keyboard
from loader import dp, adldb
from services.helper_functions import generate_workday_text, get_upcoming_work_dates_with_hours


@dp.message_handler(F.text == "sasa", state="*")
async def handle_get_doctor(message: types.Message):
    doctor = await adldb.get_doctor_work_days()

    text = generate_workday_text(doctor)

    dates_by_day = get_upcoming_work_dates_with_hours(doctor)

    keyboard = create_sorted_date_inline_keyboard(dates_by_day=dates_by_day)

    await message.answer(text=text, reply_markup=keyboard)


@dp.callback_query_handler(F.data.startswith("date_"), state="*")
async def handle_choose_date(call: types.CallbackQuery):
    await call.answer()

    _, day_code, date_str, time_range = call.data.split("_")

    start_time, end_time = time_range.split("-")

    formatted_date = datetime.strptime(date_str, "%d-%m-%Y").date()

    doctor_time = await adldb.get_doctor_time(
        formatted_date=formatted_date
    )
    print(doctor_time)
    # await call.message.answer(
    #     f"📅 Sana: {date_str}\n🕒 Ish vaqti: {start_time} - {end_time}"
    # )
    # _, week_day, date = call.data.split(":")
    #

    # print(doctor_time[0]['appointment_time'])
    # day = week_days[week_day]
    # await call.message.answer(
    #     text=f"Сана: {date} | {day}"
    # )
