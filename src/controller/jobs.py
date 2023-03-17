import aiohttp
import asyncio
import ujson

from loguru import logger
from telegram.ext import ContextTypes

from utils import states

db = [
    {"symbol": "BTCUSDT"},
    {"symbol": "BNBUSDT"},
    {"symbol": "ETHUSDT"},
    {"symbol": "ADAUSDT"},
    {"symbol": "LTCUSDT"},
    {"symbol": "DOTUSDT"},
]


async def get_all_reminders() -> None:
    for reminder in db:
        yield (reminder)
        await asyncio.sleep(0.5)


async def sym_request(context: ContextTypes.DEFAULT_TYPE) -> None:
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        async for reminder in get_all_reminders():
            async with session.get(
                f"https://api.binance.com/api/v3/klines?"
                f"symbol={reminder['symbol']}&interval=1h&limit=1",
                headers=states.headers,
            ) as response:
                data = (await response.json())[0]
                logger.info(f"DATA: {data}")

    context.job_queue.run_once(
        callback=sym_request,
        when=10,
        name="once_job",
    )
    logger.info(f"JOBS - {context.job_queue.jobs()}")
