import asyncio
import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from motor.core import AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorCursor

from src.keyboards import *

CODE_WORD = 'омномном'
router = Router()


class AdminStates(StatesGroup):
    waiting_for_send_to_all = State()


@router.message(lambda message: message.text.lower() == CODE_WORD.lower())
async def handle_text_message(message: Message):
    await message.answer('вітаю в адмінці', reply_markup=admin_keyboard)


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
