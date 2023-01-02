from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_keyboard = InlineKeyboardMarkup()
admin_load = InlineKeyboardButton(text='ДОДАТИ СТРАВУ', callback_data='admin_load')
admin_delete = InlineKeyboardButton(text='ВИДАЛИТИ СТРАВУ', callback_data='admin_delete')
admin_edit = InlineKeyboardButton(text='РЕДАГУВАТИ СТРАВУ', callback_data='admin_edit')
admin_quit = InlineKeyboardButton(text='ВИЙТИ', callback_data='admin_quit')
admin_back = InlineKeyboardButton(text="НАЗАД", callback_data='admin_back')
admin_keyboard.add(admin_load, admin_edit).add(admin_delete).add(admin_quit)

admin_back_keyboard = InlineKeyboardMarkup()
admin_back_keyboard.add(admin_back)