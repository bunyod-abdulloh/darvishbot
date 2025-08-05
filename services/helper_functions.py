from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.user_buttons import main_dkb
from keyboards.inline.admin_ibuttons import check_patient_datas_ikbs
from loader import udb, adldb, bot
from services.consultation import week_days, patient_dict


async def check_user_test(call: types.CallbackQuery) -> bool:
    check_user = await udb.check_user(telegram_id=str(call.from_user.id))
    if not check_user:
        text = "Тест ишлаш учун маълумотларингиз тўлиқ киритилмаган!"
        await call.message.answer(text=text, reply_markup=main_dkb)
        return False
    return True


async def handle_add_results(state: FSMContext, telegram_id: str, photo_file_id=None, username=None,
                             is_patient: bool = False):
    data = await state.get_data()

    eysenc = data['ayzenk']
    yakhin = data['yaxin']
    leo = data['leongard']

    consultation_date = data.get("consultation_date")
    consultation_day = week_days[data.get("consultation_day")]
    consultation_time = data.get("consultation_time")
    consultation_duration = data.get("consultation_duration")

    bot_user = await udb.select_user(telegram_id=telegram_id)

    gender = patient_dict[bot_user['gender']]
    age = int(bot_user['age'])

    # patient, patient_id, full_name, gender, age, marital_status,   = None

    if is_patient:
        patient = await adldb.get_patient(
            telegram_id=telegram_id
        )
        patient_id = patient['id']
        full_name = patient['name']
        marital_status = patient_dict[patient['marital_status']]
        absence_children = patient_dict[patient['absence_children']]
        work = patient['work']
        result_eeg = patient['result_eeg']
        phone = patient['phone']
    else:
        full_name = data['user_full_name']
        marital_status = data['marital_status']
        absence_children = data['absence_children']
        phone = data['phone']
        work = data['work']
        result_eeg = data['eeg_result']

        # Patient jadvaliga user ma'lumotlarini qo'shish
        patient_id = await adldb.add_patient(
            telegram_id=telegram_id, name=full_name, phone=phone, marital_status=marital_status,
            absence_children=absence_children, work=work, result_eeg=result_eeg
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

    await bot.send_photo(
        chat_id=ADMINS[0],
        photo=photo_file_id,
        caption=f"<b>Янги бемор маълумотлари қабул қилинди!</b>\n\n"
                f"<b>Исм шарифи:</b> {full_name}\n"
                f"<b>Жинси:</b> {gender}\n"
                f"<b>Ёши:</b> {age}\n"
                f"<b>Оилавий ҳолати:</b> {marital_status}\n"
                f"<b>Фарзандлари:</b> {absence_children}\n"
                f"<b>Иш соҳаси:</b> {work}\n"
                f"<b>ЭЭГ натижаси:</b> {result_eeg}\n"
                f"<b>Телефон рақами:</b> {phone}\n"
                f"<b>Телеграм ID:</b> <code>{telegram_id}</code>\n"
                f"<b>Телеграм username:</b>  @{username}\n"
                f"<b>Консультация санаси:</b> {consultation_date} | {consultation_day} | {consultation_time}\n"
                f"<b>Давомийлиги:</b> {consultation_duration} дақиқа\n\n"
                f"<b>Тестлар натижасини CRMдан кўришингиз мумкин!</b>", reply_markup=check_patient_datas_ikbs(
            patient_id=patient_id)
    )

    doctor_id = await adldb.get_doctor_id()

    # Appointments jadvaliga ma'lumotlarni kiritish

    appointment_datetime = datetime.strptime(f"{consultation_date} {consultation_time}", "%d-%m-%Y %H:%M")

    if age >= 17:
        age_group = "adult"
    else:
        age_group = "child"

    await adldb.add_to_appointments(
        patient_id=patient_id, doctor_id=doctor_id, company_id=1, consultation_duration=consultation_duration,
        age_group=age_group, appointment_date=appointment_datetime
    )


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


