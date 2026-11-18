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
// CONDITION THEMES
////////////////////

function upcomingPrecip(weather) {
  const hours = weather.hours || []
  let maxRainProb = 0
  let maxSnowProb = 0
  let wetHour = null
  for (const h of hours) {
    const snowy =
      (h.snow || 0) > (h.rain || 0) ||
      [71, 73, 75, 77, 85, 86].includes(h.weatherCode)
    const prob = h.precipProb || 0
    if (snowy) maxSnowProb = Math.max(maxSnowProb, prob)
    else maxRainProb = Math.max(maxRainProb, prob)
    if (prob >= 40 && !wetHour) wetHour = h
  }
  return { maxRainProb, maxSnowProb, wetHour }
}

function moodFromWeather(weather) {
  const code = weather.weatherCode
  const day = weather.isDayTime
  const upcoming = upcomingPrecip(weather)

  // Current precipitation / storm codes win first
  if ([95, 96, 99].includes(code)) return "thunder"
  if ([71, 73, 75, 77, 85, 86].includes(code)) return day ? "snow" : "snowNight"
  if ([65, 82].includes(code)) return "heavyRain"
  if ([51, 53, 55, 56, 57, 61, 63, 66, 67, 80, 81].includes(code)) {
    return day ? "rain" : "rainNight"
  }
  if ([45, 48].includes(code)) return "fog"
  if (code === 3) return day ? "overcast" : "overcastNight"
  if (code === 2) return day ? "partlyCloudy" : "partlyCloudyNight"

  // Clear / mainly clear — still shift if rain/snow is projected soon
  if (upcoming.maxSnowProb >= 45) return day ? "snowSoon" : "snowNight"
  if (upcoming.maxRainProb >= 45) return day ? "rainSoon" : "rainNight"

  if (code === 1) return day ? "mostlyClear" : "clearNight"
  return day ? "clear" : "clearNight"
}

function themeForMood(mood) {
  // Soft sky atmospheres — light themes use dark ink for readability
  const themes = {
    clear: {
      colors: ["#3BA4E6", "#7EC8F0", "#B8DFF5"],
      locations: [0, 0.55, 1],
      text: "#0B2A44",
      muted: "#1A4A6E",
      soft: "#2C6288",
      accent: "#F5C542",
      icon: "sun.max.fill",
      precipAccent: "#1B6CA8",
      hint: null,
    },
    mostlyClear: {
      colors: ["#4FA8DE", "#8FCBEA", "#D2EAF7"],
      locations: [0, 0.55, 1],
      text: "#0F2F4A",
      muted: "#255879",
      soft: "#3A6F90",
      accent: "#E8B84A",
      icon: "sun.max.fill",
      precipAccent: "#1B6CA8",
      hint: null,
    },
    clearNight: {
      colors: ["#071325", "#13233D", "#1E3352"],
      locations: [0, 0.5, 1],
      text: "#F2F6FA",
      muted: "#C5D2E0",
      soft: "#9AAEBF",
      accent: "#E6D5A4",
      icon: "moon.stars.fill",
      precipAccent: "#7EB6D9",
      hint: null,
    },
    partlyCloudy: {
      colors: ["#5E90B8", "#8FB0C8", "#C5D8E6"],
      locations: [0, 0.5, 1],
      text: "#14324A",
      muted: "#2E5570",
      soft: "#4A718A",
      accent: "#D4A84B",
      icon: "cloud.sun.fill",
      precipAccent: "#2A6F9A",
      hint: null,
    },
    partlyCloudyNight: {
      colors: ["#121C2C", "#24364A", "#3A5166"],
      locations: [0, 0.5, 1],
      text: "#F0F4F8",
      muted: "#C2CEDA",
      soft: "#97A8B8",
      accent: "#C9B896",
      icon: "cloud.moon.fill",
      precipAccent: "#7EB6D9",
      hint: null,
    },
    overcast: {
      colors: ["#6D7C89", "#8A98A4", "#AEB8C0"],
      locations: [0, 0.5, 1],
      text: "#1A242C",
      muted: "#33414C",
      soft: "#4C5C68",
      accent: "#5F7D95",
      icon: "cloud.fill",
      precipAccent: "#3D5F78",
      hint: null,
    },
    overcastNight: {
      colors: ["#1A222A", "#2B3640", "#3E4B56"],
      locations: [0, 0.5, 1],
      text: "#EEF2F5",
      muted: "#C0CAD2",
      soft: "#96A3AD",
      accent: "#8FA4B5",
      icon: "cloud.fill",
      precipAccent: "#7EB6D9",
      hint: null,
    },
    fog: {
      colors: ["#9AA4AB", "#B7BFC4", "#D5DBDF"],
      locations: [0, 0.5, 1],
      text: "#243037",
      muted: "#3E4C54",
      soft: "#5A6A73",
      accent: "#6C7F8A",
      icon: "cloud.fog.fill",
      precipAccent: "#4A6573",
      hint: null,
    },
    rainSoon: {
      colors: ["#4A6F8C", "#6F90A8", "#A7BFC9"],
      locations: [0, 0.45, 1],
      text: "#122636",
      muted: "#2A4A5E",
      soft: "#456678",
      accent: "#3E7EA6",
      icon: "cloud.sun.rain.fill",
      precipAccent: "#1F5F86",
      hint: "Rain on the way",
    },
    rain: {
      colors: ["#3A5266", "#5A7388", "#7F96A6"],
      locations: [0, 0.5, 1],
      text: "#F3F7FA",
      muted: "#D0DCE5",
      soft: "#A9BBC8",
      accent: "#8EC5E8",
      icon: "cloud.rain.fill",
      precipAccent: "#B8E0F7",
      hint: null,
    },
    rainNight: {
      colors: ["#141C26", "#243140", "#35485A"],
      locations: [0, 0.5, 1],
      text: "#F0F5F9",
      muted: "#C5D3DF",
      soft: "#95A9BA",
      accent: "#7EB8DC",
      icon: "cloud.moon.rain.fill",
      precipAccent: "#9FD0F0",
      hint: null,
    },
    heavyRain: {
      colors: ["#1B2733", "#2E4050", "#455A6B"],
      locations: [0, 0.5, 1],
      text: "#F4F8FB",
      muted: "#D2DEE8",
      soft: "#A7B8C6",
      accent: "#8FCAF0",
      icon: "cloud.heavyrain.fill",
      precipAccent: "#B6E2FF",
      hint: null,
    },
    thunder: {
      colors: ["#171A22", "#2A3140", "#3F4858"],
      locations: [0, 0.5, 1],
      text: "#F5F6F8",
      muted: "#D2D6DE",
      soft: "#A7AEBA",
      accent: "#F0D56A",
      icon: "cloud.bolt.rain.fill",
      precipAccent: "#F0D56A",
      hint: null,
    },
    snow: {
      colors: ["#A9C0D4", "#C9D8E6", "#E8EEF4"],
      locations: [0, 0.5, 1],
      text: "#1A2C3C",
      muted: "#355066",
      soft: "#567188",
      accent: "#5B8FB5",
      icon: "cloud.snow.fill",
      precipAccent: "#3F6F94",
      hint: null,
    },
    snowSoon: {
      colors: ["#8FA9BE", "#B5C7D6", "#DCE5EC"],
      locations: [0, 0.5, 1],
      text: "#1A2C3C",
      muted: "#355066",
      soft: "#567188",
      accent: "#5B8FB5",
      icon: "cloud.snow.fill",
      precipAccent: "#3F6F94",
      hint: "Snow on the way",
    },
    snowNight: {
      colors: ["#1A2430", "#2C3B4A", "#445868"],
      locations: [0, 0.5, 1],
      text: "#F2F6FA",
      muted: "#C7D4E0",
      soft: "#9AADC0",
      accent: "#B7D4EA",
      icon: "cloud.snow.fill",
      precipAccent: "#D3E8F6",
      hint: null,
    },
  }

  return themes[mood] || themes.clear
}

////////////////////
// WIDGET UI
////////////////////

function buildWidget(weather, place) {
  const mood = moodFromWeather(weather)
  const theme = themeForMood(mood)
  const upcoming = upcomingPrecip(weather)

  const w = new ListWidget()
  w.setPadding(10, 12, 10, 12)

  const bg = new LinearGradient()
  bg.locations = theme.locations
  bg.colors = theme.colors.map((hex) => new Color(hex))
  w.backgroundGradient = bg
  w.refreshAfterDate = new Date(Date.now() + CONFIG.refreshMinutes * 60 * 1000)

  const primary = new Color(theme.text)
  const muted = new Color(theme.muted)
  const soft = new Color(theme.soft)
  const accent = new Color(theme.accent)

  // Header: place + condition
  const header = w.addStack()
  header.layoutHorizontally()
  header.centerAlignContent()

  const title = header.addText(place.name)
  title.font = Font.semiboldSystemFont(12)
  title.textColor = primary
  title.lineLimit = 1
  title.minimumScaleFactor = 0.8

  header.addSpacer()

  const status = theme.hint || weather.weatherText
  const cond = header.addText(status)
  cond.font = Font.semiboldSystemFont(11)
  cond.textColor = muted
  cond.lineLimit = 1
  cond.minimumScaleFactor = 0.8

  w.addSpacer(4)

  // Hero row: icon + temp | metrics
  const row = w.addStack()
  row.layoutHorizontally()
  row.centerAlignContent()

  const left = row.addStack()
  left.layoutHorizontally()
  left.centerAlignContent()
  left.spacing = 8

  addSymbol(left, theme.icon, accent, 28)

  const tempStack = left.addStack()
  tempStack.layoutVertically()
  tempStack.spacing = 0

  const temp = tempStack.addText(`${Math.round(weather.temperature)}°${weather.unit}`)
  temp.font = Font.boldSystemFont(34)
  temp.textColor = primary
  temp.lineLimit = 1

  const feelBits = []
  if (weather.realFeel != null) feelBits.push(`Feels ${Math.round(weather.realFeel)}°`)
  if (theme.hint && weather.weatherText) feelBits.push(weather.weatherText)
  if (feelBits.length) {
    const rf = tempStack.addText(feelBits.join(" · "))
    rf.font = Font.systemFont(10)
    rf.textColor = soft
    rf.lineLimit = 1
    rf.minimumScaleFactor = 0.75
  }

  row.addSpacer()

  const metrics = row.addStack()
  metrics.layoutVertically()
  metrics.spacing = 2
  metrics.centerAlignContent()

  addMetric(metrics, "Humidity", weather.humidity != null ? `${weather.humidity}%` : "—", muted, primary)
  if (weather.airQuality) {
    const aqCat = shortAqiCategory(weather.airQuality.category)
    addMetric(
      metrics,
      "AQI",
      `${weather.airQuality.index} ${aqCat}`,
      muted,
      aqiTextColor(weather.airQuality.index, theme)
    )
  } else {
    addMetric(metrics, "AQI", "—", muted, primary)
  }

  w.addSpacer(6)

  const hourlyTitle =
    upcoming.maxSnowProb >= upcoming.maxRainProb && upcoming.maxSnowProb > 0
      ? "Hourly snow chance"
      : upcoming.maxRainProb >= 30 || ["rain", "rainNight", "rainSoon", "heavyRain", "thunder"].includes(mood)
        ? "Hourly rain chance"
        : "Next hours"

  const label = w.addText(hourlyTitle)
  label.font = Font.semiboldSystemFont(10)
  label.textColor = muted
  label.lineLimit = 1

  w.addSpacer(2)

  const hours = w.addStack()
  hours.layoutHorizontally()
  hours.spacing = 4

  for (const h of weather.hours) {
    const col = hours.addStack()
    col.layoutVertically()
    col.centerAlignContent()
    col.spacing = 1
    col.size = new Size(40, 0)

    const t = col.addText(formatHour(h.time))
    t.font = Font.systemFont(9)
    t.textColor = soft
    t.centerAlignText()
    t.lineLimit = 1

    const kind = precipKind(h)
    addSymbol(col, kind.symbol, kind.prob >= 40 ? new Color(theme.precipAccent) : soft, 12)

    const wet = kind.prob >= 40
    const pct = col.addText(`${Math.round(kind.prob)}%`)
    pct.font = Font.boldSystemFont(10)
    pct.textColor = wet ? new Color(theme.precipAccent) : primary
    pct.centerAlignText()
    pct.lineLimit = 1

    if (h.temp != null) {
      const ht = col.addText(`${Math.round(h.temp)}°`)
      ht.font = Font.systemFont(9)
      ht.textColor = soft
      ht.centerAlignText()
      ht.lineLimit = 1
    }
  }

  return w
}

function addSymbol(parent, name, tint, size) {
  try {
    const sym = SFSymbol.named(name)
    sym.applyFont(Font.systemFont(size + 2))
    const img = parent.addImage(sym.image)
    img.imageSize = new Size(size, size)
    img.tintColor = tint
    img.centerAlignImage()
  } catch (_) {
    // Symbol missing on older iOS — skip quietly
  }
}

function shortAqiCategory(category) {
  if (!category) return ""
  if (category.startsWith("Unhealthy (Sensitive)")) return "Sensitive"
  if (category === "Very Unhealthy") return "Very Bad"
  return category
}

function aqiTextColor(aqi, theme) {
  // Soften neon EPA colors so they stay readable on light sky themes
  const lightSky = ["#0B2A44", "#0F2F4A", "#14324A", "#1A242C", "#243037", "#122636", "#1A2C3C"].includes(
    theme.text
  )
  if (aqi <= 50) return new Color(lightSky ? "#1B7A2A" : "#00E400")
  if (aqi <= 100) return new Color(lightSky ? "#9A7A00" : "#F0D000")
  if (aqi <= 150) return new Color(lightSky ? "#C45A00" : "#FF7E00")
  if (aqi <= 200) return new Color(lightSky ? "#C41E1E" : "#FF4D4D")
  if (aqi <= 300) return new Color(lightSky ? "#6B2F8A" : "#C78AD6")
  return new Color(lightSky ? "#5A0018" : "#FF6B8A")
}

function addMetric(parent, label, value, labelColor, valueColor) {
  const s = parent.addStack()
  s.layoutHorizontally()
  const l = s.addText(`${label}  `)
  l.font = Font.systemFont(10)
  l.textColor = labelColor
  l.lineLimit = 1
  const v = s.addText(value)
  v.font = Font.semiboldSystemFont(11)
  v.textColor = valueColor
  v.lineLimit = 1
  v.minimumScaleFactor = 0.75
}

function precipKind(h) {
  const snow = h.snow || 0
  const rain = h.rain || 0
  const prob = h.precipProb || 0
  if (snow > rain && snow > 0) {
    return { symbol: "snowflake", fallback: "S", prob }
  }
  const code = h.weatherCode
  if (code === 71 || code === 73 || code === 75 || code === 77 || code === 85 || code === 86) {
    return { symbol: "snowflake", fallback: "S", prob }
  }
  if (code === 66 || code === 67 || code === 56 || code === 57) {
    return { symbol: "cloud.sleet.fill", fallback: "M", prob }
  }
  if (prob >= 60) return { symbol: "cloud.heavyrain.fill", fallback: "R", prob }
  return { symbol: "cloud.rain.fill", fallback: "R", prob }
}

function formatHour(iso) {
  const d = new Date(iso)
  let h = d.getHours()
  const ampm = h >= 12 ? "p" : "a"
  h = h % 12
  if (h === 0) h = 12
  return `${h}${ampm}`
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
