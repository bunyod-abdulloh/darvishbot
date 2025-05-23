from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

inline_keyboard = [[
    InlineKeyboardButton(text="✅ Yes", callback_data='yes'),
    InlineKeyboardButton(text="❌ No", callback_data='no')
]]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# def key_returner_selected(items, table_name, current_page, all_pages, selected):
#     keys = InlineKeyboardMarkup(row_width=5)
#     for item in items:
#         if selected == item['lesson_number']:
#             keys.insert(
#                 InlineKeyboardButton(
#                     text=f"[ {item['lesson_number']} ]",
#                     callback_data=f"id:{item['lesson_number']}:{current_page}:{table_name}"
#                 )
#             )
#         else:
#             keys.add(
#                 InlineKeyboardButton(
#                     text=f"{item['lesson_number']}",
#                     callback_data=f"id:{item['lesson_number']}:{current_page}:{table_name}"
#                 )
#             )
#     keys.row(
#         InlineKeyboardButton(
#             text="◀️",
#             callback_data=f"prev:{current_page}:{table_name}"
#         ),
#         InlineKeyboardButton(
#             text=f"{current_page}/{all_pages}",
#             callback_data=f"alertmessage:{current_page}:{table_name}"
#         ),
#         InlineKeyboardButton(
#             text="▶️",
#             callback_data=f"next:{current_page}:{table_name}"
#         )
#     )
#     return keys


def key_returner_articles(current_page, all_pages):
    keys = InlineKeyboardMarkup(row_width=3)
    keys.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=f"prev_articles:{current_page}"
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=f"alertarticles:{current_page}"
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=f"next_articles:{current_page}"
        )
    )
    return keys


def key_returner_projects(items, current_page, all_pages):
    keys = InlineKeyboardMarkup(row_width=5)
    for item in items:
        keys.insert(
            InlineKeyboardButton(
                text=f"{item['rank']}",
                callback_data=f"projects:{item['id']}"
            )
        )
    keys.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=f"prev_projects:{current_page}"
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=f"alert_projects:{current_page}"
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=f"next_projects:{current_page}"
        )
    )
    return keys


def interviews_first_ibuttons(items, current_page, all_pages, selected):
    builder = InlineKeyboardMarkup(row_width=5)
    for item in items:
        if selected == item['sequence']:
            builder.insert(
                InlineKeyboardButton(
                    text=f"[ {item['sequence']} ]",
                    callback_data=f"select_projects:{item['id']}:{current_page}"
                )
            )
        else:
            builder.insert(
                InlineKeyboardButton(
                    text=f"{item['sequence']}",
                    callback_data=f"select_pts:{item['id']}:{current_page}"
                )
            )
    builder.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=f"prev_pts:{current_page}:{items[0]['id']}"
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=f"alert_pts:{current_page}"
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=f"next_pts:{current_page}:{items[0]['id']}"
        )
    )
    # builder.row(
    #     InlineKeyboardButton(
    #         text="📖 Mundarija",
    #         callback_data=f"content_projects:{current_page}:{items[0]['id']}"
    #     )
    # )
    return builder


def test_link_ibutton(link):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🧑‍⚕️ Кўрсатмалар", web_app=WebAppInfo(
                url=link
            ))
        ]]
    )
    return markup


def ayzenktemp_ikb(testdb):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Ҳа", callback_data=f"ayztemp:yes:{testdb['question_number']}"
                ),
                InlineKeyboardButton(
                    text="Йўқ", callback_data=f"ayztemp:no:{testdb['question_number']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Ortga", callback_data=f"ayztempback:{testdb['question_number'] - 1}"
                )
            ]
        ]
    )
    return markup


def start_test(callback):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🚀 Бошлаш", callback_data=callback)
        ]]
    )
    return markup


def leotest_ikb(testdb):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Ҳа", callback_data=f"leoyes:{testdb['question_number']}"
                ),
                InlineKeyboardButton(
                    text="Йўқ", callback_data=f"leono:{testdb['question_number']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Ortga", callback_data=f"leoback:{testdb['question_number'] - 1}"
                )
            ]
        ]
    )
    return markup


def test_ibuttons(testdb):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=testdb['a'], callback_data=f"point_five:{testdb['scale_type']}:{testdb['id']}"
                ),
                InlineKeyboardButton(
                    text=testdb['b'], callback_data=f"point_four:{testdb['scale_type']}:{testdb['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=testdb['c'], callback_data=f"point_three:{testdb['scale_type']}:{testdb['id']}"
                ),
                InlineKeyboardButton(
                    text=testdb['d'], callback_data=f"point_two:{testdb['scale_type']}:{testdb['id']}"
                ),
                InlineKeyboardButton(
                    text=testdb['e'], callback_data=f"point_one:{testdb['scale_type']}:{testdb['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Ortga", callback_data=f"yaxinback:{testdb['id'] - 1}"
                )
            ]
        ]
    )
    return markup
