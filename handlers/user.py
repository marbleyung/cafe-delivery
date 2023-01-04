import sqlite3 as sql
from aiogram import Bot
from aiogram.types import LabeledPrice

from environs import Env
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.database import cur, sql_select_user, sql_delete_user
from lexicon.lexicon import LEXICON_EN, LEXICON_UA
from keyboards import menu_kb as mkb
from dataclasses import dataclass
from services import order_process
from database import database
from handlers.admin import _isadmin


@dataclass
class Order(StatesGroup):
    pizza = State()
    add_pizza = State()
    steak = State()
    add_steak = State()

    delivery_type = State()
    delivery_time = State()
    payment_type = State()
    details = State()
    payed = State()


async def process_help_command(message, state: FSMContext):
    await message.answer(f"{LEXICON_EN['/help']}\n"
                         f"Також є зручне меню зліва, в якому наявні всі команди")
    await state.finish()


async def process_cart_command(message, state: FSMContext):
    result = order_process.check_order(message.from_user.id)
    await message.answer(text=result, reply_markup=mkb.make_order_kb)
    await state.finish()


async def process_quit_command(message, state: FSMContext):
    await message.answer("До побачення!")
    await state.finish()


async def process_me_command(message, state: FSMContext):
    await state.finish()
    data = message.from_user.id
    result = sql_select_user(data)
    if isinstance(result, tuple):
        await message.answer(text=f"Ваше ім'я: {result[1]}\nВаш телефон: {result[2]}\n"
                                  f"Ваша адреса: {result[3]}")
    else:
        await message.answer(text=result)


async def process_del_command(message, state: FSMContext):
    await state.finish()
    data = message.from_user.id
    result = sql_delete_user(data)
    if result == 'Ваш запис видалено':
        await message.answer(text=f"{result}. Щоб зареєструватись, просто пропишіть /start")
    else:
        await message.answer(text=f"{result}")


async def process_m_command(message, state: FSMContext):
    await state.finish()

    for r in cur.execute('SELECT photo, category FROM menu GROUP BY category').fetchall():
        await message.answer_photo(r[0], f'{r[1].upper()}')
    await message.answer(text="Оберіть страву, яку хочете скуштувати", reply_markup=mkb.menu_kb)

async def process_about_command(message, state: FSMContext):
    await message.answer(LEXICON_UA['/about'])
    await state.finish()


async def process_pizza_press(callback):
    await callback.message.edit_text(text='Оберіть піццу (натисніть, щоб дізнатись більше)',
                                     reply_markup=mkb.pizza_kb)
    await callback.answer()


async def process_choice_pizza(callback, state: FSMContext):
    chosen_pizza = callback.data.split('_')[1:]
    chosen_pizza = ' '.join(chosen_pizza).title()
    await Order.pizza.set()
    await state.update_data(pizza=chosen_pizza)
    base = sql.connect('menu.db')
    curs = base.cursor()
    pizza_info = curs.execute("SELECT * FROM menu WHERE name = ?", (chosen_pizza,)).fetchone()
    await callback.message.answer_photo(pizza_info[0])
    await callback.message.answer(text=f'{pizza_info[2]}\n{pizza_info[3]}\n{pizza_info[-1]}',
                                  reply_markup=mkb.add_or_back_kb)
    await callback.answer()
    curs.close()
    base.close()
    await Order.next()


async def process_add_to_pizza(callback, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    user_data = sql_select_user(user_id)
    dish_data = database.sql_select_dish_with_data(data['pizza'])
    insert_data = [i for i in user_data]
    price = int(dish_data[-1].split()[0])
    insert_data.append(dish_data[2])
    insert_data.append(price)
    result = order_process.add_to_order(insert_data)
    amount = order_process.check_howmany_dish_in_order((insert_data[0], insert_data[-2]))
    amount = amount[0][0]
    await callback.message.edit_text(text=f'{amount} {data["pizza"]} у кошику',
                                     reply_markup=mkb.pizza_kb)
    await callback.answer(text=result)
    await state.finish()


async def process_del_from_pizza(callback, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    dish = data['pizza']
    result = order_process.delete_from_order(user_id, dish)
    amount = order_process.check_howmany_dish_in_order((user_id, dish))
    amount = amount[0][0]
    await callback.message.edit_text(text=f'{amount} {data["pizza"]} у кошику',
                                     reply_markup=mkb.pizza_kb)
    await callback.answer(text=result)
    await state.finish()


async def process_back_to_pizza_press(callback, state: FSMContext):
    await callback.message.edit_text(text='Оберіть піццу (натисніть, щоб дізнатись більше)',
                                     reply_markup=mkb.pizza_kb)
    await state.finish()


async def process_steak_press(callback):
    await callback.message.edit_text(text='Оберіть стейк (натисніть, щоб дізнатись більше)',
                                     reply_markup=mkb.steak_kb)
    await callback.answer()


async def process_choice_steak(callback, state: FSMContext):
    chosen_steak = callback.data.split('_')[1:]
    chosen_steak = ' '.join(chosen_steak).title()
    await Order.steak.set()
    await state.update_data(steak=chosen_steak)
    base = sql.connect('menu.db')
    curs1 = base.cursor()
    steak_info = curs1.execute("SELECT * FROM menu WHERE name = ?", (chosen_steak,)).fetchone()
    await callback.message.answer_photo(steak_info[0])
    await callback.message.answer(text=f'{steak_info[2]}\n{steak_info[3]}\n{steak_info[-1]}',
                                  reply_markup=mkb.add_or_back_kb)
    await callback.answer()
    curs1.close()
    base.close()
    await Order.next()


async def process_add_to_steak(callback, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    user_data = sql_select_user(user_id)
    dish_data = database.sql_select_dish_with_data(data['steak'])
    insert_data = [i for i in user_data]
    price = int(dish_data[-1].split()[0])
    insert_data.append(dish_data[2])
    insert_data.append(price)
    result = order_process.add_to_order(insert_data)
    amount = order_process.check_howmany_dish_in_order((insert_data[0], insert_data[-2]))
    amount = amount[0][0]
    await callback.message.edit_text(text=f'{amount} {data["steak"]} у кошику',
                                     reply_markup=mkb.steak_kb)
    await callback.answer(text=result)
    await state.finish()


async def process_del_from_steak(callback, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    dish = data['steak']
    result = order_process.delete_from_order(user_id, dish)
    amount = order_process.check_howmany_dish_in_order((user_id, dish))
    amount = amount[0][0]
    await callback.message.edit_text(text=f'{amount} {data["steak"]} у кошику',
                                     reply_markup=mkb.steak_kb)
    await callback.answer(text=result)
    await state.finish()


async def process_back_to_steak_press(callback, state: FSMContext):
    await callback.message.edit_text(text='Оберіть стейк (натисніть, щоб дізнатись більше)',
                                     reply_markup=mkb.steak_kb)
    await state.finish()


async def process_to_menu_press(callback, state: FSMContext):
    await state.finish()
    await callback.message.answer(text="Оберіть страву", reply_markup=mkb.menu_kb)
    await callback.answer()


async def process_check_order_press(callback):
    result = order_process.check_order(callback.from_user.id)
    await callback.message.edit_text(text=result, reply_markup=mkb.make_order_kb)
    await callback.answer()


async def make_order_press(callback):
    result = order_process.check_order(callback.from_user.id)
    if 'СУМА ЗАМОВЛЕННЯ: None UAH' in result:
        await callback.message.edit_text(text="Спочатку додайте товари до корзини",
                                         reply_markup=mkb.menu_kb)
        await callback.answer()
    else:
        await callback.message.edit_text(text=f"Оберіть спосіб доставки\n"
                                              f"{LEXICON_UA['/about']}",
                                         reply_markup=mkb.delivery_type)
        await callback.answer()
        await Order.delivery_type.set()


async def process_delivery_type(callback, state: FSMContext):
    await state.update_data(delivery_type=callback.data)
    await callback.message.edit_text(text="На який час готувати замовлення?",
                                     reply_markup=mkb.delivery_time)
    await callback.answer()
    await Order.next()


async def process_delivery_time(callback, state: FSMContext):
    await state.update_data(delivery_time=callback.data)
    await callback.message.edit_text(text='Виберіть спосіб оплати\nНе бійтесь, оплата в '
                                          'телеграмі цілком безпечна і дуже зручна!',
                                     reply_markup=mkb.payment_type)
    await callback.answer()
    await Order.next()


async def process_online_payment(callback, state: FSMContext):
    await state.update_data(payment_type=callback.data)
    await callback.message.edit_text(text=f'ONLINE PAYMENT\nЯкщо ви маєте що додати або відредагувати,'
                                          'напишіть це тут\n(або відправте будь-який символ, якщо все окей)\n'
                                          'Ви перейдете до платежу')
    await callback.answer()
    await Order.next()


async def process_offline_payment(callback, state: FSMContext):
    await state.update_data(payment_type=callback.data)
    await callback.message.edit_text(text='OFFLINE PAYMENT\nЯкщо ви маєте що додати або відредагувати,'
                                          'напишіть це тут\n(або відправте будь-що, якщо все окей)')
    await callback.answer()
    await Order.next()


async def process_details(message, state: FSMContext):
    user_cart = order_process.check_order(message.from_user.id)
    order_process.delete_confirmed_order(message.from_user.id)
    await state.update_data(details=message.text)
    data = await state.get_data()
    await message.answer(text=f"Замовлення прийнято в обробку\n"
                              f"Ми зв'яжемось з вами")
    env = Env()
    env.read_env(r'C:\Users\snapk\PycharmProjects\Alpha\cafe_delievery_bot\.env')
    payment_token = env("PAYMENT_TOKEN")
    bot = Bot(token=env("BOT_TOKEN"))
    admin_ids = _isadmin()
    data = await state.get_data()

    user_sum = int(user_cart[:user_cart.find(' UAH')].split()[2])
    if user_sum < 500 and data['delivery_type'] == 'courier_delivery':
        user_sum += 120
    user_cart = str(user_cart[:user_cart.find(":") + 1]) + ' ' + str(user_sum) + ' UAH'
    user_info = sql_select_user(message.from_user.id)
    user_info = f"ЗАМОВЛЕННЯ:\nІм'я: {user_info[1]}\nТелефон: {user_info[2]}\n" \
                f"Адреса: {user_info[3]}\n"

    data = f"Спосіб доставки: {data['delivery_type']}\n" \
           f"Час доставки: {data['delivery_time']}\n" \
           f"Тип сплати: {data['payment_type']}\n" \
           f"Деталі: {data['details']}"

    for i in admin_ids:
        await bot.send_message(i, user_info + user_cart + '\n'
                               + data)

    await bot.close()
    data = await state.get_data()
    if data['payment_type'] == 'pay_online':
        final_sum = [LabeledPrice(amount=user_sum * 100, label='Сума')]
        await bot.send_invoice(chat_id=message.from_user.id,
                               title='СПЛАТИТИ ЗАМОВЛЕННЯ',
                               description="Доставка їжі Cafe Delivery",
                               payload='payload',
                               provider_token=payment_token,
                               currency='uah',
                               prices=final_sum)
        await Order.next()
        await bot.close()
        await state.finish()
    else:
        await state.finish()


async def is_payed():
    pass


def register_user_handlers(dp):
    dp.register_message_handler(process_help_command, commands='help', state='*')
    dp.register_message_handler(process_about_command, commands='about', state='*')
    dp.register_message_handler(process_cart_command, commands='cart', state='*')
    dp.register_message_handler(process_me_command, commands='me', state='*')
    dp.register_message_handler(process_quit_command, commands=['q', 'quit'], state='*')
    dp.register_message_handler(process_del_command, commands='del', state='*')
    dp.register_message_handler(process_m_command, commands=['m', 'menu'], state='*')
    dp.register_callback_query_handler(process_pizza_press, text='pizza')
    dp.register_callback_query_handler(process_choice_pizza, text=['pizza_margherita', 'pizza_pepperoni',
                                                                   'pizza_diavola', 'pizza_quattro_formaggi',
                                                                   'pizza_calzone'])

    dp.register_callback_query_handler(process_steak_press, text='steak')
    dp.register_callback_query_handler(process_choice_steak, text=['steak_beef', 'steak_pork', 'steak_chicken'])
    dp.register_callback_query_handler(process_to_menu_press, text='to_menu', state='*')

    dp.register_callback_query_handler(process_add_to_pizza, text='add_to', state=Order.add_pizza)
    dp.register_callback_query_handler(process_del_from_pizza, text='del_from', state=Order.add_pizza)
    dp.register_callback_query_handler(process_back_to_pizza_press, text='back_to', state=Order.add_pizza)

    dp.register_callback_query_handler(process_add_to_steak, text='add_to', state=Order.add_steak)
    dp.register_callback_query_handler(process_del_from_steak, text='del_from', state=Order.add_steak)
    dp.register_callback_query_handler(process_back_to_steak_press, text='back_to', state=Order.add_steak)

    dp.register_callback_query_handler(process_check_order_press, text='check_order')
    dp.register_callback_query_handler(make_order_press, text='make_order')
    dp.register_callback_query_handler(process_delivery_type, text=['self_delivery',
                                                                    'courier_delivery'],
                                       state=Order.delivery_type)
    dp.register_callback_query_handler(process_delivery_time, text=['asap_time',
                                                                    'another_time'],
                                       state=Order.delivery_time)
    dp.register_callback_query_handler(process_online_payment, text='pay_online', state=Order.payment_type)
    dp.register_callback_query_handler(process_offline_payment, text=['pay_offline_cash',
                                                                      'pay_offline_card'],
                                       state=Order.payment_type)
    dp.register_message_handler(process_details, state=Order.details)
    dp.register_message_handler(is_payed, state=Order.payed)
