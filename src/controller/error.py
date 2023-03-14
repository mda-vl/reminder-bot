import traceback
import html
import ujson
from loguru import logger

from telegram import Update
from telegram.ext import ContextTypes

from utils import states


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Exception while handling an update: {context.error}")

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)

    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(ujson.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    admins_id = states.config.admins
    for id in admins_id:
        await context.bot.send_message(chat_id=id, text=message)
