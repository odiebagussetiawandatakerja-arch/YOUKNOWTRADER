"""
YouKnowTrader News Bot - Telegram bot for real-time financial news.
Covers: Crypto, Forex, Saham IDX, Komoditas, dan berita umum.
Auto-translate to Bahasa Indonesia.
"""

import asyncio
import logging
import sys

from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from config import (
    ALL_CATEGORIES,
    CATEGORY_DISPLAY,
    CATEGORY_EMOJI,
    POLL_INTERVAL,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHANNEL_ID,
)
from database import (
    cleanup_old_news,
    get_all_subscribers,
    get_subscribers_for_category,
    get_user_subscriptions,
    init_db,
    is_news_sent,
    mark_news_sent,
    subscribe_user,
    unsubscribe_user,
)
from news_fetcher import NewsItem, close_session, fetch_all_categories, fetch_category
from translator import is_indonesian, translate_news_item

# ─── Logging ─────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("NewsBot")


# ─── Message Formatting ─────────────────────────────────────────────

def format_news_message(item: NewsItem, translated_title: str, translated_summary: str) -> str:
    """Format a news item for Telegram."""
    emoji = CATEGORY_EMOJI.get(item.category, "📰")
    cat_display = CATEGORY_DISPLAY.get(item.category, item.category.upper())

    lines = [
        f"{emoji} <b>[{cat_display}] {translated_title}</b>",
        "",
    ]

    if translated_summary:
        # Limit summary length for readability
        summary = translated_summary[:300]
        if len(translated_summary) > 300:
            summary += "..."
        lines.append(f"{summary}")
        lines.append("")

    lines.append(f"📡 <i>{item.source}</i>")

    if item.url:
        lines.append(f"🔗 <a href=\"{item.url}\">Baca selengkapnya</a>")

    # Show original title if translated
    if translated_title != item.title:
        lines.append(f"\n<blockquote>EN: {item.title[:200]}</blockquote>")

    return "\n".join(lines)


# ─── Command Handlers ────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    if not update.effective_chat or not update.effective_user:
        return

    keyboard = [
        [
            InlineKeyboardButton("₿ Crypto", callback_data="sub_crypto"),
            InlineKeyboardButton("💱 Forex", callback_data="sub_forex"),
        ],
        [
            InlineKeyboardButton("📈 Saham IDX", callback_data="sub_idx"),
            InlineKeyboardButton("🛢 Komoditas", callback_data="sub_commodities"),
        ],
        [
            InlineKeyboardButton("📰 Umum", callback_data="sub_general"),
            InlineKeyboardButton("🌐 Semua", callback_data="sub_all"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.effective_chat.send_message(
        text=(
            "⚡ <b>YouKnowTrader News Bot</b> ⚡\n\n"
            "Bot berita finansial tercepat!\n"
            "Crypto • Forex • Saham IDX • Komoditas\n\n"
            "🔄 <b>Auto-translate</b> ke Bahasa Indonesia\n"
            "⏱ Update setiap 60 detik\n\n"
            "Pilih kategori yang ingin kamu subscribe:\n"
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    if not update.effective_chat:
        return

    await update.effective_chat.send_message(
        text=(
            "📖 <b>Daftar Perintah:</b>\n\n"
            "/start - Mulai & pilih kategori\n"
            "/subscribe - Subscribe kategori baru\n"
            "/unsubscribe - Unsubscribe kategori\n"
            "/mystatus - Lihat subscription kamu\n"
            "/latest [kategori] - Berita terbaru\n"
            "/crypto - Berita crypto terbaru\n"
            "/forex - Berita forex terbaru\n"
            "/idx - Berita saham IDX terbaru\n"
            "/commodities - Berita komoditas terbaru\n"
            "/all - Semua berita terbaru\n"
            "/help - Tampilkan bantuan ini\n\n"
            "💡 <b>Tips:</b> Subscribe ke kategori untuk dapat "
            "notifikasi otomatis setiap ada berita baru!"
        ),
        parse_mode=ParseMode.HTML,
    )


async def cmd_subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /subscribe command - show subscription menu."""
    if not update.effective_chat:
        return

    keyboard = [
        [
            InlineKeyboardButton("₿ Crypto", callback_data="sub_crypto"),
            InlineKeyboardButton("💱 Forex", callback_data="sub_forex"),
        ],
        [
            InlineKeyboardButton("📈 Saham IDX", callback_data="sub_idx"),
            InlineKeyboardButton("🛢 Komoditas", callback_data="sub_commodities"),
        ],
        [
            InlineKeyboardButton("📰 Umum", callback_data="sub_general"),
            InlineKeyboardButton("🌐 Semua", callback_data="sub_all"),
        ],
    ]

    await update.effective_chat.send_message(
        text="📬 Pilih kategori untuk di-subscribe:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def cmd_unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /unsubscribe command."""
    if not update.effective_chat:
        return

    keyboard = [
        [
            InlineKeyboardButton("₿ Crypto", callback_data="unsub_crypto"),
            InlineKeyboardButton("💱 Forex", callback_data="unsub_forex"),
        ],
        [
            InlineKeyboardButton("📈 Saham IDX", callback_data="unsub_idx"),
            InlineKeyboardButton("🛢 Komoditas", callback_data="unsub_commodities"),
        ],
        [
            InlineKeyboardButton("📰 Umum", callback_data="unsub_general"),
            InlineKeyboardButton("❌ Semua", callback_data="unsub_all"),
        ],
    ]

    await update.effective_chat.send_message(
        text="🗑 Pilih kategori untuk di-unsubscribe:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def cmd_mystatus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /mystatus command."""
    if not update.effective_chat:
        return

    subs = await get_user_subscriptions(update.effective_chat.id)

    if not subs:
        await update.effective_chat.send_message(
            text=(
                "📭 Kamu belum subscribe ke kategori apapun.\n"
                "Gunakan /subscribe untuk mulai!"
            ),
        )
        return

    sub_list = "\n".join(
        f"  {CATEGORY_EMOJI.get(s, '📰')} {CATEGORY_DISPLAY.get(s, s)}"
        for s in subs
    )
    await update.effective_chat.send_message(
        text=f"📬 <b>Subscription kamu:</b>\n\n{sub_list}",
        parse_mode=ParseMode.HTML,
    )


async def cmd_latest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /latest [category] command."""
    if not update.effective_chat:
        return

    category = ""
    if context.args:
        category = context.args[0].lower()

    if category and category in ALL_CATEGORIES:
        await _send_latest_for_category(update.effective_chat.id, category, context)
    elif category:
        await update.effective_chat.send_message(
            text=f"❌ Kategori '{category}' tidak ditemukan.\nGunakan: crypto, forex, idx, commodities, general",
        )
    else:
        await _send_latest_all(update.effective_chat.id, context)


async def cmd_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /crypto, /forex, /idx, /commodities, /all commands."""
    if not update.effective_chat or not update.message:
        return

    command = update.message.text or ""
    command = command.split("@")[0].lstrip("/").lower()

    if command == "all":
        await _send_latest_all(update.effective_chat.id, context)
    elif command in ALL_CATEGORIES:
        await _send_latest_for_category(update.effective_chat.id, command, context)


async def _send_latest_for_category(
    chat_id: int, category: str, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Fetch and send latest news for a category."""
    emoji = CATEGORY_EMOJI.get(category, "📰")
    cat_name = CATEGORY_DISPLAY.get(category, category)

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"⏳ Mengambil berita {emoji} {cat_name} terbaru...",
    )

    items = await fetch_category(category)

    if not items:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"😔 Tidak ada berita {cat_name} saat ini. Coba lagi nanti!",
        )
        return

    # Send top 5 latest
    count = 0
    for item in items[:5]:
        translated_title, translated_summary = await _maybe_translate(item)
        msg = format_news_message(item, translated_title, translated_summary)
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
            count += 1
            await asyncio.sleep(0.3)  # Rate limit
        except Exception as e:
            logger.warning("Failed to send message: %s", e)

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"✅ {count} berita {emoji} {cat_name} terbaru ditampilkan.",
    )


async def _send_latest_all(
    chat_id: int, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Fetch and send latest news from all categories."""
    await context.bot.send_message(
        chat_id=chat_id,
        text="⏳ Mengambil semua berita terbaru...",
    )

    all_news = await fetch_all_categories()
    total = 0

    for category, items in all_news.items():
        if not items:
            continue

        for item in items[:3]:  # Top 3 per category
            translated_title, translated_summary = await _maybe_translate(item)
            msg = format_news_message(item, translated_title, translated_summary)
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=msg,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
                total += 1
                await asyncio.sleep(0.3)
            except Exception as e:
                logger.warning("Failed to send message: %s", e)

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"✅ Total {total} berita terbaru ditampilkan dari semua kategori.",
    )


# ─── Callback Query Handler ─────────────────────────────────────────

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard callbacks for subscribe/unsubscribe."""
    query = update.callback_query
    if not query or not query.data or not update.effective_user or not update.effective_chat:
        return

    await query.answer()

    data = query.data
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if data.startswith("sub_"):
        category = data[4:]

        if category == "all":
            results = []
            for cat in ALL_CATEGORIES:
                is_new = await subscribe_user(user_id, chat_id, cat)
                if is_new:
                    results.append(cat)
            if results:
                cat_list = ", ".join(
                    f"{CATEGORY_EMOJI.get(c, '📰')} {CATEGORY_DISPLAY.get(c, c)}"
                    for c in results
                )
                await query.edit_message_text(
                    f"✅ Berhasil subscribe ke: {cat_list}\n\n"
                    "Kamu akan mendapat notifikasi berita otomatis!"
                )
            else:
                await query.edit_message_text(
                    "ℹ️ Kamu sudah subscribe ke semua kategori!"
                )
        elif category in ALL_CATEGORIES:
            is_new = await subscribe_user(user_id, chat_id, category)
            emoji = CATEGORY_EMOJI.get(category, "📰")
            name = CATEGORY_DISPLAY.get(category, category)
            if is_new:
                await query.edit_message_text(
                    f"✅ Berhasil subscribe ke {emoji} {name}!\n"
                    "Kamu akan mendapat notifikasi berita otomatis."
                )
            else:
                await query.edit_message_text(
                    f"ℹ️ Kamu sudah subscribe ke {emoji} {name}."
                )

    elif data.startswith("unsub_"):
        category = data[6:]

        if category == "all":
            removed = []
            for cat in ALL_CATEGORIES:
                was_sub = await unsubscribe_user(chat_id, cat)
                if was_sub:
                    removed.append(cat)
            if removed:
                await query.edit_message_text(
                    "✅ Berhasil unsubscribe dari semua kategori."
                )
            else:
                await query.edit_message_text(
                    "ℹ️ Kamu tidak subscribe ke kategori manapun."
                )
        elif category in ALL_CATEGORIES:
            was_sub = await unsubscribe_user(chat_id, category)
            emoji = CATEGORY_EMOJI.get(category, "📰")
            name = CATEGORY_DISPLAY.get(category, category)
            if was_sub:
                await query.edit_message_text(
                    f"✅ Berhasil unsubscribe dari {emoji} {name}."
                )
            else:
                await query.edit_message_text(
                    f"ℹ️ Kamu tidak subscribe ke {emoji} {name}."
                )


# ─── Translation Helper ─────────────────────────────────────────────

async def _maybe_translate(item: NewsItem) -> tuple[str, str]:
    """Translate a news item if it's not already in Indonesian."""
    if is_indonesian(item.title) or is_indonesian(item.summary):
        return item.title, item.summary

    try:
        return await translate_news_item(item.title, item.summary)
    except Exception as e:
        logger.warning("Translation failed: %s", e)
        return item.title, item.summary


# ─── Scheduled News Broadcast ───────────────────────────────────────

async def scheduled_news_check(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Background job: fetch new news and send to subscribers."""
    logger.info("Running scheduled news check...")

    try:
        all_news = await fetch_all_categories()
    except Exception as e:
        logger.error("Failed to fetch news: %s", e)
        return

    # Also send to channel if configured
    channel_id = TELEGRAM_CHANNEL_ID

    for category, items in all_news.items():
        if not items:
            continue

        subscribers = await get_subscribers_for_category(category)
        if not subscribers and not channel_id:
            continue

        for item in items:
            # Check dedup
            if await is_news_sent(item.hash):
                continue

            # Translate
            translated_title, translated_summary = await _maybe_translate(item)
            msg = format_news_message(item, translated_title, translated_summary)

            # Send to all subscribers
            for chat_id in subscribers:
                try:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=msg,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(0.05)  # Minimal rate limiting
                except Exception as e:
                    logger.warning(
                        "Failed to send to %d: %s", chat_id, e
                    )

            # Send to channel if configured
            if channel_id:
                try:
                    await context.bot.send_message(
                        chat_id=channel_id,
                        text=msg,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                except Exception as e:
                    logger.warning("Failed to send to channel: %s", e)

            # Mark as sent
            await mark_news_sent(
                item.hash, item.title, item.source, item.category, item.url
            )

    # Cleanup old news every run
    removed = await cleanup_old_news(days=7)
    if removed:
        logger.info("Cleaned up %d old news entries", removed)

    logger.info("Scheduled news check complete.")


# ─── Main ────────────────────────────────────────────────────────────

async def post_init(application: Application) -> None:
    """Set bot commands after initialization."""
    commands = [
        BotCommand("start", "Mulai & pilih kategori"),
        BotCommand("help", "Tampilkan bantuan"),
        BotCommand("subscribe", "Subscribe kategori"),
        BotCommand("unsubscribe", "Unsubscribe kategori"),
        BotCommand("mystatus", "Lihat subscription"),
        BotCommand("latest", "Berita terbaru [kategori]"),
        BotCommand("crypto", "Berita crypto"),
        BotCommand("forex", "Berita forex"),
        BotCommand("idx", "Berita saham IDX"),
        BotCommand("commodities", "Berita komoditas"),
        BotCommand("all", "Semua berita"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands registered.")


async def post_shutdown(application: Application) -> None:
    """Cleanup on shutdown."""
    await close_session()
    logger.info("Bot shutdown complete.")


def main() -> None:
    """Entry point."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error(
            "TELEGRAM_BOT_TOKEN not set! "
            "Set it in .env or as environment variable."
        )
        sys.exit(1)

    logger.info("Starting YouKnowTrader News Bot...")
    logger.info("Poll interval: %d seconds", POLL_INTERVAL)
    logger.info("Categories: %s", ", ".join(ALL_CATEGORIES.keys()))

    # Build application
    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )

    # Register command handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("subscribe", cmd_subscribe))
    app.add_handler(CommandHandler("unsubscribe", cmd_unsubscribe))
    app.add_handler(CommandHandler("mystatus", cmd_mystatus))
    app.add_handler(CommandHandler("latest", cmd_latest))

    # Category shortcuts
    for cat in list(ALL_CATEGORIES.keys()) + ["all"]:
        app.add_handler(CommandHandler(cat, cmd_category))

    # Callback handler for inline keyboards
    app.add_handler(CallbackQueryHandler(handle_callback))

    # Initialize database
    asyncio.get_event_loop().run_until_complete(init_db())
    logger.info("Database initialized.")

    # Schedule news check job
    if app.job_queue:
        app.job_queue.run_repeating(
            scheduled_news_check,
            interval=POLL_INTERVAL,
            first=10,  # Start 10s after bot starts
            name="news_check",
        )
        logger.info("Scheduled news check every %ds", POLL_INTERVAL)
    else:
        logger.warning("Job queue not available! Install python-telegram-bot[job-queue]")

    # Start bot
    logger.info("Bot is running! Press Ctrl+C to stop.")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
