from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.menu_kb import yes_no_kb
from database.database import sql_add_user
from aiogram.dispatcher.filters import Text
from lexicon.lexicon import LEXICON_UA

class FSMuser(StatesGroup):
    name = State()
    phone = State()
    address = State()
    is_correct = State()

async def user_register(message: types.Message):
    await message.answer('Вітаємо! Зареєструйтесь, будь ласка.\nЦе не забере багато часу.\n'
                         'Просто введіть своє імя, номер телефону та адресу.\nЦе потрібно для того, щоби бот запам`ятав вас.\n'
                         '/esc - якщо ви потрапили сюда помилково')
    await message.answer("Будь ласка, введіть ваше ім'я")
    await FSMuser.name.set()


async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.title())
    await message.answer("Будь ласка, введіть ваш номер телефону")
    await FSMuser.next()


async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Чудово! Залишилось додати адресу.")
    await FSMuser.next()


async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    await message.answer(f"Ми майже зареєстрували вас, {data['name']}!\n"
                         f"Ваш номер телефону: {data['phone']}\n"
                         f"Ваша адреса: {data['address']}\nБудь ласка, передивіться дані уважно.\n"
                         f"Чи правильно введено дані?", reply_markup=yes_no_kb)

    await FSMuser.next()


async def is_correct_yes(callback, state: FSMContext):
    data = await state.get_data()
    data = list(data.values())
    data.insert(0, int(callback.from_user.id))
    result = sql_add_user(data)
    if result == 'Ви вже були успішно зареєстровані.\nБудь ласка, пропишіть /esc і починайте користуватись ботом':
        await callback.answer(result, show_alert=True)
    else:
        await callback.message.edit_text("Чудово! В вашому розпорядженні цілий арсенал команд!\nПочніть з /m\n"
                                         "Якщо колись вам потрібно буде змінити дані, введіть /start")
        await state.finish()


async def is_correct_no(callback, state: FSMContext):
    await user_register(message=callback.message)
    await callback.message.edit_text('Введіть дані заново')


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=LEXICON_UA['/help'])


def register_reg_handlers(dp):
    dp.register_message_handler(user_register, commands='start')
    dp.register_message_handler(cancel, state="*", commands='esc')
    dp.register_message_handler(cancel, Text(equals='esc', ignore_case=True), state='*')
    dp.register_message_handler(get_name, state=FSMuser.name)
    dp.register_message_handler(get_phone_number, state=FSMuser.phone)
    dp.register_message_handler(get_address, state=FSMuser.address)
    dp.register_callback_query_handler(is_correct_yes, state=FSMuser.is_correct, text='yes')
    dp.register_callback_query_handler(is_correct_no, state=FSMuser.is_correct, text='no')

