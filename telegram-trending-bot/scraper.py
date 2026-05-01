"""Web scraper for hotel & attraction trending data using search engines."""

import asyncio
import logging
import re
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup

import database as db

logger = logging.getLogger(__name__)

CITIES = {
    "surabaya": {
        "display": "Surabaya",
        "traveloka_id": "103570",
        "booking_ss": "Surabaya",
        "agoda_slug": "surabaya-id",
    },
    "sidoarjo": {
        "display": "Sidoarjo",
        "traveloka_id": "103741",
        "booking_ss": "Sidoarjo",
        "agoda_slug": "sidoarjo-id",
    },
    "mojokerto": {
        "display": "Mojokerto",
        "traveloka_id": "103393",
        "booking_ss": "Mojokerto",
        "agoda_slug": "mojokerto-id",
    },
    "pasuruan": {
        "display": "Pasuruan",
        "traveloka_id": "103262",
        "booking_ss": "Pasuruan",
        "agoda_slug": "pasuruan-id",
    },
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
}


def _extract_rating(text: str) -> float | None:
    patterns = [
        r"(\d+[.,]\d+)\s*/\s*10",
        r"rating[:\s]*(\d+[.,]\d+)",
        r"(\d+[.,]\d+)\s*(?:rating|score|stars?)",
        r"scored?\s+(\d+[.,]\d+)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = float(m.group(1).replace(",", "."))
            if 0 < val <= 10:
                return val
    return None


def _extract_price_idr(text: str) -> str | None:
    patterns = [
        r"Rp\.?\s*([\d.,]+)",
        r"IDR\s*([\d.,]+)",
        r"([\d.,]+)\s*(?:per malam|/malam|per night)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return f"Rp {m.group(1)}"
    return None


def _extract_reviews(text: str) -> int:
    patterns = [
        r"(\d[\d.,]*)\s*(?:review|ulasan|penilaian|ratings?)",
        r"(?:review|ulasan|penilaian)\s*[:\s]*(\d[\d.,]*)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            num_str = m.group(1).replace(",", "").replace(".", "")
            try:
                return int(num_str)
            except ValueError:
                pass
    return 0


async def _fetch_page(session: aiohttp.ClientSession, url: str) -> str | None:
    try:
        async with session.get(
            url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=20)
        ) as resp:
            if resp.status == 200:
                return await resp.text()
            logger.warning("HTTP %d for %s", resp.status, url)
    except Exception as e:
        logger.warning("Fetch error for %s: %s", url, e)
    return None


async def _search_ddgs(query: str, max_results: int = 8) -> list[dict]:
    """Search via DuckDuckGo and return results."""
    try:
        from ddgs import DDGS

        results = DDGS().text(query, max_results=max_results)
        return results
    except Exception as e:
        logger.warning("DDGS search error: %s", e)
        return []


async def scrape_hotels_search(city: str) -> int:
    """Scrape hotel data via search engine queries."""
    display = CITIES[city]["display"]
    queries = [
        f"hotel terpopuler {display} rating terbaik 2025 2026 Traveloka",
        f"best hotel {display} Booking.com Agoda review rating",
        f"hotel trending {display} Trip.com promo harga",
        f"rekomendasi hotel {display} terlaris banyak review",
    ]

    found = 0
    for query in queries:
        results = await _search_ddgs(query)
        await asyncio.sleep(1)

        for r in results:
            title = r.get("title", "")
            body = r.get("body", "")
            href = r.get("href", "")
            combined = f"{title} {body}"

            # Determine platform from URL
            platform = "Web"
            if "traveloka.com" in href:
                platform = "Traveloka"
            elif "booking.com" in href:
                platform = "Booking.com"
            elif "agoda.com" in href:
                platform = "Agoda"
            elif "trip.com" in href:
                platform = "Trip.com"
            elif "tiket.com" in href:
                platform = "Tiket.com"
            elif "trivago" in href:
                platform = "Trivago"

            # Try to extract hotel names from the text
            hotel_names = _extract_hotel_names(combined, display)
            rating = _extract_rating(combined)
            price = _extract_price_idr(combined)
            reviews = _extract_reviews(combined)

            for name in hotel_names:
                if len(name) < 5 or len(name) > 80:
                    continue
                db.upsert_hotel(
                    city=city,
                    name=name,
                    stars=_guess_stars(name, rating),
                    rating=rating,
                    reviews=reviews,
                    price=price or "Lihat di platform",
                    platform=platform,
                    highlight=body[:120] if body else "",
                    url=href,
                )
                found += 1

    return found


def _extract_hotel_names(text: str, city_display: str) -> list[str]:
    """Extract hotel names from search result text."""
    names = []

    # Pattern: "Hotel Name" or specific hotel keywords
    patterns = [
        r"((?:Hotel|Resort|Inn|Hostel|Villa|Cottage|Homestay|Penginapan)\s+[A-Z][A-Za-z\s&'-]+)",
        r"([A-Z][A-Za-z\s&'-]*(?:Hotel|Resort|Inn|Suites|Lodge|Palace|Residence))",
        r"((?:JW Marriott|Sheraton|Four Points|Swiss-Bel\w+|Aston|Novotel|Ibis|Mercure|Pullman|Shangri-La|Hyatt|Holiday Inn|Best Western|Fave\w*|OYO|RedDoorz|Grand\s\w+|Royal\s\w+|Platinum)\s*[A-Za-z\s&'-]*)",
    ]

    for pat in patterns:
        matches = re.findall(pat, text)
        for m in matches:
            name = m.strip().rstrip(".")
            # Filter out generic/irrelevant matches
            skip_words = ["Hotel Deals", "Hotel Search", "Hotel Price", "Hotel Booking",
                          "Hotel Indonesia", "Hotel Murah", "Hotel Review", "Hotels in"]
            if any(s.lower() in name.lower() for s in skip_words):
                continue
            if name and len(name) > 4:
                names.append(name)

    return list(set(names))


def _guess_stars(name: str, rating: float | None) -> int:
    luxury = ["marriott", "sheraton", "shangri", "hyatt", "pullman", "majapahit", "regent"]
    mid = ["aston", "novotel", "mercure", "swiss-bel", "four points", "holiday inn", "best western", "platinum"]
    budget = ["oyo", "reddoorz", "fave", "ibis", "pop!", "zen"]

    name_lower = name.lower()
    for kw in luxury:
        if kw in name_lower:
            return 5
    for kw in mid:
        if kw in name_lower:
            return 4
    for kw in budget:
        if kw in name_lower:
            return 2

    if rating and rating >= 9.0:
        return 4
    if rating and rating >= 8.0:
        return 3
    return 3


async def scrape_attractions_search(city: str) -> int:
    """Scrape attraction data via search engine queries."""
    display = CITIES[city]["display"]
    queries = [
        f"wisata populer {display} tiket atraksi terlaris 2025 2026",
        f"tempat wisata {display} Traveloka Klook trending",
        f"things to do {display} Klook Traveloka most booked",
    ]

    found = 0
    for query in queries:
        results = await _search_ddgs(query)
        await asyncio.sleep(1)

        for r in results:
            title = r.get("title", "")
            body = r.get("body", "")
            href = r.get("href", "")
            combined = f"{title} {body}"

            platform = "Web"
            if "traveloka.com" in href:
                platform = "Traveloka"
            elif "klook.com" in href:
                platform = "Klook"
            elif "tiket.com" in href:
                platform = "Tiket.com"
            elif "tripadvisor" in href:
                platform = "TripAdvisor"

            attraction_names = _extract_attraction_names(combined, display)
            price = _extract_price_idr(combined)
            booked = _extract_booked(combined)

            for name in attraction_names:
                if len(name) < 5 or len(name) > 80:
                    continue
                db.upsert_attraction(
                    city=city,
                    name=name,
                    price=price or "Lihat di platform",
                    platform=platform,
                    booked=booked or "Populer",
                    highlight=body[:120] if body else "",
                    url=href,
                )
                found += 1

    return found


def _extract_attraction_names(text: str, city_display: str) -> list[str]:
    names = []
    patterns = [
        r"((?:Taman|Kebun|Museum|Candi|Air Terjun|Gunung|Pantai|Waterpark|Zoo|Safari)\s+[A-Z][A-Za-z\s&'-]+)",
        r"([A-Z][A-Za-z\s&'-]*(?:Park|Waterpark|Adventure|Land|World|Safari|Zoo))",
    ]
    for pat in patterns:
        matches = re.findall(pat, text)
        for m in matches:
            name = m.strip().rstrip(".")
            if name and len(name) > 4:
                names.append(name)
    return list(set(names))


def _extract_booked(text: str) -> str | None:
    m = re.search(r"(\d+[Kk+]*)\s*(?:booked|dipesan|terjual)", text, re.IGNORECASE)
    if m:
        return f"{m.group(1)} booked"
    return None


async def scrape_city(city: str) -> dict:
    """Run all scrapers for a given city."""
    logger.info("Scraping %s ...", city)

    hotel_count = await scrape_hotels_search(city)
    db.log_scrape(city, "hotel", "search", "success" if hotel_count > 0 else "no_data", hotel_count)
    logger.info("  Hotels found: %d", hotel_count)

    await asyncio.sleep(2)

    attraction_count = await scrape_attractions_search(city)
    db.log_scrape(city, "attraction", "search", "success" if attraction_count > 0 else "no_data", attraction_count)
    logger.info("  Attractions found: %d", attraction_count)

    return {"city": city, "hotels": hotel_count, "attractions": attraction_count}


async def scrape_all() -> list[dict]:
    """Scrape all cities sequentially (to avoid rate limits)."""
    db.init_db()
    results = []
    for city in CITIES:
        result = await scrape_city(city)
        results.append(result)
        await asyncio.sleep(3)
    return results


# ── Seed from curated data ─────────────────────────────────────────────


def seed_from_curated() -> None:
    """Load initial curated data from data.py into the database."""
    from data import ATTRACTIONS, HOTELS

    db.init_db()

    for city, hotels in HOTELS.items():
        for h in hotels:
            db.upsert_hotel(
                city=city,
                name=h["name"],
                stars=h["stars"],
                rating=h["rating"],
                reviews=h["reviews"],
                price=h["price"],
                platform=h["platform"],
                highlight=h["highlight"],
                url=h.get("url", ""),
            )

    for city, attractions in ATTRACTIONS.items():
        for a in attractions:
            db.upsert_attraction(
                city=city,
                name=a["name"],
                price=a["price"],
                platform=a["platform"],
                booked=a.get("booked", "Populer"),
                highlight=a["highlight"],
                url=a.get("url", ""),
            )

    logger.info("Seeded curated data into database.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Seeding curated data...")
    seed_from_curated()
    print("Running search scrape...")
    results = asyncio.run(scrape_all())
    for r in results:
        print(f"  {r['city']}: {r['hotels']} hotels, {r['attractions']} attractions")
    print("Done!")
