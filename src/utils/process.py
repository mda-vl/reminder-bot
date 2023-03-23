from telegram.ext import Application


async def set_bot_commands(app: Application) -> None:
    await app.bot.set_my_commands(
        [
            ("start", "Запустить бот"),
            ("help", "Помощь"),
            ("set", "Установить напоминание"),
            ("list", "Просмотр напоминаний"),
            ("tlist", "Таблица напоминаний"),
            ("slist", "Короткий список напоминаний"),
        ]
    )
