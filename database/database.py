import sqlite3 as sql
import aiogram
base = sql.connect('menu.db')
cur = base.cursor()


def sql_add_dish(data):
    menu = sql.connect('menu.db')
    cursor = menu.cursor()
    try:
        cursor.execute("INSERT INTO menu VALUES(?, ?, ?, ?, ?)", tuple(data.values()))
        result = 'Успішно зареєстровано'
    except sql.IntegrityError:
        result = "Ця страва вже є в меню"
    finally:
        menu.commit()
        menu.close()
    return result


def sql_del_dish(data):
    menu = sql.connect('menu.db')
    cursor = menu.cursor()
    try:
        x = cursor.execute('SELECT * from menu WHERE name = ?', data).fetchone()
        cursor.execute("DELETE FROM menu WHERE name = ?", data)
        if not x is None:
            result = 'Успішно видалено'
        else:
            result = "Цієї страви нема в меню"
    except :
        result = "Цієї страви нема в меню"
    finally:
        menu.commit()
        menu.close()
    return result


def sql_add_user(data):
    users_db = sql.connect('users.db')
    cursor = users_db.cursor()
    try:
        cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", data)
        result = 'Успішно зареєстровано'
    except sql.IntegrityError:
        result = "Ви вже були успішно зареєстровані.\nБудь ласка, пропишіть /esc і починайте користуватись ботом"
    finally:
        users_db.commit()
        users_db.close()
    return result


def sql_select_user(data):
    users_db = sql.connect('users.db')
    cursor = users_db.cursor()
    try:
        result = cursor.execute('SELECT * FROM users WHERE id = ?', (data, )).fetchone()
        if result is None:
            result = 'Помилка. Радше за все, ви не зареєстровані. Зареєструйтесь, будь ласка (/start)'
    except:
        result = 'Помилка. Радше за все, ви не зареєстровані. Зареєструйтесь, будь ласка (/start)'
    finally:
        users_db.close()
    return result


def sql_delete_user(data):
    users_db = sql.connect('users.db')
    cursor = users_db.cursor()
    try:
        cursor.execute('DELETE FROM users WHERE id = ?', (data, ))
        result = 'Ваш запис видалено'
    except:
        result = 'Помилка. Радше за все, ви не зареєстровані. Зареєструйтесь, будь ласка (/start)'
    finally:
        users_db.commit()
        users_db.close()
    return result