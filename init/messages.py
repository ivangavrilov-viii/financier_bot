from datetime import datetime


def start_message(message) -> str:
    if message.chat.first_name is not None:
        return f'Здравствуйте, {message.chat.first_name}!\nЭто финансовый бот, разработанный @gavril_23\n'
    return f'Здравствуйте!\nЭто финансовый бот, разработанный @gavril_23\n'


def function_list() -> str:
    return (f'Сегодня: *{datetime.now().date().strftime("%d.%m.%Y")}*\n\n'
            f'Вы можете воспользоваться командами:\n'
            f'*/help* – Помощь по командам финансового помощника\n'
            f'*/set_budget* – Установить бюджет на выбранный период\n'
            f'*/balance* – Посмотреть состояние Вашего счета\n'
            f'*/add_expenses* – Добавить затраты за день\n'
            f'*/add_profit* – Добавить прибыль\n'
            f'*/period_history* – Список затрат в текущем периоде\n')


###################################################################################################
def input_start_date() -> str:
    return f"Введите дату начала периода:\n(Пример: *01.01.2024*)"


def input_end_date() -> str:
    return f"Введите дату окончания периода:\n(Пример: *15.01.2024*)"


def input_budget(start_date, end_date, days_count) -> str:
    return f"Введите сумму выделенного бюджета на период\nс *{start_date}* по *{end_date}* (*{days_count}* дней):"


######################################### WRONG MESSAGES ################################################
def wrong_date() -> str:
    return f"Введенная дата не соответствует необходимому формату (*01.01.2024*)\nПопробуйте ввести дату заново: "


def wrong_date_early() -> str:
    return f"Введенная дата не может быть меньше даты начала периода\nПопробуйте ввести дату заново:"
