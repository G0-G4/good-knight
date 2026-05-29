# goodnight-bot

Telegram secretary bot that detects "спокойной ночи" messages and replies with funny responses.

Uses the [Chat Automation (Secretary Bots)](https://core.telegram.org/bots/features#secretary-bots) feature — users connect the bot to their profile, and it automatically responds to goodnight messages on their behalf.

## Setup

1. Create a bot via [@BotFather](https://t.me/botfather) and enable **Secretary Mode** in bot settings.
2. Copy `.env.example` to `.env` and set `BOT_TOKEN`:

```bash
cp .env.example .env
```

3. Install dependencies:

```bash
uv sync
```

4. Generate the detection model (required for the `fasttext` detection strategy):

```bash
uv run python scripts/train_model.py
```

This reads training data from `data/train.txt` and saves the model to `model/goodnight.bin`. You can customize the path and training parameters — see `uv run python scripts/train_model.py --help`.

5. Run the bot:

```bash
uv run goodnight-bot
```

## Configuration

| Variable              | Default               | Description                                                              |
|-----------------------|-----------------------|--------------------------------------------------------------------------|
| `BOT_TOKEN`           | *(required)*          | Telegram bot token from @BotFather                                       |
| `REPLY_STRATEGY`      | `predefined`          | Reply generation strategy (`predefined`)                                 |
| `DETECTION_STRATEGY`  | `fasttext`            | Detection strategy (`fasttext`)                                          |
| `MODEL_PATH`          | `model/goodnight.bin` | Path to the fastText model file (generate with `scripts/train_model.py`) |
| `DETECTION_THRESHOLD` | `0.5`                 | Confidence threshold for detection                                       |

## Connecting to your profile

1. Go to **Settings → Chat Automation** in Telegram.
2. Select the bot and choose which chats it can access.
3. When someone sends a message containing "спокойной ночи" (or variants), the bot replies on your behalf.

## Adding a new reply strategy

1. Create a new class in `src/goodnight_bot/replies/` implementing `ReplyStrategy`:

```python
from goodnight_bot.replies.base import ReplyStrategy

class MyStrategy(ReplyStrategy):
    async def generate_reply(self, message_text: str) -> str:
        return "my reply"
```

2. Register it in `main.py` in the `_STRATEGIES` dict.
3. Set `REPLY_STRATEGY=my_strategy` in `.env`.
