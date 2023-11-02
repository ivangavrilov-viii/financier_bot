from datetime import datetime


months = {
    '1': 'Январь',
    '2': 'Февраль',
    '3': 'Март',
    '4': 'Апрель',
    '5': 'Май',
    '6': 'Июнь',
    '7': 'Июль',
    '8': 'Август',
    '9': 'Сентябрь',
    '10': 'Октябрь',
    '11': 'Ноябрь',
    '12': 'Декабрь',
}


def function_list() -> str:
    return (f'Сегодня: {datetime.now().date().strftime("%d.%m.%Y")}\n\n'
            f'Вы можете воспользоваться командами:\n'
            f'/help — Помощь по командам финансового помощника\n'
            f'/set_budget - Установить бюджет на выбранный период\n'
            f'/balance - Посмотреть состояние Вашего счета\n'
            f'/add_expenses - Добавить затраты за день\n'
            f'/add_profit - Добавить прибыль\n'
            f'/period_history - Список затрат в текущем периоде\n')


def input_budget() -> str:
    return f'Введите величину Вашего бюджета:'


def input_start_period() -> str:
    return f"Введите число и месяц для начала периода:\nПример: 01.01"


def input_end_period() -> str:
    return f"Введите число и месяц для конца периода:\nПример: 01.01"


def success_set_budget(budget, day_budget, start, end) -> str:
    return f"Отлично!\nВы установили бюджет: {budget}RUB\nНа срок с {start} по {end} включительно\nВозможная сумма трат за день: {day_budget}RUB"


def balance(budget, day_budget, start, end) -> str:
    return f"Ваш бюджет в размере: {budget}RUB на период с {start} по {end}\nВозможная сумма трат за день: {day_budget}RUB"


def show_balance_msg(budget, day_budget, start, end) -> str:
    return f"Ваш бюджет в размере: {budget}RUB на период с {start} по {end}\nВозможная сумма трат за день: {day_budget}RUB"


def add_expenses_msg() -> str:
    return f"Сегодня {datetime.now().date().strftime('%d.%m.%Y')}\nВведите сумму затрат за день: "


def add_expenses_add_comment() -> str:
    return f"Добавьте комментарий для Ваших сегодняшних затрат:"


def add_expenses_success() -> str:
    return f"Введенная сумма успешно добавлена в траты сегодняшнего дня"


def add_profit_msg() -> str:
    return f"Сегодня {datetime.now().date().strftime('%d.%m.%Y')}\nВведите сумму прибыли за день: "


def add_profit_success() -> str:
    return f"Введенная сумма успешно добавлена к выделенному бюджету"
