# weather_fetch.py
import os
import csv
import time
import json
from pathlib import Path
from datetime import datetime, timezone
import requests

# ======= CONFIG =======
# Add/remove citiesgit
CITIES = [
    "Chennai", "Mumbai", "Delhi", "Bengaluru",
    "Kolkata", "Hyderabad", "Pune", "Ahmedabad"
]

# Choose endpoint: "current" for now conditions,
# or "forecast" to also capture hourly (next 24–72h depending on your plan).
USE_FORECAST = False   # set True if you want forecast hourly too
FORECAST_DAYS = 1      # WeatherAPI supports up to 10 depending on plan

BASE_URL = "http://api.weatherapi.com/v1"
DATA_DIR = Path("data")  # where CSV/JSON will be stored
RAW_JSON_DIR = DATA_DIR / "raw"  # optional raw dumps for debugging
TIMEOUT = 20  # seconds for HTTP calls
# ======================

API_KEY = os.getenv("WEATHER_API_KEY")
if not API_KEY:
    raise SystemExit("Missing WEATHER_API_KEY env var. Set it as a GitHub Secret.")

DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_JSON_DIR.mkdir(parents=True, exist_ok=True)

def monthly_csv_path() -> Path:
    """Create one CSV per month to keep files tidy."""
    now = datetime.now(timezone.utc)
    return DATA_DIR / f"weather_india_{now:%Y_%m}.csv"

CSV_HEADERS = [
    "ts_utc", "city", "lat", "lon",
    "temp_c", "feelslike_c", "condition_text",
    "humidity", "wind_kph", "wind_dir",
    "pressure_mb", "precip_mm", "cloud", "uv",
    "is_day"
]

def write_csv_row(row: dict):
    csv_path = monthly_csv_path()
    file_exists = csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def dump_raw_json(city: str, payload: dict):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = RAW_JSON_DIR / f"{city.replace(' ', '_').lower()}_{ts}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

def fetch_current(city: str) -> dict:
    url = f"{BASE_URL}/current.json"
    params = {"key": API_KEY, "q": city, "aqi": "no"}
    r = requests.get(url, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def fetch_forecast(city: str, days: int = 1) -> dict:
    url = f"{BASE_URL}/forecast.json"
    params = {"key": API_KEY, "q": city, "days": days, "aqi": "no", "alerts": "no"}
    r = requests.get(url, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def row_from_current(city: str, data: dict) -> dict:
    loc = data.get("location", {})
    cur = data.get("current", {})
    cond = (cur.get("condition") or {})
    # WeatherAPI returns localtime; we use our own UTC timestamp for consistency
    ts_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "ts_utc": ts_utc,
        "city": city,
        "lat": loc.get("lat"),
        "lon": loc.get("lon"),
        "temp_c": cur.get("temp_c"),
        "feelslike_c": cur.get("feelslike_c"),
        "condition_text": cond.get("text"),
        "humidity": cur.get("humidity"),
        "wind_kph": cur.get("wind_kph"),
        "wind_dir": cur.get("wind_dir"),
        "pressure_mb": cur.get("pressure_mb"),
        "precip_mm": cur.get("precip_mm"),
        "cloud": cur.get("cloud"),
        "uv": cur.get("uv"),
        "is_day": cur.get("is_day"),
    }

def main():
    failures = []
    for city in CITIES:
        try:
            if USE_FORECAST:
                data = fetch_forecast(city, days=FORECAST_DAYS)
            else:
                data = fetch_current(city)

            # optional: keep a raw snapshot for audits/debugging
            dump_raw_json(city, data)

            if USE_FORECAST:
                # Save *current* portion even if using forecast endpoint
                if "current" in data:
                    write_csv_row(row_from_current(city, data))
                # If you want hourly forecast rows, uncomment below:
                # for day in data.get("forecast", {}).get("forecastday", []):
                #     for hour in day.get("hour", []):
                #         # Map hour data to your schema or a second CSV
                #         pass
            else:
                write_csv_row(row_from_current(city, data))

            # Be polite to the API if you have many cities
            time.sleep(0.2)

        except Exception as e:
            failures.append((city, str(e)))

    if failures:
        # Make it visible in Action logs
        print("Some cities failed:", failures)

if __name__ == "__main__":
    main()
