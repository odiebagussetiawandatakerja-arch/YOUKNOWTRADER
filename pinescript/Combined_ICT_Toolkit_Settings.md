# Combined ICT Toolkit — Setting Optimal per Instrument & Timeframe
## M15 | H4 | D1

---

## 🔧 GLOBAL SETTINGS (Berlaku untuk semua)

| Parameter | Nilai |
|-----------|-------|
| Timezone | America/New_York |
| VWAP Anchor | Session (M15), Week (H4), Month (D1) |
| DWM H/L | ON — Daily + Weekly + Monthly |
| HTF Candles | ON di M15 (tampilkan H1, H4), ON di H4 (tampilkan D1, W) |

---

## 1️⃣ FOREX MAJOR (EUR/USD, GBP/USD, USD/JPY, USD/CHF, AUD/USD, NZD/USD, USD/CAD)

### Killzone Times (EST — sudah default di script)
| Killzone | Waktu EST | Catatan |
|----------|-----------|---------|
| Asia | 20:00-00:00 | Setup liquidity, low volatility |
| London | 02:00-05:00 | Breakout utama, highest probability |
| NY AM | 09:30-11:00 | Highest volume, overlap London |
| NY Lunch | 12:00-13:00 | Low volume, sering reversal |
| NY PM | 13:30-16:00 | Closing moves, position squaring |

### EMA Settings

| Timeframe | EMA 1 | EMA 2 | EMA 3 | EMA 4 | HTF EMAs dari | Signal TF (Short/Med/Long) |
|-----------|-------|-------|-------|-------|---------------|---------------------------|
| **M15** | 9 | 21 | 50 | 200 | H1 | H1 / H4 / D1 |
| **H4** | 12 | 26 | 100 | 200 | D1 | H4 / D1 / W |
| **D1** | 20 | 50 | 100 | 200 | W | D1 / W / M |

### VWAP
| Timeframe | Anchor | Catatan |
|-----------|--------|---------|
| M15 | Session | Reset setiap hari |
| H4 | Week | Weekly VWAP |
| D1 | Month | Monthly VWAP |

### DWM H/L
- Daily H/L: ON (lookback 2)
- Weekly H/L: ON (lookback 1)
- Monthly H/L: ON (lookback 1)
- Projections: ON

### HTF Candles
| Timeframe | HTF 1 | HTF 2 | HTF 3 | HTF 4 |
|-----------|-------|-------|-------|-------|
| M15 | H1 (10 candles) | H4 (6 candles) | D1 (5 candles) | OFF |
| H4 | D1 (10 candles) | W (5 candles) | OFF | OFF |
| D1 | W (5 candles) | M (3 candles) | OFF | OFF |

---

## 2️⃣ FOREX CROSS (EUR/GBP, EUR/JPY, GBP/JPY, AUD/JPY, EUR/AUD, GBP/CHF, dll)

### Killzone Times — sama seperti Major, TAPI:
- **JPY crosses (GBP/JPY, EUR/JPY, AUD/JPY):** Asia killzone paling penting! Aktifkan Asia + London
- **EUR crosses (EUR/GBP, EUR/CHF):** London killzone paling penting! NY kurang relevan
- **AUD/NZD crosses:** Asia + London overlap paling aktif

### EMA Settings

| Timeframe | EMA 1 | EMA 2 | EMA 3 | EMA 4 | HTF EMAs dari | Signal TF |
|-----------|-------|-------|-------|-------|---------------|-----------|
| **M15** | 9 | 21 | 50 | 200 | H1 | H1 / H4 / D1 |
| **H4** | 12 | 26 | 100 | 200 | D1 | H4 / D1 / W |
| **D1** | 20 | 50 | 100 | 200 | W | D1 / W / M |

### Catatan Khusus Cross Pairs:
- Spread lebih besar → gunakan EMA lebih lambat (21 bukan 9 di M15)
- Volatilitas tinggi (GBP/JPY, GBP/NZD) → EMA 200 sebagai support/resistance kuat
- Low volatility crosses (EUR/GBP, EUR/CHF) → EMA 50 lebih reliabel

---

## 3️⃣ ALTCOIN (SOL, AVAX, MATIC, DOGE, SHIB, ARB, OP, dll)

### Killzone Times
Crypto 24/7, tapi masih ada pattern:
| Zone | Waktu EST | Catatan |
|------|-----------|---------|
| Asia | 20:00-00:00 | Altcoin Asia sering pump di sini |
| London | 02:00-05:00 | Volume mulai naik |
| NY AM | 09:30-11:00 | Volume tertinggi, banyak listing/news |
| NY PM | 13:30-16:00 | Follow-through dari NY open |

### EMA Settings

| Timeframe | EMA 1 | EMA 2 | EMA 3 | EMA 4 | HTF EMAs dari | Signal TF |
|-----------|-------|-------|-------|-------|---------------|-----------|
| **M15** | 9 | 21 | 50 | 200 | H1 | H1 / H4 / D1 |
| **H4** | 9 | 21 | 50 | 200 | D1 | H4 / D1 / W |
| **D1** | 12 | 26 | 50 | 200 | W | D1 / W / M |

### Catatan Khusus Altcoin:
- Altcoin SANGAT volatile → EMA 9/21 crossover sering false signal
- Gunakan EMA 50 dan 200 sebagai konfirmasi trend utama
- VWAP Session anchor paling berguna di M15
- Buy signal paling reliable: harga di atas EMA 200 D1 + EMA 9 cross di atas 21 di M15
- DWM H/L sangat penting — altcoin sering test previous day high/low

---

## 4️⃣ MAJOR CRYPTO (BTC/USD, ETH/USD)

### Killzone Times — sama seperti Altcoin tapi:
- BTC/ETH paling aktif di **NY AM overlap** (09:30-11:00 EST)
- CME Futures open/close berpengaruh besar
- Weekly close (Sunday 17:00 EST) penting untuk swing

### EMA Settings

| Timeframe | EMA 1 | EMA 2 | EMA 3 | EMA 4 | HTF EMAs dari | Signal TF |
|-----------|-------|-------|-------|-------|---------------|-----------|
| **M15** | 9 | 21 | 50 | 200 | H1 | H1 / H4 / D1 |
| **H4** | 12 | 26 | 100 | 200 | D1 | H4 / D1 / W |
| **D1** | 20 | 50 | 100 | 200 | W | D1 / W / M |

### Catatan Khusus BTC/ETH:
- EMA 20 & 50 di D1 = "bull/bear line" — sangat diperhatikan institusi
- EMA 200 D1 = level psikologis terpenting
- Golden Cross (EMA 50 > EMA 200 di D1) = sinyal bullrun jangka panjang
- VWAP Weekly anchor berguna di H4 untuk swing trading
- HTF Candles: tampilkan D1 + W di H4 chart

---

## 5️⃣ KOMODITAS (XAUUSD Gold, XAGUSD Silver, Oil WTI/Brent)

### Killzone Times
| Killzone | Waktu EST | Instrument |
|----------|-----------|-----------|
| Asia | 20:00-00:00 | Gold sering range, Oil tenang |
| London | 02:00-05:00 | **Gold paling aktif!** London fix |
| NY AM | 09:30-11:00 | **Gold + Oil paling aktif!** |
| NY Lunch | 12:00-13:00 | Sering reversal Gold |
| NY PM | 13:30-16:00 | Oil inventory report (Rabu) |

### EMA Settings — GOLD (XAUUSD)

| Timeframe | EMA 1 | EMA 2 | EMA 3 | EMA 4 | HTF EMAs dari | Signal TF |
|-----------|-------|-------|-------|-------|---------------|-----------|
| **M15** | 9 | 21 | 50 | 200 | H1 | H1 / H4 / D1 |
| **H4** | 12 | 26 | 100 | 200 | D1 | H4 / D1 / W |
| **D1** | 20 | 50 | 100 | 200 | W | D1 / W / M |

### EMA Settings — OIL (WTI/Brent)

| Timeframe | EMA 1 | EMA 2 | EMA 3 | EMA 4 | HTF EMAs dari | Signal TF |
|-----------|-------|-------|-------|-------|---------------|-----------|
| **M15** | 9 | 21 | 50 | 200 | H1 | H1 / H4 / D1 |
| **H4** | 12 | 26 | 100 | 200 | D1 | H4 / D1 / W |
| **D1** | 20 | 50 | 100 | 200 | W | D1 / W / M |

### Catatan Khusus Komoditas:
- **Gold:** London session = #1 trading window, NY AM = #2
- **Gold:** EMA 21 di M15 = dynamic support/resistance terbaik untuk scalping
- **Gold:** VWAP Session sangat dihormati — price sering bounce dari VWAP
- **Oil:** NY session (EIA report Rabu 10:30 EST) = volatilitas tinggi
- **Silver:** Mirip Gold tapi spread lebih besar, gunakan EMA lebih lambat (21 bukan 9)

---

## 6️⃣ SAHAM IDX (BBCA, BBRI, TLKM, BMRI, ASII, UNVR, dll)

### Killzone Times
IDX hanya buka di jam WIB, jadi killzone berbeda:
| Zone | Waktu WIB | EST Equivalent | Catatan |
|------|-----------|---------------|---------|
| Pre-Market | 08:45-09:00 | 20:45-21:00 | Setup |
| Morning Session | 09:00-11:30 | 21:00-23:30 | **Paling aktif!** |
| Lunch Break | 11:30-13:30 | 23:30-01:30 | Market tutup |
| Afternoon Session | 13:30-15:00 | 01:30-03:00 | Volume menurun |
| Closing | 14:50-15:00 | 02:50-03:00 | ARA/ARB sering di sini |

**⚠️ Killzone module kurang relevan untuk IDX** — nonaktifkan atau set custom session sesuai jam WIB

### EMA Settings

| Timeframe | EMA 1 | EMA 2 | EMA 3 | EMA 4 | HTF EMAs dari | Signal TF |
|-----------|-------|-------|-------|-------|---------------|-----------|
| **M15** | 9 | 20 | 50 | 200 | H1 | H1 / H4 / D1 |
| **H4** | 12 | 26 | 100 | 200 | D1 | H4 / D1 / W |
| **D1** | 20 | 50 | 100 | 200 | W | D1 / W / M |

### Catatan Khusus Saham IDX:
- **EMA 20 dan 50 di D1** = paling banyak digunakan trader IDX
- **EMA 200 D1** = support/resistance institusional
- **Volume sangat penting** — konfirmasi breakout dengan volume
- **VWAP** = Session anchor (reset harian), sangat berguna di M15
- **DWM H/L**: Daily lookback 3, Weekly lookback 2 — karena IDX range-bound
- Saham big cap (BBCA, BBRI) → EMA lebih lambat (20/50), small cap → EMA lebih cepat (9/21)
- **Timezone:** Set GMT+7 atau gunakan custom session di killzone settings

---

## 7️⃣ SAHAM US (AAPL, TSLA, MSFT, NVDA, AMZN, META, GOOGL, dll)

### Killzone Times (EST)
| Zone | Waktu EST | Catatan |
|------|-----------|---------|
| Pre-Market | 04:00-09:30 | News-driven moves, low liquidity |
| Market Open | 09:30-10:30 | **Highest volume!** Best scalping window |
| Mid-Morning | 10:30-12:00 | Trend development |
| Lunch | 12:00-13:00 | Low volume, choppy |
| Power Hour | 15:00-16:00 | **Second highest volume** — closing moves |

**Gunakan killzone settings:**
- NY AM: 09:30-11:00 (Market Open)
- NY Lunch: 12:00-13:00
- NY PM: 13:30-16:00 (termasuk Power Hour)
- Asia & London: OFF (tidak relevan untuk US stocks)

### EMA Settings

| Timeframe | EMA 1 | EMA 2 | EMA 3 | EMA 4 | HTF EMAs dari | Signal TF |
|-----------|-------|-------|-------|-------|---------------|-----------|
| **M15** | 9 | 21 | 50 | 200 | H1 | H1 / H4 / D1 |
| **H4** | 12 | 26 | 100 | 200 | D1 | H4 / D1 / W |
| **D1** | 20 | 50 | 100 | 200 | W | D1 / W / M |

### Catatan Khusus Saham US:
- **EMA 9/21 crossover di M15** = entry signal terbaik untuk day trading
- **EMA 20/50 di D1** = swing trading — 67% win rate dengan volume confirmation
- **EMA 200 D1** = institutional benchmark, fund managers watch this
- **VWAP Session** = #1 indicator untuk day trading US stocks
- **Golden Cross** (EMA 50 > 200 di D1) = strong bullish signal
- **Power Hour** (15:00-16:00) = sering ada big moves
- Tech stocks (TSLA, NVDA) lebih volatile → EMA 9/21 lebih responsif
- Blue chips (AAPL, MSFT) → EMA 20/50 lebih stabil

---

## 📋 QUICK REFERENCE — Setting Ringkas per Kategori

### M15 Timeframe (Scalping / Intraday)

| Kategori | EMA 1 | EMA 2 | EMA 3 | EMA 4 | HTF EMAs | VWAP | Killzone Paling Penting |
|----------|-------|-------|-------|-------|----------|------|------------------------|
| Forex Major | 9 | 21 | 50 | 200 | H1 | Session | London + NY AM |
| Forex Cross | 9 | 21 | 50 | 200 | H1 | Session | Tergantung pair* |
| Altcoin | 9 | 21 | 50 | 200 | H1 | Session | NY AM |
| BTC/ETH | 9 | 21 | 50 | 200 | H1 | Session | NY AM |
| Gold | 9 | 21 | 50 | 200 | H1 | Session | London + NY AM |
| Oil | 9 | 21 | 50 | 200 | H1 | Session | NY AM |
| Saham IDX | 9 | 20 | 50 | 200 | H1 | Session | Morning (09:00 WIB) |
| Saham US | 9 | 21 | 50 | 200 | H1 | Session | NY AM + Power Hour |

### H4 Timeframe (Swing Intraday / Short Swing)

| Kategori | EMA 1 | EMA 2 | EMA 3 | EMA 4 | HTF EMAs | VWAP | DWM H/L |
|----------|-------|-------|-------|-------|----------|------|---------|
| Forex Major | 12 | 26 | 100 | 200 | D1 | Week | D+W+M |
| Forex Cross | 12 | 26 | 100 | 200 | D1 | Week | D+W+M |
| Altcoin | 9 | 21 | 50 | 200 | D1 | Week | D+W |
| BTC/ETH | 12 | 26 | 100 | 200 | D1 | Week | D+W+M |
| Gold | 12 | 26 | 100 | 200 | D1 | Week | D+W+M |
| Oil | 12 | 26 | 100 | 200 | D1 | Week | D+W |
| Saham IDX | 12 | 26 | 100 | 200 | D1 | Week | D+W |
| Saham US | 12 | 26 | 100 | 200 | D1 | Week | D+W+M |

### D1 Timeframe (Swing / Position Trading)

| Kategori | EMA 1 | EMA 2 | EMA 3 | EMA 4 | HTF EMAs | VWAP | DWM H/L |
|----------|-------|-------|-------|-------|----------|------|---------|
| Forex Major | 20 | 50 | 100 | 200 | W | Month | W+M |
| Forex Cross | 20 | 50 | 100 | 200 | W | Month | W+M |
| Altcoin | 12 | 26 | 50 | 200 | W | Month | W+M |
| BTC/ETH | 20 | 50 | 100 | 200 | W | Month | W+M |
| Gold | 20 | 50 | 100 | 200 | W | Month | W+M |
| Oil | 20 | 50 | 100 | 200 | W | Month | W+M |
| Saham IDX | 20 | 50 | 100 | 200 | W | Month | W+M |
| Saham US | 20 | 50 | 100 | 200 | W | Month | W+M |

---

## 🎯 TIPS PENGGUNAAN

1. **Jangan aktifkan semua modul sekaligus** — pilih 2-3 modul yang paling relevan
2. **M15 scalping:** Fokus pada Killzones + EMA 9/21 + VWAP
3. **H4 swing:** Fokus pada DWM H/L + EMA 12/26/100 + HTF Candles
4. **D1 position:** Fokus pada EMA 20/50/200 + DWM H/L + Weekly VWAP
5. **Konfirmasi entry:** Harga di atas EMA 200 = bias long, di bawah = bias short
6. **Buy signal terbaik:** EMA short cross above EMA long + harga di atas VWAP + di killzone aktif
7. **Sell signal terbaik:** EMA short cross below EMA long + harga di bawah VWAP

---

*Settings ini berdasarkan research dari multiple sources dan best practices trading community. Selalu backtest terlebih dahulu dan sesuaikan dengan style trading kamu.*
