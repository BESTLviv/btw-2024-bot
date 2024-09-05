from datetime import datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from motor.core import AgnosticDatabase

from src.keyboards import *

router = Router()


class RegStates(StatesGroup):
    waiting_for_university = State()
    waiting_for_course = State()
    waiting_for_speciality = State()
    completed = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, db: AgnosticDatabase):
    user_id = message.from_user.id
    await db.users.update_one(
        {'user_id': user_id},
        {'$set': {
            'user_id': user_id,
            'username': message.from_user.username,
            'name': message.from_user.first_name,
            'created_at': datetime.now(),
            'state': 'waiting_for_university',
        }},
        upsert=True
    )

    await state.set_state(RegStates.waiting_for_university)
    text = 'Готовий розпочати захопливу подорож з BTW? 🚀\nСпершу давай трохи познайомимося!'
    await message.answer(text)
    text = 'Де ти навчаєшся? (питання 1 з 3)'
    await message.answer(text, reply_markup=university_keyboard)


@router.message(RegStates.waiting_for_university)
async def reg_university(message: Message, state: FSMContext, db: AgnosticDatabase):
    await db.users.update_one(
        {'user_id': message.from_user.id},
        {'$set': {
            'university': message.text,
            'last_interaction_at': datetime.now(),
            'state': 'waiting_for_course',
        }}
    )
    await state.set_state(RegStates.waiting_for_course)
    text = 'На якому ти курсі? (питання 2 з 3)'
    await message.answer(text, reply_markup=course_keyboard)


@router.message(RegStates.waiting_for_course)
async def reg_course(message: Message, state: FSMContext, db: AgnosticDatabase):
    await db.users.update_one(
        {'user_id': message.from_user.id},
        {'$set': {
            'course': message.text,
            'last_interaction_at': datetime.now(),
            'state': 'waiting_for_speciality',
        }}
    )
    await state.set_state(RegStates.waiting_for_speciality)
    text = 'Яка твоя спеціальність? (питання 3 з 3)'
    await message.answer(text, reply_markup=speciality_keyboard)


@router.message(RegStates.waiting_for_speciality)
async def reg_speciality(message: Message, state: FSMContext, db: AgnosticDatabase):
    await db.users.update_one(
        {'user_id': message.from_user.id},
        {'$set': {
            'speciality': message.text,
            'last_interaction_at': datetime.now(),
            'state': 'completed',
        }}
    )
    text = 'Дякуємо за реєстрацію! Чекаємо тебе на BTW! 🌟'
    await message.answer(text, reply_markup=main_reply_keyboard)
    text = 'Тепер ти можеш переглянути розклад заходу та дізнатися більше про наших спікерів'
    await message.answer(text, reply_markup=main_inline_keyboard)
    await state.clear()
