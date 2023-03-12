from telegram.ext import ContextTypes


async def init_tg_menu(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.set_my_commands(
        [
            ("/start", "Запустить бот."),
            ("/help", "Получить справку."),
        ]
    )


async def periodic_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        960389355,
        text="Hello from periodic",
    )
