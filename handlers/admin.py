from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dataclasses import dataclass
from aiogram.dispatcher.filters import Text
from environs import Env
from database import database
from keyboards.admin_kb import admin_keyboard, admin_back_keyboard

@dataclass
class FSMadmin(StatesGroup):
    photo = State()
    category = State()
    name = State()
    description = State()
    price = State()
    name_to_delete = State()


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


async def admin_load(callback):
    await callback.message.edit_text(text='Якщо ви хочете додати нову страву, завантажте фото\n'
                          '/q для виходу з даного меню', reply_markup=admin_back_keyboard)
    await callback.answer()
    await FSMadmin.photo.set()


async def admin_delete(callback):
    await callback.message.edit_text(text='Якщо ви хочете видалити страву, введіть її назву\n'
                         'Наприклад, Margherita для видалення відповідної піци,\n'
                         'Quattro Formaggi для видалення відповідної піци тощо.\n'
                         '/q для виходу з даного меню', reply_markup=admin_back_keyboard)
    await callback.answer()
    await FSMadmin.name_to_delete.set()


async def del_dish(message: types.Message, state: FSMContext):
    await state.update_data(name_to_delete=message.text.title())
    data = await state.get_data()
    data = data['name_to_delete'],
    print(data)
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

    dp.register_callback_query_handler(admin_load, text='admin_load')
    dp.register_callback_query_handler(admin_delete, text='admin_delete')
    dp.register_message_handler(del_dish, state=FSMadmin.name_to_delete)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMadmin.photo)
    dp.register_message_handler(load_category, state=FSMadmin.category)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_description, state=FSMadmin.description)
    dp.register_message_handler(load_price, state=FSMadmin.price)
    dp.register_callback_query_handler(admin_back, text='admin_back', state='*')
    dp.register_callback_query_handler(admin_quit, text='admin_quit', state="*")