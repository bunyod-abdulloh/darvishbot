from datetime import datetime, date

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.user_buttons import main_dkb, tests_main_dkb
from keyboards.inline.admin_ibuttons import check_patient_datas_ikbs
from loader import udb, adldb, bot
from services.consultation import week_days, patient_dict
from states.user import UserAnketa


async def check_user_test(call: types.CallbackQuery) -> bool:
    check_user = await udb.check_user(telegram_id=str(call.from_user.id))
    if not check_user:
        text = "Тест ишлаш учун маълумотларингиз тўлиқ киритилмаган!"
        await call.message.answer(text=text, reply_markup=main_dkb)
        return False
    return True


COMPANY_ID = 1


async def handle_add_results(state: FSMContext, telegram_id: str, photo_file_id=None, username=None,
                             is_patient: bool = False):
    data = await state.get_data()

    consultation_info = {
        "date": data.get("consultation_date"),
        "day": week_days[data.get("consultation_day")],
        "time": data.get("consultation_time"),
        "duration": data.get("consultation_duration")
    }

    test_results = {
        "eysenc": data['eysenc'],
        "yakhin": data['yakhin'],
        "leonhard": data['leonhard'],
        "questionnaire": data['questionnaire']
    }

    bot_user = await udb.select_user(telegram_id=telegram_id)
    gender = patient_dict[bot_user['gender']]
    age = int(bot_user['age'])

    patient, patient_id = await get_or_create_patient(data, telegram_id, is_patient)

    await save_test_results(patient_id, test_results)

    await notify_admin(
        photo_file_id=photo_file_id,
        full_name=patient['name'],
        gender=gender,
        age=age,
        marital_status=patient_dict[patient['marital_status']],
        absence_children=patient_dict[patient['absence_children']],
        work=patient['work'],
        eeg_result=patient['result_eeg'],
        phone=patient['phone'],
        telegram_id=telegram_id,
        username=username,
        consultation_info=consultation_info,
        patient_id=patient_id
    )

    await add_appointment(patient_id, age, consultation_info)


async def get_or_create_patient(data, telegram_id: str, is_patient: bool):
    if is_patient:
        patient = await adldb.get_patient(telegram_id=telegram_id)
        return patient, patient['id']
    else:
        patient_id = await adldb.add_patient(
            telegram_id=telegram_id,
            name=data['user_full_name'],
            phone=data['phone'],
            marital_status=data['marital_status'],
            absence_children=data['absence_children'],
            work=data['work'],
            result_eeg=data['eeg_result']
        )
        patient = {
            'id': patient_id,
            'name': data['user_full_name'],
            'phone': data['phone'],
            'marital_status': data['marital_status'],
            'absence_children': data['absence_children'],
            'work': data['work'],
            'result_eeg': data['eeg_result']
        }
        return patient, patient_id


async def save_test_results(patient_id: int, results: dict):
    e = results['eysenc']
    y = results['yakhin']
    l = results['leonhard']
    q = results['questionnaire']

    current_date = date.today()

    await adldb.add_to_tt_eysenc(
        patient_id=patient_id, temperament=e['temperament'],
        extraversion=e['extroversion'], neuroticism=e['neuroticism'], current_date=current_date
    )

    await adldb.add_to_tt_yakhin(
        patient_id=patient_id, neurotic_detected=str(y['neurotic_detected']), anxiety=y['anxiety'],
        depression=y['depression'], asthenia=y['asthenia'], hysteroid_response=y['hysteroid_response'],
        obsessive_phobic=y['obsessive_phobic'], vegetative=y['vegetative'], current_date=current_date
    )

    await adldb.add_tt_leonhard(
        patient_id=patient_id,
        hysteroid=l['isteroid'], pedantic=l['pedantic'], rigid=l['rigid'], epileptoid=l['epileptoid'],
        hyperthymic=l['gipertim'], dysthymic=l['distimic'], anxious=l['danger'],
        cyclothymic=l['ciclomistic'], affective=l['affectexaltir'], emotive=l['emotiv'], current_date=current_date
    )

    await adldb.add_or_update_questionnaire(
        patient_id=patient_id, headache=q['headache'], dizziness=q['dizziness'], nausea=q['nausea'],
        abdominal_pain=q['abdominal_pain'], feeling_choking=q['feeling_choking'],
        heart_palpitations=q['heart_palpitations'], sleep_disturbance=q['sleep_disturbance'], low_mood=q['low_mood'],
        crying=q['crying'], indifference=q['indifference'], current_date=current_date
    )


async def notify_admin(photo_file_id, full_name, gender, age, marital_status,
                       absence_children, work, eeg_result, phone, telegram_id,
                       username, consultation_info, patient_id):
    caption = (
        f"<b>Исм шарифи:</b> {full_name}\n"
        f"<b>Жинси:</b> {gender}\n"
        f"<b>Ёши:</b> {age}\n"
        f"<b>Оилавий ҳолати:</b> {marital_status}\n"
        f"<b>Фарзандлари:</b> {absence_children}\n"
        f"<b>Иш соҳаси:</b> {work}\n"
        f"<b>ЭЭГ натижаси:</b> {eeg_result}\n"
        f"<b>Телефон рақами:</b> {phone}\n"        
        f"<b>Консультация санаси:</b> {consultation_info['date']} | {consultation_info['day']} | {consultation_info['time']}\n"
        f"<b>Давомийлиги:</b> {consultation_info['duration']} дақиқа\n"
    )

    # Send message to admin
    await bot.send_photo(
        chat_id=ADMINS[0],
        photo=photo_file_id,
        caption=f"<b>Янги бемор маълумотлари қабул қилинди!</b>\n\n"
                f"{caption}"
                f"<b>Телеграм ID:</b> <code>{telegram_id}</code>\n"
                f"<b>Телеграм username:</b>  @{username}\n\n"
                f"<b>Тестлар натижасини CRMдан кўришингиз мумкин!</b>",
        reply_markup=check_patient_datas_ikbs(patient_id=patient_id)
    )

    # Send message to patient
    await bot.send_photo(
        chat_id=telegram_id,
        photo=photo_file_id,
        caption=f"{caption}\n"
                f"Маълумотларингиз қабул қилинди! Тез орада админ Сизга алоқага чиқади!"
    )

async def add_appointment(patient_id, age, consultation_info):
    appointment_datetime = datetime.strptime(
        f"{consultation_info['date']} {consultation_info['time']}",
        "%d-%m-%Y %H:%M"
    )

    age_group = "adult" if age >= 17 else "child"
    doctor_id = await adldb.get_doctor_id()

    await adldb.add_to_appointments(
        patient_id=patient_id,
        doctor_id=doctor_id,
        company_id=COMPANY_ID,
        consultation_duration=consultation_info['duration'],
        age_group=age_group,
        appointment_date=appointment_datetime
    )


# 1. O'zbekcha simptom nomlari
uzbek_symptoms = {
    1: "бош оғриғи",
    2: "бош айланиши",
    3: "кўнгил айниши",
    4: "қорин оғриши",
    5: "томоқда бўғилиш хисси",
    6: "юрак уриб кетиши",
    7: "уйқу бузилиши",
    8: "кайфиятсизлик",
    9: "йиғлаш",
    10: "бефарқлик"
}

# 2. Inglizcha kalitlari
english_symptoms = {
    1: "headache",
    2: "dizziness",
    3: "nausea",
    4: "abdominal_pain",
    5: "feeling_choking",
    6: "heart_palpitations",
    7: "sleep_disturbance",
    8: "low_mood",
    9: "crying",
    10: "indifference"
}


async def handle_tests_main(event: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(event, types.CallbackQuery):
        user_id = event.from_user.id
        message_obj = event.message
    else:
        user_id = event.from_user.id
        message_obj = event

    check_user = await udb.check_user(telegram_id=str(user_id))

    await state.finish()

    if check_user:
        await message_obj.answer(text="🧑‍💻 Тестлар | Сўровномалар", reply_markup=tests_main_dkb)
        return
    else:
        await message_obj.answer(text="Ёшингизни киритинг\n\n<b>Намуна: 35</b>")
        await UserAnketa.GET_AGE.set()


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


