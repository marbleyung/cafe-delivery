import sqlite3 as sql

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


def sql_get_menu():
    menu = sql.connect('menu.db')
    cursor = menu.cursor()
    result = cursor.execute("SELECT name FROM menu").fetchall()
    print(result)
    menu.close()
    return result


def sql_get_advanced_menu():
    menu = sql.connect('menu.db')
    cursor = menu.cursor()
    result = cursor.execute("SELECT category, name, description, price FROM menu").fetchall()
    result = [' '.join(i) + '\n' for i in result]
    result = '\n'.join(result)
    menu.close()
    return result


def sql_select_dish(data):
    menu = sql.connect('menu.db')
    cursor = menu.cursor()
    try:
        x = cursor.execute('SELECT * from menu WHERE name = ?', (data,)).fetchone()
        if x is not None:
            result = "Елемент знайдено. Що редагуємо?"
        else:
            result = "Цієї страви нема в меню"
    except Exception:
        result = "Цієї страви нема в меню"
    finally:
        menu.commit()
        menu.close()
    return result


def sql_select_dish_with_data(data):
    menu = sql.connect('menu.db')
    cursor = menu.cursor()
    try:
        x = cursor.execute('SELECT * from menu WHERE name = ?', (data,)).fetchone()
        if x is not None:
            result = x
        else:
            result = "Цієї страви нема в меню"
    except Exception:
        result = "Цієї страви нема в меню"
    finally:
        menu.commit()
        menu.close()
    return result


def sql_edit_dish(field, data1, data2):
    menu = sql.connect('menu.db')
    cursor = menu.cursor()
    try:
        cursor.execute(f'UPDATE menu SET {field} = ? WHERE name = ?', (data2, data1))
        result = 'Done!'
    except Exception as e:
        result = 'Щось пішло не так...' + '\n' + str(e)
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
        if x is not None:
            result = 'Успішно видалено'
        else:
            result = "Цієї страви нема в меню"
    except Exception:
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
        result = cursor.execute('SELECT * FROM users WHERE id = ?', (data,)).fetchone()
        if result is None:
            result = 'Помилка. Радше за все, ви не зареєстровані. Зареєструйтесь, будь ласка (/start)'
    except Exception as e:
        result = str(e) + '\n' + 'Помилка. Радше за все, ви не зареєстровані. Зареєструйтесь, будь ласка (/start)'
    finally:
        users_db.close()
    return result


def sql_delete_user(data):
    users_db = sql.connect('users.db')
    cursor = users_db.cursor()
    try:
        cursor.execute('DELETE FROM users WHERE id = ?', (data,))
        result = 'Ваш запис видалено'
    except Exception as e:
        result = str(e) + '\n' + 'Помилка. Радше за все, ви не зареєстровані. Зареєструйтесь, будь ласка (/start)'
    finally:
        users_db.commit()
        users_db.close()
    return result


def sql_mass_send():
    users_db = sql.connect('users.db')
    cursor = users_db.cursor()
    try:
        result = cursor.execute('SELECT id FROM users').fetchall()
        result = [i[0] for i in result]
    except Exception as e:
        result = e
    finally:
        users_db.commit()
        users_db.close()
    return result
