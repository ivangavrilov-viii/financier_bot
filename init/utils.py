from datetime import datetime


def user_to_json(user) -> dict:
    """ CONVERT USER FROM DB TO JSON """

    user_json = {
        'chat_id': int(user[0]),
        'role': user[1],
        'name': user[2],
        'second_name': user[3],
        'username': user[4],
        'daily_budget': user[5],
        'budget': user[6],
        'start_date': user[7],
        'end_date': user[8],
        'expense_history': user[9],
    }

    return user_json


def get_days_count(start_date, end_date) -> list:
    """ FORMAT DATES AND DAYS COUNT FOR MESSAGE """

    days = (end_date - start_date).days + 1
    start_date_str = start_date.strftime('%d.%m.%Y')
    end_date_str = end_date.strftime('%d.%m.%Y')

    return [start_date_str, end_date_str, days]
