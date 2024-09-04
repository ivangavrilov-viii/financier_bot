from datetime import datetime, timedelta


def start_message(message) -> str:
    if message.chat.first_name is not None:
        return f'Здравствуйте, {message.chat.first_name}!\nЭто финансовый бот, разработанный @gavril_23\n'
    return f'Здравствуйте!\nЭто финансовый бот, разработанный @gavril_23\n'


def function_list() -> str:
    return (f'Сегодня: *{datetime.now().date().strftime("%d.%m.%Y")}*\n\n'
            f'Вы можете воспользоваться командами:\n'
            f'*/help* – Помощь по командам финансового помощника\n'
            f'*/balance* – Посмотреть состояние Вашего счета\n'
            f'*/period_history* – Список затрат в текущем периоде\n\n'
            f'*/add_expense* – Добавить затраты за день\n'
            f'*/add_profit* – Добавить прибыль\n'
            f'*/update_budget* – Рассчитать дневной бюджет\n\n'
            f'*/set_budget* – Установить бюджет на выбранный период\n'
            f'*/clean_history* – Удалить историю\n')


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

    if user["start_date"] and user["end_date"] and user["budget"]:
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
    return "У Вас нет активного периода\nВоспользуйтесь командой */set_budget* для начала работы"


######################################### HISTORY MESSAGES ################################################
def history_message(user: dict) -> str:

    history = user['expense_history'][-1]

    if history:
        output_str = f"Ваша история: "
        history_str = (
            f"\n\n{history['id'] + 1}. Период _{user['start_date']} – {user['end_date']}_\n"
            f"Бюджет на период: *{history['start_budget']}* RUB\nДневной бюджет: *{history['start_daily_budget']}* RUB\n"
        )

        if history['expenses']:
            history_str += f"\nЗатраты:\n"
            for index, expense in enumerate(history['expenses']):
                history_str += f"*{index + 1}*. {expense['comment']}\nСумма: *{expense['price']}* RUB\n"

        if history['profits']:
            history_str += f"\nДоходы:\n"
            for index, profit in enumerate(history['profits']):
                history_str += f"*{index + 1}*. {profit['comment']}\nСумма: *{profit['price']}* RUB\n"

        output_str += history_str
    else:
        output_str = empty_history_message()
    return output_str


def empty_history_message() -> str:
    return "Ваша история еще пуста\nВоспользуйтесь командой */set_budget* для начала работы"


def clear_history_message() -> str:
    return (
        f"Вы действительно хотите удалить всю Вашу история ?\n"
        f"Ваш действующий период тоже будет удален"
    )


def no_clear_history_message() -> str:
    return f"Хорошо, что Вы передумали !)\nИстория осталась не тронутой"


def success_clear_history_message() -> str:
    return f"Я удалил всю Вашу историю"


######################################### EXPENSE MESSAGES ################################################
def input_expense_value() -> str:
    return f"Введите сумму Вашей траты:"


def no_active_period() -> str:
    return "У Вас нет активного периода\nВоспользуйтесь командой */set_budget* для начала работы"


def input_expense_comment() -> str:
    return f"Введите комментарий для Вашей траты:"


def success_add_expense() -> str:
    return f"Данная сумма успешно добавлена в Ваши траты"


def input_profit_value() -> str:
    return f"Введите сумму Вашей прибыли:"


def input_profit_comment() -> str:
    return f"Введите комментарий для Вашей прибыли:"


def success_add_profit() -> str:
    return f"Данная сумма успешно добавлена в Ваши прибыли"


def update_daily_budget() -> str:
    tommorow = (datetime.now().date() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    tommorow = datetime.strptime(tommorow, '%Y-%m-%d %H:%M:%S')
    delta = tommorow - datetime.now()

    return (
        f"Вы действительно хотите рассчитать дневной бюджет ?\n"
        f"До конца дня еще {delta.seconds // 3600} часов {(delta.seconds // 60) % 60} минут"
    )


def no_update_daily_budget() -> str:
    return f"Хорошо, сумма дневного бюджета осталась прежней"


def success_update_daily_budget_message() -> str:
    return f"Я пересчитал и сохранил новую сумму дневного бюджета"


######################################### WRONG MESSAGES ################################################
def wrong_date() -> str:
    return f"Введенная дата не соответствует необходимому формату (*01.01.2024*)\nПопробуйте ввести дату заново: "


def wrong_date_early() -> str:
    return f"Введенная дата не может быть меньше даты начала периода\nПопробуйте ввести дату заново:"


def wrong_date_today() -> str:
    return f"Введенная дата не может быть раньше, чем сегодня\nПопробуйте ввести дату заново:"


def wrong_budget() -> str:
    return f"Вы ввели некорректную сумму.\nПопробуйе еще раз"


def wrong_save_budget() -> str:
    return f"Прошу прощения, к сожалению не удалось рассчитать и сохранить бюджет...\nПопробуйте позже"


def wrong_clear_history_message() -> str:
    return f"Прошу прощения, к сожалению не удалось удалить Вашу историю...\nПопробуйте позже"


def wrong_expense_value() -> str:
    return f"Введена неверная сумма...\nПопробуйте еще раз"


def wrong_add_expense() -> str:
    return f"Прошу прощения, к сожалению не удалось сохранить трату...\nПопробуйте позже"


def wrong_add_profit() -> str:
    return f"Прошу прощения, к сожалению не удалось сохранить прибыль...\nПопробуйте позже"


def wrong_update_daily_budget_message() -> str:
    return f"Прошу прощения, к сожалению не удалось сделать перерасчет дневного бюджета...\nПопробуйте позже"


######################################### KEYBOARDS MESSAGES ################################################
def delete_history() -> str:
    return f"Да, я хочу удалить всю историю"


def back_delete_history() -> str:
    return f"Нет, я передумал"


def update_daily() -> str:
    return f"Да, я хочу пересчитать дневной бюджет"


def back_update_daily() -> str:
    return f"Нет, я передумал"
