from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from .commands import start, echo
from .jobs import periodic_message


def add_command_handlers(app: Application) -> None:
    app.add_handler(CommandHandler(["start", "help"], start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))


def add_jobs_queue(app: Application) -> None:
    job_queue = app.job_queue

    job_queue.run_repeating(
        callback=periodic_message,
        interval=10,
        name="periodic_job",
    )
