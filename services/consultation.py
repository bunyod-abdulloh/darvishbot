from datetime import datetime, timedelta, time

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.consultation_ikbs import confirm_reenter_ibtn, show_consultation_dates_keyboard
from loader import adldb
from states.user import UserAnketa

patient_dict = {
    "male": "Эркак",
    "female": "Аёл",
    "married": "Турмуш қурган",
    "unmarried": "Турмуш қурмаган",
    "yes": "Бор",
    "no": "Йўқ"
}

week_days = {
    "dushanba": "Душанба",
    "seshanba": "Сешанба",
    "chorshanba": "Чоршанба",
    "payshanba": "Пайшанба",
    "juma": "Жума",
    "shanba": "Шанба",
    "yakshanba": "Якшанба"
}

demo_results = {'yakhin': {'anxiety': 7.81, 'depression': 7.79, 'asthenia': 9.9, 'hysteroid_response': 7.24,
                           'obsessive_phobic': 6.03, 'vegetative': 17.23, 'neurotic_detected': False},
                'eysenc': {'temperament': 'Xolerik', 'extroversion': 15.0, 'neuroticism': 24.0},
                'leonhard': {'isteroid': 22, 'pedantic': 22, 'rigid': 18, 'epileptoid': 24, 'gipertim': 24,
                             'distimic': 15,
                             'danger': 21, 'ciclomistic': 24, 'affectexaltir': 24, 'emotiv': 21},
                'questionnaire': {'headache': 'yes', 'dizziness': 'yes', 'nausea': 'yes', 'abdominal_pain': 'yes',
                                  'feeling_choking': 'yes', 'heart_palpitations': 'yes', 'sleep_disturbance': 'yes',
                                  'low_mood': 'yes', 'crying': 'yes', 'indifference': 'yes'}}

duration_text = "Консультация давомийлигини танланг"


async def missing_test(state: FSMContext) -> str | None:
    data = await state.get_data()
    tests = ['eysenc', 'leonhard', 'yakhin', 'questionnaire']

    test_names = {
        'eysenc': 'Айзенк | Темперамент аниқлаш',
        'leonhard': 'Леонгард сўровномаси',
        'yakhin': 'Яхин Менделевич сўровномаси',
        'questionnaire': 'Оддий сўровнома'
    }

    missing = [t for t in tests if t not in data]
    if missing:
        missing_text = "\n".join(f"{i + 1}. {test_names.get(t, t)}" for i, t in enumerate(missing))
        return (f"{consultation_text}\n\n"
                f"Қуйидагилар ишланмади:\n\n{missing_text}")
    return None


async def check_patient_datas(event: types.Message | types.CallbackQuery, state: FSMContext) -> str | None:
    await state.update_data(demo_results)

    # 1. Message obyektini ajratib olish
    if isinstance(event, types.CallbackQuery):
        user_id = event.from_user.id
        message_obj = event.message
    else:
        user_id = event.from_user.id
        message_obj = event

    # 2. Testlar tekshiruvi
    test_error = await missing_test(state)
    if test_error:
        await message_obj.answer(test_error)
        return None

    # 3. Ma'lumotlarni olish
    patient = await adldb.get_patient(telegram_id=str(user_id))
    if not patient:
        await message_obj.answer(
            text=f"{consultation_text}\n\nИсм шарифингизни киритинг.\n\n<b>Намуна: Тешабоева Гавҳар Дарвишовна</b>"
        )
        await UserAnketa.FULL_NAME.set()
        return None

    await state.finish()

    await state.update_data(demo_results)

    full_name = patient['name']
    gender = patient_dict[patient['gender']]
    age = patient['age']
    marital_status = patient_dict[patient['marital_status']]
    absence_children = patient_dict[patient['absence_children']]
    work = patient['work']
    result_eeg = patient['result_eeg']
    phone = patient['phone']

    text = (f"{consultation_text}\n\n"
            f"Маълумотларингиз сақланган\n\n"
            f"1. Исм шариф: {full_name}\n"
            f"2. Жинс: {gender}\n"
            f"3. Ёш: {age}\n"
            f"4. Оилавий ҳолат: {marital_status}\n"
            f"5. Фарзандлар: {absence_children}\n"
            f"6. Иш соҳаси: {work.capitalize()}\n"
            f"7. ЭЭГ натижаси: {result_eeg.capitalize()}\n"
            f"8. Телефон рақам: {phone}\n\n"
            f"Барчаси тўғри бўлса <b>Тасдиқлаш</b> тугмасини, тўғри бўлмаса керакли тугмани босинг")

    await message_obj.answer(text=text, reply_markup=confirm_reenter_ibtn())

    return None


def float_to_time_str(hour_float):
    hours = int(hour_float)
    minutes = int((hour_float - hours) * 60)
    return time(hour=hours, minute=minutes).strftime("%H:%M")


def generate_workday_text(doctor: list) -> str:
    lines = ["Консультация санасини танланг\n\n"
             "<b>Иш кун ва вақтлари</b>\n"]
    for day in doctor:
        start_hour = float_to_time_str(hour_float=day['start_hour'])
        end_hour = float_to_time_str(hour_float=day['end_hour'])
        day_name = week_days.get(day['code'], day['code'].capitalize())
        lines.append(f"{day_name} | {start_hour} - {end_hour}")
    return "\n".join(lines)


def get_upcoming_work_dates_with_hours(doctor: list[dict], days_ahead=60) -> dict[
    str, dict[str, list[str] | list[str]]]:
    """
    doctor - quyidagi ko‘rinishda bo‘ladi:
    [
        {'code': 'dushanba', 'start_hour': 9.0, 'end_hour': 17.0},
        {'code': 'seshanba', 'start_hour': 9.0, 'end_hour': 17.0},
        ...
    ]
    """
    day_code_to_weekday = {
        "dushanba": 0,
        "seshanba": 1,
        "chorshanba": 2,
        "payshanba": 3,
        "juma": 4,
        "shanba": 5,
        "yakshanba": 6
    }

    today = datetime.today().date()
    dates_by_day = {}

    for day in doctor:
        code = day['code']
        start_hour = float_to_time_str(day['start_hour'])
        end_hour = float_to_time_str(day['end_hour'])
        weekday_number = day_code_to_weekday[code]

        dates = []
        for i in range(days_ahead):
            current_date = today + timedelta(days=i)
            if current_date.weekday() == weekday_number:
                dates.append(current_date.strftime("%d-%m-%Y"))

        dates_by_day[code] = {
            "dates": dates,
            "time": f"{start_hour}-{end_hour}"
        }

    return dates_by_day


consultation_text = ("<b>Консультацияга ёзилиш учун қуйидагиларни бажаришингиз лозим!</b>\n\n"
                     "1. Барча тестларни ишлаш\n"
                     "2. Сўровномага жавоб бериш\n"
                     "3. Шахсий маълумотларни киритиш\n"
                     "4. Консультация учун 50 фоиз тўловни амалга ошириб чек расмини юбориш"
                     )


async def show_consultation_dates_menu(call: types.CallbackQuery):
    doctor = await adldb.get_doctor_work_days()

    text = generate_workday_text(doctor)

    dates_by_day = get_upcoming_work_dates_with_hours(doctor)

    keyboard = show_consultation_dates_keyboard(dates_by_day=dates_by_day)

    await call.message.edit_text(text=text, reply_markup=keyboard)
