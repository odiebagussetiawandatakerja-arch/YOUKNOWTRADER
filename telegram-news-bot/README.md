# ⚡ YouKnowTrader News Bot

Bot Telegram berita finansial **tercepat** dengan auto-translate ke Bahasa Indonesia.

## Fitur

- **Multi-kategori**: Crypto, Forex, Saham IDX, Komoditas, Berita Umum
- **30+ sumber berita**: CoinDesk, CoinTelegraph, DailyFX, CNBC Indonesia, Kontan, Kitco, Reuters, dll
- **Auto-translate**: Semua berita otomatis diterjemahkan ke Bahasa Indonesia
- **Update cepat**: Polling setiap 60 detik
- **Anti-duplikat**: SQLite dedup, tidak ada berita yang dikirim dua kali
- **Subscribe per kategori**: User bisa pilih kategori yang diminati
- **Channel broadcast**: Opsional kirim otomatis ke channel Telegram
- **Docker ready**: Siap deploy dengan Docker

## Sumber Berita

| Kategori | Sumber |
|----------|--------|
| ₿ Crypto | CoinDesk, CoinTelegraph, CryptoSlate, Bitcoin Magazine, Decrypt, The Block, CryptoNews |
| 💱 Forex | DailyFX, FXStreet, Investing.com, ForexLive |
| 📈 Saham IDX | CNBC Indonesia, Kontan, Bisnis.com, IDX Channel, Detik Finance |
| 🛢 Komoditas | Kitco, OilPrice, Investing.com Commodities |
| 📰 Umum | Reuters, Yahoo Finance, MarketWatch, Bloomberg |

## Setup

### 1. Buat Bot Telegram

1. Buka [@BotFather](https://t.me/BotFather) di Telegram
2. Kirim `/newbot`
3. Ikuti instruksi, simpan **Bot Token**

### 2. Install & Jalankan

```bash
cd telegram-news-bot

# Buat virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env, masukkan TELEGRAM_BOT_TOKEN

# Jalankan bot
python bot.py
```

### 3. Dengan Docker

```bash
cd telegram-news-bot

# Build image
docker build -t youknowtrader-newsbot .

# Jalankan
docker run -d \
  --name newsbot \
  -e TELEGRAM_BOT_TOKEN=your_token_here \
  -e TELEGRAM_CHANNEL_ID=@your_channel \
  -v newsbot-data:/app \
  youknowtrader-newsbot
```

## Perintah Bot

| Perintah | Deskripsi |
|----------|-----------|
| `/start` | Mulai & pilih kategori |
| `/help` | Tampilkan bantuan |
| `/subscribe` | Subscribe kategori baru |
| `/unsubscribe` | Unsubscribe kategori |
| `/mystatus` | Lihat subscription kamu |
| `/latest [kategori]` | Berita terbaru |
| `/crypto` | Berita crypto terbaru |
| `/forex` | Berita forex terbaru |
| `/idx` | Berita saham IDX terbaru |
| `/commodities` | Berita komoditas terbaru |
| `/all` | Semua berita terbaru |

## Konfigurasi

| Variable | Default | Deskripsi |
|----------|---------|-----------|
| `TELEGRAM_BOT_TOKEN` | (required) | Token dari @BotFather |
| `TELEGRAM_CHANNEL_ID` | (optional) | ID channel untuk broadcast |
| `POLL_INTERVAL` | `60` | Interval polling dalam detik |
| `DB_PATH` | `news_bot.db` | Path database SQLite |
| `TARGET_LANG` | `id` | Bahasa target terjemahan |
| `MAX_ITEMS_PER_FETCH` | `5` | Maks item per fetch per sumber |

## Arsitektur

```
telegram-news-bot/
├── bot.py              # Main bot + command handlers + scheduler
├── news_fetcher.py     # Async RSS feed fetcher (parallel)
├── translator.py       # Auto-translate (Google Translate, free)
├── database.py         # SQLite dedup + user subscriptions
├── config.py           # Configuration & RSS feed URLs
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker containerization
├── .env.example        # Environment template
└── README.md           # Dokumentasi
```

## Cara Kerja

1. **Scheduler** berjalan setiap 60 detik
2. **news_fetcher** mengambil RSS feeds dari 30+ sumber secara **paralel** (async)
3. **database** mengecek apakah berita sudah pernah dikirim (dedup via SHA-256 hash)
4. **translator** menerjemahkan berita ke Bahasa Indonesia (skip jika sudah bahasa Indonesia)
5. **bot** mengirim berita ke semua subscriber sesuai kategori mereka

## License

MIT
