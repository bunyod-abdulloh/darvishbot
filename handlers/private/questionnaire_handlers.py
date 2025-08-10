from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.questionnaire_ikbs import symptom_keyboard
from loader import dp
from services.helper_functions import uzbek_symptoms, english_symptoms


@dp.message_handler(F.text == "Оддий сўровнома", state="*")
async def start_symptoms(message: types.Message):

    symptom_id = 1
    await message.answer(
        f"Сизда {uzbek_symptoms[symptom_id]} борми?",
        reply_markup=symptom_keyboard(symptom_id)
    )


@dp.callback_query_handler(F.data.startswith("symptom:"), state="*")
async def handle_symptom_answer(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    # Format: symptom:<symptom_id>:<yes/no>
    _, symptom_id_str, answer = callback_query.data.split(":")
    symptom_id = int(symptom_id_str)

    await state.update_data({english_symptoms[symptom_id]: answer.lower()})

    # Keyingi simptomga o'tamiz
    next_symptom_id = symptom_id + 1
    if next_symptom_id <= len(uzbek_symptoms):
        await callback_query.message.edit_text(
            f"Сизда {uzbek_symptoms[next_symptom_id]} борми?",
            reply_markup=symptom_keyboard(next_symptom_id)
        )

    else:
        await callback_query.message.edit_text("Барча симптомлар сўралди. Раҳмат!")


@dp.callback_query_handler(F.data.startswith("back:"), state="*")
async def handle_back(callback_query: types.CallbackQuery):
    # Format: back:<symptom_id>
    symptom_id = int(callback_query.data.split(":")[1])
    await callback_query.answer("Орқадаги симптомга қайтилди.")
    await callback_query.answer()
    await callback_query.message.edit_text(
        f"Сизда {uzbek_symptoms[symptom_id]} борми?",
        reply_markup=symptom_keyboard(symptom_id)
    )

