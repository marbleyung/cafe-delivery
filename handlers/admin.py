from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dataclasses import dataclass
from environs import Env
from database import database
from keyboards.admin_kb import admin_keyboard, admin_back_keyboard, admin_edit_keyboard

@dataclass
class FSMadmin(StatesGroup):
    photo = State()
    category = State()
    name = State()
    description = State()
    price = State()
    name_to_delete = State()

    select = State()
    edit_name = State()
    set_new_name = State()
    edit_photo = State()
    set_new_photo = State()
    edit_category = State()
    set_new_category = State()
    edit_price = State()
    set_new_price = State()
    edit_description = State()
    set_new_description = State()


def _isadmin():
    env = Env()
    env.read_env(r'.env')
    admin_ids = env('ADMIN_IDS').split(',')
    return admin_ids


async def load_admin_panel(message):
    admin_ids = _isadmin()
    if str(message.from_user.id) in admin_ids:
        await message.answer(text='Вітаємо!', reply_markup=admin_keyboard)
    else:
        await message.answer(text='Упс, ця команда не для вас')


async def admin_get_menu(callback):
    result = str(database.sql_get_menu()).replace(')', '').replace('(', '').replace(',,', ',')
    result = result[1:-2]
    await callback.message.answer(text=result, reply_markup=admin_keyboard)
    await callback.answer()


async def admin_get_advanced_menu(callback):
    result = database.sql_get_advanced_menu()
    await callback.message.answer(text=result, reply_markup=admin_keyboard)
    await callback.answer()


async def admin_load(callback):
    await callback.message.edit_text(text='Якщо ви хочете додати нову страву, завантажте фото\n',
                                     reply_markup=admin_back_keyboard)
    await callback.answer()
    await FSMadmin.photo.set()


async def admin_edit(callback):
    await callback.message.edit_text(text="Введіть назву страви, яку потрібно змінити",
                                     reply_markup=admin_back_keyboard)
    await FSMadmin.select.set()


async def select_dish(message, state: FSMContext):
    tmp = message.text.title()
    await state.update_data(select=tmp)
    result = database.sql_select_dish(tmp)
    if result == 'Елемент знайдено. Що редагуємо?':
        await FSMadmin.next()
        await message.answer(text=result, reply_markup=admin_edit_keyboard)
    else:
        await message.answer(text=result, reply_markup=admin_keyboard)
        await state.finish()


async def edit_name(callback, state: FSMContext):
    print(1)
    await state.update_data(edit_name=True)
    await callback.message.edit_text(text='Введіть нову назву', reply_markup=admin_back_keyboard)
    await callback.answer()
    await FSMadmin.next()

async def set_new_name(message, state: FSMContext):
    await state.update_data(set_new_name=message.text.title())
    data = await state.get_data()
    result = database.sql_edit_dish('name', data['select'], data['set_new_name'])
    await message.answer(text=result, reply_markup=admin_keyboard)
    await state.finish()

async def edit_price(callback, state: FSMContext):
    await state.update_data(edit_price=True)
    await callback.message.edit_text(text='Введіть нову ціну', reply_markup=admin_back_keyboard)
    await callback.answer()
    await FSMadmin.next()

async def set_new_price(message, state: FSMContext):
    await state.update_data(set_new_price=message.text.title())
    data = await state.get_data()
    result = database.sql_edit_dish('price', data['select'], data['set_new_price'])
    await message.answer(text=result, reply_markup=admin_keyboard)
    await state.finish()

async def admin_delete(callback):
    await callback.message.edit_text(text='Якщо ви хочете видалити страву, введіть її назву\n'
                         'Наприклад, Margherita для видалення відповідної піци,\n'
                         'Quattro Formaggi для видалення відповідної піци тощо.\n',
                         reply_markup=admin_back_keyboard)
    await callback.answer()
    await FSMadmin.name_to_delete.set()


async def del_dish(message: types.Message, state: FSMContext):
    await state.update_data(name_to_delete=message.text.title())
    data = await state.get_data()
    data = data['name_to_delete'],
    result = database.sql_del_dish(data)
    await message.answer(text=result, reply_markup=admin_keyboard)
    await state.finish()


async def load_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id)
    await FSMadmin.next()
    await message.answer('До якої категорії відноситься страва?')


async def load_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text.lower())
    await FSMadmin.next()
    await message.answer('Як називається страва?')


async def load_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.title())
    await FSMadmin.next()
    await message.answer('Будь ласка, вкажіть інгредієнти, вагу та калорійність (опціонально)')


async def load_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await FSMadmin.next()
    await message.answer('Введіть ціну (ціле число)')


async def load_price(message: types.Message, state: FSMContext):
    await state.update_data(price=f"{message.text} UAH")
    data = await state.get_data()
    database.sql_add_dish(data)
    await message.answer(text='Готово! Страву додано', reply_markup=admin_keyboard)
    await state.finish()


async def admin_back(callback, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(text='Вітаємо!', reply_markup=admin_keyboard)


async def admin_quit(callback, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(text="See you soon")


def register_admin_handlers(dp):
    dp.register_message_handler(load_admin_panel, commands=['admin'], state=None)

    dp.register_callback_query_handler(admin_get_menu, text='admin_get_menu')
    dp.register_callback_query_handler(admin_get_advanced_menu, text='admin_get_advanced_menu')
    dp.register_callback_query_handler(admin_load, text='admin_load')
    dp.register_callback_query_handler(admin_edit, text='admin_edit')
    dp.register_callback_query_handler(admin_delete, text='admin_delete')

    dp.register_message_handler(del_dish, state=FSMadmin.name_to_delete)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMadmin.photo)
    dp.register_message_handler(load_category, state=FSMadmin.category)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_description, state=FSMadmin.description)
    dp.register_message_handler(load_price, state=FSMadmin.price)
    dp.register_message_handler(select_dish, state=FSMadmin.select)


    dp.register_callback_query_handler(edit_name, text='edit_name', state=FSMadmin.edit_name)
    dp.register_message_handler(set_new_name, state=FSMadmin.set_new_name)
    dp.register_callback_query_handler(edit_price, text='edit_price', state=FSMadmin.edit_price)
    dp.register_message_handler(set_new_price, state=FSMadmin.set_new_price)
    dp.register_callback_query_handler(admin_back, text='admin_back', state='*')
    dp.register_callback_query_handler(admin_quit, text='admin_quit', state="*")