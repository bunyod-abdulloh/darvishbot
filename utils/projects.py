from aiogram import types

from keyboards.inline.user_ibuttons import key_returner_projects, interviews_first_ibuttons
from loader import db
from services.error_service import notify_exception_to_admin
from utils.all_functions import extracter


async def get_all_projects():
    """Fetch all projects from the database and return paginated data."""
    all_projects = await db.select_projects()
    return extracter(all_medias=all_projects, delimiter=10) if all_projects else []


async def send_projects_page(extract, current_page, all_pages, call: types.CallbackQuery = None,
                             message: types.Message = None):
    """Show projects in a specific page."""
    items = extract[current_page - 1]
    projects = "\n".join(f"{n['rank']}. {n['category']}" for n in items)
    markup = key_returner_projects(items=items, current_page=current_page, all_pages=all_pages)

    try:
        if call:
            await call.message.edit_text(text=projects, reply_markup=markup)
        if message:
            await message.answer(text=projects, reply_markup=markup)
    except Exception as err:
        await call.answer(text=f"Xatolik: {err}", show_alert=True)
        await notify_exception_to_admin(err=err)


async def edit_media_by_type(call: types.CallbackQuery, media, caption, file_type, markup):
    caption = caption.replace("nn", "\n")
    try:
        if file_type == 'audio':
            await call.message.edit_media(
                media=types.InputMediaAudio(media=media, caption=caption),
                reply_markup=markup
            )
        elif file_type == 'video':
            await call.message.edit_media(
                media=types.InputMediaVideo(media=media, caption=caption),
                reply_markup=markup
            )
    except Exception as err:
        await call.answer(text=f"Xatolik yuz berdi: {err}", show_alert=True)
        await notify_exception_to_admin(err=err)


async def send_media(call: types.CallbackQuery, items, markup):
    if not items:  # Empty check
        await call.answer(text="No media available", show_alert=True)
        return

    media = items[0]['file_id']
    caption = items[0]['caption'].replace("nn", "\n")
    try:
        if items[0]['file_type'] == "audio":
            await call.message.edit_media(
                media=types.InputMediaAudio(media=media, caption=caption), reply_markup=markup
            )
        elif items[0]['file_type'] == "video":
            await call.message.edit_media(
                media=types.InputMediaVideo(media=media, caption=caption), reply_markup=markup
            )
    except Exception as err:
        await call.answer(text=f"Xatolik yuz berdi: {err}", show_alert=True)
        await notify_exception_to_admin(err=err)


async def fetch_and_handle_page(call: types.CallbackQuery, category_id=None, current_page=1):
    """General method to fetch category and handle page change."""
    # Fetch category data based on category_id or category name
    if category_id:
        get_category = await db.select_project_by_id(id_=category_id)
        select_category = await db.select_project_by_categories(category_name=get_category['category'])
    else:
        select_category = await db.select_project_by_categories(category_name=category_id)

    extract = extracter(all_medias=select_category, delimiter=5)
    all_pages = len(extract)

    if current_page < 1:
        current_page = all_pages
    elif current_page > all_pages:
        current_page = 1

    items = extract[current_page - 1]
    markup = interviews_first_ibuttons(
        items=items, current_page=current_page, all_pages=all_pages, selected=items[0]['sequence'] if items else 1
    )

    await send_media(call, items, markup)
