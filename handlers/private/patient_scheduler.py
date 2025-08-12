from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from keyboards.inline.admin_ibuttons import patient_message_ikbs
from loader import dp, bot
from services.helper_functions import handle_tests_main
from states.admin import AdminStates
from states.user import Patient


@dp.callback_query_handler(F.data == "patient_ready", state="*")
async def handle_patient_ready(call: types.CallbackQuery):
    await call.message.edit_text(text="Раҳмат!")


@dp.callback_query_handler(F.data == "patient_warn", state="*")
async def handle_patient_warn(call: types.CallbackQuery):
    await call.message.edit_text(text="Сабабни киритинг. Матнингизни яхшилаб текшириб кейин юборинг")
    await Patient.WARN.set()


@dp.message_handler(state=Patient.WARN, content_types=types.ContentType.TEXT)
async def handle_warn_text(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(
        chat_id=ADMINS[0],
        text=f"<b>Бемордан хабар:</b> {message.text}\n\n <b>Телеграм ID:</b> <code>{message.from_user.id}</code>\nьььььььььььььь"
             f"Телеграм username: @{message.from_user.username}", reply_markup=patient_message_ikbs(
            telegram_id=message.from_user.id
        )
    )
    await message.answer(
        text="Хабарингиз админга етказилди!"
    )


@dp.callback_query_handler(F.data == "patient_go_to_tests", state="*")
async def handle_patient_go_to_tests(call: types.CallbackQuery, state: FSMContext):
    await handle_tests_main(event=call, state=state)
    await call.message.delete()


@dp.callback_query_handler(F.data.startswith("admin_message:"), state="*")
async def handle_send_patient_warn(call: types.CallbackQuery, state: FSMContext):
    patient_telegram = call.data.split(":")[1]
    await state.update_data(
        admin_patient_telegram=patient_telegram
    )
    await call.message.edit_text(
        text=""
    )
    await AdminStates.SEND_PATIENT_WARN.set()


@dp.message_handler(state=AdminStates.SEND_PATIENT_WARN, content_types=types.ContentType.TEXT)
async def handle_send_patient_warn_st(message: types.Message, state: FSMContext):
    patient_telegram = (await state.get_data()).get('admin_patient_telegram')

