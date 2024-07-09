from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Случайный математический факт", callback_data='math_fact')]
])

keyboard1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Случайный математический факт")]
    ],
    resize_keyboard=True
)

