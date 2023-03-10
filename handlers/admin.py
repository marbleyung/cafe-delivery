from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dataclasses import dataclass
from environs import Env
from database import database
from keyboards.admin_kb import admin_keyboard, admin_back_keyboard, admin_edit_keyboard
from asyncio import sleep


@dataclass
class FSMadmin(StatesGroup):
    mass_message = State()
    photo = State()
    category = State()
    name = State()
    description = State()
    price = State()
    name_to_delete = State()

    select_in_db = State()
    edit_text_element = State()
    set_new_text_element = State()

    select_in_db_photo = State()
    set_new_photo_element = State()


def _isadmin():
    env = Env()
    env.read_env(r'.env')
    admin_ids = env('ADMIN_IDS').split(',')
    return admin_ids


async def send_message_to_everyone(message):
    admin_ids = _isadmin()
    if str(message.from_user.id) in admin_ids:
        await message.answer(text='Type the message that will be sent to all users',
                             reply_markup=admin_back_keyboard)
        await FSMadmin.mass_message.set()
    else:
        await message.answer(text='Whoops, this command is not for you')


async def mass_message(message, state: FSMContext):
    await state.update_data(mass_message=message.text)
    result = database.sql_mass_send()
    env = Env()
    env.read_env(r'C:\Users\snapk\PycharmProjects\Alpha\cafe_delievery_bot\.env')
    bot = Bot(token=env('BOT_TOKEN'))
    for i in result:
        await bot.send_message(i, message.text)
        await sleep(.05)

    await bot.close()
    await message.answer(text=f"Sent\n{message.text}", reply_markup=admin_keyboard)
    await state.finish()


async def load_admin_panel(message):
    admin_ids = _isadmin()
    if str(message.from_user.id) in admin_ids:
        await message.answer(text='Hello!', reply_markup=admin_keyboard)
    else:
        await message.answer(text='Whoops, this command is not for you')


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
    await callback.message.edit_text(text='If you want to add a new dish, load a photo\n',
                                     reply_markup=admin_back_keyboard)
    await callback.answer()
    await FSMadmin.photo.set()


async def admin_edit(callback):
    await callback.message.edit_text(text="Enter the name of the dish that is has to be edited",
                                     reply_markup=admin_back_keyboard)
    await FSMadmin.select_in_db.set()


async def admin_edit_photo(callback):
    await callback.message.edit_text(text='Enter the name of the dish, which photo is has to be edited',
                                     reply_markup=admin_back_keyboard)
    await FSMadmin.select_in_db_photo.set()


async def select_dish_photo(message, state: FSMContext):
    tmp = message.text.title()
    await state.update_data(select_in_db_photo=tmp)
    result = database.sql_select_dish(tmp)
    if result == "Item has been found. What is to edit?":
        await FSMadmin.next()
        await message.answer(text=result,
                             reply_markup=admin_back_keyboard)
    else:
        await message.answer(text=result, reply_markup=admin_keyboard)
        await state.finish()


async def set_new_photo_element(message, state: FSMContext):
    await state.update_data(set_new_photo_element=message.photo[0].file_id)
    data = await state.get_data()
    result = database.sql_edit_dish('photo',
                                    data['select_in_db_photo'],
                                    data['set_new_photo_element'])
    await message.answer(text=result, reply_markup=admin_keyboard)
    await state.finish()


async def select_dish(message, state: FSMContext):
    tmp = message.text.title()
    await state.update_data(select_in_db=tmp)
    result = database.sql_select_dish(tmp)
    if result == "Item has been found. What is to edit?":
        await FSMadmin.next()
        await message.answer(text=result, reply_markup=admin_edit_keyboard)
    else:
        await message.answer(text=result, reply_markup=admin_keyboard)
        await state.finish()


async def edit_text_element(callback, state: FSMContext):
    await state.update_data(edit_text_element=callback.data.split('_')[1])
    await callback.message.edit_text(text='Enter new value', reply_markup=admin_back_keyboard)
    await callback.answer()
    await FSMadmin.next()


async def set_new_text_element(message, state: FSMContext):
    await state.update_data(set_new_text_element=message.text)
    data = await state.get_data()

    tmp_category = data['edit_text_element']
    tmp_name = data['set_new_text_element']
    if tmp_category == 'name':
        tmp_name = tmp_name.title()
    elif tmp_category == 'category':
        tmp_name = tmp_name.lower()
    elif tmp_category == 'price':
        tmp_name += ' UAH'
    result = database.sql_edit_dish(data['edit_text_element'],
                                    data['select_in_db'],
                                    tmp_name)
    await message.answer(text=result, reply_markup=admin_keyboard)
    await state.finish()


async def admin_delete(callback):
    await callback.message.edit_text(text='If you want to delete a dish, enter its name\n'
                                          'Margherita to delete pizza Margherita\n'
                                          'Quattro Formaggi to delete pizza Quattro Formaggi',
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
    await message.answer('What is the category of the dish?')


async def load_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text.lower())
    await FSMadmin.next()
    await message.answer('What is the name of the dish?')


async def load_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.title())
    await FSMadmin.next()
    await message.answer('Please, enter weight, calories and ingredients')


async def load_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await FSMadmin.next()
    await message.answer('Enter the price (integer)')


async def load_price(message: types.Message, state: FSMContext):
    await state.update_data(price=f"{message.text} UAH")
    data = await state.get_data()
    database.sql_add_dish(data)
    await message.answer(text='Done! The dish has been added',
                         reply_markup=admin_keyboard)
    await state.finish()


async def admin_back(callback, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(text='Hello!',
                                     reply_markup=admin_keyboard)


async def admin_quit(callback, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(text="See you soon")


def register_admin_handlers(dp):
    dp.register_message_handler(send_message_to_everyone, commands=['massmessage',
                                                                    'mass_message',
                                                                    'mass_dm',
                                                                    'massdm',
                                                                    'send_all',
                                                                    'sendall'])
    dp.register_message_handler(mass_message, state=FSMadmin.mass_message)

    dp.register_message_handler(load_admin_panel, commands=['admin'], state=None)
    dp.register_callback_query_handler(admin_get_menu, text='admin_get_menu')
    dp.register_callback_query_handler(admin_get_advanced_menu, text='admin_get_advanced_menu')
    dp.register_callback_query_handler(admin_load, text='admin_load')
    dp.register_callback_query_handler(admin_delete, text='admin_delete')
    dp.register_callback_query_handler(admin_edit, text='admin_edit')
    dp.register_callback_query_handler(admin_edit_photo, text='admin_edit_photo')

    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMadmin.photo)
    dp.register_message_handler(load_category, state=FSMadmin.category)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_description, state=FSMadmin.description)
    dp.register_message_handler(load_price, state=FSMadmin.price)
    dp.register_message_handler(del_dish, state=FSMadmin.name_to_delete)
    dp.register_message_handler(select_dish, state=FSMadmin.select_in_db)
    dp.register_callback_query_handler(edit_text_element, state=FSMadmin.edit_text_element)
    dp.register_message_handler(set_new_text_element, state=FSMadmin.set_new_text_element)
    dp.register_message_handler(select_dish_photo, state=FSMadmin.select_in_db_photo)
    dp.register_message_handler(set_new_photo_element, content_types=['photo'],
                                state=FSMadmin.set_new_photo_element)

    dp.register_callback_query_handler(admin_back, text='admin_back', state='*')
    dp.register_callback_query_handler(admin_quit, text='admin_quit', state="*")
