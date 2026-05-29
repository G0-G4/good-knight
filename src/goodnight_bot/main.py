import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from goodnight_bot.config import get_settings
from goodnight_bot.handler import create_router
from goodnight_bot.replies.base import ReplyStrategy
from goodnight_bot.replies.predefined import PredefinedListStrategy

_STRATEGIES: dict[str, type[ReplyStrategy]] = {
    "predefined": PredefinedListStrategy,
}

logger = logging.getLogger(__name__)


def _resolve_strategy(name: str) -> ReplyStrategy:
    cls = _STRATEGIES.get(name)
    if cls is None:
        raise ValueError(
            f"Unknown reply strategy: {name}. Available: {list(_STRATEGIES)}"
        )
    return cls()


async def _run() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s  %(message)s",
    )

    settings = get_settings()
    strategy = _resolve_strategy(settings.reply_strategy)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(create_router(strategy))

    logger.info("Starting goodnight-bot with strategy=%s", settings.reply_strategy)
    await dp.start_polling(bot)


def main() -> None:
    asyncio.run(_run())
