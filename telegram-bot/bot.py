import json
import logging
import os
import tempfile
from datetime import datetime

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import database as db
from utils import extract_urls, fetch_page_title, format_bookmark, format_bookmark_short

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

PAGE_SIZE = 5


# ─── Helpers ────────────────────────────────────────────────────────────────────


def _ensure_user(update: Update) -> None:
    user = update.effective_user
    if user:
        db.ensure_user(user.id, user.username, user.first_name)


def _nav_keyboard(
    page: int,
    total: int,
    prefix: str,
    extra_params: str = "",
) -> list[list[InlineKeyboardButton]]:
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    buttons: list[InlineKeyboardButton] = []
    if page > 0:
        buttons.append(
            InlineKeyboardButton("\u25C0 Prev", callback_data=f"{prefix}:{page - 1}{extra_params}")
        )
    buttons.append(InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="noop"))
    if (page + 1) * PAGE_SIZE < total:
        buttons.append(
            InlineKeyboardButton("Next \u25B6", callback_data=f"{prefix}:{page + 1}{extra_params}")
        )
    return [buttons] if buttons else []


def _bookmark_action_keyboard(bookmark_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "\U0001F4CC Pin/Unpin", callback_data=f"pin:{bookmark_id}"
                ),
                InlineKeyboardButton(
                    "\U0001F3F7 Tag", callback_data=f"tagprompt:{bookmark_id}"
                ),
                InlineKeyboardButton(
                    "\U0001F5D1 Hapus", callback_data=f"del:{bookmark_id}"
                ),
            ]
        ]
    )


# ─── Command Handlers ──────────────────────────────────────────────────────────


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    text = (
        "\U0001F516 <b>Bookmark Bot</b>\n\n"
        "Simpan apa saja ke bookmark!\n\n"
        "<b>Cara pakai:</b>\n"
        "\u2022 Forward pesan apa saja ke sini \u2192 otomatis tersimpan\n"
        "\u2022 Kirim link \u2192 otomatis ambil judul halaman\n"
        "\u2022 Kirim teks/foto/video/dokumen \u2192 tersimpan\n\n"
        "<b>Perintah:</b>\n"
        "/list \u2014 Lihat semua bookmark\n"
        "/search <i>kata kunci</i> \u2014 Cari bookmark\n"
        "/tags \u2014 Lihat semua tag\n"
        "/filter <i>nama_tag</i> \u2014 Filter berdasarkan tag\n"
        "/pinned \u2014 Lihat bookmark yang di-pin\n"
        "/stats \u2014 Statistik bookmark\n"
        "/export \u2014 Export semua bookmark (JSON)\n"
        "/help \u2014 Tampilkan bantuan ini"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await cmd_start(update, context)


async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    user_id = update.effective_user.id
    await _send_bookmark_list(update, context, user_id, page=0)


async def _send_bookmark_list(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_id: int,
    page: int = 0,
    tag: str | None = None,
    content_type: str | None = None,
    pinned_only: bool = False,
    search: str | None = None,
    edit_message: bool = False,
) -> None:
    total = db.count_bookmarks(user_id, tag=tag, content_type=content_type, pinned_only=pinned_only, search=search)
    if total == 0:
        text = "\U0001F4ED Belum ada bookmark."
        if search:
            text = f'\U0001F50D Tidak ditemukan bookmark untuk "<i>{search}</i>".'
        elif tag:
            text = f'\U0001F3F7 Tidak ada bookmark dengan tag <b>#{tag}</b>.'
        if edit_message:
            await update.callback_query.edit_message_text(text, parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text(text, parse_mode=ParseMode.HTML)
        return

    bookmarks = db.get_bookmarks(
        user_id, limit=PAGE_SIZE, offset=page * PAGE_SIZE,
        tag=tag, content_type=content_type, pinned_only=pinned_only, search=search,
    )

    lines = []
    if search:
        lines.append(f'\U0001F50D Hasil pencarian: "<b>{search}</b>"\n')
    elif tag:
        lines.append(f"\U0001F3F7 Tag: <b>#{tag}</b>\n")
    elif pinned_only:
        lines.append("\U0001F4CC <b>Bookmark yang di-pin:</b>\n")
    else:
        lines.append("\U0001F516 <b>Bookmark kamu:</b>\n")

    for bm in bookmarks:
        tags = db.get_bookmark_tags(bm["id"])
        lines.append(format_bookmark(bm, tags))
        lines.append("")

    lines.append(f"\U0001F4CA Total: {total} bookmark")

    extra = ""
    prefix = "list"
    if tag:
        extra = f":t={tag}"
        prefix = "filt"
    elif search:
        extra = f":s={search}"
        prefix = "srch"
    elif pinned_only:
        prefix = "pinn"

    nav = _nav_keyboard(page, total, prefix, extra)

    action_rows = []
    for bm in bookmarks:
        action_rows.append(
            [
                InlineKeyboardButton(
                    f"#{bm['id']} \U0001F4CC", callback_data=f"pin:{bm['id']}"
                ),
                InlineKeyboardButton(
                    f"#{bm['id']} \U0001F3F7", callback_data=f"tagprompt:{bm['id']}"
                ),
                InlineKeyboardButton(
                    f"#{bm['id']} \U0001F5D1", callback_data=f"del:{bm['id']}"
                ),
            ]
        )

    keyboard = InlineKeyboardMarkup(action_rows + nav)
    text = "\n".join(lines)

    if edit_message:
        await update.callback_query.edit_message_text(
            text, parse_mode=ParseMode.HTML, reply_markup=keyboard, disable_web_page_preview=True,
        )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.HTML, reply_markup=keyboard, disable_web_page_preview=True,
        )


async def cmd_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    if not context.args:
        await update.message.reply_text(
            "\U0001F50D Pakai: /search <i>kata kunci</i>", parse_mode=ParseMode.HTML
        )
        return
    query = " ".join(context.args)
    user_id = update.effective_user.id
    await _send_bookmark_list(update, context, user_id, search=query)


async def cmd_filter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    if not context.args:
        await update.message.reply_text(
            "\U0001F3F7 Pakai: /filter <i>nama_tag</i>", parse_mode=ParseMode.HTML
        )
        return
    tag_name = context.args[0].lower().strip().lstrip("#")
    user_id = update.effective_user.id
    await _send_bookmark_list(update, context, user_id, tag=tag_name)


async def cmd_pinned(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    user_id = update.effective_user.id
    await _send_bookmark_list(update, context, user_id, pinned_only=True)


async def cmd_tags(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    user_id = update.effective_user.id
    tags = db.get_user_tags(user_id)
    if not tags:
        await update.message.reply_text("\U0001F3F7 Belum ada tag. Tambahkan tag ke bookmark dengan tombol \U0001F3F7.")
        return

    lines = ["\U0001F3F7 <b>Tag kamu:</b>\n"]
    buttons = []
    for t in tags:
        lines.append(f"  \u2022 <b>#{t['name']}</b> ({t['count']} bookmark)")
        buttons.append(
            [InlineKeyboardButton(f"#{t['name']} ({t['count']})", callback_data=f"filtertag:{t['name']}")]
        )

    keyboard = InlineKeyboardMarkup(buttons) if buttons else None
    await update.message.reply_text(
        "\n".join(lines), parse_mode=ParseMode.HTML, reply_markup=keyboard
    )


async def cmd_tag(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    if len(context.args) < 2:
        await update.message.reply_text(
            "\U0001F3F7 Pakai: /tag <i>id_bookmark</i> <i>nama_tag</i>\n"
            "Contoh: /tag 5 travel",
            parse_mode=ParseMode.HTML,
        )
        return
    try:
        bookmark_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("\u274C ID bookmark harus angka.")
        return

    tag_name = context.args[1].lower().strip().lstrip("#")
    user_id = update.effective_user.id

    bm = db.get_bookmark_by_id(bookmark_id, user_id)
    if not bm:
        await update.message.reply_text("\u274C Bookmark tidak ditemukan.")
        return

    tag_id = db.add_tag(user_id, tag_name)
    db.tag_bookmark(bookmark_id, tag_id)
    await update.message.reply_text(
        f"\U0001F3F7 Tag <b>#{tag_name}</b> ditambahkan ke bookmark <b>#{bookmark_id}</b>.",
        parse_mode=ParseMode.HTML,
    )


async def cmd_untag(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    if len(context.args) < 2:
        await update.message.reply_text(
            "\U0001F3F7 Pakai: /untag <i>id_bookmark</i> <i>nama_tag</i>",
            parse_mode=ParseMode.HTML,
        )
        return
    try:
        bookmark_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("\u274C ID bookmark harus angka.")
        return

    tag_name = context.args[1].lower().strip().lstrip("#")
    user_id = update.effective_user.id

    tag = db.get_tag_by_name(user_id, tag_name)
    if not tag:
        await update.message.reply_text(f'\u274C Tag "{tag_name}" tidak ditemukan.')
        return

    db.untag_bookmark(bookmark_id, tag["id"])
    await update.message.reply_text(
        f"\U0001F3F7 Tag <b>#{tag_name}</b> dihapus dari bookmark <b>#{bookmark_id}</b>.",
        parse_mode=ParseMode.HTML,
    )


async def cmd_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    if not context.args:
        await update.message.reply_text(
            "\U0001F5D1 Pakai: /delete <i>id_bookmark</i>",
            parse_mode=ParseMode.HTML,
        )
        return
    try:
        bookmark_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("\u274C ID bookmark harus angka.")
        return

    user_id = update.effective_user.id
    if db.delete_bookmark(bookmark_id, user_id):
        await update.message.reply_text(f"\U0001F5D1 Bookmark <b>#{bookmark_id}</b> dihapus.", parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text("\u274C Bookmark tidak ditemukan.")


async def cmd_pin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    if not context.args:
        await update.message.reply_text(
            "\U0001F4CC Pakai: /pin <i>id_bookmark</i>",
            parse_mode=ParseMode.HTML,
        )
        return
    try:
        bookmark_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("\u274C ID bookmark harus angka.")
        return

    user_id = update.effective_user.id
    result = db.toggle_pin(bookmark_id, user_id)
    if result is None:
        await update.message.reply_text("\u274C Bookmark tidak ditemukan.")
    elif result:
        await update.message.reply_text(f"\U0001F4CC Bookmark <b>#{bookmark_id}</b> di-pin!", parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(f"\U0001F4CC Bookmark <b>#{bookmark_id}</b> di-unpin.", parse_mode=ParseMode.HTML)


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    user_id = update.effective_user.id
    stats = db.get_stats(user_id)

    lines = [
        "\U0001F4CA <b>Statistik Bookmark</b>\n",
        f"\U0001F516 Total: <b>{stats['total']}</b>",
        f"\U0001F4CC Di-pin: <b>{stats['pinned']}</b>",
        f"\U0001F3F7 Tag: <b>{stats['tags']}</b>",
    ]
    if stats["types"]:
        lines.append("\n<b>Berdasarkan tipe:</b>")
        type_emoji = {
            "text": "\U0001F4DD", "link": "\U0001F517", "photo": "\U0001F5BC",
            "video": "\U0001F3AC", "document": "\U0001F4CE", "audio": "\U0001F3B5",
            "voice": "\U0001F3A4", "sticker": "\U0001F600",
        }
        for t, c in stats["types"].items():
            emoji = type_emoji.get(t, "\U0001F4DD")
            lines.append(f"  {emoji} {t}: <b>{c}</b>")

    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)


async def cmd_export(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    user_id = update.effective_user.id
    bookmarks = db.export_bookmarks(user_id)

    if not bookmarks:
        await update.message.reply_text("\U0001F4ED Belum ada bookmark untuk di-export.")
        return

    export_data = {
        "exported_at": datetime.now().isoformat(),
        "total": len(bookmarks),
        "bookmarks": bookmarks,
    }

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", prefix="bookmarks_", delete=False
    ) as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        filepath = f.name

    await update.message.reply_document(
        document=open(filepath, "rb"),
        filename=f"bookmarks_{user_id}_{datetime.now().strftime('%Y%m%d')}.json",
        caption=f"\U0001F4E6 Export selesai! {len(bookmarks)} bookmark.",
    )
    os.unlink(filepath)


# ─── Message Handler (Save Bookmark) ───────────────────────────────────────────


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    _ensure_user(update)
    user_id = update.effective_user.id
    message = update.message

    content = ""
    content_type = "text"
    url = None
    title = None
    file_id = None

    if message.photo:
        content_type = "photo"
        file_id = message.photo[-1].file_id
        content = message.caption or "[Photo]"
    elif message.video:
        content_type = "video"
        file_id = message.video.file_id
        content = message.caption or "[Video]"
    elif message.document:
        content_type = "document"
        file_id = message.document.file_id
        content = message.caption or message.document.file_name or "[Document]"
    elif message.audio:
        content_type = "audio"
        file_id = message.audio.file_id
        content = message.caption or message.audio.title or "[Audio]"
    elif message.voice:
        content_type = "voice"
        file_id = message.voice.file_id
        content = "[Voice Message]"
    elif message.sticker:
        content_type = "sticker"
        file_id = message.sticker.file_id
        content = message.sticker.emoji or "[Sticker]"
    elif message.text:
        content = message.text
        urls = extract_urls(message.text)
        if urls:
            content_type = "link"
            url = urls[0]
            title = await fetch_page_title(url)

    if not content and not file_id:
        return

    bookmark_id = db.add_bookmark(
        user_id=user_id,
        content=content,
        content_type=content_type,
        url=url,
        title=title,
        file_id=file_id,
    )

    response_lines = [f"\U0001F516 Tersimpan! <b>#{bookmark_id}</b>"]
    if title:
        response_lines.append(f"\U0001F4D6 {title}")
    if url:
        response_lines.append(f"\U0001F517 {url}")

    response_lines.append(
        "\n\U0001F4A1 Tambah tag: /tag " + str(bookmark_id) + " <i>nama_tag</i>"
    )

    keyboard = _bookmark_action_keyboard(bookmark_id)

    await message.reply_text(
        "\n".join(response_lines),
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


# ─── Callback Query Handler ────────────────────────────────────────────────────


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id

    if data == "noop":
        return

    if data.startswith("pin:"):
        bookmark_id = int(data.split(":")[1])
        result = db.toggle_pin(bookmark_id, user_id)
        if result is None:
            await query.answer("Bookmark tidak ditemukan.", show_alert=True)
        elif result:
            await query.answer("\U0001F4CC Di-pin!")
        else:
            await query.answer("\U0001F4CC Di-unpin.")

    elif data.startswith("del:"):
        bookmark_id = int(data.split(":")[1])
        if db.delete_bookmark(bookmark_id, user_id):
            await query.answer("\U0001F5D1 Dihapus!")
            try:
                await query.edit_message_text(
                    f"\U0001F5D1 Bookmark <b>#{bookmark_id}</b> telah dihapus.",
                    parse_mode=ParseMode.HTML,
                )
            except Exception:
                pass
        else:
            await query.answer("Bookmark tidak ditemukan.", show_alert=True)

    elif data.startswith("tagprompt:"):
        bookmark_id = data.split(":")[1]
        await query.answer()
        await query.message.reply_text(
            f"\U0001F3F7 Untuk menambah tag ke bookmark <b>#{bookmark_id}</b>, kirim:\n"
            f"/tag {bookmark_id} <i>nama_tag</i>",
            parse_mode=ParseMode.HTML,
        )

    elif data.startswith("filtertag:"):
        tag_name = data.split(":")[1]
        await _send_bookmark_list(update, context, user_id, tag=tag_name, edit_message=True)

    elif data.startswith("list:"):
        page = int(data.split(":")[1])
        await _send_bookmark_list(update, context, user_id, page=page, edit_message=True)

    elif data.startswith("filt:"):
        parts = data.split(":")
        page = int(parts[1])
        tag = parts[2].replace("t=", "") if len(parts) > 2 else None
        await _send_bookmark_list(update, context, user_id, page=page, tag=tag, edit_message=True)

    elif data.startswith("srch:"):
        parts = data.split(":")
        page = int(parts[1])
        search = parts[2].replace("s=", "") if len(parts) > 2 else None
        await _send_bookmark_list(update, context, user_id, page=page, search=search, edit_message=True)

    elif data.startswith("pinn:"):
        page = int(data.split(":")[1])
        await _send_bookmark_list(update, context, user_id, page=page, pinned_only=True, edit_message=True)


# ─── Main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        return

    db.init_db()

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("list", cmd_list))
    app.add_handler(CommandHandler("search", cmd_search))
    app.add_handler(CommandHandler("filter", cmd_filter))
    app.add_handler(CommandHandler("pinned", cmd_pinned))
    app.add_handler(CommandHandler("tags", cmd_tags))
    app.add_handler(CommandHandler("tag", cmd_tag))
    app.add_handler(CommandHandler("untag", cmd_untag))
    app.add_handler(CommandHandler("delete", cmd_delete))
    app.add_handler(CommandHandler("pin", cmd_pin))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("export", cmd_export))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

    logger.info("Bot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
