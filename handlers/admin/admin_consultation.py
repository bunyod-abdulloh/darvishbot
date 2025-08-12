from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.admin_ibuttons import are_you_sure_markup
from loader import dp, adldb, bot
from states.admin import AdminStates


@dp.callback_query_handler(F.data.startswith("admin_cancel:"), state="*")
async def handle_check_consultation(call: types.CallbackQuery, state: FSMContext):
    patient_telegram = call.data.split(":")[1]
    await state.update_data(admin_patient_telegram=str(patient_telegram))

    await call.message.answer(
        text="Рад этилиш сабабини киритинг"
    )
    await AdminStates.СANCEL_CONSULTATION.set()


@dp.message_handler(state=AdminStates.СANCEL_CONSULTATION, content_types=types.ContentType.TEXT)
async def handle_check_consultation_st(message: types.Message, state: FSMContext):
    patient_telegram = (await state.get_data()).get("admin_patient_telegram")

    try:
        await bot.send_message(
            chat_id=patient_telegram,
            text=f"Консультация учун сўровингиз рад этилди!\n\nСабаб:\n\n<b>{message.text}</b>"
        )
    except Exception as err:
        await message.answer(
            text=f"{err}"
        )

    await message.answer(
        text="Хабар фойдаланувчига юборилди!\n\nФойдаланувчи маълумотлари ўчирилсинми?",
        reply_markup=are_you_sure_markup()
    )
    await AdminStates.DELETE_USER_DATAS.set()


@dp.callback_query_handler(state=AdminStates.DELETE_USER_DATAS)
async def handle_delete_user_datas(call: types.CallbackQuery, state: FSMContext):
    if call.data == "yes":
        patient_telegram = (await state.get_data()).get("admin_patient_telegram")
        await adldb.delete_patient_datas(patient_telegram=patient_telegram)
        await call.message.edit_text(
            text="Маълумотлар ўчирилди!"
        )
    elif call.data == "no":
        await call.message.edit_text(
            text="Тушунарли!"
        )
    await state.finish()
