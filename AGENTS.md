# AGENTS.md

## Commands

- **Run the bot:** `uv run goodnight-bot` (requires `.env` with `BOT_TOKEN`)
- **Install deps:** `uv sync`
- **Build package:** `uv build`

No test suite, linter, or typechecker is configured yet.

## Architecture

Secretary-mode-only Telegram bot using aiogram v3. No regular group/private chat handlers — only `business_connection` and `business_message` updates.

- **Entry point:** `goodnight_bot.main:main` (async, registered as `goodnight-bot` console script)
- **Config:** `config.py` — pydantic-settings, reads `.env`. Required: `BOT_TOKEN`. Optional: `REPLY_STRATEGY` (default `predefined`)
- **Message flow:** `handler.py` receives business messages → `detector.py` checks for goodnight phrases → `replies/` strategy generates reply → sent via `message.answer(business_connection_id=...)`
- **Reply strategies:** Strategy pattern. Add new strategy class in `replies/`, implement `ReplyStrategy` ABC, register in `_STRATEGIES` dict in `main.py`

## Key gotchas

- Source is under `src/goodnight_bot/` (src layout), not flat at repo root
- Bot token must be set in `.env` before running; the app will crash on startup without it
- The bot **must** have Secretary Mode enabled via @BotFather — it won't respond to regular messages
- `detector.py` regex uses negative lookahead `(?!о(?!й))` to match "спокойной" (goodnight) but reject "спокойно" (calmly) — changing patterns requires care to avoid false positives
- `handler.py` tracks active business connections in an in-memory dict `_active_connections`; connections are lost on restart
- aiogram `message.answer()` with `business_connection_id` is what makes the reply appear on behalf of the connected user
