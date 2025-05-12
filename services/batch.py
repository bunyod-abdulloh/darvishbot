import asyncio
from itertools import islice

from loader import udb


def chunk_dict(data: dict, size: int):
    it = iter(data.items())
    while chunk := list(islice(it, size)):
        yield dict(chunk)


async def process_users_in_batches(users: dict, batch_size: int = 100):
    for batch in chunk_dict(users, batch_size):
        tasks = [
            udb.add_user_json(telegram_id=int(telegram_id), fio=full_name, phone=phone)
            for telegram_id, (full_name, phone) in batch.items()
        ]
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")  # logging tavsiya etiladi
        await asyncio.sleep(1)
