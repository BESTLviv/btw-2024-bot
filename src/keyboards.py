from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove

university_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='НУЛП'), KeyboardButton(text='ЛНУ'), ],
        [KeyboardButton(text='УКУ'), KeyboardButton(text='КПІ'), ],
        [KeyboardButton(text='КНУ'), KeyboardButton(text='Ще в школі'), ],
        [KeyboardButton(text='Вже закінчив(-ла)')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Вибери або введи...'
)

course_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='1️⃣'), KeyboardButton(text='2️⃣'), KeyboardButton(text='3️⃣'),
         KeyboardButton(text='4️⃣'), ],
        [KeyboardButton(text='Магістратура'), KeyboardButton(text='Вже закінчив(-ла)')],
        [KeyboardButton(text='Нічого з переліченого'), ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Вибери або введи...'
)

speciality_keyboard = ReplyKeyboardRemove()

main_reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Розклад")],
        [KeyboardButton(text="Приєднатися до чату")],
        [KeyboardButton(text="Приєднатися до BEST")],
    ],
    resize_keyboard=True,
)

main_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Розклад", callback_data="schedule")],
        [InlineKeyboardButton(text="Приєднатися до чату",
                              url="https://t.me/+V-ZP4rwg--A3Yjcy")],
        [InlineKeyboardButton(text="Приєднатися до BEST",
                              url="https://beacons.ai/best.lviv")],
    ],
    resize_keyboard=True,
)

admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Написати всім", callback_data="send_to_all")],
        [InlineKeyboardButton(text="Кількість користувачів", callback_data="get_all_users")],
        [InlineKeyboardButton(text="Кількість зареєстрованих користувачів", callback_data="get_all_registered_users")],
        [InlineKeyboardButton(text="Написати всім про ..", callback_data="send_to_all_about_")],
    ],
    resize_keyboard=True,
)

send_to_all_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Відміна", callback_data="cancel")]
    ],
    input_field_placeholder='Ей всі...'
)


def schedule_keyboard(current_day):
    days = ["Пн", "Вт", "Ср", "Чт", "Пт"]
    buttons = [
        [InlineKeyboardButton(
            text=f"➡️️{day}⬅️" if day == current_day else day,
            callback_data=f"schedule_{day}")
            for day in days]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


send_to_all_about__keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔥Уся інформація ТУТ🔥", url="https://cutt.ly/HrtPhRvB")],
    ],
    resize_keyboard=True,
)
