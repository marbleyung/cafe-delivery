from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


yes_no_kb = InlineKeyboardMarkup()
yes_button = InlineKeyboardButton(text='ТАК', callback_data='yes')
no_button = InlineKeyboardButton(text='НІ', callback_data='no')
yes_no_kb.add(yes_button).add(no_button)


menu_kb = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(text='PIZZA', callback_data='pizza')
button_2 = InlineKeyboardButton(text='STEAK', callback_data='steak')
menu_kb.add(button_1).add(button_2)


pizza_kb = InlineKeyboardMarkup(row_width=4)
pizza_1 = InlineKeyboardButton(text='Margherita'.upper(), callback_data='pizza_margherita')
pizza_2 = InlineKeyboardButton(text='Pepperoni'.upper(), callback_data='pizza_pepperoni')
pizza_3 = InlineKeyboardButton(text='Diavola'.upper(), callback_data='pizza_diavola')
pizza_4 = InlineKeyboardButton(text='Quattro Formaggi'.upper(), callback_data='pizza_quattro_formaggi')
pizza_5 = InlineKeyboardButton(text='Calzone'.upper(), callback_data='pizza_calzone')
to_menu = InlineKeyboardButton(text='В МЕНЮ', callback_data='to_menu')
check_order = InlineKeyboardButton(text='ДО КОШИКУ', callback_data='check_order')
pizza_kb.add(pizza_1, pizza_2, pizza_3, pizza_4, pizza_5).add(check_order).add(to_menu)

add_to = InlineKeyboardButton(text='ДОДАТИ ДО ЗАМОВЛЕННЯ', callback_data='add_to')
del_from = InlineKeyboardButton(text='ВИДАЛИТИ ІЗ ЗАМОВЛЕННЯ', callback_data='del_from')
back_to = InlineKeyboardButton(text='НАЗАД', callback_data='back_to')
add_or_back_kb = InlineKeyboardMarkup(row_width=1)
add_or_back_kb.add(add_to, del_from).add(back_to)

steak_kb = InlineKeyboardMarkup()
steak_1 = InlineKeyboardButton(text='Beef'.upper(), callback_data='steak_beef')
steak_2 = InlineKeyboardButton(text='Pork'.upper(), callback_data='steak_pork')
steak_3 = InlineKeyboardButton(text='Chicken'.upper(), callback_data='steak_chicken')
steak_kb.add(steak_1, steak_2, steak_3).add(check_order).add(to_menu)


make_order_kb = InlineKeyboardMarkup()
make_order = InlineKeyboardButton(text='ЗАМОВИТИ', callback_data='make_order')
make_order_kb.add(make_order).add(to_menu)

delivery_type = InlineKeyboardMarkup(row_width=1)
self_delivery = InlineKeyboardButton(text="ЗАБЕРУ САМ", callback_data='self_delivery')
courier_delivery = InlineKeyboardButton(text='ЗАМОВЛЮ КУР`ЄРА', callback_data='courier_delivery')
delivery_type.add(self_delivery, courier_delivery).add(to_menu)

delivery_time = InlineKeyboardMarkup(row_width=1)
asap_time = InlineKeyboardButton(text='НАЙБЛИЖЧИЙ ЧАС', callback_data='asap_time')
another_time = InlineKeyboardButton(text='ІНШИЙ ЧАС', callback_data='another_time')
delivery_time.add(asap_time, another_time, to_menu)

payment_type = InlineKeyboardMarkup(row_width=2)
pay_online = InlineKeyboardMarkup(text='СПЛАТИТИ ТУТ', callback_data='pay_online')
pay_offline_cash = InlineKeyboardMarkup(text='КЕШ ПРИ ОТРИМАННІ', callback_data='pay_offline_cash')
pay_offline_card = InlineKeyboardMarkup(text='КАРТА ПРИ ОТРИМАННІ', callback_data='pay_offline_card')
payment_type.add(pay_online).add(pay_offline_card, pay_offline_cash).add(to_menu)