from datetime import timedelta

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from . import commands
from .jobs import sym_request


def add_command_handlers(app: Application) -> None:
    app.add_handler(CommandHandler(["start", "help"], commands.start))
    app.add_handler(CommandHandler("set", commands.set))
    app.add_handler(CommandHandler("tlist", commands.tlst))
    app.add_handler(CommandHandler("list", commands.lst))
    app.add_handler(CommandHandler("slist", commands.slst))
    app.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), commands.echo),
    )


def add_jobs_queue(app: Application) -> None:
    job_queue = app.job_queue

    job_queue.run_once(
        callback=sym_request,
        when=timedelta(seconds=10),
        name="once_job",
    )
