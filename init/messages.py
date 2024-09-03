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


def success_save_budget(user: dict) -> str:
    return (
        f"Бюджет успешно установлен !\n\nНачало: *{user['start_date']}*\nКонец: *{user['end_date']}*\n"
        f"Сумма бюджета: *{user['budget']}* RUB\nБюджет на день: *{user['daily_budget']}* RUB\n"
    )


def balance_message(user: dict) -> str:
    start = datetime.now().date()
    end = datetime.strptime(user['end_date'], "%d.%m.%Y").date()
    days_count = (end - start).days + 1

    return (
        f"Сегодня: *{datetime.now().date().strftime('%d.%m.%Y')}*\n"
        f"Информация о действующем периоде:\n\n"
        f"Дата начала: *{user['start_date']}*\n"
        f"Дата окончания: *{user['end_date']}*\n"
        f"Осталось: *{days_count}* дней\n\n"
        f"Остаток бюджета до конца периода:\n*{user['budget']}* _RUB_\n\n"
        f"Актуальный бюджет на день: \n*{user['daily_budget']}* _RUB_"
    )


######################################### WRONG MESSAGES ################################################
def wrong_date() -> str:
    return f"Введенная дата не соответствует необходимому формату (*01.01.2024*)\nПопробуйте ввести дату заново: "


def wrong_date_early() -> str:
    return f"Введенная дата не может быть меньше даты начала периода\nПопробуйте ввести дату заново:"


def wrong_budget() -> str:
    return f"Вы ввели некорректную сумму.\nПопробуйе еще раз"


def wrong_save_budget() -> str:
    return f"Прошу прощения, к сожалению не удалось рассчитать и сохранить бюджет...\nПопробуйте позже"
