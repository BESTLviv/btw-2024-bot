import asyncio
import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile
from motor.core import AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorCursor

from src.keyboards import *

CODE_WORD = 'омномном2'
router = Router()


class AdminStates(StatesGroup):
    waiting_for_send_to_all = State()


@router.message(lambda message: message.text.lower() == CODE_WORD.lower())
async def handle_text_message(message: Message):
    await message.answer('вітаю в адмінці2', reply_markup=admin_keyboard)


@router.callback_query(F.data == "send_to_all")
async def send_to_all(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введіть повідомлення для розсилки:", reply_markup=send_to_all_keyboard)
    await state.set_state(AdminStates.waiting_for_send_to_all)


@router.callback_query(F.data == "get_all_users")
async def send_to_all(callback_query: CallbackQuery, db: AgnosticDatabase):
    all_users = await db.users.count_documents({})
    await callback_query.message.answer(f"Загальна кількість користувачів: {all_users}")


@router.callback_query(F.data == "get_all_registered_users")
async def send_to_all(callback_query: CallbackQuery, db: AgnosticDatabase):
    all_registered_users = await db.users.count_documents({'state': 'completed'})
    await callback_query.message.answer(f"Кількість зареєстрованих користувачів: {all_registered_users}")


@router.callback_query(F.data == "send_to_all_bec")
async def send_to_all(callback_query: CallbackQuery, db: AgnosticDatabase):
    users_cursor: AsyncIOMotorCursor = db.users.find({}, {'user_id': 1})

    success_count = 0
    fail_count = 0

    video_path = 'src/data/IMG_3028.MP4'
    video = FSInputFile(video_path)
    text = """Хай там що станеться у житті, саме інженери завжди відбудовували цей світ👷
Сьогодні ми раді повідомити, що реєстрацію на BEST Engineering Competition відкрито!

<b>Подія відбудеться вже зовсім скоро, а саме 25-29 жовтня у Львові.</b>

Тематика цьогорічних змагань — <b>military</b>, тому всі завдання будуть спрямовані на розв’язання проблем дотичних до війни чи повоєнної відбудови.

Дві категорії на вибір пропонують перевірити свої як практичні (<b>Team Design</b>), так і теоретичні (<b>Case Study</b>) знання та навички.⚙️

Чому зволікаєш?
<b>Реєструйся за посиланням нижче і доведи, що майбутнє за інженерами!</b>"""

    async def send_message(user):
        nonlocal success_count, fail_count
        try:
            await callback_query.message.bot.send_video(user['user_id'], video, caption=text, parse_mode='HTML', reply_markup=bec_keyboard)
            success_count += 1
        except Exception as e:
            fail_count += 1
            logging.error(f"Помилка при відправці повідомлення користувачу {user['user_id']}: {e}")

    tasks = []
    async for user in users_cursor:
        tasks.append(asyncio.create_task(send_message(user)))

    await asyncio.gather(*tasks)

    result_text = f"Розсилка завершена!\nУспішно: {success_count}\nНевдало: {fail_count}"
    await callback_query.message.answer(result_text)


@router.message(AdminStates.waiting_for_send_to_all)
async def send_message_to_all_users(message: Message, state: FSMContext, db: AgnosticDatabase):
    sender_id = message.from_user.id
    text = message.text
    users_cursor: AsyncIOMotorCursor = db.users.find({'user_id': {'$ne': sender_id}}, {'user_id': 1})

    success_count = 0
    fail_count = 0

    async def send_message(user):
        nonlocal success_count, fail_count
        try:
            await message.bot.send_message(user['user_id'], text, parse_mode='HTML')
            success_count += 1
        except Exception as e:
            fail_count += 1
            logging.error(f"Помилка при відправці повідомлення користувачу {user['user_id']}: {e}")

    tasks = []
    async for user in users_cursor:
        tasks.append(asyncio.create_task(send_message(user)))

    await asyncio.gather(*tasks)

    result_text = f"Розсилка завершена!\nУспішно: {success_count}\nНевдало: {fail_count}"
    await message.answer(result_text)
    await state.clear()
