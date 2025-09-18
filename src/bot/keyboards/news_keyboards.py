from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

def stop_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Готово", callback_data="stop")]
    ])
    return keyboard


def confirmation_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да", callback_data="confirmation_yes")],
        [InlineKeyboardButton(text="❌ Нет", callback_data="confirmation_no")],
    ])
    return keyboard
