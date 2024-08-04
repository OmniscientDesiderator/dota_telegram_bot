from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class MyCallback(CallbackData, prefix="my"):
    foo: str
    bar: int

pages = ['Игроки', 'Баны']

def get_pages():
    builder = InlineKeyboardBuilder()
    for page in pages:
        builder.button(
            text=page,
            callback_data=MyCallback(foo=page, bar="42")
        )
    return builder.as_markup()