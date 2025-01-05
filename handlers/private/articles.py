from aiogram import types
from magic_filter import F

from keyboards.inline.user_ibuttons import key_returner_articles
from loader import dp, db
from utils.articles import process_articles_page
from utils.all_functions import extracter


@dp.message_handler(F.text == "📝 Maqolalar")
async def articles_hr_one(message: types.Message):
    all_articles = await db.select_all_articles()
    if all_articles:
        extract = extracter(all_medias=all_articles, delimiter=10)
        current_page = 1
        all_pages = len(extract)
        extracted_articles = extract[current_page - 1]

        articles_text = "\n".join(
            f"{n['id']}. <a href='{n['link']}'>{n['file_name']}</a>" for n in extracted_articles
        )

        await message.answer(
            text=articles_text,
            reply_markup=key_returner_articles(current_page=current_page, all_pages=all_pages),
            disable_web_page_preview=True
        )


@dp.callback_query_handler(F.data.startswith("prev_articles"))
async def articles_hr_prev(call: types.CallbackQuery):
    await process_articles_page(call, direction="prev")


@dp.callback_query_handler(F.data.startswith("next_articles"))
async def articles_hr_next(call: types.CallbackQuery):
    await process_articles_page(call, direction="next")


@dp.callback_query_handler(F.data.startswith("alertarticles"))
async def articles_hr_alert(call: types.CallbackQuery):
    current_page = call.data.split(":")[1]
    await call.answer(text=f"Siz {current_page} - sahifadasiz", show_alert=True)
