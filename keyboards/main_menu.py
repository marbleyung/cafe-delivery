from aiogram import Dispatcher, types

async def set_main_menu(dp):
    main_menu_commands = [
        types.BotCommand(command='/help', description='Викликати довідку'),
        types.BotCommand(command='/cart', description='Відкрити кошик'),
        types.BotCommand(command='/m', description='Відкрити меню'),
        types.BotCommand(command='/esc', description='Вийти з реєстрації'),
        types.BotCommand(command='/q', description='Вийти'),
        types.BotCommand(command='/about', description='Графік та умови доставки')
    ]
    await dp.bot.set_my_commands(main_menu_commands)