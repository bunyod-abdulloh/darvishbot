import asyncio
from itertools import islice

from loader import udb, db

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
            except Exception as e:
                print(f"{warning_txt}: {e}")
        await asyncio.sleep(1)


# Articles uchun
async def process_articles_in_batches(articles: list, batch_size: int = 100):
    for i in range(0, len(articles), batch_size):
        batch = articles[i:i + batch_size]
        tasks = []

        for article in batch:
            title = article.get('file_name')
            link = article.get('link')
            tasks.append(
                db.add_articles(file_name=title, link=link)
            )

        if tasks:
            try:
                await asyncio.gather(*tasks)
            except Exception as e:
                print(f"{warning_txt}: {e}")
        await asyncio.sleep(1)


# Ilmiy suhbatlar uchun
async def process_suhbats_in_batches(suhbats: list, batch_size: int = 100):
    for i in range(0, len(suhbats), batch_size):
        batch = suhbats[i:i + batch_size]
        tasks = []

        for suhbat in batch:
            sequence = suhbat.get('sequence')
            file_id = suhbat.get('file_id')  # 'file_id' ni olish
            file_type = suhbat.get('file_type')  # 'file_type' ni olish
            category = suhbat.get('category')  # 'category' ni olish
            subcategory = suhbat.get('subcategory')  # 'subcategory' ni olish
            caption = suhbat.get('caption')
            tasks.append(
                db.add_projects(sequence=sequence, file_id=file_id, file_type=file_type, category=category,
                                subcategory=subcategory, caption=caption))

            if tasks:
                try:
                    await asyncio.gather(*tasks)
                except Exception as e:
                    print(f"{warning_txt}: {e}")
        await asyncio.sleep(1)
