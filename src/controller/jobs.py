from telegram.ext import ContextTypes


async def periodic_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        960389355,
        text="Hello from periodic",
    )
