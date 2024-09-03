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
            f'*/period_history* – Список затрат в текущем периоде\n'
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


def history_message(user: dict) -> str:

    histories = user['expense_history']

    if histories:
        output_str = f"Ваша история: "
        for history in histories:
            history_str = (
                f"\n\n{history['id'] + 1}. Период *{user['start_date']} – {user['end_date']}*\n"
                f"Бюджет на период: *{history['start_budget']}* RUB\nДневной бюджет: *{history['start_daily_budget']}* RUB\n"
            )
            for expense in history['expenses']:
                history_str += f"Затраты"

            for profit in history['profits']:
                history_str += f"Доходы"

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


######################################### WRONG MESSAGES ################################################
def wrong_date() -> str:
    return f"Введенная дата не соответствует необходимому формату (*01.01.2024*)\nПопробуйте ввести дату заново: "


def wrong_date_early() -> str:
    return f"Введенная дата не может быть меньше даты начала периода\nПопробуйте ввести дату заново:"


def wrong_budget() -> str:
    return f"Вы ввели некорректную сумму.\nПопробуйе еще раз"


def wrong_save_budget() -> str:
    return f"Прошу прощения, к сожалению не удалось рассчитать и сохранить бюджет...\nПопробуйте позже"


def wrong_clear_history_message() -> str:
    return f"Прошу прощения, к сожалению не удалось удалить Вашу историю...\nПопробуйте позже"


######################################### WRONG MESSAGES ################################################
def delete_history() -> str:
    return f"Да, я хочу удалить всю историю"


def back_delete_history() -> str:
    return f"Нет, я передумал"
