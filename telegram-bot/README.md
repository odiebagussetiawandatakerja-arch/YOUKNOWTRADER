# Telegram Bookmark Bot

Bot Telegram untuk menyimpan dan mengelola bookmark dari chat. Simpan link, teks, foto, video, dokumen — semuanya terorganisir dengan tag dan pencarian.

## Fitur

- **Auto-save** — Forward pesan atau kirim apa saja ke bot, otomatis tersimpan
- **Auto-detect URL** — Link otomatis dideteksi dan judul halaman diambil
- **Mendukung semua tipe** — Teks, link, foto, video, dokumen, audio, voice, sticker
- **Tag system** — Organisasi bookmark dengan tag (#travel, #work, dll)
- **Search** — Cari bookmark berdasarkan kata kunci
- **Filter** — Filter bookmark berdasarkan tag
- **Pin/Favorite** — Pin bookmark penting supaya selalu di atas
- **Pagination** — Navigasi bookmark dengan tombol inline
- **Export** — Export semua bookmark ke file JSON
- **Statistik** — Lihat ringkasan bookmark kamu

## Perintah Bot

| Perintah | Fungsi |
|----------|--------|
| `/start` | Mulai bot dan lihat panduan |
| `/list` | Lihat semua bookmark |
| `/search <kata>` | Cari bookmark |
| `/tags` | Lihat semua tag |
| `/filter <tag>` | Filter berdasarkan tag |
| `/tag <id> <tag>` | Tambah tag ke bookmark |
| `/untag <id> <tag>` | Hapus tag dari bookmark |
| `/pin <id>` | Pin/unpin bookmark |
| `/delete <id>` | Hapus bookmark |
| `/pinned` | Lihat bookmark yang di-pin |
| `/stats` | Statistik bookmark |
| `/export` | Export bookmark ke JSON |
| `/help` | Tampilkan bantuan |

## Setup

### 1. Buat Bot di Telegram

1. Buka [@BotFather](https://t.me/BotFather) di Telegram
2. Kirim `/newbot`
3. Ikuti instruksi, beri nama dan username untuk bot
4. Salin **Bot Token** yang diberikan

### 2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Jalankan Bot

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token-here"
python bot.py
```

### Environment Variables

| Variable | Deskripsi | Default |
|----------|-----------|---------|
| `TELEGRAM_BOT_TOKEN` | Token dari @BotFather (wajib) | - |
| `BOOKMARK_DB_PATH` | Path file database SQLite | `bookmarks.db` |

## Cara Pakai

1. **Simpan bookmark** — Kirim atau forward pesan apa saja ke bot
2. **Tambah tag** — Klik tombol 🏷 atau kirim `/tag <id> <nama_tag>`
3. **Pin bookmark** — Klik tombol 📌 atau kirim `/pin <id>`
4. **Cari** — Kirim `/search kata kunci`
5. **Filter** — Kirim `/filter nama_tag` atau klik tag di `/tags`
6. **Hapus** — Klik tombol 🗑 atau kirim `/delete <id>`
7. **Export** — Kirim `/export` untuk download file JSON

## Tech Stack

- Python 3.12+
- python-telegram-bot 22.x
- SQLite (via built-in sqlite3)
- aiohttp + BeautifulSoup4 (untuk fetch judul halaman)
