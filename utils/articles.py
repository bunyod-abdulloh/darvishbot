from aiogram import types

from keyboards.inline.user_ibuttons import key_returner_articles
from loader import db
from services.error_service import notify_exception_to_admin
from utils.all_functions import extracter


async def send_articles_page(call: types.CallbackQuery, current_page, all_pages, extracted_articles):
    if not extracted_articles:  # If no articles are available
        await call.answer(text="No articles available.", show_alert=True)
        return

    articles_text = "\n".join(
        f"{n['id']}. <a href='{n['link']}'>{n['file_name']}</a>" for n in extracted_articles
    )

    try:
        await call.message.edit_text(
            text=articles_text,
            reply_markup=key_returner_articles(
                current_page=current_page,
                all_pages=all_pages
            ),
            disable_web_page_preview=True
        )
        await call.answer(cache_time=0)
    except Exception as err:
        await call.answer(text=f"Xatolik: {err}", show_alert=True)
        await notify_exception_to_admin(err=err)


async def process_articles_page(call: types.CallbackQuery, direction: str):
    all_articles = await db.select_all_articles()
    if not all_articles:
        await call.answer(text="Maqolalar topilmadi.", show_alert=True)
        return

    extract = extracter(all_medias=all_articles, delimiter=10)
    current_page = int(call.data.split(":")[1])
    all_pages = len(extract)

    if direction == "prev":
        current_page = current_page - 1 if current_page > 1 else all_pages
    elif direction == "next":
        current_page = current_page + 1 if current_page < all_pages else 1

    extracted_articles = extract[current_page - 1]

    await send_articles_page(call, current_page, all_pages, extracted_articles)