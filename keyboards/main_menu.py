from aiogram import Dispatcher, types

async def set_main_menu(dp):
    main_menu_commands = [
        types.BotCommand(command='/help', description='Викликати довідку'),
        types.BotCommand(command='/saved', description='Відкрити збережені'),
        types.BotCommand(command='/m', description='Відкрити меню'),
        types.BotCommand(command='/esc', description='Вийти з реєстрації')
    ]
    await dp.bot.set_my_commands(main_menu_commands)