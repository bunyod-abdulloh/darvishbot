from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.consultation_ikbs import select_gender_btn, marital_status_ikb, absence_children_ikb
from loader import dp, adldb
from services.consultation import check_patient_datas
from states.user import UserEditDatas


# === FULL NAME ===
@dp.callback_query_handler(F.data == "edit_fullname", state="*")
async def edit_fullname(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Исм шарифингизни киритинг:")
    await UserEditDatas.EDIT_FULLNAME.set()


# === GENDER ===
@dp.callback_query_handler(F.data == "edit_gender", state="*")
async def edit_gender(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Керакли тугмани босинг:", reply_markup=select_gender_btn())
    await UserEditDatas.EDIT_GENDER.set()


# === AGE ===
@dp.callback_query_handler(F.data == "edit_age", state="*")
async def edit_age(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Ёшингизни киритинг:")
    await UserEditDatas.EDIT_AGE.set()


# === MARITAL STATUS ===
@dp.callback_query_handler(F.data == "edit_marital_status", state="*")
async def edit_marital_status(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Оилавий ҳолатингизни танланг:", reply_markup=marital_status_ikb())
    await UserEditDatas.EDIT_MARITAL_STATUS.set()


# === CHILDREN ===
@dp.callback_query_handler(F.data == "edit_absence_children", state="*")
async def edit_absence_children(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Фарзандларингиз борми?", reply_markup=absence_children_ikb())
    await UserEditDatas.EDIT_ABSENCE_CHILDREN.set()


# === WORK ===
@dp.callback_query_handler(F.data == "edit_work", state="*")
async def edit_work(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Қайси соҳада ишлайсиз?")
    await UserEditDatas.EDIT_WORK.set()


# === EEG ===
@dp.callback_query_handler(F.data == "edit_eeg", state="*")
async def edit_eeg(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("ЭЭГ натижасини юборинг:")
    await UserEditDatas.EDIT_EEG.set()


# === PHONE ===
@dp.callback_query_handler(F.data == "edit_phone", state="*")
async def edit_phone(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer("Телефон рақамингизни киритинг:\n\nНамуна: <b>+998901234567</b>")
    await UserEditDatas.EDIT_PHONE.set()


@dp.message_handler(state=UserEditDatas.EDIT_FULLNAME, content_types=types.ContentType.TEXT)
async def set_fullname(message: types.Message, state: FSMContext):
    await adldb.set_fullname(
        fullname=message.text, telegram_id=str(message.from_user.id)
    )
    await message.answer("✅ Исм шариф ўзгартирилди!")
    await check_patient_datas(event=message, state=state)


@dp.callback_query_handler(state=UserEditDatas.EDIT_GENDER)
async def set_gender(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    gender = call.data.split("_")[1]
    await adldb.set_gender(gender=gender, telegram_id=str(call.from_user.id))
    await call.message.answer("✅ Жинс ўзгартирилди!")
    await check_patient_datas(event=call, state=state)


@dp.message_handler(state=UserEditDatas.EDIT_AGE, content_types=types.ContentType.TEXT)
async def set_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if not (1 <= age <= 120):
            raise ValueError
        await adldb.set_age(age=age, telegram_id=str(message.from_user.id))
        await message.answer("✅ Ёш ўзгартирилди!")
        await check_patient_datas(event=message, state=state)

    except ValueError:
        await message.answer("❌ Илтимос, ёшни 1–120 орасидаги сон билан киритинг.")


@dp.callback_query_handler(state=UserEditDatas.EDIT_MARITAL_STATUS)
async def set_marital_status(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await adldb.set_marital_status(marital_status=call.data, telegram_id=str(call.from_user.id))
    await call.message.answer("✅ Оилавий ҳолат янгиланди!")
    await check_patient_datas(event=call, state=state)


@dp.callback_query_handler(state=UserEditDatas.EDIT_ABSENCE_CHILDREN)
async def set_absence_children(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    absence_children = call.data.split("_")[0]
    await adldb.set_absence_children(absence_children=absence_children, telegram_id=str(call.from_user.id))
    await call.message.answer("✅ Маълумот янгиланди!")
    await check_patient_datas(event=call, state=state)


@dp.message_handler(state=UserEditDatas.EDIT_WORK, content_types=types.ContentType.TEXT)
async def set_work(message: types.Message, state: FSMContext):
    await adldb.set_work(work=message.text.lower(), telegram_id=str(message.from_user.id))
    await message.answer("✅ Маълумот янгиланди!")
    await check_patient_datas(event=message, state=state)


@dp.message_handler(state=UserEditDatas.EDIT_EEG, content_types=types.ContentType.TEXT)
async def set_eeg(message: types.Message, state: FSMContext):
    await adldb.set_result_eeg(result_eeg=message.text.lower(), telegram_id=str(message.from_user.id))
    await message.answer("✅ Маълумот янгиланди!")
    await check_patient_datas(event=message, state=state)


@dp.message_handler(state=UserEditDatas.EDIT_PHONE, content_types=types.ContentType.TEXT)
async def set_phone(message: types.Message, state: FSMContext):
    phone = message.text.strip()
    if phone.startswith("+998") and len(phone) == 13 and phone.isdigit():
        await adldb.set_phone(phone=phone, telegram_id=str(message.from_user.id))
        await message.answer("✅ Телефон рақами янгиланди!")
        await check_patient_datas(event=message, state=state)
    else:
        await message.answer("❌ Телефон рақами намунадагидек киритилиши лозим: +998901234567")
