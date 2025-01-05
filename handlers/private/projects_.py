from aiogram import types
from magic_filter import F
from keyboards.inline.user_ibuttons import interviews_first_ibuttons
from loader import db, dp
from utils.all_functions import extracter
from utils.projects import fetch_and_handle_page, edit_media_by_type


@dp.callback_query_handler(F.data.startswith("projects:"))
async def interviews_projects_hr_projects(call: types.CallbackQuery):
    category_id = int(call.data.split(":")[1])
    await fetch_and_handle_page(call, category_id=category_id, current_page=1)


@dp.callback_query_handler(F.data.startswith("prev_pts"))
async def projects_two_prev(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    data = call.data.split(":")
    current_page, id_ = int(data[1]), int(data[2])

    await fetch_and_handle_page(call, category_id=id_, current_page=current_page - 1)


@dp.callback_query_handler(F.data.startswith("select_pts:"))
async def projects_two_two(call: types.CallbackQuery):
    await call.answer(cache_time=0)
    data = call.data.split(":")
    id_, current_page = int(data[1]), int(data[2])

    get_data = await db.select_project_by_id(id_=id_)
    select_category = await db.select_project_by_categories(category_name=get_data['category'])

    extract = extracter(all_medias=select_category, delimiter=5)
    items = extract[current_page - 1]
    markup = interviews_first_ibuttons(
        items=items, current_page=current_page, all_pages=len(extract),
        selected=get_data['sequence']
    )

    await edit_media_by_type(call, get_data['file_id'], get_data['caption'], get_data['file_type'], markup)


@dp.callback_query_handler(F.data.startswith("alert_pts:"))
async def projects_two_alert(call: types.CallbackQuery):
    current_page = call.data.split(":")[1]
    await call.answer(text=f"Siz {current_page} - sahifadasiz", show_alert=True)


@dp.callback_query_handler(F.data.startswith("next_pts"))
async def projects_two_next(call: types.CallbackQuery):
    await call.answer(cache_time=0)

    data = call.data.split(":")
    current_page, id_ = int(data[1]), int(data[2])

    await fetch_and_handle_page(call, category_id=id_, current_page=current_page + 1)


@dp.callback_query_handler(F.data.startswith("content_projects:"))
async def projects_two_one(call: types.CallbackQuery):
    data = call.data.split(":")
    current_page, category = int(data[1]), data[2]

    get_category = await db.select_project_by_categories(category_name=category)
    extract = extracter(all_medias=get_category, delimiter=5)
    items = extract[current_page - 1]

    content = "\n".join(item['subcategory'] for item in items)
    await call.answer(text=content, show_alert=True)
