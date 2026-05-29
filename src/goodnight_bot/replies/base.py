from abc import ABC, abstractmethod


class ReplyStrategy(ABC):
    @abstractmethod
    async def generate_reply(self, message_text: str) -> str: ...
