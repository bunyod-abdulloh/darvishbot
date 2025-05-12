import logging

from aiogram import Dispatcher

from data.config import ADMIN_GROUP
from services.error_service import notify_exception_to_admin


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(ADMIN_GROUP, "Bot ishga tushdi")

    except Exception as err:
        await notify_exception_to_admin(err=err)
