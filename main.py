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
    else:
        bot.send_message(chat_id, mes.function_list(), parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call: CallbackQuery) -> None:
    """ KEYBOARD HANDLER """

    chat_id = call.message.chat.id
    keyboard_command = call.data

    if keyboard_command == "no_delete_history":
        bot.send_message(chat_id, mes.no_clear_history_message(), parse_mode="Markdown")
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
        start = datetime.strptime(start_date, "%d.%m.%Y").date()
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


#     elif message.text == '/add_expenses':
#         if users_dict[message.chat.id].period_budget != 0 and users_dict[message.chat.id].period_budget:
#             bot.send_message(message.chat.id, add_expenses_msg())
#             bot.register_next_step_handler(message, add_expenses)
#         else:
#             bot.send_message(message.chat.id, input_budget())
#             bot.register_next_step_handler(message, set_budget)
#     elif message.text == '/add_profit':
#         bot.send_message(message.chat.id, add_profit_msg())
#         bot.register_next_step_handler(message, add_profit)
#     elif message.text == '/period_history':
#         user = users_dict[message.chat.id]
#         bot.send_message(message.chat.id, user.period_history())
#     else:
#         bot.send_message(message.chat.id, function_list())
#
#
# def add_expenses(message: Message) -> None:
#     expenses_value = message.text
#     user_id = message.chat.id
#     user = users_dict[user_id]
#     today = str(datetime.now().date().strftime('%d.%m.%Y'))
#
#     try:
#         print(user.expenses_history.keys())
#         print(today)
#         if today in user.expenses_history.keys():
#             user.expenses_history[today]['value'] += float(expenses_value)
#             user.period_budget -= float(expenses_value)
#         else:
#             user.expenses_history[today] = dict()
#             user.expenses_history[today]['value'] = float(expenses_value)
#             user.period_budget -= float(expenses_value)
#         user.set_day_budget()
#         bot.send_message(user_id, add_expenses_add_comment())
#         bot.register_next_step_handler(message, add_expenses_comment)
#     except Exception as error:
#         logger.error(f"Wrong input expenses value = {expenses_value} by {user}. Error: {error}")
#         bot.send_message(user_id, 'Введено неверная сумма трат...\nПопробуйте снова')
#         bot.register_next_step_handler(message, add_expenses)
#
#
# def add_expenses_comment(message: Message) -> None:
#     expenses_comment = message.text
#     user_id = message.chat.id
#     user = users_dict[user_id]
#     today = str(datetime.now().date().strftime('%d.%m.%Y'))
#
#     try:
#         if 'comment' in user.expenses_history[today].keys():
#             user.expenses_history[today]['comment'] += f"{expenses_comment}\n"
#         else:
#             user.expenses_history[today]['comment'] = f"{expenses_comment}\n"
#         bot.send_message(user_id, add_expenses_success())
#         bot.send_message(message.chat.id, balance(user.period_budget, user.day_budget, user.start_period_date, user.end_period_date))
#     except Exception as error:
#         logger.error(f"Wrong input expenses value = {expenses_comment} by {user}. Error: {error}")
#         bot.send_message(user_id, 'Некорректный ввод...\nПопробуйте снова')
#         bot.register_next_step_handler(message, add_expenses_comment)
#
#
# def add_profit(message: Message) -> None:
#     profit_value = message.text
#     user_id = message.chat.id
#     user = users_dict[user_id]
#
#     try:
#         user.period_budget += float(profit_value)
#         user.set_day_budget()
#         bot.send_message(user_id, add_profit_success())
#         bot.send_message(message.chat.id, balance(user.period_budget, user.day_budget, user.start_period_date, user.end_period_date))
#     except Exception as error:
#         logger.error(f"Wrong input profit value = {profit_value} by {user}. Error: {error}")
#         bot.send_message(user_id, 'Введено неверная сумма прибыли...\nПопробуйте снова')
#         bot.register_next_step_handler(message, add_profit)


if __name__ == '__main__':
    logger.add('logger.log', level='DEBUG', format='{time} {level} {message}', encoding='utf-8')
    bot.polling(none_stop=True, interval=0)
