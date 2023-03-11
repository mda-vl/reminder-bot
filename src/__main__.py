import pytz
from pathlib import Path

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    Defaults,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from system import log
from utils import settings, states

LOG_LEVEL = "INFO"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}",
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"{update.message.text}")


def main() -> None:
    log.set_log_to_console(LOG_LEVEL)
    states.config = settings.get_config(
        Path(__file__).parent / "settings.json",
    )
    log.set_log_to_files(LOG_LEVEL)

    app = (
        ApplicationBuilder()
        .defaults(
            Defaults(
                parse_mode=ParseMode.HTML,
                tzinfo=pytz.timezone("Asia/Vladivostok"),
            )
        )
        .token(states.config.api_token)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    app.run_polling()


if __name__ == "__main__":
    main()
