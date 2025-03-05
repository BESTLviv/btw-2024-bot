import asyncio
import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile
from motor.core import AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorCursor

from src.keyboards import *

CODE_WORD = '42омномном24'
router = Router()

class AdminStates(StatesGroup):
    waiting_for_send_to_all = State()


@router.message(F.text == CODE_WORD)
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


# треба добавити функціонал для надсилання не лише тексту
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

@router.callback_query(F.data == "send_to_all_about_")
async def send_to_all(callback_query: CallbackQuery, db: AgnosticDatabase):
    users_cursor: AsyncIOMotorCursor = db.users.find({}, {'user_id': 1})

    success_count = 0
    fail_count = 0

    logo = FSInputFile('src/data/photo_2025-03-05_10-29-49.jpg')
    text = """🔥 <b>ОТРИМАЙ ФУТБОЛКУ, ШКАРПЕТКИ І ШОПЕР ВЖЕ ЦЬОГО ЧЕТВЕРГА!</b>
Просто вкажи своє прізвище в <a href="https://cutt.ly/HrtPhRvB">формі</a>
А також приходь до нас вже в цей четвер в 4 корпус, 214 ауд.
🕠 16:30 – презентація про <b>BEST</b>

Універ, пари, дім – і так по колу? 😴 Відчуваєш, що студентське життя проходить повз?

Час це змінити! <b>BEST</b> — це не просто про навчання, а про крутий досвід, подорожі, знайомства та розвиток. Тут ти зможеш:
<b>Прокачати скіли</b> (Figma, Python, JavaScript тощо)
<b>Організовувати заходи та працювати в команді</b>
<b>Брати участь у масштабних івентах:</b> BEST Hackath0n, Training Week, Engineering Competition

Приходь на презентацію та дізнайся, як стати частиною цього всього! 

Встигни <a href="https://cutt.ly/HrtPhRvB">потрапити до нас</a> до 09.03!
Stop being better. Start being BEST!"""

    async def send_message(user):
        nonlocal success_count, fail_count
        try:
            await callback_query.message.bot.send_photo(user['user_id'], logo, caption=text, parse_mode='HTML',
                                                        reply_markup=send_to_all_about__keyboard)
            await asyncio.sleep(0.5)
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