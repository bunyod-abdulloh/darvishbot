from keyboards.inline.consultation_ikbs import scheduler_patients_ikb
from loader import adldb, bot


async def scheduler_message_to_patients():
    patients_appointment = await adldb.get_appointment_datas()

    for patient in patients_appointment:
        dt_obj = patient['appointment_date']
        appointment_time = dt_obj.strftime("%H:%M")

        patient_data = await adldb.get_patient_by_id(
            patient_id=patient['patient_id']
        )

        text = (f"Ассалому алайкум, {patient_data['name']}!\n\n"
                f"Эртага соат {appointment_time} да Сизнинг консультациянгиз бўлиб ўтади!\n\n"
                f"Сиздан ўз вақтида етиб келишингизни, мабодо режаларингиз ўзгариб қолган бўлса олдиндан хабар бериб "
                f"қўйишингизни сўраймиз!\n\nКонсультацияга келишдан олдин ботимиздаги тестлар ва саволномани ишлашни унутманг!")
        await bot.send_message(
            chat_id=patient_data['tg_id'], text=text, reply_markup=scheduler_patients_ikb()
        )
