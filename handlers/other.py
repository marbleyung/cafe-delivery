from aiogram import Dispatcher
from aiogram.types import Message


async def reply_to_another(message: Message):
    await message.answer("This command never exists. Type /help to call the list of existing commands.")


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(reply_to_another)
