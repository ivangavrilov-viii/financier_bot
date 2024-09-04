from datetime import datetime
import json


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
        'expense_history': json.loads(user[9]) if user[9] else None,
    }

    return user_json


def get_days_count(start_date, end_date) -> list:
    """ FORMAT DATES AND DAYS COUNT FOR MESSAGE """

    days = (end_date - start_date).days + 1
    start_date_str = start_date.strftime('%d.%m.%Y')
    end_date_str = end_date.strftime('%d.%m.%Y')

    return [start_date_str, end_date_str, days]


def get_budget_info(start_date, end_date, budget) -> bool:
    """ SET BUDGET FOR USER IN DB """

    budget_info = {
        "daily_budget": round(budget / ((end_date - start_date).days + 1), 2),
        "start_date_str": start_date.strftime('%d.%m.%Y'),
        "end_date_str": end_date.strftime('%d.%m.%Y'),
        "budget": budget,
    }

    return budget_info


def get_expenses(user_info, budget_info) -> str:
    """ CREATE AND FORMAT BUDGET INFO IN JSON AND ADD EXPENSES INFO """

    if user_info["expense_history"] is None:
        user_info["expense_history"] = list()

    expense_dict = {
        "id": len(user_info["expense_history"]),
        "start_date": budget_info["start_date_str"],
        "end_date": budget_info["end_date_str"],
        "start_budget": budget_info["budget"],
        "start_daily_budget": budget_info["daily_budget"],
        "expenses": [],
        "profits": []
    }

    user_info["expense_history"].append(expense_dict)

    return json.dumps(user_info["expense_history"])


def add_expense(user, expense_value, expense_comment, today):
    """ ADD EXPENSE IN USER DICT """

    user["budget"] -= expense_value
    last_period = user['expense_history'][-1]
    expense_id = len(last_period["expenses"])

    last_period["expenses"].append({
        "id": expense_id,
        "date": today,
        "price": expense_value,
        "comment": expense_comment
    })
    return user


def add_profit(user, profit_value, profit_comment, today):
    """ ADD EXPENSE IN USER DICT """

    user["budget"] += profit_value
    last_period = user['expense_history'][-1]
    profit_id = len(last_period["profits"])

    last_period["profits"].append({
        "id": profit_id,
        "date": today,
        "price": profit_value,
        "comment": profit_comment
    })
    return user


def calculate_daily_budget(user):
    """ CALCULATE NEW DAILY BUDGET """

    end_date = datetime.strptime(user["end_date"], "%d.%m.%Y").date()
    days_count = (end_date - datetime.now().date()).days + 1
    new_daily_budget = user["budget"] / days_count

    return round(new_daily_budget, 2)
