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
    await message.answer(text = 'Hello! Please, register first\n'
                                'Just enter your name, phone number and address\n'
                                'The bot will remember your data\n'
                                '/esc to escape from here if you are ALREADY REGISTERED')
    await message.answer("Enter your name")
    await FSMuser.name.set()


async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.title())
    await message.answer("Enter your phone number")
    await FSMuser.next()


async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Great! And now enter your address.")
    await FSMuser.next()


async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    await message.answer(f"We almost register you, {data['name']}!\n"
                         f"Your phone number: {data['phone']}\n"
                         f"Your address: {data['address']}\nPlease, check your data.\n"
                         f"Is it correct?", reply_markup=yes_no_kb)

    await FSMuser.next()


async def is_correct_yes(callback, state: FSMContext):
    data = await state.get_data()
    data = list(data.values())
    data.insert(0, int(callback.from_user.id))
    result = sql_add_user(data)
    if result == "You have been already registered.\nPlease, enter /esc and use bot :)":
        await callback.answer(result, show_alert=True)
    else:
        await callback.message.edit_text("Great! Start with \m!\n"
                                         "If you need to change your data, enter /del and then /start")
        await state.finish()


async def is_correct_no(callback, state: FSMContext):
    await user_register(message=callback.message)
    await callback.message.edit_text('Re-enter your data')


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

