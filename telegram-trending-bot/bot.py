"""Telegram Bot — Top Trending Hotels & Attractions (East Java)."""

import logging
import os
from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from data import (
    ATTRACTIONS,
    CITIES,
    HOTELS,
    get_city_display,
    get_today_str,
)

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


# ── Formatters ──────────────────────────────────────────────────────────


def format_hotel(h: dict, rank: int) -> str:
    stars = STAR_EMOJI * h["stars"]
    url_part = f" [🔗 Lihat]({h['url']})" if h.get("url") else ""
    return (
        f"*{rank}. {h['name']}* {stars}\n"
        f"   {CHART_EMOJI} Rating: *{h['rating']}/10* ({h['reviews']:,} review)\n"
        f"   {MONEY_EMOJI} Harga: `{h['price']}` /malam\n"
        f"   {GLOBE_EMOJI} Platform: {h['platform']}\n"
        f"   {FIRE_EMOJI} {h['highlight']}{url_part}\n"
    )


def format_attraction(a: dict, rank: int) -> str:
    booked_part = f" | {a['booked']} booked" if a.get("booked") else ""
    url_part = f" [🔗 Lihat]({a['url']})" if a.get("url") else ""
    return (
        f"*{rank}. {a['name']}*\n"
        f"   {MONEY_EMOJI} Tiket: `{a['price']}`\n"
        f"   {GLOBE_EMOJI} Platform: {a['platform']}{booked_part}\n"
        f"   {FIRE_EMOJI} {a['highlight']}{url_part}\n"
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
    text = (
        f"{FIRE_EMOJI} *Top Trending Hotel & Atraksi*\n"
        f"📅 Update: {get_today_str()}\n\n"
        "Pilih kota untuk lihat trending hari ini:\n\n"
        "Atau ketik langsung:\n"
        "• `/top surabaya` — Top Surabaya\n"
        "• `/top sidoarjo` — Top Sidoarjo\n"
        "• `/top mojokerto` — Top Mojokerto\n"
        "• `/top pasuruan` — Top Pasuruan\n"
        "• `/hotel surabaya` — Hotel saja\n"
        "• `/atraksi pasuruan` — Atraksi saja\n"
        "• `/semua` — Semua kota\n"
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
        "• `/start` — Menu utama\n\n"
        "*Kota tersedia:*\n"
        "Surabaya, Sidoarjo, Mojokerto, Pasuruan\n\n"
        "*Data dari:*\n"
        "Traveloka, Booking.com, Agoda, Trip.com, Klook, Tiket.com\n\n"
        f"📅 Terakhir update: {get_today_str()}"
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
    if city not in CITIES:
        await update.message.reply_text(
            f"❌ Kota *{city}* tidak ditemukan.\n"
            f"Kota tersedia: {', '.join(c.title() for c in CITIES)}",
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
    if city not in CITIES:
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
    if city not in CITIES:
        await update.message.reply_text(f"❌ Kota *{city}* tidak tersedia.", parse_mode="Markdown")
        return

    text = build_attraction_text(city)
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=back_keyboard(city),
        disable_web_page_preview=True,
    )


async def cmd_semua(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = f"{FIRE_EMOJI} *RINGKASAN TRENDING — SEMUA KOTA*\n📅 {get_today_str()}\n\n"

    for city in CITIES:
        display = get_city_display(city)
        hotels = HOTELS.get(city, [])
        attractions = ATTRACTIONS.get(city, [])

        top_hotel = hotels[0] if hotels else None
        top_attr = attractions[0] if attractions else None

        text += f"*{PIN_EMOJI} {display}*\n"
        if top_hotel:
            text += f"   {HOTEL_EMOJI} Top Hotel: *{top_hotel['name']}* ({top_hotel['rating']}/10)\n"
        if top_attr:
            text += f"   {ATTRACTION_EMOJI} Top Atraksi: *{top_attr['name']}*\n"
        text += f"   ➡️ /top {city}\n\n"

    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=city_keyboard(),
        disable_web_page_preview=True,
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
    hotels = HOTELS.get(city, [])[:5]
    attractions = ATTRACTIONS.get(city, [])[:3]

    text = (
        f"{FIRE_EMOJI} *TOP TRENDING — {display.upper()}*\n"
        f"📅 {get_today_str()}\n\n"
    )

    text += f"*{HOTEL_EMOJI} Top 5 Hotel:*\n\n"
    for i, h in enumerate(hotels, 1):
        text += format_hotel(h, i) + "\n"

    text += f"*{ATTRACTION_EMOJI} Top 3 Atraksi:*\n\n"
    for i, a in enumerate(attractions, 1):
        text += format_attraction(a, i) + "\n"

    return text


def build_hotel_text(city: str) -> str:
    display = get_city_display(city)
    hotels = HOTELS.get(city, [])

    text = (
        f"{HOTEL_EMOJI} *SEMUA HOTEL TRENDING — {display.upper()}*\n"
        f"📅 {get_today_str()}\n\n"
    )

    for i, h in enumerate(hotels, 1):
        text += format_hotel(h, i) + "\n"

    text += f"_Total: {len(hotels)} hotel trending_"
    return text


def build_attraction_text(city: str) -> str:
    display = get_city_display(city)
    attractions = ATTRACTIONS.get(city, [])

    text = (
        f"{ATTRACTION_EMOJI} *SEMUA ATRAKSI TRENDING — {display.upper()}*\n"
        f"📅 {get_today_str()}\n\n"
    )

    for i, a in enumerate(attractions, 1):
        text += format_attraction(a, i) + "\n"

    text += f"_Total: {len(attractions)} atraksi trending_"
    return text


# ── Main ───────────────────────────────────────────────────────────────


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("top", cmd_top))
    app.add_handler(CommandHandler("hotel", cmd_hotel))
    app.add_handler(CommandHandler("atraksi", cmd_atraksi))
    app.add_handler(CommandHandler("semua", cmd_semua))
    app.add_handler(CallbackQueryHandler(handle_callback))

    logger.info("Bot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
