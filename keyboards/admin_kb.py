from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_keyboard = InlineKeyboardMarkup(row_width=2)
admin_load = InlineKeyboardButton(text='ADD DISH', callback_data='admin_load')
admin_delete = InlineKeyboardButton(text='DELETE DISH', callback_data='admin_delete')
admin_edit = InlineKeyboardButton(text='EDIT DISH (text)', callback_data='admin_edit')
admin_edit_photo = InlineKeyboardButton(text='EDIT DISH (img)', callback_data='admin_edit_photo')
admin_quit = InlineKeyboardButton(text='QUIT', callback_data='admin_quit')
admin_back = InlineKeyboardButton(text="BACK", callback_data='admin_back')
admin_get_menu = InlineKeyboardButton(text="LIST OF ITEMS", callback_data='admin_get_menu')
admin_get_advanced_menu = InlineKeyboardButton(text='ADVANCED LIST', callback_data='admin_get_advanced_menu')
admin_keyboard.add(admin_load, admin_edit, admin_edit_photo, admin_delete).add(admin_get_menu, admin_get_advanced_menu).add(admin_quit)


admin_edit_keyboard = InlineKeyboardMarkup(row_width=2)
edit_category = InlineKeyboardButton(text='CATEGORY', callback_data='edit_category')
edit_name = InlineKeyboardButton(text='NAME ', callback_data='edit_name')
edit_description = InlineKeyboardButton(text='DESCRIPTION', callback_data='edit_description')
edit_price = InlineKeyboardButton(text='PRICE', callback_data='edit_price')
admin_edit_keyboard.add(edit_category, edit_name, edit_description, edit_price).add(admin_back)

admin_back_keyboard = InlineKeyboardMarkup()
admin_back_keyboard.add(admin_back)