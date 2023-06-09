import pytz
from pathlib import Path

from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    Defaults,
)

from system import log
from utils import settings, states, process
from controller import controller, error
from model import db
from model import model

LOG_LEVEL = "INFO"


def main() -> None:
    log.set_log_to_console(LOG_LEVEL)

    states.config = settings.get_config(
        Path(__file__).parent / "settings.json",
    )

    log.set_log_to_files(LOG_LEVEL)

    model.Base.metadata.create_all(db.get_engine())

    app = (
        ApplicationBuilder()
        .defaults(
            Defaults(
                parse_mode=ParseMode.HTML,
                tzinfo=pytz.timezone("Asia/Vladivostok"),
            )
        )
        .token(states.config.api_token)
        .post_init(process.set_bot_commands)
        .build()
    )

    controller.add_jobs_queue(app)
    controller.add_command_handlers(app)

    app.add_error_handler(error.error_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
