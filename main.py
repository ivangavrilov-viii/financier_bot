from bot_users.class_user import BotUser
from telebot.types import Message
from decouple import config
from loguru import logger
from typing import Dict
import telebot

from datetime import datetime
from messages import *


bot = telebot.TeleBot(config('financier_by_gavrilov_bot'))
users_dict: Dict[int, BotUser] = dict()


@bot.message_handler(content_types=['text'])
def start(message: Message) -> None:
    """ Функция вызова и обработки основных команд бота """

    global users_dict

    if message.text == '/start':
        if message.chat.id not in users_dict:
            users_dict[message.chat.id] = BotUser(message.chat)
        bot.send_message(message.chat.id, start_message(message))
        bot.send_message(message.chat.id, function_list())
    elif message.text == '/help':
        bot.send_message(message.chat.id, function_list())
    elif message.text == '/set_budget':
        bot.send_message(message.chat.id, input_budget())
        bot.register_next_step_handler(message, set_budget)
    elif message.text == '/balance':
        user = users_dict[message.chat.id]
        user.show_balance()
        today = datetime.strftime(datetime.now().date(), "%d.%m.%Y")
        bot.send_message(message.chat.id, show_balance_msg(user.period_budget, user.day_budget, today, user.end_period_date))
    elif message.text == '/add_expenses':
        if users_dict[message.chat.id].period_budget != 0 and users_dict[message.chat.id].period_budget:
            bot.send_message(message.chat.id, add_expenses_msg())
            bot.register_next_step_handler(message, add_expenses)
        else:
            bot.send_message(message.chat.id, input_budget())
            bot.register_next_step_handler(message, set_budget)
    elif message.text == '/add_profit':
        bot.send_message(message.chat.id, add_profit_msg())
        bot.register_next_step_handler(message, add_profit)
    elif message.text == '/period_history':
        user = users_dict[message.chat.id]
        bot.send_message(message.chat.id, user.period_history())
    else:
        bot.send_message(message.chat.id, function_list())


def set_budget(message: Message) -> None:
    budget_value = message.text
    user_id = message.chat.id

    try:
        users_dict[user_id].period_budget = float(budget_value)
        bot.send_message(user_id, input_start_period())
        bot.register_next_step_handler(message, set_start_period)
    except Exception as error:
        logger.error(f"Wrong input budget value = {budget_value} by {users_dict[user_id]}. Error: {error}")
        bot.send_message(user_id, 'Введено неверное значение суммы...\nПопробуйте снова')
        bot.register_next_step_handler(message, set_budget)


def set_start_period(message: Message) -> None:
    start_date = message.text
    user_id = message.chat.id

    try:
        start_day, start_month = start_date.split('.')
        if 32 > int(start_day) > 0 and start_day.isdigit() and 13 > int(start_month) > 0 and start_month.isdigit():
            users_dict[user_id].start_day_date = int(start_day)
            users_dict[user_id].start_month_date = int(start_month)
            users_dict[user_id].month = datetime.now().date().month
            bot.send_message(user_id, input_end_period())
            bot.register_next_step_handler(message, set_end_period)
        else:
            logger.error(f"Wrong input start period date value = {start_date} by {users_dict[user_id]}.")
            bot.send_message(user_id, 'Введено неверное число месяца...\nПопробуйте снова')
            bot.register_next_step_handler(message, set_start_period)
    except Exception as error:
        logger.error(f"Wrong input start period date value = {start_date} by {users_dict[user_id]}. Error: {error}")
        bot.send_message(user_id, 'Введено неверная дата...\nПопробуйте снова')
        bot.register_next_step_handler(message, set_start_period)


def set_end_period(message: Message) -> None:
    end_date = message.text
    user_id = message.chat.id
    user = users_dict[message.chat.id]

    try:
        end_day, end_month = end_date.split('.')
        if 32 > int(end_day) > 0 and end_day.isdigit() and 13 > int(end_month) > 0 and end_month.isdigit():
            users_dict[user_id].end_day_date = int(end_day)
            users_dict[user_id].end_month_date = int(end_month)
            start_date, end_date = user.set_day_budget()
            users_dict[user_id].start_period_date = start_date
            users_dict[user_id].end_period_date = end_date
            bot.send_message(user_id, success_set_budget(user.period_budget, user.day_budget, start_date, end_date))
        else:
            logger.error(f"Wrong input end period date value = {end_date} by {users_dict[user_id]}.")
            bot.send_message(user_id, 'Введено неверная дата...\nПопробуйте снова')
            bot.register_next_step_handler(message, set_end_period)
    except Exception as error:
        logger.error(f"Wrong input end period date value = {end_date} by {users_dict[user_id]}. Error: {error}")
        bot.send_message(user_id, 'Введено неверное число месяца...\nПопробуйте снова')
        bot.register_next_step_handler(message, set_end_period)


def add_expenses(message: Message) -> None:
    expenses_value = message.text
    user_id = message.chat.id
    user = users_dict[user_id]
    today = str(datetime.now().date().strftime('%d.%m.%Y'))

    try:
        print(user.expenses_history.keys())
        print(today)
        if today in user.expenses_history.keys():
            user.expenses_history[today]['value'] += float(expenses_value)
            user.period_budget -= float(expenses_value)
        else:
            user.expenses_history[today] = dict()
            user.expenses_history[today]['value'] = float(expenses_value)
            user.period_budget -= float(expenses_value)
        user.set_day_budget()
        bot.send_message(user_id, add_expenses_add_comment())
        bot.register_next_step_handler(message, add_expenses_comment)
    except Exception as error:
        logger.error(f"Wrong input expenses value = {expenses_value} by {user}. Error: {error}")
        bot.send_message(user_id, 'Введено неверная сумма трат...\nПопробуйте снова')
        bot.register_next_step_handler(message, add_expenses)


def add_expenses_comment(message: Message) -> None:
    expenses_comment = message.text
    user_id = message.chat.id
    user = users_dict[user_id]
    today = str(datetime.now().date().strftime('%d.%m.%Y'))

    try:
        if 'comment' in user.expenses_history[today].keys():
            user.expenses_history[today]['comment'] += f"{expenses_comment}\n"
        else:
            user.expenses_history[today]['comment'] = f"{expenses_comment}\n"
        bot.send_message(user_id, add_expenses_success())
        bot.send_message(message.chat.id, balance(user.period_budget, user.day_budget, user.start_period_date, user.end_period_date))
    except Exception as error:
        logger.error(f"Wrong input expenses value = {expenses_comment} by {user}. Error: {error}")
        bot.send_message(user_id, 'Некорректный ввод...\nПопробуйте снова')
        bot.register_next_step_handler(message, add_expenses_comment)


def add_profit(message: Message) -> None:
    profit_value = message.text
    user_id = message.chat.id
    user = users_dict[user_id]

    try:
        user.period_budget += float(profit_value)
        user.set_day_budget()
        bot.send_message(user_id, add_profit_success())
        bot.send_message(message.chat.id, balance(user.period_budget, user.day_budget, user.start_period_date, user.end_period_date))
    except Exception as error:
        logger.error(f"Wrong input profit value = {profit_value} by {user}. Error: {error}")
        bot.send_message(user_id, 'Введено неверная сумма прибыли...\nПопробуйте снова')
        bot.register_next_step_handler(message, add_profit)


def start_message(message: Message) -> str:
    if message.chat.first_name is not None:
        return f'Здравствуйте, {message.chat.first_name} 👋\n' \
               f'Это финансовый бот, разработанный @gavril_23\n'
    return f'Здравствуйте 👋\n' \
           f'Это финансовый бот, разработанный @gavril_23\n'


if __name__ == '__main__':
    logger.add('logger.log', level='DEBUG', format='{time} {level} {message}', encoding='utf-8')
    bot.polling(none_stop=True, interval=0)
