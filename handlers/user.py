import sqlite3 as sql
from database.database import cur, sql_select_user, sql_delete_user
from lexicon.lexicon import LEXICON_EN
from keyboards.menu_kb import menu_kb, pizza_kb, steak_kb


async def process_help_command(message):
    await message.answer(f"{LEXICON_EN['/help']}")


async def process_me_command(message):
    data = message.from_user.id
    result = sql_select_user(data)
    if isinstance(result, tuple):
        await message.answer(text=f"Ваше ім'я: {result[1]}\nВаш телефон: {result[2]}\nВаша адреса: {result[3]}")
    else:
        await message.answer(text=result)


async def process_del_command(message):
    data = message.from_user.id
    result = sql_delete_user(data)
    if result == 'Ваш запис видалено':
        await message.answer(text=f"{result}. Щоб зареєструватись, пропишіть /start")
    else:
        await message.answer(text=f"{result}")


async def process_m_command(message):
    for r in cur.execute('SELECT photo, category FROM menu GROUP BY category').fetchall():
        await message.answer_photo(r[0], f'{r[1].upper()}')
    await message.answer(text="Оберіть страву, яку хочете скуштувати", reply_markup=menu_kb)


async def process_pizza_press(callback):
    await callback.message.edit_text(text='Оберіть піццу (тицяйте, щоб дізнатись більше)',
        reply_markup=pizza_kb)
    await callback.answer()


async def process_choice_pizza(callback):
    chosen_pizza = callback.data.split('_')[1:]
    chosen_pizza = ' '.join(chosen_pizza).title()
    base = sql.connect('menu.db')
    cur = base.cursor()
    pizza_info = cur.execute("SELECT * FROM menu WHERE name = ?", (chosen_pizza,)).fetchone()
    await callback.message.answer_photo(pizza_info[0])
    await callback.message.answer(text=f'{pizza_info[2]}\n{pizza_info[-1]}', reply_markup=pizza_kb)
    await callback.answer()
    cur.close()
    base.close()


async def process_steak_press(callback):
    await callback.message.edit_text(text='Оберіть стейк (тицяйте, щоб дізнатись більше)',
        reply_markup=steak_kb)
    await callback.answer()


async def process_choice_steak(callback):
    chosen_steak = callback.data.split('_')[1:]
    chosen_steak = ' '.join(chosen_steak).title()
    base = sql.connect('menu.db')
    cur = base.cursor()
    steak_info = cur.execute("SELECT * FROM menu WHERE name = ?", (chosen_steak,)).fetchone()
    await callback.message.answer_photo(steak_info[0])
    await callback.message.answer(text=f'{steak_info[2]}\n{steak_info[-1]}', reply_markup=steak_kb)
    await callback.answer()
    cur.close()
    base.close()


async def process_back_press(callback):
    await callback.message.answer(text="Оберіть страву, яку хочете скуштувати", reply_markup=menu_kb)
    await callback.answer()


async def process_make_order_press(callback):
    await callback.answer('Поки що це неможливо')


async def process_add_to_order_press(callback):
    await callback.answer('Страва додана до замовлення')


async def process_check_order_press(callback):
    await callback.answer()


def register_user_handlers(dp):
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(process_me_command, commands='me')
    dp.register_message_handler(process_del_command, commands='del')
    dp.register_message_handler(process_m_command, commands=['m', 'menu'])
    dp.register_callback_query_handler(process_pizza_press, text='pizza')
    dp.register_callback_query_handler(process_choice_pizza, text=['pizza_margherita', 'pizza_pepperoni',
                                                                   'pizza_diavola', 'pizza_quattro_formaggi',
                                                                   'pizza_calzone'])
    dp.register_callback_query_handler(process_steak_press, text='steak')
    dp.register_callback_query_handler(process_choice_steak, text=['steak_beef', 'steak_pork', 'steak_chicken'])
    dp.register_callback_query_handler(process_back_press, text='back')
    dp.register_callback_query_handler(process_make_order_press, text='make_order')
    dp.register_callback_query_handler(process_add_to_order_press, text='add_to_order')
    dp.register_callback_query_handler(process_check_order_press, text='check_order')