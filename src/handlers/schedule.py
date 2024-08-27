from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.enums import ParseMode

from src.data.schedule_text import schedule
from src.keyboards import *

router = Router()


def schedule_text(day):
    text = ''
    text += f"<b>🎓 Хто:</b> {schedule[day]['Хто']}\n"
    text += f"<b>📖 Тема:</b> {schedule[day]['Тема']}\n"
    text += f"<b>📃 Опис:</b> {schedule[day]['Опис']}\n"
    text += "<i>може ще якісь контакти якщо є: інстаграм, ютуб..</i>\n"
    text += "\n"
    text += f'<b>🕘 Коли:</b> {schedule[day]["Коли"]} (<a href="{schedule[day]["Календар_url"]}">додати у Google Calendar↗️</a>)\n'
    text += f'<b>📍 Де:</b> <a href="{schedule[day]["Корпус_url"]}">{schedule[day]["Корпус"]}</a>, {schedule[day]["Аудиторія"]}\n'
    return text


@router.callback_query(F.data == "schedule")
async def show_schedule1(callback_query: CallbackQuery):
    day = 'Пн'
    photo = FSInputFile(f"src/data/lecturers_photo/{day}.jpg")
    text = schedule_text(day)
    await callback_query.answer('')
    await callback_query.message.answer_photo(photo=photo,
                                              caption=text,
                                              reply_markup=schedule_keyboard(day),
                                              parse_mode='HTML',
                                              disable_web_page_preview=True)


@router.message(F.text == "Розклад")
async def show_schedule2(message: Message):
    day = 'Пн'
    photo = FSInputFile(f"src/data/lecturers_photo/{day}.jpg")
    text = schedule_text(day)
    await message.answer_photo(photo=photo,
                               caption=text,
                               reply_markup=schedule_keyboard(day),
                               parse_mode='HTML',
                               disable_web_page_preview=True)


@router.message(F.text == "Приєднатися до BEST")
async def join_best(message: Message):
    link_text = "Форма для подачі"
    url = "https://docs.google.com/forms/d/e/1FAIpQLSdTcKMiPuStsqNnYsosn4wJmKXgpXpSWuq37gVVEk5OtcaT_w/viewform"
    text = f"[{link_text}]({url})"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


@router.callback_query(lambda c: c.data.startswith('schedule_'))
async def change_schedule(callback_query: CallbackQuery):
    day = callback_query.data.split('_')[1]
    photo = FSInputFile(f"src/data/lecturers_photo/{day}.jpg")
    text = schedule_text(day)
    media = InputMediaPhoto(media=photo, caption=text, parse_mode='HTML')
    await callback_query.message.edit_media(media=media,
                                            reply_markup=schedule_keyboard(day),
                                            disable_web_page_preview=True)
