# 🌦️ Weather Data Automation (India)

This repository automatically fetches **current weather data for major Indian cities** every 3 hours using the [WeatherAPI](https://www.weatherapi.com/) service.
All data is saved into a CSV file for each month and committed back to this repository automatically by **GitHub Actions**.

---

## 🚀 Features

* Fetches **current weather** for a configurable list of cities.
* Runs automatically **every 3 hours** (via GitHub Actions cron schedule).
* Saves data to:

  * `data/weather_india_YYYY_MM.csv` — summarized current conditions.
  * `data/raw/*.json` — optional raw API responses for debugging.
* Auto-commits results to the repository (no manual work needed).
* Simple, lightweight, and free to host on GitHub.

---

## 🧩 Tech Stack

* **Language:** Python 3.11
* **Scheduler:** GitHub Actions
* **API:** [WeatherAPI.com](https://www.weatherapi.com/)
* **Storage:** CSV files inside the repo

---

## 🧠 How It Works

1. The Python script (`weather_fetch.py`) calls WeatherAPI for a list of cities every 3 hours.
2. Weather data (temperature, humidity, condition, etc.) is appended to a monthly CSV.
3. GitHub Actions automatically commits and pushes the updated data back to the repo.

---

## 🛠️ Setup Instructions

### 1️⃣ Get your WeatherAPI key

* Go to [https://www.weatherapi.com/](https://www.weatherapi.com/)
* Create a free account and copy your API key.

### 2️⃣ Add the key as a GitHub Secret

* Go to **Settings → Secrets and variables → Actions → New repository secret**
* Name it:

  ```
  WEATHER_API_KEY
  ```
* Paste your API key as the value.

### 3️⃣ Repository Files

Make sure your repo includes:

```
.
├── weather_fetch.py
├── requirements.txt
└── .github/
    └── workflows/
        └── weather.yml
```

### 4️⃣ Adjust city list (optional)

Edit the `CITIES` list inside `weather_fetch.py` to track any Indian cities you want:

```python
CITIES = ["Chennai", "Mumbai", "Delhi", "Bengaluru", "Kolkata"]
```

---

## ⚙️ GitHub Action Schedule

The script runs automatically every 3 hours (UTC):

```yaml
schedule:
  - cron: "0 */3 * * *"
```

You can also run it manually under the **Actions** tab → “Run workflow”.

---

## 🗂️ Output Example

**CSV file structure:**

| ts_utc               | city    | temp_c | condition_text | humidity | wind_kph | cloud |
| -------------------- | ------- | ------ | -------------- | -------- | -------- | ----- |
| 2025-11-04T06:00:00Z | Chennai | 28.5   | Partly cloudy  | 73       | 11.0     | 40    |
| 2025-11-04T06:00:00Z | Delhi   | 23.2   | Clear          | 55       | 5.4      | 5     |

---

## 🔐 Environment Variables

| Variable          | Description                                                |
| ----------------- | ---------------------------------------------------------- |
| `WEATHER_API_KEY` | API key from [WeatherAPI.com](https://www.weatherapi.com/) |

---

## 🧾 License

This project is open-source and available under the **MIT License**.

---

## 💡 Future Enhancements

* [ ] Add hourly forecast data.
* [ ] Push data to a database (MySQL / PostgreSQL).
* [ ] Create a dashboard (e.g., Streamlit / Power BI) to visualize trends.

---

## 👨‍💻 Author

**Anwar M**
Data Automation Enthusiast • India 🇮🇳
If you like this project, ⭐ it on GitHub!
