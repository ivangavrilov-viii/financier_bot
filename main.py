from telebot.types import Message, CallbackQuery
from datetime import datetime
from decouple import config
from loguru import logger
import telebot

import init.messages as mes
import init.db_funcs as db
import init.keyboards as k
import init.utils as u


bot = telebot.TeleBot(config('key_bot'))


@bot.message_handler(content_types=['text'])
def start(message: Message) -> None:
    """ CALLING AND PROCESSING BASIC BOT COMMANDS """

    chat_id = message.chat.id
    db.create_user(message.chat)

    if message.text == '/start':
        bot.send_message(chat_id, mes.start_message(message))
        bot.send_message(chat_id, mes.function_list(), parse_mode="Markdown")
    elif message.text == '/help':
        bot.send_message(chat_id, mes.function_list(), parse_mode="Markdown")
    elif message.text == '/set_budget':
        bot.send_message(chat_id, mes.input_start_date(), parse_mode="Markdown")
        bot.register_next_step_handler(message, set_start_date)
    elif message.text == '/balance':
        user = db.user_in_db(chat_id)
        bot.send_message(chat_id, mes.balance_message(user), parse_mode="Markdown")
    elif message.text == '/period_history':
        user = db.user_in_db(chat_id)
        bot.send_message(chat_id, mes.history_message(user), parse_mode="Markdown")
    elif message.text == '/clean_history':
        user = db.user_in_db(chat_id)
        if user["expense_history"]:
            bot.send_message(chat_id, mes.clear_history_message(), reply_markup=k.clean_history(), parse_mode="Markdown")
        else:
            bot.send_message(chat_id, mes.empty_history_message(), parse_mode="Markdown")
    elif message.text == '/add_expense':
        user = db.user_in_db(chat_id)
        if user['start_date']:
            bot.send_message(chat_id, mes.input_expense_value(), parse_mode="Markdown")
            bot.register_next_step_handler(message, add_expense)
        else:
            bot.send_message(chat_id, mes.no_active_period(), parse_mode="Markdown")
    elif message.text == '/add_profit':
        user = db.user_in_db(chat_id)
        if user['start_date']:
            bot.send_message(chat_id, mes.input_profit_value(), parse_mode="Markdown")
            bot.register_next_step_handler(message, add_profit)
        else:
            bot.send_message(chat_id, mes.no_active_period(), parse_mode="Markdown")
    elif message.text == '/update_budget':
        user = db.user_in_db(chat_id)
        if user['start_date']:
            bot.send_message(chat_id, mes.update_daily_budget(), reply_markup=k.update_daily_budget(), parse_mode="Markdown")
        else:
            bot.send_message(chat_id, mes.no_active_period(), parse_mode="Markdown")
    else:
        bot.send_message(chat_id, mes.function_list(), parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call: CallbackQuery) -> None:
    """ KEYBOARD HANDLER """

    chat_id = call.message.chat.id
    keyboard_command = call.data

    if keyboard_command == "no_delete_history":
        bot.send_message(chat_id, mes.no_clear_history_message(), parse_mode="Markdown")
    elif keyboard_command == "no_update_daily":
        bot.send_message(chat_id, mes.no_update_daily_budget(), parse_mode="Markdown")
    elif keyboard_command == "update_daily":
        user = db.user_in_db(chat_id)
        update_daily_budget = db.update_daily_budget(user)
        if update_daily_budget:
            bot.send_message(chat_id, mes.success_update_daily_budget_message(), parse_mode="Markdown")
            bot.send_message(chat_id, mes.balance_message(user), parse_mode="Markdown")
        else:
            bot.send_message(chat_id, mes.wrong_update_daily_budget_message(), parse_mode="Markdown")
    elif keyboard_command == "delete_history":
        user = db.user_in_db(chat_id)
        delete_history = db.delete_history(user["chat_id"])
        if delete_history:
            bot.send_message(chat_id, mes.success_clear_history_message(), parse_mode="Markdown")
        else:
            bot.send_message(chat_id, mes.wrong_clear_history_message(), parse_mode="Markdown")
    bot.delete_message(chat_id, call.message.message_id)


def set_start_date(message: Message) -> None:
    """ SET START DATE FOR CALCULATING BUDGET """

    start_date = message.text
    chat_id = message.chat.id

    try:
        today = datetime.now().date()
        start = datetime.strptime(start_date, "%d.%m.%Y").date()
        if today > start:
            bot.send_message(chat_id, mes.wrong_date_today(), parse_mode="Markdown")
            bot.register_next_step_handler(message, set_start_date)
        else:
            bot.send_message(chat_id, mes.input_end_date(), parse_mode="Markdown")
            bot.register_next_step_handler(message, set_end_date, start)
    except Exception as error:
        logger.error(f'Error with input start date: {error}')
        bot.send_message(chat_id, mes.wrong_date(), parse_mode="Markdown")
        bot.register_next_step_handler(message, set_start_date)


def set_end_date(message: Message, start_date) -> None:
    """ SET START DATE FOR CALCULATING BUDGET """

    end_date = message.text
    chat_id = message.chat.id

    try:
        end = datetime.strptime(end_date, "%d.%m.%Y").date()
        if start_date >= end:
            bot.send_message(chat_id, mes.wrong_date_early(), parse_mode="Markdown")
            bot.register_next_step_handler(message, set_end_date, start_date)
        else:
            start_date_str, end_date_str, days = u.get_days_count(start_date, end)
            bot.send_message(chat_id, mes.input_budget(start_date_str, end_date_str, days), parse_mode="Markdown")
            bot.register_next_step_handler(message, set_budget, start_date, end)
    except Exception as error:
        logger.error(f'Error with input start date: {error}')
        bot.send_message(chat_id, mes.wrong_date(), parse_mode="Markdown")
        bot.register_next_step_handler(message, set_end_date, start_date)


def set_budget(message: Message, start_date, end_date) -> None:
    """ SET BUDGET FOR CALCULATING BUDGET """

    budget = message.text
    chat_id = message.chat.id

    if budget.isdigit() and float(budget) > 0.0:
        user = db.user_in_db(chat_id)
        save_new_budget = db.save_budget(chat_id, user, start_date, end_date, float(budget))
        if save_new_budget:
            user = db.user_in_db(chat_id)
            bot.send_message(chat_id, mes.success_save_budget(user), parse_mode="Markdown")
        else:
            bot.send_message(chat_id, mes.wrong_save_budget(), parse_mode="Markdown")
    else:
        bot.send_message(chat_id, mes.wrong_budget(), parse_mode="Markdown")
        bot.register_next_step_handler(message, set_budget, start_date, end_date)


def add_expense(message: Message) -> None:
    """ CHECK EXPENSE VALUE FOR USER """

    expense_value = message.text
    chat_id = message.chat.id

    if expense_value.isdigit() and float(expense_value) > 0:
        bot.send_message(chat_id, mes.input_expense_comment(), parse_mode="Markdown")
        bot.register_next_step_handler(message, add_expense_comment, float(expense_value))
    else:
        bot.send_message(chat_id, mes.wrong_expense_value(), parse_mode="Markdown")
        bot.send_message(chat_id, mes.function_list(), parse_mode="Markdown")


def add_expense_comment(message: Message, expense_value: float) -> None:
    """ ADD EXPENSE IN HISTORY FOR USER """

    expense_comment = message.text
    chat_id = message.chat.id
    today_date = str(datetime.now().date().strftime('%d.%m.%Y'))

    add_response = db.add_expense(chat_id, expense_value, expense_comment, today_date)
    if add_response:
        bot.send_message(chat_id, mes.success_add_expense(), parse_mode="Markdown")
    else:
        bot.send_message(chat_id, mes.wrong_add_expense(), parse_mode="Markdown")


def add_profit(message: Message) -> None:
    """ CHECK PROFIT VALUE FOR USER """

    profit_value = message.text
    chat_id = message.chat.id

    if profit_value.isdigit() and float(profit_value) > 0:
        bot.send_message(chat_id, mes.input_profit_comment(), parse_mode="Markdown")
        bot.register_next_step_handler(message, add_profit_comment, float(profit_value))
    else:
        bot.send_message(chat_id, mes.wrong_expense_value(), parse_mode="Markdown")
        bot.send_message(chat_id, mes.function_list(), parse_mode="Markdown")


def add_profit_comment(message: Message, profit_value: float) -> None:
    """ ADD EXPENSE IN HISTORY FOR USER """

    profit_comment = message.text
    chat_id = message.chat.id
    today_date = str(datetime.now().date().strftime('%d.%m.%Y'))

    add_response = db.add_profit(chat_id, profit_value, profit_comment, today_date)
    if add_response:
        bot.send_message(chat_id, mes.success_add_profit(), parse_mode="Markdown")
    else:
        bot.send_message(chat_id, mes.wrong_add_profit(), parse_mode="Markdown")


if __name__ == '__main__':
    logger.add('logger.log', level='DEBUG', format='{time} {level} {message}', encoding='utf-8')
    bot.polling(none_stop=True, interval=0)
