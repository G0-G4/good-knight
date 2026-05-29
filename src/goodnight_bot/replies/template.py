import random

from goodnight_bot.replies.base import ReplyStrategy

_GREETINGS = [
    "Спокойной ночи!",
    "Споки!",
    "Ночи!",
    "Баиньки!",
    "Сладких снов!",
    "Спок!",
    "Спокойной!",
    "Ноченьки!",
    "Ночки!",
    "Спок ночки!",
]

_REASONS = [
    "Пусть тебе приснится, что ты проснулся вовремя",
    "Твой будильник уже точит ножи",
    "А кто будет дописывать тот код?",
    "Завтра снова в бой, воин подушки",
    "Не забудь выключить ноут — он тоже хочет спать",
    "Завтра среда... а может и нет, кто знает",
    "Пусть приснится повышение зп и бесплатный кофе",
    "Постель уже скучала по тебе",
    "Спи крепко, пока кто-нибудь не написал в чат в 3 часа ночи",
    "Помни: лучший сон — после 'деплой прошёл'",
    "А утро ближе, чем кажется...",
    "Не забудь зарядить телефон, иначе завтра без будильника",
    "Завтра новый день, новые баги, старый код",
    "Спи, пока кот не решил пробежаться по тебе в 4 утра",
    "Да пребудет с тобой сила... силы воли проснуться",
]

_EMOJIS = [
    "😴",
    "🌙💤",
    "⏰😏",
    "🛡️💤",
    "🤖",
    "💻😴",
    "☕✨",
    "🛏️❤️",
    "📱👻",
    "😌🚀",
    "🌅😈",
    "📱⏰",
    "🐛😎",
    "🐈💨",
    "💪😴",
]


class TemplateStrategy(ReplyStrategy):
    def __init__(
        self,
        reason_probability: float = 0.5,
        emoji_probability: float = 0.7,
    ) -> None:
        self._reason_prob = reason_probability
        self._emoji_prob = emoji_probability

    async def generate_reply(self, message_text: str) -> str:
        parts = [random.choice(_GREETINGS)]
        if random.random() < self._reason_prob:
            parts.append(random.choice(_REASONS))
        if random.random() < self._emoji_prob:
            parts.append(random.choice(_EMOJIS))
        return " ".join(parts)