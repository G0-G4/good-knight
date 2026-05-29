import asyncio
import logging
import logging.handlers
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from goodnight_bot.config import get_settings
from goodnight_bot.detectors.base import DetectorStrategy
from goodnight_bot.detectors.fasttext import FasttextDetector
from goodnight_bot.detectors.regex import RegexDetector
from goodnight_bot.handler import create_router
from goodnight_bot.replies.base import ReplyStrategy
from goodnight_bot.replies.predefined import PredefinedListStrategy
from goodnight_bot.replies.template import TemplateStrategy

_REPLY_STRATEGIES: dict[str, type[ReplyStrategy]] = {
    "predefined": PredefinedListStrategy,
    "template": TemplateStrategy,
}

_DETECTION_STRATEGIES: dict[str, type[DetectorStrategy]] = {
    "regex": RegexDetector,
    "fasttext": FasttextDetector,
}

logger = logging.getLogger(__name__)


def _resolve_reply_strategy(name: str) -> ReplyStrategy:
    cls = _REPLY_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(
            f"Unknown reply strategy: {name}. Available: {list(_REPLY_STRATEGIES)}"
        )
    return cls()


def _resolve_detection_strategy(name: str, model_path: str, threshold: float) -> DetectorStrategy:
    cls = _DETECTION_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(
            f"Unknown detection strategy: {name}. Available: {list(_DETECTION_STRATEGIES)}"
        )
    if cls is FasttextDetector:
        return cls(model_path=model_path, threshold=threshold)
    return cls()


async def _run() -> None:
    log_format = logging.Formatter("%(asctime)s %(levelname)-8s %(name)s  %(message)s")

    os.makedirs("logs", exist_ok=True)

    file_handler = logging.handlers.TimedRotatingFileHandler(
        "logs/bot.log",
        when="midnight",
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(log_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    settings = get_settings()
    detector = _resolve_detection_strategy(settings.detection_strategy, settings.model_path, settings.detection_threshold)
    strategy = _resolve_reply_strategy(settings.reply_strategy)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(create_router(bot, detector, strategy, goodnight_ttl=settings.goodnight_ttl))

    logger.info("Starting goodnight-bot with detection=%s strategy=%s", settings.detection_strategy, settings.reply_strategy)
    await dp.start_polling(bot)


def main() -> None:
    asyncio.run(_run())

if __name__ == '__main__':
    main()