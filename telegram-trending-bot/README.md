# 🔥 Bot Telegram — Top Trending Hotel & Atraksi

Bot Telegram untuk menampilkan hotel dan atraksi yang sedang trending/terlaris di Jawa Timur.
**Auto-scrape harian** — data otomatis di-update setiap hari dari search engine.

## Kota Tersedia
- **Surabaya** — 2.288 hotel, wisata kota
- **Sidoarjo** — Dekat bandara Juanda, wisata keluarga
- **Mojokerto** — Warisan Majapahit, wisata alam Trawas/Pacet
- **Pasuruan** — Taman Safari, wisata Tretes/Prigen

## Sumber Data
- Traveloka, Booking.com, Agoda, Trip.com, Klook, Tiket.com, Trivago, TripAdvisor
- Data di-scrape via search engine (DuckDuckGo) untuk menghindari anti-bot platform OTA

## Arsitektur
```
bot.py          — Telegram bot handlers & scheduler
data.py         — Curated seed data (initial/fallback)
database.py     — SQLite storage (hotels, attractions, scrape logs)
scraper.py      — Search-based scraper (DuckDuckGo → parse hotel/attraction data)
requirements.txt
```

## Perintah Bot
| Perintah | Fungsi |
|----------|--------|
| `/start` | Menu utama dengan tombol pilih kota |
| `/top [kota]` | Top 5 hotel & 3 atraksi trending |
| `/hotel [kota]` | Semua hotel trending di kota |
| `/atraksi [kota]` | Semua atraksi trending di kota |
| `/semua` | Ringkasan semua kota |
| `/status` | Lihat status last update & jumlah data |
| `/refresh` | Manual trigger scraping data terbaru |
| `/help` | Panduan bot |

## Fitur Auto-Update
- **Scheduled scrape** — setiap hari jam 06:00 WIB (configurable via env var)
- **Manual refresh** — ketik `/refresh` untuk force update kapan saja
- **SQLite database** — data tersimpan persisten, survive restart
- **Fallback** — kalau DB kosong, pakai curated data sebagai backup

### Environment Variables
| Variable | Default | Keterangan |
|----------|---------|------------|
| `TELEGRAM_BOT_TOKEN` | (required) | Token dari @BotFather |
| `SCRAPE_HOUR` | `6` | Jam scrape harian (0-23) |
| `SCRAPE_MINUTE` | `0` | Menit scrape harian (0-59) |

## Cara Menjalankan

### 1. Buat Bot di Telegram
1. Buka [@BotFather](https://t.me/BotFather)
2. Kirim `/newbot`
3. Ikuti instruksi, beri nama & username
4. Copy token yang diberikan

### 2. Install & Run
```bash
pip install -r requirements.txt
TELEGRAM_BOT_TOKEN="your-token-here" python bot.py
```

### 3. Mulai Chat
Buka bot kamu di Telegram, ketik `/start` dan pilih kota!

## Screenshot Preview

```
🔥 TOP TRENDING — SURABAYA
📅 2026-05-01T02:28
🕐 Auto-update setiap hari jam 06:00 WIB

🏨 Top 5 Hotel:

1. Platinum Hotel Tunjungan ⭐⭐⭐⭐
   📊 Rating: 9.2/10 (1,757 review)
   💰 Harga: Rp 988.867 /malam
   🌐 Platform: Traveloka
   🔥 #1 popularitas Traveloka Surabaya

🎢 Top 3 Atraksi:

1. Tour Gunung Bromo (dari Surabaya)
   💰 Tiket: Rp 370rb-1.6jt
   🌐 Platform: Klook | 6K+ booked
   🔥 TERLARIS #1! Sunrise tour paling dicari
```

## Pengembangan Selanjutnya
- [x] ~~Web scraping dari platform OTA~~ (via search engine)
- [x] ~~Scheduled daily update~~ (APScheduler, jam 06:00 WIB)
- [ ] Notifikasi otomatis ke channel/group
- [ ] Tambah kota lain di Jawa Timur
- [ ] Filter berdasarkan harga, rating, platform
- [ ] Deploy ke Railway/Fly.io untuk 24/7
