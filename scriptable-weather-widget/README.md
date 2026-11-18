# Free Weather Scriptable Widget

Scriptable home-screen widget with **temperature**, **humidity**, **US AQI**, and an **hourly rain/snow** strip.

## Data source

Uses **[Open-Meteo](https://open-meteo.com)** — free, no API key, no sign-up.

| Data | Endpoint |
| --- | --- |
| Temp, humidity, conditions, hourly precip | `api.open-meteo.com/v1/forecast` |
| Air quality (US AQI) | `air-quality-api.open-meteo.com/v1/air-quality` |
| Place name | iOS `Location.reverseGeocode` |

Open-Meteo blends national models (NOAA GFS/HRRR, ECMWF, and others). Free for non-commercial use (CC BY 4.0 attribution). Commercial products need their paid plan.

## Setup

1. In **Scriptable**, create a new script and paste `WeatherWidget.js`.
2. Allow **Location** when prompted.
3. Run the script once to preview, then add a Scriptable widget to the Home Screen (Medium size works best).

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

- **Weather unavailable / network error** — Check cellular/Wi‑Fi; Open-Meteo needs internet.
- **Wrong city name** — Set `CONFIG.fixedLocation` or wait for a fresh reverse-geocode cache.
- **AQI Unavailable** — Rare AQ endpoint hiccup; weather still shows; retry later.
