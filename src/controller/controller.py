from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from .commands import start, echo


def add_command_handlers(app: Application) -> None:
    app.add_handler(CommandHandler(["start", "help"], start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
