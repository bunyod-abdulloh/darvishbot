from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from magic_filter import F

from filters.admins import IsBotAdminFilter
from keyboards.default.admin_buttons import admin_main_btns

from loader import dp, db, adb
from states.admin import AdminStates
from utils.db_functions import send_message_to_users, send_media_group_to_users

WARNING_TEXT = (
    "Habar yuborishdan oldin postingizni yaxshilab tekshirib oling!\n\n"
    "Imkoni bo'lsa postingizni oldin tayyorlab olib keyin yuboring.\n\n"
    "Habaringizni kiriting:"
)


@dp.message_handler(IsBotAdminFilter(), Command(commands="admin"))
async def admin_main_page(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Admin panel", reply_markup=admin_main_btns)


@dp.message_handler(IsBotAdminFilter(), F.text == "Foydalanuvchilar soni")
async def user_count(message: types.Message):
    count = await db.count_users()
    await message.answer(f"Foydalanuvchilar soni: {count}")


@dp.message_handler(IsBotAdminFilter(), F.text == "Yaxin tozalash")
async def handle_delete_from_yaxin(message: types.Message):
    count = await adb.delete_from_yaxin()
    await message.answer(f"{count} ta qator o'chirildi!")


@dp.message_handler(IsBotAdminFilter(), F.text == "Leo tozalash")
async def handle_delete_from_yaxin(message: types.Message):
    count = await adb.delete_from_leo()
    await message.answer(f"{count} ta qator o'chirildi!")


@dp.message_handler(IsBotAdminFilter(), F.text == "Ayzenk tozalash")
async def handle_delete_from_yaxin(message: types.Message):
    count = await adb.delete_from_ayzenk()
    await message.answer(f"{count} ta qator o'chirildi!")


@dp.message_handler(IsBotAdminFilter(), F.text == "✅ Oddiy post yuborish")
async def send_to_bot_users(message: types.Message):
    send_status = await adb.get_send_status()
    if send_status:
        await message.answer("Xabar yuborish jarayoni yoqilgan! Hisobot kelganidan so'ng xabar yuborishingiz mumkin!")
    else:
        await message.answer(text=WARNING_TEXT)
        await AdminStates.SEND_TO_USERS.set()


@dp.message_handler(state=AdminStates.SEND_TO_USERS, content_types=types.ContentTypes.ANY)
async def send_to_bot_users_two(message: types.Message, state: FSMContext):
    await state.finish()
    success_count, failed_count = await send_message_to_users(message)

    await adb.update_send_status(False)
    await message.answer(
        f"Xabar {success_count} ta foydalanuvchiga yuborildi!\n{failed_count} ta foydalanuvchi botni bloklagan."
    )


@dp.message_handler(IsBotAdminFilter(), F.text == "🎞 Mediagroup post yuborish")
async def send_media_to_bot(message: types.Message):
    send_status = await adb.get_send_status()
    if send_status:
        await message.answer("Xabar yuborish jarayoni yoqilgan! Hisobot kelganidan so'ng xabar yuborishingiz mumkin!")
    else:
        await message.answer(text=WARNING_TEXT)
        await AdminStates.SEND_MEDIA_TO_USERS.set()


@dp.message_handler(state=AdminStates.SEND_MEDIA_TO_USERS, content_types=types.ContentTypes.ANY, is_media_group=True)
async def send_media_to_bot_second(message: types.Message, album: List[types.Message], state: FSMContext):
    await state.finish()

    try:

        media_group = types.MediaGroup()

        for obj in album:
            file_id = obj.photo[-1].file_id if obj.photo else obj[obj.content_type].file_id
            media_group.attach(
                {"media": file_id, "type": obj.content_type, "caption": obj.caption}
            )

    except Exception as err:
        await message.answer(f"Media qo'shishda xatolik!: {err}")
        return

    success_count, failed_count = await send_media_group_to_users(media_group)

    await adb.update_send_status(False)
    await message.answer(
        f"Media {success_count} ta foydalanuvchiga yuborildi!\n{failed_count} ta foydalanuvchi botni bloklagan."
    )
