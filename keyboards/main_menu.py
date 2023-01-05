from aiogram import Dispatcher, types

async def set_main_menu(dp):
    main_menu_commands = [
        types.BotCommand(command='/help', description='Help'),
        types.BotCommand(command='/cart', description='Cart'),
        types.BotCommand(command='/m', description='Menu'),
        types.BotCommand(command='/esc', description='Escape from registration'),
        types.BotCommand(command='/q', description='Quit'),
        types.BotCommand(command='/about', description='Schedule and delivery conditions')
    ]
    await dp.bot.set_my_commands(main_menu_commands)