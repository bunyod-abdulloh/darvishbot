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
        patient_id = (await adldb.add_patient(
            telegram_id=telegram_id, name=data['user_full_name'], phone=phone,
            marital_status=data['marital_status'], absence_children=data['absence_children'], work=data['work'],
            result_eeg=data['eeg_result']
        ))['id']
    print(patient_id)
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


