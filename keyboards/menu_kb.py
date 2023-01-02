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
order = InlineKeyboardButton(text='MAKE ORDER', callback_data='make_order')
add_to = InlineKeyboardButton(text='ADD TO ORDER', callback_data='add_to_order')
back = InlineKeyboardButton(text='BACK', callback_data='back')
check_order = InlineKeyboardButton(text='CHECK MY ORDER', callback_data='check_order')
pizza_kb.add(pizza_1, pizza_2, pizza_3, pizza_4, pizza_5).add(order, add_to).add(check_order).add(back)


steak_kb = InlineKeyboardMarkup()
steak_1 = InlineKeyboardButton(text='Beef'.upper(), callback_data='steak_beef')
steak_2 = InlineKeyboardButton(text='Pork'.upper(), callback_data='steak_pork')
steak_3 = InlineKeyboardButton(text='Chicken'.upper(), callback_data='steak_chicken')
steak_kb.add(steak_1, steak_2, steak_3).add(order, add_to).add(check_order).add(back)