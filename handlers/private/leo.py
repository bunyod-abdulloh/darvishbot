from aiogram import types
from magic_filter import F

from keyboards.default.user_buttons import tests_main_dkb
from keyboards.inline.user_ibuttons import start_test, leotest_ikb
from loader import dp, db
from utils.all_functions import warning_text
from utils.leo import handle_answer


@dp.message_handler(F.text == "Leongard so'rovnomasi")
async def leo_main_router(message: types.Message):
    await db.delete_leotemp(telegram_id=message.from_user.id)
    await message.answer(
        text="Ушбу тест характернинг акцентуациясини ўрганувчи Сўровнома бўлиб, ўз ичига 88 та савол, 10 та шкалани "
             "олади. Биринчи шкала шахсни хаётий фаоллигини ўрганувчи, иккинчи шкала эса акцентуацияни таъсирланишини "
             "намойиш этади. Учинчи шкала синалувчининг эмоционал хаётининг чуқурлигини хисобланади. Тўртинчи шкала "
             "эса синалувчининг педантизмга бўлган мойиллигини ўрганувчи хисобланади.  Бешинчи шкала юқори "
             "хавотирликни, олтинчи шкала эса кайфиятнинг сабабсиз кўтарилиб ёки аксинча тушишга бўлган мойиллигини, "
             "еттинчи шкала бўлса шахснинг намойишкорона хулқ-атворини,  саккизинчи шкаласи эса турғун турмайдиган "
             "феъл атвор,  тўққизинчи шкала чарчоқлик даражасини аниқлаш, ўнинчи эмоционал реакциясининг кучи ва ифода "
             "даражасини аниқлашга қаратилган.\nТест саволларини ечишга вақт чегараланмаган.  Биз Сиз учун, Сизни "
             "характерингизга тегишли бўлган тасдиқ саволларни хавола этамиз. Агар Сиз тасдиқ саволларга розилик "
             "берсангиз «Ҳа» тугмасини, розилик билдирмасангиз «Йўқ» тугмасини босинг. Саволлар устида кўп ўйланманг "
             "чунки тўғри ёки нотўғри жавоблар мавжуд эмас.",
        reply_markup=start_test(callback="leoxarakter")
    )


@dp.callback_query_handler(F.data == "leoxarakter")
async def leo_second_router(call: types.CallbackQuery):
    all_questions = await db.select_questions_leo()
    await call.message.edit_text(
        text=f"{warning_text}\n\n{all_questions[0]['question_number']} / {len(all_questions)}\n\n"
             f"{all_questions[0]['question']}",
        reply_markup=leotest_ikb(all_questions[0])
    )


@dp.callback_query_handler(F.data.startswith("leoyes:"))
async def leoyes_callback(call: types.CallbackQuery):
    question_id = int(call.data.split(":")[1])
    await handle_answer(call, question_id, is_yes=True)


@dp.callback_query_handler(F.data.startswith("leono:"))
async def leono_callback(call: types.CallbackQuery):
    question_id = int(call.data.split(":")[1])
    await handle_answer(call, question_id, is_yes=False)


@dp.callback_query_handler(F.data.startswith("leoback"))
async def leoback_callback(call: types.CallbackQuery):
    question_id = int(call.data.split(":")[1])

    if question_id == 0:
        await call.message.delete()
        await call.message.answer(
            text="🧑‍💻 Testlar | So'rovnomalar", reply_markup=tests_main_dkb
        )
    else:
        await db.back_leotemp(telegram_id=call.from_user.id, question_number=question_id)
        all_questions = await db.select_questions_leo()
        await call.message.edit_text(
            text=f"{all_questions[question_id - 1]['question_number']} / {len(all_questions)}"
                 f"\n\n{all_questions[question_id - 1]['question']}",
            reply_markup=leotest_ikb(testdb=all_questions[question_id - 1])
        )
