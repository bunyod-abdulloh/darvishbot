from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.consultation_ikbs import create_free_time_keyboard
from loader import dp, adldb
from services.consultation import week_days, \
    show_consultation_dates_menu
from services.helper_functions import handle_add_results
from states.user import UserAnketa


@dp.callback_query_handler(F.data.startswith("duration_"), state="*")
async def handle_consultation_duration(call: types.CallbackQuery, state: FSMContext):
    duration = call.data.split("_")[1]
    await state.update_data(
        consultation_duration=duration
    )
    await show_consultation_dates_menu(call=call)



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
    
    photo_file_id = message.photo[-1].file_id
    telegram_id = str(message.from_user.id)
    username = message.from_user.username

    if len(data) == 8:
        await handle_add_results(
            state=state, telegram_id=telegram_id, username=username, photo_file_id=photo_file_id, is_patient=True
        )

    elif len(data) == 14:
        await handle_add_results(
            state=state, telegram_id=telegram_id, username=username, photo_file_id=photo_file_id
        )

    else:
        await message.answer(
            text="Маълумотларингиз тўлиқ киритилмади! Қайта <b>✍️ Консультацияга ёзилиш</b> тугмасини босинг!"
        )
