from telegram.ext import Application


async def set_bot_commands(app: Application) -> None:
    await app.bot.set_my_commands(
        [
            ("start", "Запустить бот"),
            ("help", "Помощь"),
        ]
    )
