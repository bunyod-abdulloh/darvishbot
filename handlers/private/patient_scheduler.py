from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from data.config import ADMINS
from loader import dp, bot
from services.helper_functions import handle_tests_main
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
        text=f"<b>Бемордан хабар:</b> {message.text}\n\n <b>Телеграм ID:</b> <code>{message.from_user.id}</code>"
    )
    await message.answer(
        text="Хабарингиз админга етказилди!"
    )


@dp.callback_query_handler(F.data == "patient_go_to_tests", state="*")
async def handle_patient_go_to_tests(call: types.CallbackQuery, state: FSMContext):
    await handle_tests_main(event=call, state=state)
    await call.message.delete()
