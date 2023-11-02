from telebot.types import Chat
from datetime import datetime


class BotUser:
    """ Класс: Пользователь Телеграм-бота. """

    def __init__(self, chat: Chat) -> None:
        self.first_name = chat.first_name
        self.last_name = chat.last_name
        self.username = chat.username
        self.user_id = chat.id
        self.period_budget = float()
        self.day_budget = float()
        self.month = None
        self.start_day_date = int()
        self.start_month_date = int()
        self.end_day_date = int()
        self.end_month_date = int()
        self.start_period_date = str()
        self.end_period_date = str()
        self.expenses_history = dict()

    def __str__(self) -> str:
        return f'First name: {self.first_name}, Last name: {self.last_name}, User ID: {self.user_id}, ' \
               f'Username: @{self.username}'

    def insert_in_table(self) -> list:
        first_name = f'{self.first_name}'
        last_name = f'{self.last_name}'
        username = f'@{self.username}'
        user_id = f'{self.user_id}'

        return [user_id, first_name, last_name, username]

    def set_day_budget(self):
        current_year = datetime.now().date().year
        date1 = datetime.strptime(f"{self.start_day_date}/{self.start_month_date}/{current_year}", '%d/%m/%Y')
        date2 = datetime.strptime(f"{self.end_day_date}/{self.end_month_date}/{current_year}", '%d/%m/%Y')
        day_count = (date2 - date1).days + 1
        budget_for_day = float(self.period_budget / day_count)
        self.day_budget = round(budget_for_day, 2)
        return date1.strftime("%d.%m.%Y"), date2.strftime("%d.%m.%Y")

    def look_history(self):
        for key, value in self.expenses_history.items():
            print(f"{key}: {value}RUB")

    def period_history(self):
        output_string = ""
        history_dict = self.expenses_history
        if history_dict:
            for day, expense in history_dict.items():
                output_string += f"Дата: {day}\nСумма трат: {expense['value']}RUB\nКомментарии: {expense['comment']}\n\n"
            return output_string
        return f"На данный момент Ваша история затрат пуста"

    def show_balance(self):
        today_date = datetime.now()
        date1 = datetime.strptime(f"{today_date.day}/{today_date.month}/{today_date.year}", '%d/%m/%Y')
        date2 = datetime.strptime(f"{self.end_day_date}/{self.end_month_date}/{today_date.year}", '%d/%m/%Y')
        day_count = (date2 - date1).days + 1
        budget_for_day = float(self.period_budget / day_count)
        self.day_budget = round(budget_for_day, 2)
