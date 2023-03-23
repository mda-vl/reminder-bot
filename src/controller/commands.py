from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session
from loguru import logger
import prettytable as pt

from model import model, db


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Привет <b>{user.first_name}!</b>\n"
        f"☝️ Для установки уведомления о достижении пары"
        f" заданной цены, необходимо выполнить команду:\n"
        f"  <b>/set symbol price</b>\n"
        f"☝️ Для просмотра установленных напоминаний набери <b>/list</b>",
    )


async def set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    args = context.args
    try:
        parms = dict(zip(("symbol", "price"), (args[0], args[1])))
        model_set = model.AlarmSetModel(**{**(user.to_dict()), **parms})
    except Exception:
        logger.error("Ошибка при указании параметров команды /set.")
        await update.message.reply_text(
            "Неверно указаны параметры команды set"
            "\nОбратитесь к справке /help"
            "\nдля уточнения синтаксиса.",
        )
    else:
        try:
            with Session(db.get_engine()) as session:
                row = model.AlarmSetORM(**(model_set.dict()))
                session.add(row)
                session.commit()

        except Exception:
            logger.error("Ошибка записи напоминания в базу данных.")
            await update.message.reply_text(
                "Ошибка записи напоминания в базу данных.",
            )
        else:
            logger.info(
                f"Пользоваль {model_set.username}"
                f" с id {model_set.id} успешно установил напоминание"
                f" {model_set.symbol} -> {model_set.price}.",
            )
            await update.message.reply_text("👍")
            await update.message.reply_text(
                f"Напоминание {model_set.symbol}"
                f" 👉  {model_set.price}"
                f" успешно установлено."
            )


async def tlst(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with Session(db.get_engine()) as session:
        stmt = session.query(model.AlarmSetORM).all()
        model_stmt = [model.AlarmSetModel.from_orm(row) for row in stmt]
        if len(model_stmt) > 0:
            table = pt.PrettyTable(["Пара", "Цена", "Время установки"])
            table.align["Пара"] = "l"
            table.align["Цена"] = "l"
            for item in model_stmt:
                table.add_row(
                    [
                        item.symbol,
                        f"{item.price}",
                        f"{(item.created_at).strftime('%d-%m-%Y %H:%M')}",
                    ]
                )

        await update.message.reply_text(f"<pre>{table}</pre>")


async def lst(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with Session(db.get_engine()) as session:
        stmt = session.query(model.AlarmSetORM).all()
        model_stmt = [model.AlarmSetModel.from_orm(row) for row in stmt]
        if len(model_stmt) > 0:
            lst = ""
            for item in model_stmt:
                lst += (
                    f"🔖{(item.symbol).ljust(8)}👉 {(str(item.price)).ljust(9)}"
                    f"🗓{(item.created_at).strftime('%d-%m-%Y %H:%M')}\n"
                )
        await update.message.reply_text(f"<pre>{lst}</pre>")
        

async def slst(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with Session(db.get_engine()) as session:
        stmt = session.query(model.AlarmSetORM).all()
        model_stmt = [model.AlarmSetModel.from_orm(row) for row in stmt]
        if len(model_stmt) > 0:
            lst = ""
            for item in model_stmt:
                lst += (
                    f"🔖{(item.symbol).ljust(8)}👉 {(str(item.price)).ljust(9)}\n"
                )
        await update.message.reply_text(f"<pre>{lst}</pre>")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"{update.message.text}")
