from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_keyboard = InlineKeyboardMarkup(row_width=2)
admin_load = InlineKeyboardButton(text='ДОДАТИ СТРАВУ', callback_data='admin_load')
admin_delete = InlineKeyboardButton(text='ВИДАЛИТИ СТРАВУ', callback_data='admin_delete')
admin_edit = InlineKeyboardButton(text='РЕДАГУВАТИ СТРАВУ (текст)', callback_data='admin_edit')
admin_edit_photo = InlineKeyboardButton(text='РЕДАГУВАТИ СТРАВУ (фото)', callback_data='admin_edit_photo')
admin_quit = InlineKeyboardButton(text='ВИЙТИ', callback_data='admin_quit')
admin_back = InlineKeyboardButton(text="НАЗАД", callback_data='admin_back')
admin_get_menu = InlineKeyboardButton(text="ПЕРЕЛІК СТРАВ", callback_data='admin_get_menu')
admin_get_advanced_menu = InlineKeyboardButton(text='РОЗШИРЕНИЙ ПЕРЕЛІК', callback_data='admin_get_advanced_menu')
admin_keyboard.add(admin_load, admin_edit, admin_edit_photo, admin_delete).add(admin_get_menu, admin_get_advanced_menu).add(admin_quit)


admin_edit_keyboard = InlineKeyboardMarkup(row_width=2)
edit_category = InlineKeyboardButton(text='КАТЕГОРІЯ', callback_data='edit_category')
edit_name = InlineKeyboardButton(text='НАЗВА ', callback_data='edit_name')
edit_description = InlineKeyboardButton(text='ОПИС', callback_data='edit_description')
edit_price = InlineKeyboardButton(text='ЦІНА', callback_data='edit_price')
admin_edit_keyboard.add(edit_category, edit_name, edit_description, edit_price).add(admin_back)

admin_back_keyboard = InlineKeyboardMarkup()
admin_back_keyboard.add(admin_back)