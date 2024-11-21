

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup

from data.config import ADMINS
from loader import dp, bot, kino_db, user_db
from keyboards.default.button_kino import menu_movie




class KinoAdd(StatesGroup):
    kino_add=State()
    kino_code=State()


class KinoDelete(StatesGroup):
    kino_code=State()
    # get_kino=State()
    is_confirm = State()

#kinolarni qo`shish uchun handler
@dp.message_handler(commands='kino_add')
async def message_kino_add(message: types.Message):
    admin_id=message.from_user.id
    if admin_id in ADMINS:
        await KinoAdd.kino_add.set()
        await message.answer("Kinoni yuboring ")
    else:
        await message.answer("Siz admin emmasiz")

@dp.message_handler(state=KinoAdd.kino_add,content_types=types.ContentType.VIDEO)
async def kino_file_handler(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['file_id']=message.video.file_id
        data['caption']=message.caption
    await KinoAdd.kino_code.set()
    await message.answer("Kino uchun kod kiriting")


@dp.message_handler(state=KinoAdd.kino_code,content_types=types.ContentType.TEXT)
async def kino_code_handler(message:types.Message,state:FSMContext):
    try:
        post_id=int(message.text)
        async with state.proxy() as data:
            data['post_id']=post_id
            kino_db.add_kino(post_id=data['post_id'], file_id=data['file_id'], caption=data['caption'])
        await message.answer("Kino muvaffaqiyatli qo`shildi")
        await state.finish()

    except ValueError:
      await message.answer("Iltimos kino kodini faqat raqam bilan kiriting")



# kinoni o`chirish buyrug`i
@dp.message_handler(commands='delete_kino')
async def movie_delete_handler(message: types.Message):
    admin_id = message.from_user.id
    if admin_id in ADMINS:
        await KinoDelete.kino_code.set()
        await message.answer("O`chirmoqchi bo`lgan kino kodini yubioring ")
    else:
        await message.answer("Siz admin emassiz")


#kino koddini ushlab olish amallari
@dp.message_handler(state=KinoDelete.kino_code,content_types=types.ContentType.TEXT)
async def movie_kino_code(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['post_id']=int(message.text)
        result=kino_db.search_kino_by_post_id(data['post_id'])
        if result:
            await message.answer_video(video=result['file_id'],caption=result['caption'])
        else:
            await message.answer_video(f"{data['post_id']} : fod bilan kino topilmadi")

    await KinoDelete.is_confirm.set()
    await message.answer("Quydagilardan birini tanlang" ,reply_markup=menu_movie)




@dp.message_handler(state=KinoDelete.is_confirm,content_types=types.ContentType.TEXT)
async def movie_kino_code(message:types.Message,state:FSMContext):
    async with state.proxy() as data:
        data['is_confirm']=message.text
        if data['is_confirm']=="✅Tasdiqlash":
            kino_db.delete_kino(data['post_id'])
            await message.answer("Kino muvaffaqiyatli o`chirildi")
            await state.finish()
        elif data['is_confirm']=="❌Bekor qilish":
            await message.answer("Bekor qilindi")
            await state.finish()
        else:
            await message.answer("ILtimos quydagilardan bitini tanlang",reply_markup=menu_movie)



@dp.message_handler(commands="count_kinos")
async def message_count_kino(message:types.Message):
    count=kino_db.count_kinos()
    admin_id=message.from_user.id
    if admin_id in ADMINS:
        await message.answer(f"Bazada {count['count']} ta kino bor ")

    else:
        await message.answer("Siz admin emassiz")


#users
@dp.message_handler(commands='user')
async def movie_user_handler(message: types.Message):
         count = user_db.count_users()
         count_id=message.from_user.id
         if count_id in ADMINS:
             await message.answer(f"Bazada {count} ta foydalanuvchi bor ")
         else:
             await message.answer("Siz admin emassiz")









# === Kino tavsifi bo'yicha izlash ===
@dp.message_handler(lambda msg: not msg.text.startswith("/"))
async def search_kino_by_caption_handler(message: types.Message):
    query = message.text.strip()
    if not query:
        await message.answer("Iltimos, kino izlash uchun tavsif kiriting.")
        return
    kinolar = kino_db.search_kino_by_caption(query)
    if kinolar:
        for file_id, caption in kinolar:
            await message.answer_video(video=file_id, caption=caption)
    else:
        await message.answer(f"'{query}' tavsifi bilan hech qanday kino topilmadi.")














#kinolarni topish va uzatish
@dp.message_handler(lambda x:x.text.isdigit())
async def search_kino_handler(message:types.Message):
    if message.text.isdigit():
        post_id=int(message.text)
        data=kino_db.search_kino_by_post_id(post_id)
        if data:
            try:
                await bot.send_video(
                chat_id=message.from_user.id,
                video=data['file_id'],
                caption=f"{data['caption']} \n\n  Ko`proq kinolar uchun @jozilova_kino_bot"
                )
            except Exception as err:
                await message.answer(f"Kino topildi lekin yuborilishda xatolik : {err}")

        else:
            await message.answer(f"{post_id}  fod bilan kino topilmadi")
    else:
        await message.answer("Iltimos kino kodini raqam bilan kiriting")
















