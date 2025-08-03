from datetime import time

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.user_buttons import main_dkb
from keyboards.inline.consultation_ikbs import confirm_reenter_ibtn

from loader import udb, adldb
from states.user import UserAnketa


async def check_user_test(call: types.CallbackQuery) -> bool:
    check_user = await udb.check_user(telegram_id=str(call.from_user.id))
    if not check_user:
        text = "Тест ишлаш учун маълумотларингиз тўлиқ киритилмаган!"
        await call.message.answer(text=text, reply_markup=main_dkb)
        return False
    return True


async def handle_add_results(state: FSMContext, telegram_id: str, is_patient: bool = False, phone: str = None):
    data = await state.get_data()

    eysenc = data['ayzenk']
    yakhin = data['yaxin']
    leo = data['leongard']

    if is_patient:
        patient_id = await adldb.get_patient(
            telegram_id=telegram_id
        )
    else:
        # Patient jadvaliga user ma'lumotlarini qo'shish
        patient_id = await adldb.add_patient(
            telegram_id=telegram_id, name=data['user_full_name'], phone=phone,
            marital_status=data['marital_status'], absence_children=data['absence_children'], work=data['work'],
            result_eeg=data['eeg_result']
        )

    await adldb.add_to_tt_eysenc(
        patient_id=patient_id, temperament=eysenc['temperament'], extraversion=eysenc['extroversion'],
        neuroticism=eysenc['neuroticism']
    )

    await adldb.add_to_tt_yakhin(
        patient_id=patient_id, neurotic_detected=str(yakhin['neurotic_detected']), anxiety=yakhin['anxiety'],
        depression=yakhin['depression'], asthenia=yakhin['asthenia'], hysteroid_response=yakhin['hysteroid_response'],
        obsessive_phobic=yakhin['obsessive_phobic'], vegetative=yakhin['vegetative']
    )

    await adldb.add_tt_leonhard(
        patient_id=patient_id, hysteroid=leo['isteroid'], pedantic=leo['pedantic'], rigid=leo['rigid'],
        epileptoid=leo['epileptoid'], hyperthymic=leo['gipertim'], dysthymic=leo['distimic'],
        anxious=leo['danger'], cyclothymic=leo['ciclomistic'], affective=leo['affectexaltir'], emotive=leo['emotiv']
    )


async def missing_test(state: FSMContext) -> str | None:
    data = await state.get_data()
    tests = ['ayzenk', 'leongard', 'yaxin']

    # Tarjimasi
    test_names = {
        'ayzenk': 'Айзенк | Темперамент аниқлаш',
        'leongard': 'Леонгард сўровномаси',
        'yaxin': 'Яхин Менделевич сўровномаси'
    }

    missing = [t for t in tests if t not in data]
    if missing:
        missing_text = "\n".join(f"{i + 1}. {test_names.get(t, t)}" for i, t in enumerate(missing))
        return (f"Консультацияга ёзилиш учун барча тестларни ишлашингиз лозим!\n\n"
                f"Қуйидаги тестлар ишланмади:\n\n{missing_text}")
    return None


async def check_patient_datas(event: types.Message | types.CallbackQuery, state: FSMContext) -> str | None:
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
        await message_obj.edit_text(
            text="Исм шарифингизни киритинг.\n\n<b>Намуна: Тешабоева Гавҳар Дарвишовна</b>"
        )
        await UserAnketa.FULL_NAME.set()
        return None

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

    text = (f"Маълумотларингиз сақланган\n\n"
            f"1. Исм шариф: {full_name}\n"
            f"2. Жинс: {patient_dict.get(gender, gender)}\n"
            f"3. Ёш: {age}\n"
            f"4. Оилавий ҳолат: {patient_dict.get(marital_status, marital_status)}\n"
            f"5. Фарзандлар: {patient_dict.get(absence_children, absence_children)}\n"
            f"6. Иш соҳаси: {work.capitalize()}\n"
            f"7. ЭЭГ натижаси: {result_eeg.capitalize()}\n"
            f"8. Телефон рақам: {phone}\n\n"
            f"Барчаси тўғри бўлса <b>Тасдиқлаш</b> тугмасини, тўғри бўлмаса керакли тугмани босинг")

    await message_obj.edit_text(text=text, reply_markup=confirm_reenter_ibtn())
    return None


def float_to_time_str(hour_float):
    hours = int(hour_float)
    minutes = int((hour_float - hours) * 60)
    return time(hour=hours, minute=minutes).strftime("%H:%M")


week_days = {
    "dushanba": "Душанба",
    "seshanba": "Сешанба",
    "chorshanba": "Чоршанба",
    "payshanba": "Пайшанба",
    "juma": "Жума",
    "shanba": "Шанба",
    "yakshanba": "Якшанба"
}


def generate_workday_text(doctor: list) -> str:
    lines = ["<b>Иш кун ва вақтлари</b>\n"]
    for day in doctor:
        start_hour = float_to_time_str(hour_float=day['start_hour'])
        end_hour = float_to_time_str(hour_float=day['end_hour'])
        day_name = week_days.get(day['code'], day['code'].capitalize())
        lines.append(f"{day_name} | {start_hour} - {end_hour}")
    return "\n".join(lines)


from datetime import datetime, timedelta


def get_upcoming_work_dates_with_hours(doctor: list[dict], days_ahead=30) -> dict[str, dict[str, list[str] | list[str]]]:
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

# import csv
#
# result = {}
#
# with open('darvish_users.json', mode='r', encoding='utf-8') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         telegram_id = int(row['telegram_id'])
#         fio = row['fio'] if row['fio'] not in ('null', 'None', '') else None
#         phone = row['phone'] if row['phone'] not in ('null', 'None', '') else None
#         result[telegram_id] = {'fio': fio, 'phone': phone}
#


users_data = {}


