"""Telegram Bot — Top Trending Hotels & Attractions (East Java).

Auto-scrapes data daily from search engines and serves via Telegram commands.
"""

import asyncio
import logging
import os
from datetime import date, datetime, time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

import database as db
from data import CITIES as CITY_LIST, get_city_display, get_today_str
from scraper import scrape_all, seed_from_curated

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

STAR_EMOJI = "⭐"
HOTEL_EMOJI = "🏨"
ATTRACTION_EMOJI = "🎢"
FIRE_EMOJI = "🔥"
PIN_EMOJI = "📍"
MONEY_EMOJI = "💰"
CHART_EMOJI = "📊"
GLOBE_EMOJI = "🌐"
CLOCK_EMOJI = "🕐"

SCRAPE_HOUR = int(os.environ.get("SCRAPE_HOUR", "6"))
SCRAPE_MINUTE = int(os.environ.get("SCRAPE_MINUTE", "0"))


# ── Data access (from DB, fallback to curated) ─────────────────────────


def get_hotels(city: str, limit: int = 10) -> list[dict]:
    rows = db.get_hotels(city, limit)
    if rows:
        return rows
    from data import HOTELS
    return HOTELS.get(city, [])[:limit]


def get_attractions(city: str, limit: int = 10) -> list[dict]:
    rows = db.get_attractions(city, limit)
    if rows:
        return rows
    from data import ATTRACTIONS
    return ATTRACTIONS.get(city, [])[:limit]


# ── Formatters ──────────────────────────────────────────────────────────


def format_hotel(h: dict, rank: int) -> str:
    stars_count = h.get("stars", 3)
    stars = STAR_EMOJI * stars_count
    url_part = f" [🔗 Lihat]({h['url']})" if h.get("url") else ""
    rating = h.get("rating") or 0
    reviews = h.get("reviews") or 0
    return (
        f"*{rank}. {h['name']}* {stars}\n"
        f"   {CHART_EMOJI} Rating: *{rating}/10* ({reviews:,} review)\n"
        f"   {MONEY_EMOJI} Harga: `{h.get('price', 'N/A')}` /malam\n"
        f"   {GLOBE_EMOJI} Platform: {h.get('platform', 'N/A')}\n"
        f"   {FIRE_EMOJI} {h.get('highlight', '')}{url_part}\n"
    )


def format_attraction(a: dict, rank: int) -> str:
    booked = a.get("booked", "")
    booked_part = f" | {booked}" if booked else ""
    url_part = f" [🔗 Lihat]({a['url']})" if a.get("url") else ""
    return (
        f"*{rank}. {a['name']}*\n"
        f"   {MONEY_EMOJI} Tiket: `{a.get('price', 'N/A')}`\n"
        f"   {GLOBE_EMOJI} Platform: {a.get('platform', 'N/A')}{booked_part}\n"
        f"   {FIRE_EMOJI} {a.get('highlight', '')}{url_part}\n"
    )


def city_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("🏙 Surabaya", callback_data="top_surabaya"),
            InlineKeyboardButton("🏭 Sidoarjo", callback_data="top_sidoarjo"),
        ],
        [
            InlineKeyboardButton("🏛 Mojokerto", callback_data="top_mojokerto"),
            InlineKeyboardButton("⛰ Pasuruan", callback_data="top_pasuruan"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def detail_keyboard(city: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                f"{HOTEL_EMOJI} Hotel {get_city_display(city)}",
                callback_data=f"hotel_{city}",
            ),
            InlineKeyboardButton(
                f"{ATTRACTION_EMOJI} Atraksi {get_city_display(city)}",
                callback_data=f"atraksi_{city}",
            ),
        ],
        [
            InlineKeyboardButton("⬅️ Pilih Kota Lain", callback_data="back_cities"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def back_keyboard(city: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                f"⬅️ Kembali ke {get_city_display(city)}",
                callback_data=f"top_{city}",
            ),
            InlineKeyboardButton("🏠 Pilih Kota", callback_data="back_cities"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


# ── Commands ────────────────────────────────────────────────────────────


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    last = db.get_last_scrape()
    update_info = f"Last scrape: {last[:16]}" if last else get_today_str()
    text = (
        f"{FIRE_EMOJI} *Top Trending Hotel & Atraksi*\n"
        f"📅 {update_info}\n"
        f"{CLOCK_EMOJI} Auto-update setiap hari jam {SCRAPE_HOUR:02d}:{SCRAPE_MINUTE:02d} WIB\n\n"
        "Pilih kota untuk lihat trending hari ini:\n\n"
        "Atau ketik langsung:\n"
        "• `/top surabaya` — Top Surabaya\n"
        "• `/top sidoarjo` — Top Sidoarjo\n"
        "• `/top mojokerto` — Top Mojokerto\n"
        "• `/top pasuruan` — Top Pasuruan\n"
        "• `/hotel surabaya` — Hotel saja\n"
        "• `/atraksi pasuruan` — Atraksi saja\n"
        "• `/semua` — Semua kota\n"
        "• `/status` — Status & last update\n"
        "• `/refresh` — Manual update data\n"
        "• `/help` — Bantuan\n"
    )
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=city_keyboard()
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "*📖 Panduan Bot Trending*\n\n"
        "*Perintah:*\n"
        "• `/top [kota]` — Top 5 hotel & atraksi\n"
        "• `/hotel [kota]` — Semua hotel trending\n"
        "• `/atraksi [kota]` — Semua atraksi trending\n"
        "• `/semua` — Ringkasan semua kota\n"
        "• `/status` — Info last update & stats\n"
        "• `/refresh` — Manual scrape data terbaru\n"
        "• `/start` — Menu utama\n\n"
        "*Kota tersedia:*\n"
        "Surabaya, Sidoarjo, Mojokerto, Pasuruan\n\n"
        "*Data dari:*\n"
        "Traveloka, Booking.com, Agoda, Trip.com, Klook, Tiket.com\n\n"
        f"*Auto-update:* Setiap hari jam {SCRAPE_HOUR:02d}:{SCRAPE_MINUTE:02d} WIB\n"
        "Data di-scrape dari search engine untuk mendapatkan\n"
        "info hotel & atraksi terbaru dari semua platform."
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def cmd_top(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            f"{FIRE_EMOJI} *Pilih kota:*",
            parse_mode="Markdown",
            reply_markup=city_keyboard(),
        )
        return

    city = context.args[0].lower()
    if city not in CITY_LIST:
        await update.message.reply_text(
            f"❌ Kota *{city}* tidak ditemukan.\n"
            f"Kota tersedia: {', '.join(c.title() for c in CITY_LIST)}",
            parse_mode="Markdown",
        )
        return

    text = build_top_text(city)
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=detail_keyboard(city),
        disable_web_page_preview=True,
    )


async def cmd_hotel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            f"{HOTEL_EMOJI} Ketik `/hotel [kota]`\nContoh: `/hotel surabaya`",
            parse_mode="Markdown",
        )
        return

    city = context.args[0].lower()
    if city not in CITY_LIST:
        await update.message.reply_text(f"❌ Kota *{city}* tidak tersedia.", parse_mode="Markdown")
        return

    text = build_hotel_text(city)
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=back_keyboard(city),
        disable_web_page_preview=True,
    )


async def cmd_atraksi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            f"{ATTRACTION_EMOJI} Ketik `/atraksi [kota]`\nContoh: `/atraksi pasuruan`",
            parse_mode="Markdown",
        )
        return

    city = context.args[0].lower()
    if city not in CITY_LIST:
        await update.message.reply_text(f"❌ Kota *{city}* tidak tersedia.", parse_mode="Markdown")
        return

    text = build_attraction_text(city)
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=back_keyboard(city),
        disable_web_page_preview=True,
    )


async def cmd_semua(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = f"{FIRE_EMOJI} *RINGKASAN TRENDING — SEMUA KOTA*\n📅 {get_today_str()}\n\n"

    for city in CITY_LIST:
        display = get_city_display(city)
        hotels = get_hotels(city, 1)
        attractions = get_attractions(city, 1)

        top_hotel = hotels[0] if hotels else None
        top_attr = attractions[0] if attractions else None

        text += f"*{PIN_EMOJI} {display}*\n"
        if top_hotel:
            rating = top_hotel.get('rating', 0)
            text += f"   {HOTEL_EMOJI} Top Hotel: *{top_hotel['name']}* ({rating}/10)\n"
        if top_attr:
            text += f"   {ATTRACTION_EMOJI} Top Atraksi: *{top_attr['name']}*\n"
        text += f"   ➡️ /top {city}\n\n"

    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=city_keyboard(),
        disable_web_page_preview=True,
    )


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    last = db.get_last_scrape()
    stats = db.get_scrape_stats()

    text = f"{CHART_EMOJI} *STATUS BOT TRENDING*\n\n"
    text += f"*Last scrape:* {last[:16] if last else 'Belum pernah'}\n"
    text += f"*Auto-update:* Setiap hari jam {SCRAPE_HOUR:02d}:{SCRAPE_MINUTE:02d} WIB\n\n"

    if stats:
        text += "*Data per kota:*\n"
        for s in stats:
            city_display = get_city_display(s["city"])
            text += (
                f"\n*{PIN_EMOJI} {city_display}*\n"
                f"   {HOTEL_EMOJI} Hotel: {db.get_hotel_count(s['city'])} data\n"
                f"   {ATTRACTION_EMOJI} Atraksi: {db.get_attraction_count(s['city'])} data\n"
                f"   📅 Update: {s['last_update'][:16] if s['last_update'] else 'N/A'}\n"
            )
    else:
        for city in CITY_LIST:
            h_count = db.get_hotel_count(city)
            a_count = db.get_attraction_count(city)
            text += f"*{get_city_display(city)}*: {h_count} hotel, {a_count} atraksi\n"

    text += f"\n_Ketik /refresh untuk update manual_"
    await update.message.reply_text(text, parse_mode="Markdown")


async def cmd_refresh(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"🔄 *Memulai scraping data terbaru...*\n"
        "Ini bisa memakan waktu 1-2 menit.",
        parse_mode="Markdown",
    )

    try:
        results = await scrape_all()
        summary = "\n".join(
            f"   • {r['city'].title()}: {r['hotels']} hotel, {r['attractions']} atraksi"
            for r in results
        )
        await update.message.reply_text(
            f"✅ *Scraping selesai!*\n\n{summary}\n\n"
            f"Data sudah di-update. Cek dengan /top [kota]",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error("Scrape error: %s", e)
        await update.message.reply_text(
            f"❌ *Gagal scraping:* {e}\n\nData lama masih tersedia.",
            parse_mode="Markdown",
        )


# ── Callback handler ───────────────────────────────────────────────────


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_cities":
        text = (
            f"{FIRE_EMOJI} *Top Trending Hotel & Atraksi*\n"
            f"📅 Update: {get_today_str()}\n\n"
            "Pilih kota:"
        )
        await query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=city_keyboard()
        )
        return

    if data.startswith("top_"):
        city = data.replace("top_", "")
        text = build_top_text(city)
        await query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=detail_keyboard(city),
            disable_web_page_preview=True,
        )
        return

    if data.startswith("hotel_"):
        city = data.replace("hotel_", "")
        text = build_hotel_text(city)
        await query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=back_keyboard(city),
            disable_web_page_preview=True,
        )
        return

    if data.startswith("atraksi_"):
        city = data.replace("atraksi_", "")
        text = build_attraction_text(city)
        await query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=back_keyboard(city),
            disable_web_page_preview=True,
        )
        return


# ── Text builders ──────────────────────────────────────────────────────


def build_top_text(city: str) -> str:
    display = get_city_display(city)
    hotels = get_hotels(city, 5)
    attractions = get_attractions(city, 3)

    last = db.get_last_scrape(city)
    update_str = f"Last update: {last[:16]}" if last else get_today_str()

    text = (
        f"{FIRE_EMOJI} *TOP TRENDING — {display.upper()}*\n"
        f"📅 {update_str}\n\n"
    )

    text += f"*{HOTEL_EMOJI} Top 5 Hotel:*\n\n"
    for i, h in enumerate(hotels, 1):
        text += format_hotel(h, i) + "\n"

    if not hotels:
        text += "_Belum ada data. Ketik /refresh_\n\n"

    text += f"*{ATTRACTION_EMOJI} Top 3 Atraksi:*\n\n"
    for i, a in enumerate(attractions, 1):
        text += format_attraction(a, i) + "\n"

    if not attractions:
        text += "_Belum ada data. Ketik /refresh_\n\n"

    return text


def build_hotel_text(city: str) -> str:
    display = get_city_display(city)
    hotels = get_hotels(city, 15)

    text = (
        f"{HOTEL_EMOJI} *SEMUA HOTEL TRENDING — {display.upper()}*\n"
        f"📅 {get_today_str()}\n\n"
    )

    for i, h in enumerate(hotels, 1):
        text += format_hotel(h, i) + "\n"

    if not hotels:
        text += "_Belum ada data. Ketik /refresh_\n"

    text += f"_Total: {len(hotels)} hotel trending_"
    return text


def build_attraction_text(city: str) -> str:
    display = get_city_display(city)
    attractions = get_attractions(city, 15)

    text = (
        f"{ATTRACTION_EMOJI} *SEMUA ATRAKSI TRENDING — {display.upper()}*\n"
        f"📅 {get_today_str()}\n\n"
    )

    for i, a in enumerate(attractions, 1):
        text += format_attraction(a, i) + "\n"

    if not attractions:
        text += "_Belum ada data. Ketik /refresh_\n"

    text += f"_Total: {len(attractions)} atraksi trending_"
    return text


# ── Scheduled job ──────────────────────────────────────────────────────


async def scheduled_scrape(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Run daily scrape job."""
    logger.info("Running scheduled daily scrape...")
    try:
        results = await scrape_all()
        total_h = sum(r["hotels"] for r in results)
        total_a = sum(r["attractions"] for r in results)
        logger.info("Scheduled scrape done: %d hotels, %d attractions", total_h, total_a)
    except Exception as e:
        logger.error("Scheduled scrape failed: %s", e)


# ── Main ───────────────────────────────────────────────────────────────


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return

    # Initialize database and seed with curated data
    db.init_db()
    seed_from_curated()
    logger.info("Database initialized and seeded.")

    app = Application.builder().token(token).build()

    # Commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("top", cmd_top))
    app.add_handler(CommandHandler("hotel", cmd_hotel))
    app.add_handler(CommandHandler("atraksi", cmd_atraksi))
    app.add_handler(CommandHandler("semua", cmd_semua))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("refresh", cmd_refresh))
    app.add_handler(CallbackQueryHandler(handle_callback))

    # Schedule daily scrape
    job_queue = app.job_queue
    scrape_time = time(hour=SCRAPE_HOUR, minute=SCRAPE_MINUTE)
    job_queue.run_daily(scheduled_scrape, time=scrape_time, name="daily_scrape")
    logger.info("Daily scrape scheduled at %02d:%02d", SCRAPE_HOUR, SCRAPE_MINUTE)

    logger.info("Bot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
