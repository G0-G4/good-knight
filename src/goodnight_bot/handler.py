import logging

from aiogram import Router
from aiogram.types import BusinessConnection, Message

from goodnight_bot.detector import is_goodnight
from goodnight_bot.replies.base import ReplyStrategy

logger = logging.getLogger(__name__)

_active_connections: dict[str, BusinessConnection] = {}


def create_router(strategy: ReplyStrategy) -> Router:
    router = Router()

    @router.business_connection()
    async def on_business_connection(connection: BusinessConnection) -> None:
        if connection.is_enabled:
            _active_connections[connection.id] = connection
            logger.info(
                "Business connection enabled: id=%s user=%s can_reply=%s",
                connection.id,
                connection.user.id,
                connection.can_reply,
            )
        else:
            _active_connections.pop(connection.id, None)
            logger.info("Business connection disabled: id=%s", connection.id)

    @router.business_message()
    async def on_business_message(message: Message) -> None:
        connection_id = message.business_connection_id
        if not connection_id:
            return

        connection = _active_connections.get(connection_id)
        if connection and not connection.can_reply:
            logger.debug("No reply permission for connection: %s", connection_id)
            return

        text = message.text or message.caption
        if not text or not is_goodnight(text):
            return

        reply = await strategy.generate_reply(text)
        await message.answer(reply)
        logger.info("Replied in connection %s: %s", connection_id, reply[:50])

    return router
