from decouple import config
from loguru import logger
import init.utils as u
import sqlite3


DB_NAME = config('db_name')
admin_list = [int(config('admin_1'))]


# UPDATE FUNCTIONS IN DB
def update_in_db(execute_string, params_set, error_message):
    try:
        database = sqlite3.connect(DB_NAME)
        cursor = database.cursor()

        if params_set:
            database.execute(f"{execute_string}", params_set)
        else:
            database.execute(execute_string)

        database.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        logger.error(f'{error_message}: {error}')
    return False


# OPERATIONS WITH USERS TABLE
def create_user_table():
    """ CREATE USER TABLE """

    update_in_db("CREATE TABLE IF NOT EXISTS users("
    "chat_id INTEGER, "
    "role TEXT, "
    "first_name TEXT, "
    "last_name TEXT,  "
    "username TEXT, "
    "daily_budget REAL, "
    "budget REAL, "
    "start_date TEXT, "
    "end_date TEXT, "
    "expense_history TEXT);",
    None,
    "Error with creating user table"
    )


def create_user(chat_message):
    """ CHECK USER IN DB. IF NOT EXIST, CREATE NEW USER """

    user_id = chat_message.id
    create_user_table()
    user_is_exist = user_in_db(user_id)
    role = 'admin' if user_id in admin_list else 'user'

    if not user_is_exist:
        update_in_db("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     (user_id, role, chat_message.first_name, chat_message.last_name, chat_message.username, 0.0, 0.0, None, None, None),
                     "Error with creating new user in DB"
        )


def save_sport_for_user(chat_id, sport):
    return update_in_db(
        f"UPDATE users SET sport='{sport}' WHERE chat_id={chat_id}",
        None,
        f"ERROR | Error with update sport for user(#{chat_id})"
    )


def save_school_for_user(chat_id, school_id):
    return update_in_db(
        f"UPDATE users SET school_id={school_id} WHERE chat_id={chat_id}",
        None,
        f"ERROR | Error with update school_id for user(#{chat_id})"
    )


def save_corpus_for_user(chat_id, corpus_id):
    return update_in_db(
        f"UPDATE users SET corpus_id={corpus_id} WHERE chat_id={chat_id}",
        None,
        f"ERROR | Error with update corpus_id for user(#{chat_id})"
    )


def save_phone_number(chat_id, phone_number):
    return update_in_db(
        f"UPDATE users SET phone={phone_number} WHERE chat_id={chat_id}",
        None,
        f"ERROR | Error with update phone for user(#{chat_id})"
    )


def save_role_for_user(chat_id, role):
    return update_in_db(
        f"UPDATE users SET role='{role}' WHERE chat_id={chat_id}",
        None,
        f"ERROR | Error with update role for user(#{chat_id})"
    )


def user_in_db(user_id):
    """ CHECK USER IN DB BY user_id """

    try:
        database = sqlite3.connect(DB_NAME)
        cursor = database.cursor()
        cursor.execute(f"SELECT * FROM users WHERE chat_id={user_id}")
        response = cursor.fetchall()
        cursor.close()
        if response and response[0]:
            return u.user_to_json(response[0])
    except sqlite3.Error as error:
        logger.error(f'Error with checking user in DB: {error}')
    return False


def user_in_db_by_username(username):
    """ CHECK USER IN DB BY username """

    try:
        database = sqlite3.connect(DB_NAME)
        cursor = database.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
        response = cursor.fetchall()
        cursor.close()
        if response and response[0]:
            return u.user_to_json(response[0])
    except sqlite3.Error as error:
        logger.error(f'Error with checking user in DB: {error}')
    return False


def get_all_users_in_db():
    """ GET ALL USERs IN DB """

    try:
        db = sqlite3.connect(DB_NAME)
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users")
        response = cursor.fetchall()
        cursor.close()
        if response:
            return response
    except sqlite3.Error as error:
        logger.error(f'Error with checking user in DB: {error}')
    return False


def get_user_role(chat_id):
    """ GET ROLE FOR USER IN DB """

    user = user_in_db(chat_id)
    user_role = user["role"] if user else None
    return user_role
