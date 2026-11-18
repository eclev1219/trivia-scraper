# Free Weather Scriptable Widget

Scriptable home-screen widget with **temperature**, **humidity**, **US AQI**, and an **hourly rain/snow** strip.

## Look & feel

The widget restyles itself from the current conditions and the next few hours:

- Clear blue sky → bright sky gradient + sun
- Rain now / rain likely soon → slate rain tones + rain icon (“Rain on the way” when still clear)
- Snow, fog, overcast, thunder, night → matching atmospheres

## Data source

Uses **[Open-Meteo](https://open-meteo.com)** — free, no API key, no sign-up.

| Data | Endpoint |
| --- | --- |
| Temp, humidity, conditions, hourly precip | `api.open-meteo.com/v1/forecast` |
| Air quality (US AQI) | `air-quality-api.open-meteo.com/v1/air-quality` |
| Place name | iOS `Location.reverseGeocode` |

Open-Meteo blends national models (NOAA GFS/HRRR, ECMWF, and others). Free for non-commercial use (CC BY 4.0 attribution). Commercial products need their paid plan.

## Setup (do not use Safari “Add to Home Screen”)

This is a **Scriptable** widget, not a website. Safari → Share → Add to Home Screen will fail (often with a `data:` / restricted-port error). Use the steps below instead.

### 1. Install Scriptable
Get [Scriptable](https://apps.apple.com/app/scriptable/id1405459188) from the App Store if you don’t have it.

### 2. Create the script
1. Open **Scriptable** → tap **+**
2. Delete any placeholder code
3. Paste the full contents of `WeatherWidget.js`
4. Tap the script name at the top and rename it (e.g. `Weather`)
5. Tap **Done**, then run it once (play button) and allow **Location**

### 3. Add the Home Screen widget
1. Long-press an empty spot on the Home Screen → **Edit Home Screen** → **+** (top left)
2. Search for **Scriptable** and add a **Medium** widget
3. **Assign the script** (this is the step that replaces the gear message):
   - Long-press the Scriptable widget on the Home Screen
   - Tap **Edit Widget**
   - Tap **Script** → choose your `Weather` script
   - Leave **Parameter** blank
   - (Optional) set **When Interacting** to “Run Script” or “Open App”
4. Tap outside the popup to dismiss, then tap **Done**

Running the script with the play button inside Scriptable only shows a preview in the app. It does **not** configure the Home Screen widget.

No API key step.

## Config

Edit `CONFIG` at the top of the script:

| Option | Purpose |
| --- | --- |
| `units` | `"F"` or `"C"` |
| `hourlyHours` | Hours shown in the precip strip (default 6) |
| `cacheMinutes` | Local cache TTL (default 20) |
| `fixedLocation` | Optional `{ lat, lon, name }` to skip GPS |

## Troubleshooting

- **Widget shows a gear: “Configure widget…”** — The Home Screen widget has no script yet. Long-press it → **Edit Widget** → **Script** → pick `Weather`. Do not only run the script inside the Scriptable app.
- **Tapping the widget opens Scriptable instead of editing** — That’s normal until it’s configured. Use long-press → **Edit Widget**, not a normal tap.
- **Script missing from the Script picker** — Open Scriptable, open the script, make sure it has a name and you tapped **Done** to save.
- **Weather unavailable / network error** — Check cellular/Wi‑Fi; Open-Meteo needs internet.
- **Wrong city name** — Set `CONFIG.fixedLocation` or wait for a fresh reverse-geocode cache.
- **AQI Unavailable** — Rare AQ endpoint hiccup; weather still shows; retry later.
