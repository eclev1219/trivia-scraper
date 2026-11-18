# AccuWeather Scriptable Widget

Scriptable home-screen widget that shows **temperature**, **humidity**, **air quality**, and an **hourly rain/snow** strip using AccuWeather data.

## Important limitation

**Scriptable cannot pull data from the AccuWeather iOS app.** Apps are sandboxed on iOS. This widget uses AccuWeather’s **developer API** (`dataservice.accuweather.com`) instead.

| Data | Source |
| --- | --- |
| Temperature, humidity, conditions | AccuWeather Current Conditions (`details=true`) |
| Hourly rain / snow probabilities | AccuWeather 12-hour Hourly Forecast (`details=true`) |
| Air quality | AccuWeather AQ is **Enterprise-only**. The script tries it, then falls back to free [Open-Meteo](https://open-meteo.com/) US AQI unless you disable that. |

## Setup

1. Create an API key at [developer.accuweather.com](https://developer.accuweather.com/).
2. In the **Scriptable** app on iPhone, create a new script and paste `AccuWeatherWidget.js`.
3. Store your key in Keychain (recommended):

```javascript
Keychain.set("accuweather_api_key", "YOUR_KEY_HERE")
```

   Or set `CONFIG.apiKeyFallback` near the top of the script.

4. Allow **Location** when Scriptable asks (used to resolve an AccuWeather location key).
5. Add a Scriptable widget to the Home Screen → choose this script → Medium size works best.

## Config knobs

Edit the `CONFIG` object at the top of the script:

| Option | Purpose |
| --- | --- |
| `units` | `"F"` or `"C"` |
| `locationKey` | Optional AccuWeather location key (skips geoposition lookup and saves API calls) |
| `hourlyHours` | How many hours to show (1–12) |
| `cacheMinutes` | Local cache TTL to stay under AccuWeather rate limits |
| `useOpenMeteoAirQualityFallback` | `false` to hide AQI unless AccuWeather Enterprise AQ works |

## API call budget

Each fresh (uncached) refresh typically uses:

1. Geoposition → location key *(skipped if `locationKey` is set; also cached ~24h)*
2. Current conditions
3. 12-hour hourly forecast
4. Optional AccuWeather AQ attempt *(often fails on Free/Starter)*

Keep `cacheMinutes` at 15–30 so a Free/Starter key lasts. AccuWeather’s Free Core Weather trial is limited; Starter includes Current Conditions + 12-hour forecasts.

## Find a location key manually

City search example (browser or Scriptable):

```
https://dataservice.accuweather.com/locations/v1/cities/search?apikey=YOUR_KEY&q=Boston
```

Copy the `"Key"` field into `CONFIG.locationKey`.

## Troubleshooting

- **"Add AccuWeather API key"** — Keychain / `apiKeyFallback` not set.
- **Unauthorized / 401 / 403** — Bad key, or endpoint not on your plan (especially Air Quality).
- **Quota exceeded** — Raise `cacheMinutes`, set a fixed `locationKey`, or reduce how often the widget refreshes.
- **AQI Unavailable** — Expected on Free/Starter without the Open-Meteo fallback.
