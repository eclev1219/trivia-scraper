// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: blue; icon-glyph: cloud-sun-rain;
//
// AccuWeather Report Widget for Scriptable
// Temperature • Humidity • Air Quality • Hourly rain/snow
//
// IMPORTANT: Scriptable cannot read the AccuWeather iOS app.
// This widget uses AccuWeather's developer API instead.
// Get a key at: https://developer.accuweather.com/

////////////////////
// CONFIG
////////////////////

const CONFIG = {
  // Prefer Keychain over hardcoding. Falls back to this string if Keychain is empty.
  // Set once in Scriptable with: Keychain.set("accuweather_api_key", "YOUR_KEY")
  apiKeyFallback: "YOUR_ACCUWEATHER_API_KEY",

  // Leave empty to use GPS → AccuWeather location key.
  // Or paste a known key (e.g. "349727" for NYC) to save API calls.
  locationKey: "",

  // "F" or "C"
  units: "F",

  // How many forecast hours to show in the widget (max 12 on Starter/Free Core Weather)
  hourlyHours: 6,

  // Cache weather responses to stay within AccuWeather call limits
  cacheMinutes: 20,

  // AccuWeather Air Quality is Enterprise-only.
  // When true, fall back to Open-Meteo (free, no key) for AQI if AccuWeather AQ fails.
  useOpenMeteoAirQualityFallback: true,

  // Widget refresh hint (iOS decides actual refresh timing)
  refreshMinutes: 30,
}

const BASE = "https://dataservice.accuweather.com"
const CACHE_DIR = "accuweather-widget-cache"

////////////////////
// MAIN
////////////////////

async function main() {
  try {
    const apiKey = getApiKey()
    if (!apiKey || apiKey === "YOUR_ACCUWEATHER_API_KEY") {
      const w = errorWidget(
        "Add AccuWeather API key",
        "In Scriptable run:\nKeychain.set(\"accuweather_api_key\", \"YOUR_KEY\")\nor set CONFIG.apiKeyFallback."
      )
      present(w)
      return
    }

    const coords = await getCoordinates()
    const location = await resolveLocation(apiKey, coords)
    const weather = await loadWeather(apiKey, location, coords)
    const widget = buildWidget(weather, location)
    present(widget)
  } catch (err) {
    console.error(err)
    const w = errorWidget("Weather unavailable", String(err))
    present(w)
  }
}

function present(widget) {
  if (config.runsInWidget) {
    Script.setWidget(widget)
  } else {
    widget.presentMedium()
  }
  Script.complete()
}

////////////////////
// AUTH / LOCATION
////////////////////

function getApiKey() {
  try {
    if (Keychain.contains("accuweather_api_key")) {
      return Keychain.get("accuweather_api_key")
    }
  } catch (_) {}
  return CONFIG.apiKeyFallback
}

async function getCoordinates() {
  Location.setAccuracyToKilometer()
  const loc = await Location.current()
  return { lat: loc.latitude, lon: loc.longitude }
}

async function resolveLocation(apiKey, coords) {
  if (CONFIG.locationKey) {
    return {
      Key: CONFIG.locationKey,
      LocalizedName: "Saved location",
      lat: coords.lat,
      lon: coords.lon,
    }
  }

  const cacheKey = `loc_${coords.lat.toFixed(2)}_${coords.lon.toFixed(2)}`
  const cached = readCache(cacheKey, 24 * 60) // location keys are stable
  if (cached) return cached

  const q = `${coords.lat},${coords.lon}`
  const url =
    `${BASE}/locations/v1/cities/geoposition/search` +
    `?apikey=${encodeURIComponent(apiKey)}` +
    `&q=${encodeURIComponent(q)}` +
    `&toplevel=true`

  const data = await getJSON(url)
  if (!data || !data.Key) {
    throw new Error("Could not resolve AccuWeather location key")
  }

  const location = {
    Key: data.Key,
    LocalizedName: data.LocalizedName || data.EnglishName || "Nearby",
    AdministrativeArea: data.AdministrativeArea?.ID || "",
    Country: data.Country?.ID || "",
    lat: coords.lat,
    lon: coords.lon,
  }
  writeCache(cacheKey, location)
  return location
}

////////////////////
// WEATHER FETCH
////////////////////

async function loadWeather(apiKey, location, coords) {
  const cacheKey = `wx_${location.Key}_${CONFIG.units}`
  const cached = readCache(cacheKey, CONFIG.cacheMinutes)
  if (cached) return cached

  const metric = CONFIG.units === "C"
  const currentUrl =
    `${BASE}/currentconditions/v1/${location.Key}` +
    `?apikey=${encodeURIComponent(apiKey)}` +
    `&details=true`

  const hourlyUrl =
    `${BASE}/forecasts/v1/hourly/12hour/${location.Key}` +
    `?apikey=${encodeURIComponent(apiKey)}` +
    `&details=true` +
    `&metric=${metric}`

  // AccuWeather AQ: Enterprise endpoint (often fails on free/starter)
  const aqUrl =
    `https://api.accuweather.com/airquality/v2/currentconditions/${location.Key}` +
    `?apikey=${encodeURIComponent(apiKey)}` +
    `&language=en-us`

  const [currentRes, hourlyRes, aqRes] = await Promise.all([
    getJSON(currentUrl),
    getJSON(hourlyUrl),
    getJSONSafe(aqUrl),
  ])

  const current = Array.isArray(currentRes) ? currentRes[0] : null
  if (!current) throw new Error("No current conditions returned")

  const tempObj = metric ? current.Temperature?.Metric : current.Temperature?.Imperial
  const realFeelObj = metric
    ? current.RealFeelTemperature?.Metric
    : current.RealFeelTemperature?.Imperial

  let airQuality = parseAccuWeatherAQ(aqRes)
  if (!airQuality && CONFIG.useOpenMeteoAirQualityFallback) {
    airQuality = await fetchOpenMeteoAQ(coords.lat, coords.lon)
  }

  const hours = (Array.isArray(hourlyRes) ? hourlyRes : [])
    .slice(0, CONFIG.hourlyHours)
    .map((h) => ({
      time: h.DateTime,
      temp: h.Temperature?.Value,
      phrase: h.IconPhrase || "",
      precipProb: h.PrecipitationProbability ?? 0,
      rainProb: h.RainProbability ?? h.PrecipitationProbability ?? 0,
      snowProb: h.SnowProbability ?? 0,
      precipType: h.PrecipitationType || null,
      hasPrecip: !!h.HasPrecipitation,
      icon: h.WeatherIcon,
    }))

  const weather = {
    fetchedAt: new Date().toISOString(),
    weatherText: current.WeatherText || "",
    weatherIcon: current.WeatherIcon,
    isDayTime: current.IsDayTime,
    temperature: tempObj?.Value,
    realFeel: realFeelObj?.Value,
    humidity: current.RelativeHumidity,
    unit: metric ? "C" : "F",
    airQuality,
    hours,
  }

  writeCache(cacheKey, weather)
  return weather
}

function parseAccuWeatherAQ(payload) {
  // Enterprise responses often look like { success, data: { overallIndex, category, ... } }
  const data = payload?.data || payload
  if (!data || data.overallIndex == null) return null
  return {
    source: "AccuWeather",
    index: Math.round(data.overallIndex),
    category: data.category || "",
    pollutant: data.dominantPollutant || "",
    color: data.categoryColor || null,
  }
}

async function fetchOpenMeteoAQ(lat, lon) {
  try {
    const url =
      `https://air-quality-api.open-meteo.com/v1/air-quality` +
      `?latitude=${lat}&longitude=${lon}` +
      `&current=us_aqi,european_aqi` +
      `&timezone=auto`
    const data = await getJSON(url)
    const aqi = data?.current?.us_aqi
    if (aqi == null) return null
    return {
      source: "Open-Meteo",
      index: Math.round(aqi),
      category: usAqiCategory(aqi),
      pollutant: "",
      color: usAqiColor(aqi),
    }
  } catch (_) {
    return null
  }
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

function buildWidget(weather, location) {
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

  const place = location.AdministrativeArea
    ? `${location.LocalizedName}, ${location.AdministrativeArea}`
    : location.LocalizedName

  const header = w.addStack()
  header.layoutHorizontally()
  header.centerAlignContent()

  const title = header.addText(place)
  title.font = Font.semiboldSystemFont(13)
  title.textColor = Color.white()
  title.lineLimit = 1

  header.addSpacer()

  const cond = header.addText(weather.weatherText)
  cond.font = Font.systemFont(12)
  cond.textColor = new Color("#FFFFFF", 0.85)
  cond.lineLimit = 1

  w.addSpacer(8)

  // Temp + metrics row
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
    const aqLabel = `${weather.airQuality.index} ${weather.airQuality.category}`
    addMetric(metrics, "AQI", aqLabel, weather.airQuality.color)
    if (weather.airQuality.source === "Open-Meteo") {
      const note = metrics.addText("AQI via Open-Meteo")
      note.font = Font.systemFont(9)
      note.textColor = new Color("#FFFFFF", 0.55)
    }
  } else {
    addMetric(metrics, "AQI", "Unavailable")
  }

  w.addSpacer(10)

  // Hourly precip strip
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
  // Prefer snow when snow probability dominates; otherwise rain/precip
  if ((h.snowProb || 0) >= (h.rainProb || 0) && (h.snowProb || 0) > 0) {
    return { symbol: "snowflake", fallback: "S", prob: h.snowProb }
  }
  if (h.precipType === "Snow") {
    return { symbol: "snowflake", fallback: "S", prob: h.snowProb || h.precipProb }
  }
  if (h.precipType === "Ice" || h.precipType === "Mixed") {
    return {
      symbol: "cloud.sleet",
      fallback: "M",
      prob: Math.max(h.rainProb || 0, h.snowProb || 0, h.precipProb || 0),
    }
  }
  return { symbol: "cloud.rain", fallback: "R", prob: h.rainProb || h.precipProb || 0 }
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
  return `AccuWeather · updated ${t}`
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
    // Surface AccuWeather auth / quota errors more clearly
    let raw = ""
    try {
      raw = await new Request(url).loadString()
    } catch (_) {}
    throw new Error(
      `API error: ${String(e).slice(0, 120)}` +
        (raw ? ` | ${String(raw).slice(0, 160)}` : "")
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
