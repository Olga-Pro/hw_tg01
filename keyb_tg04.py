from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder



keyboard1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет")],  # Первая строка с одной кнопкой
        [KeyboardButton(text="Пока")]     # Вторая строка с одной кнопкой
    ],
    resize_keyboard=True
)

keyboard2 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет"),
        KeyboardButton(text="Пока")]     # Одна строка с кнопками
    ],
    resize_keyboard=True
)

inline_keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Новости", url="https://ria.ru/")],
   [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru/")],
   [InlineKeyboardButton(text="Видео", url="https://www.youtube.com/?app=desktop&hl=ru")]
])

inline_keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Показать больше", callback_data='dinamic')]
])

new_buttons = ["Опция 1", "Опция 2"]

async def new_keyboard1(): # создаем кнопки в builder
    keyboard = InlineKeyboardBuilder()
    for key in new_buttons:
        keyboard.add(KeyboardButton(text=key))
    return keyboard.adjust(2).as_markup() # 2 кнопки в ряду
