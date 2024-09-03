import init.messages as mes
from telebot import types
import json


def clean_history() -> types.InlineKeyboardMarkup:
    """ KEYBOARDS FOR DELETE ALL HISTORY FOR USER """

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'{mes.delete_history()}', callback_data=f'delete_history'))
    keyboard.add(types.InlineKeyboardButton(text=f'{mes.back_delete_history()}', callback_data=f'no_delete_history'))
    return keyboard
