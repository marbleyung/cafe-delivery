import sqlite3 as sql


def delete_confirmed_order(data):
    base = sql.connect(r'C:\Users\snapk\PycharmProjects\Alpha\cafe_delievery_bot\orders.db')
    cur = base.cursor()
    try:
        cur.execute("DELETE FROM orders WHERE user_id = ?", (data,))
        result = 'Deleted'
    except Exception as e:
        result = f"{e}"
    finally:
        cur.close()
        base.commit()
        base.close()
    return result


def add_to_order(data):
    base = sql.connect(r'C:\Users\snapk\PycharmProjects\Alpha\cafe_delievery_bot\orders.db')
    cur = base.cursor()
    try:
        cur.execute("INSERT INTO orders(user_id, name, phone, address, dish, price)"
                    " VALUES(?, ?, ?, ?, ?, ?)", data)
        result = 'Успішно додано'
    except Exception as e:
        result = f"Помилка {e}"
    finally:
        cur.close()
        base.commit()
        base.close()
    return result


def delete_from_order(user_id, dish):
    base = sql.connect(r'C:\Users\snapk\PycharmProjects\Alpha\cafe_delievery_bot\orders.db')
    cur = base.cursor()
    try:
        x = cur.execute("SELECT id FROM orders WHERE user_id = ? AND dish = ? LIMIT 1", (user_id, dish)).fetchone()
        x = x[0]
        cur.execute("DELETE FROM orders WHERE id = ? AND user_id = ? AND dish = ?",
                    (x, user_id, dish))
        result = 'Успішно видалено'
    except Exception as e:
        result = f"Помилка {e}"
        print(result)
    finally:
        cur.close()
        base.commit()
        base.close()
    return result


def check_howmany_dish_in_order(data):
    base = sql.connect(r'C:\Users\snapk\PycharmProjects\Alpha\cafe_delievery_bot\orders.db')
    cur = base.cursor()
    try:
        result = cur.execute("SELECT count(user_id) FROM orders WHERE user_id = ? AND "
                             "dish = ?", data).fetchall()
    except Exception as e:
        result = e
    finally:
        cur.close()
        base.close()
    return result


def check_order(data):
    base = sql.connect(r'C:\Users\snapk\PycharmProjects\Alpha\cafe_delievery_bot\orders.db')
    cur = base.cursor()
    try:
        total = cur.execute("SELECT SUM(price) FROM orders WHERE user_id = ?", (data,)).fetchall()[0][0]
        total = f"СУМА ЗАМОВЛЕННЯ: {total} UAH"
        result = cur.execute("SELECT dish FROM orders WHERE user_id = ?",
                             (data,)).fetchall()
        result = [i[0] for i in result]
        amount = []
        for i in result:
            if [i, result.count(i)] not in amount:
                amount.append([i, result.count(i)])

        answer = total + '\n'
        for i in amount:
            answer += str(i) + '\n'
        answer = answer.replace('[', '').replace(']', '')
        answer += '\nЩоб видалити страву, знайдіть її в меню і натисніть "видалити"'.upper()
    except Exception as e:
        amount = e
        total = None
        answer = str(total) + '\n' + str(amount)
    finally:
        cur.close()
        base.close()
    return answer
