import asyncio
import logging

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
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s  %(message)s",
    )

    settings = get_settings()
    detector = _resolve_detection_strategy(settings.detection_strategy, settings.model_path, settings.detection_threshold)
    strategy = _resolve_reply_strategy(settings.reply_strategy)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(create_router(detector, strategy))

    logger.info("Starting goodnight-bot with detection=%s strategy=%s", settings.detection_strategy, settings.reply_strategy)
    await dp.start_polling(bot)


def main() -> None:
    asyncio.run(_run())