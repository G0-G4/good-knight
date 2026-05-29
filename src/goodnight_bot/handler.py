import logging
import time

from aiogram import Bot, Router
from aiogram.types import BusinessConnection, Message

from goodnight_bot.detectors.base import DetectorStrategy
from goodnight_bot.replies.base import ReplyStrategy

logger = logging.getLogger(__name__)

_connection_cache: dict[str, BusinessConnection] = {}
_owner_goodnight_at: dict[int, float] = {}


def create_router(
    bot: Bot,
    detector: DetectorStrategy,
    strategy: ReplyStrategy,
    goodnight_ttl: int = 3600,
) -> Router:
    router = Router()

    @router.business_connection()
    async def on_business_connection(connection: BusinessConnection) -> None:
        if connection.is_enabled:
            _connection_cache[connection.id] = connection
            logger.info(
                "Business connection enabled: id=%s user=%s can_reply=%s",
                connection.id,
                connection.user.id,
                connection.can_reply,
            )
        else:
            _connection_cache.pop(connection.id, None)
            logger.info("Business connection disabled: id=%s", connection.id)

    @router.business_message()
    async def on_business_message(message: Message) -> None:
        connection_id = message.business_connection_id
        if not connection_id:
            return

        connection = _connection_cache.get(connection_id)
        if not connection:
            connection = await bot.get_business_connection(connection_id)
            if not connection or not connection.is_enabled:
                logger.warning("Business connection not found or disabled: %s", connection_id)
                return
            _connection_cache[connection_id] = connection

        if not connection.can_reply:
            logger.debug("No reply permission for connection: %s", connection_id)
            return

        from_user = message.from_user
        if from_user and from_user.id == connection.user.id:
            text = message.text or message.caption
            if text and detector.is_goodnight(text):
                chat_id = message.chat.id
                _owner_goodnight_at[chat_id] = time.monotonic()
                logger.info("Owner sent goodnight in chat %s, setting TTL", chat_id)
            return

        text = message.text or message.caption
        if not text or not detector.is_goodnight(text):
            return

        chat_id = message.chat.id
        owner_sent_at = _owner_goodnight_at.get(chat_id)
        if owner_sent_at is not None:
            if time.monotonic() - owner_sent_at < goodnight_ttl:
                logger.info(
                    "Skipping goodnight reply in chat %s: owner already sent goodnight",
                    chat_id,
                )
                _owner_goodnight_at.pop(chat_id, None)
                return
            _owner_goodnight_at.pop(chat_id, None)

        reply = await strategy.generate_reply(text)
        await message.answer(reply)
        logger.info("Replied in connection %s: %s", connection_id, reply[:50])

    return router
