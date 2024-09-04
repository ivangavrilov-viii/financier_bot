import init.messages as mes
from telebot import types
import json


def clean_history() -> types.InlineKeyboardMarkup:
    """ KEYBOARDS FOR DELETE ALL HISTORY FOR USER """

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'{mes.delete_history()}', callback_data=f'delete_history'))
    keyboard.add(types.InlineKeyboardButton(text=f'{mes.back_delete_history()}', callback_data=f'no_delete_history'))
    return keyboard


def update_daily_budget() -> types.InlineKeyboardMarkup:
    """ KEYBOARDS FOR UPDATE DAILY BUDGET FOR USER """

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f'{mes.update_daily()}', callback_data=f'update_daily'))
    keyboard.add(types.InlineKeyboardButton(text=f'{mes.back_update_daily()}', callback_data=f'no_update_daily'))
    return keyboard
