import asyncio
from itertools import islice

from loader import udb
from services.error_service import notify_exception_to_admin

warning_txt = "Xatolik "

def chunk_dict(data: dict, size: int):
    it = iter(data.items())
    while chunk := list(islice(it, size)):
        yield dict(chunk)


# Userlar uchun
async def process_users_in_batches(users: dict, batch_size: int = 100):
    for batch in chunk_dict(users, batch_size):
        tasks = []
        for telegram_id, user_data in batch.items():
            fio = user_data.get('fio')
            phone = user_data.get('phone')

            # Agar foydalanuvchi nomi "NULL" yoki test bo'lsa, fio va phone ni None qilamiz
            if fio == "NULL" or fio == "🧑\u200d💻 Testlar | So`rovnomalar":
                fio = None
                phone = None

            tasks.append(
                udb.add_user_json(telegram_id=int(telegram_id), fio=fio, phone=phone)
            )

        if tasks:
            try:
                await asyncio.gather(*tasks)
            except Exception as err:
                await notify_exception_to_admin(err=err)
        await asyncio.sleep(1)
