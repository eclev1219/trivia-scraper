// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: cyan; icon-glyph: cloud-sun-rain;
//
// Free Weather Report Widget for Scriptable
// Temperature • Humidity • Air Quality • Hourly rain/snow
//
// Data: Open-Meteo (https://open-meteo.com) — no API key, free for
// non-commercial use. Attribution: CC BY 4.0.

////////////////////
// CONFIG
////////////////////

const CONFIG = {
  // "F" or "C"
  units: "F",

  // How many forecast hours to show
  hourlyHours: 6,

  // Cache weather responses (minutes)
  cacheMinutes: 20,

  // Widget refresh hint (iOS decides actual refresh timing)
  refreshMinutes: 30,

  // Optional fixed coordinates (skip GPS). Leave null to use Location.
  // Example: { lat: 40.7128, lon: -74.0060, name: "New York" }
  fixedLocation: null,
}

const CACHE_DIR = "weather-widget-cache"

////////////////////
// MAIN
////////////////////

async function main() {
  try {
    const place = await resolvePlace()
    const weather = await loadWeather(place)
    const widget = buildWidget(weather, place)
    present(widget)
  } catch (err) {
    console.error(err)
    present(errorWidget("Weather unavailable", String(err)))
  }
}

function present(widget) {
  // Always register the widget so the Home Screen can refresh it.
  // presentMedium() is only a preview when you tap Run inside Scriptable.
  Script.setWidget(widget)
  if (!config.runsInWidget) {
    widget.presentMedium()
  }
  Script.complete()
}

////////////////////
// LOCATION
////////////////////

async function resolvePlace() {
  if (CONFIG.fixedLocation) {
    return {
      lat: CONFIG.fixedLocation.lat,
      lon: CONFIG.fixedLocation.lon,
      name: CONFIG.fixedLocation.name || "Saved location",
    }
  }

  Location.setAccuracyToKilometer()
  const loc = await Location.current()
  const lat = loc.latitude
  const lon = loc.longitude

  const cacheKey = `place_${lat.toFixed(2)}_${lon.toFixed(2)}`
  const cached = readCache(cacheKey, 24 * 60)
  if (cached) return cached

  let name = "Nearby"
  try {
    const geos = await Location.reverseGeocode(lat, lon)
    const g = geos && geos[0]
    if (g) {
      const city = g.locality || g.subLocality || g.name || ""
      const region = g.administrativeArea || ""
      name = city && region ? `${city}, ${region}` : city || region || name
    }
  } catch (_) {}

  const place = { lat, lon, name }
  writeCache(cacheKey, place)
  return place
}

////////////////////
// WEATHER FETCH (Open-Meteo)
////////////////////

async function loadWeather(place) {
  const cacheKey = `wx_${place.lat.toFixed(2)}_${place.lon.toFixed(2)}_${CONFIG.units}`
  const cached = readCache(cacheKey, CONFIG.cacheMinutes)
  if (cached) return cached

  const metric = CONFIG.units === "C"
  const tempUnit = metric ? "celsius" : "fahrenheit"
  const precipUnit = metric ? "mm" : "inch"

  const forecastUrl =
    `https://api.open-meteo.com/v1/forecast` +
    `?latitude=${place.lat}&longitude=${place.lon}` +
    `&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,is_day,rain,snowfall` +
    `&hourly=temperature_2m,precipitation_probability,precipitation,rain,snowfall,weather_code` +
    `&temperature_unit=${tempUnit}` +
    `&precipitation_unit=${precipUnit}` +
    `&timezone=auto` +
    `&forecast_hours=${Math.max(CONFIG.hourlyHours, 12)}`

  const aqUrl =
    `https://air-quality-api.open-meteo.com/v1/air-quality` +
    `?latitude=${place.lat}&longitude=${place.lon}` +
    `&current=us_aqi,pm2_5,european_aqi` +
    `&timezone=auto`

  const [forecast, aq] = await Promise.all([getJSON(forecastUrl), getJSONSafe(aqUrl)])
  if (!forecast?.current) throw new Error("No forecast data returned")

  const cur = forecast.current
  const hourly = forecast.hourly || {}
  const times = hourly.time || []

  // Start at the current hour index
  let startIdx = 0
  const now = Date.now()
  for (let i = 0; i < times.length; i++) {
    if (new Date(times[i]).getTime() >= now - 30 * 60 * 1000) {
      startIdx = i
      break
    }
  }

  const hours = []
  for (let i = startIdx; i < times.length && hours.length < CONFIG.hourlyHours; i++) {
    const rain = hourly.rain?.[i] ?? 0
    const snow = hourly.snowfall?.[i] ?? 0
    const precip = hourly.precipitation?.[i] ?? 0
    const prob = hourly.precipitation_probability?.[i] ?? 0
    hours.push({
      time: times[i],
      temp: hourly.temperature_2m?.[i],
      precipProb: prob,
      rain,
      snow,
      precip,
      weatherCode: hourly.weather_code?.[i],
    })
  }

  const aqi = aq?.current?.us_aqi
  const weather = {
    fetchedAt: new Date().toISOString(),
    weatherText: wmoText(cur.weather_code),
    weatherCode: cur.weather_code,
    isDayTime: cur.is_day === 1,
    temperature: cur.temperature_2m,
    realFeel: cur.apparent_temperature,
    humidity: cur.relative_humidity_2m,
    unit: metric ? "C" : "F",
    precipUnit: metric ? "mm" : "in",
    airQuality:
      aqi == null
        ? null
        : {
            index: Math.round(aqi),
            category: usAqiCategory(aqi),
            color: usAqiColor(aqi),
            pm25: aq.current.pm2_5,
          },
    hours,
  }

  writeCache(cacheKey, weather)
  return weather
}

////////////////////
// WMO + AQI HELPERS
////////////////////

function wmoText(code) {
  const map = {
    0: "Clear",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Icy fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    56: "Freezing drizzle",
    57: "Freezing drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Freezing rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Rain showers",
    81: "Rain showers",
    82: "Heavy showers",
    85: "Snow showers",
    86: "Snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm",
    99: "Thunderstorm",
  }
  return map[code] || "Weather"
}

function usAqiCategory(aqi) {
  if (aqi <= 50) return "Good"
  if (aqi <= 100) return "Moderate"
  if (aqi <= 150) return "Unhealthy (Sensitive)"
  if (aqi <= 200) return "Unhealthy"
  if (aqi <= 300) return "Very Unhealthy"
  return "Hazardous"
}

function usAqiColor(aqi) {
  if (aqi <= 50) return "#00E400"
  if (aqi <= 100) return "#FFFF00"
  if (aqi <= 150) return "#FF7E00"
  if (aqi <= 200) return "#FF0000"
  if (aqi <= 300) return "#8F3F97"
  return "#7E0023"
}

////////////////////
// WIDGET UI
////////////////////

function buildWidget(weather, place) {
  const w = new ListWidget()
  w.setPadding(14, 16, 14, 16)
  const bg = new LinearGradient()
  bg.locations = [0, 1]
  if (weather.isDayTime) {
    bg.colors = [new Color("#1B4F72"), new Color("#2E86C1")]
  } else {
    bg.colors = [new Color("#0B1C2C"), new Color("#1A3348")]
  }
  w.backgroundGradient = bg
  w.refreshAfterDate = new Date(Date.now() + CONFIG.refreshMinutes * 60 * 1000)

  const header = w.addStack()
  header.layoutHorizontally()
  header.centerAlignContent()

  const title = header.addText(place.name)
  title.font = Font.semiboldSystemFont(13)
  title.textColor = Color.white()
  title.lineLimit = 1

  header.addSpacer()

  const cond = header.addText(weather.weatherText)
  cond.font = Font.systemFont(12)
  cond.textColor = new Color("#FFFFFF", 0.85)
  cond.lineLimit = 1

  w.addSpacer(8)

  const row = w.addStack()
  row.layoutHorizontally()
  row.bottomAlignContent()

  const tempStack = row.addStack()
  tempStack.layoutVertically()
  const temp = tempStack.addText(`${Math.round(weather.temperature)}°${weather.unit}`)
  temp.font = Font.boldSystemFont(42)
  temp.textColor = Color.white()

  if (weather.realFeel != null) {
    const rf = tempStack.addText(`Feels ${Math.round(weather.realFeel)}°`)
    rf.font = Font.systemFont(11)
    rf.textColor = new Color("#FFFFFF", 0.75)
  }

  row.addSpacer()

  const metrics = row.addStack()
  metrics.layoutVertically()
  metrics.spacing = 3

  addMetric(metrics, "Humidity", weather.humidity != null ? `${weather.humidity}%` : "—")
  if (weather.airQuality) {
    addMetric(
      metrics,
      "AQI",
      `${weather.airQuality.index} ${weather.airQuality.category}`,
      weather.airQuality.color
    )
  } else {
    addMetric(metrics, "AQI", "Unavailable")
  }

  w.addSpacer(10)

  const label = w.addText("Hourly rain / snow")
  label.font = Font.semiboldSystemFont(11)
  label.textColor = new Color("#FFFFFF", 0.8)

  w.addSpacer(4)

  const hours = w.addStack()
  hours.layoutHorizontally()
  hours.spacing = 6

  for (const h of weather.hours) {
    const col = hours.addStack()
    col.layoutVertically()
    col.centerAlignContent()
    col.size = new Size(42, 0)

    const t = col.addText(formatHour(h.time))
    t.font = Font.systemFont(10)
    t.textColor = new Color("#FFFFFF", 0.8)
    t.centerAlignText()

    col.addSpacer(2)

    const kind = precipKind(h)
    try {
      const sym = SFSymbol.named(kind.symbol)
      sym.applyFont(Font.systemFont(12))
      const img = col.addImage(sym.image)
      img.imageSize = new Size(14, 14)
      img.tintColor = Color.white()
      img.centerAlignImage()
    } catch (_) {
      const icon = col.addText(kind.fallback)
      icon.font = Font.systemFont(11)
      icon.textColor = Color.white()
      icon.centerAlignText()
    }

    const pct = col.addText(`${Math.round(kind.prob)}%`)
    pct.font = Font.boldSystemFont(11)
    pct.textColor = Color.white()
    pct.centerAlignText()

    if (h.temp != null) {
      const ht = col.addText(`${Math.round(h.temp)}°`)
      ht.font = Font.systemFont(10)
      ht.textColor = new Color("#FFFFFF", 0.7)
      ht.centerAlignText()
    }
  }

  w.addSpacer(6)
  const foot = w.addText(cacheFooter(weather.fetchedAt))
  foot.font = Font.systemFont(9)
  foot.textColor = new Color("#FFFFFF", 0.45)

  return w
}

function addMetric(parent, label, value, accentHex) {
  const s = parent.addStack()
  s.layoutHorizontally()
  const l = s.addText(`${label}  `)
  l.font = Font.systemFont(11)
  l.textColor = new Color("#FFFFFF", 0.7)
  const v = s.addText(value)
  v.font = Font.semiboldSystemFont(12)
  v.textColor = accentHex ? new Color(accentHex) : Color.white()
  v.lineLimit = 1
}

function precipKind(h) {
  const snow = h.snow || 0
  const rain = h.rain || 0
  const prob = h.precipProb || 0
  if (snow > rain && snow > 0) {
    return { symbol: "snowflake", fallback: "S", prob }
  }
  // WMO snow-ish codes
  const code = h.weatherCode
  if (code === 71 || code === 73 || code === 75 || code === 77 || code === 85 || code === 86) {
    return { symbol: "snowflake", fallback: "S", prob }
  }
  if (code === 66 || code === 67 || code === 56 || code === 57) {
    return { symbol: "cloud.sleet", fallback: "M", prob }
  }
  return { symbol: "cloud.rain", fallback: "R", prob }
}

function formatHour(iso) {
  const d = new Date(iso)
  let h = d.getHours()
  const ampm = h >= 12 ? "p" : "a"
  h = h % 12
  if (h === 0) h = 12
  return `${h}${ampm}`
}

function cacheFooter(iso) {
  const d = new Date(iso)
  const t = d.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })
  return `Open-Meteo · updated ${t}`
}

function errorWidget(title, detail) {
  const w = new ListWidget()
  w.setPadding(14, 16, 14, 16)
  w.backgroundColor = new Color("#1B2631")
  const t = w.addText(title)
  t.font = Font.boldSystemFont(14)
  t.textColor = Color.white()
  w.addSpacer(6)
  const d = w.addText(detail)
  d.font = Font.systemFont(11)
  d.textColor = new Color("#FFFFFF", 0.75)
  d.minimumScaleFactor = 0.7
  return w
}

////////////////////
// HTTP / CACHE
////////////////////

async function getJSON(url) {
  const req = new Request(url)
  req.timeoutInterval = 20
  req.headers = { Accept: "application/json" }
  try {
    return await req.loadJSON()
  } catch (e) {
    let raw = ""
    try {
      raw = await new Request(url).loadString()
    } catch (_) {}
    throw new Error(
      `API error: ${String(e).slice(0, 120)}` + (raw ? ` | ${String(raw).slice(0, 160)}` : "")
    )
  }
}

async function getJSONSafe(url) {
  try {
    return await getJSON(url)
  } catch (_) {
    return null
  }
}

function cachePath(name) {
  const fm = FileManager.local()
  const dir = fm.joinPath(fm.documentsDirectory(), CACHE_DIR)
  if (!fm.fileExists(dir)) fm.createDirectory(dir)
  return fm.joinPath(dir, `${name}.json`)
}

function readCache(name, maxAgeMinutes) {
  const fm = FileManager.local()
  const path = cachePath(name)
  if (!fm.fileExists(path)) return null
  try {
    const ageMin = (Date.now() - fm.modificationDate(path).getTime()) / 60000
    if (ageMin > maxAgeMinutes) return null
    return JSON.parse(fm.readString(path))
  } catch (_) {
    return null
  }
}

function writeCache(name, value) {
  const fm = FileManager.local()
  const path = cachePath(name)
  fm.writeString(path, JSON.stringify(value))
}

await main()
