// Variables used by Scriptable.
// icon-color: blue; icon-glyph: key;
//
// One-time helper: save your AccuWeather API key to the Keychain.
// Run this script once in Scriptable, then you can delete it.

const key = args.plainTexts[0] || ""

if (!key) {
  const alert = new Alert()
  alert.title = "AccuWeather API Key"
  alert.message = "Paste your AccuWeather developer API key."
  alert.addTextField("API key", "")
  alert.addAction("Save")
  alert.addCancelAction("Cancel")
  const idx = await alert.present()
  if (idx === -1) {
    Script.complete()
  } else {
    const value = alert.textFieldValue(0).trim()
    if (!value) {
      throw new Error("No key entered")
    }
    Keychain.set("accuweather_api_key", value)
    const done = new Alert()
    done.title = "Saved"
    done.message = "Key stored as accuweather_api_key"
    done.addAction("OK")
    await done.present()
    Script.complete()
  }
} else {
  Keychain.set("accuweather_api_key", key.trim())
  Script.complete()
}
