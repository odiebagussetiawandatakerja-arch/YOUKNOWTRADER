# 🔥 Bot Telegram — Top Trending Hotel & Atraksi

Bot Telegram untuk menampilkan hotel dan atraksi yang sedang trending/terlaris di Jawa Timur.

## Kota Tersedia
- **Surabaya** — 2.288 hotel, wisata kota
- **Sidoarjo** — Dekat bandara Juanda, wisata keluarga
- **Mojokerto** — Warisan Majapahit, wisata alam Trawas/Pacet
- **Pasuruan** — Taman Safari, wisata Tretes/Prigen

## Sumber Data
- Traveloka, Booking.com, Agoda, Trip.com, Klook, Tiket.com, Trivago, TripAdvisor

## Perintah Bot
| Perintah | Fungsi |
|----------|--------|
| `/start` | Menu utama dengan tombol pilih kota |
| `/top [kota]` | Top 5 hotel & 3 atraksi trending |
| `/hotel [kota]` | Semua hotel trending di kota |
| `/atraksi [kota]` | Semua atraksi trending di kota |
| `/semua` | Ringkasan semua kota |
| `/help` | Panduan bot |

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
📅 01 May 2026

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
- [ ] Web scraping real-time dari platform OTA
- [ ] Scheduled daily update (auto-scrape setiap hari)
- [ ] Notifikasi otomatis ke channel/group
- [ ] Tambah kota lain di Jawa Timur
- [ ] Filter berdasarkan harga, rating, platform
