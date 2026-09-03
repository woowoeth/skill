---
name: fix-air-region
description: Bypass JetBrains Air IDE region restriction for China Mainland users
user-invocable: true
allowed-tools: Bash, Read, Write
---

# Fix JetBrains Air Region Restriction

JetBrains Air (based on Fleet) has a **client-side hardcoded** region check in the onboarding flow. When the region is set to `china`, the app shows "Unfortunately, Air is not yet available in your region" and exits. This has nothing to do with network/proxy — it's purely a local preference check.

## Technical Details

- Region preference is stored in **Java Preferences** (`java.util.prefs.Preferences`)
- On macOS, this maps to `~/Library/Preferences/com.apple.java.util.prefs.plist`
- The key path is `/ -> jetbrains/ -> region/ -> code`
- The check is in class `OnboardingFlowKt$ChooseYourRegion$1` inside `fleet.frontend.commander` JAR
- Logic: `if (region == Regions.China) -> AIR_IS_NOT_AVAILABLE else -> ACCEPT_LICENSE_AGREEMENT`
- Valid region values: `not_set`, `africa`, `americas`, `apac`, `china`, `europe`

## Steps

Run the following Python script to set the region to `americas`:

```bash
python3 << 'PYTHON'
import plistlib
import os

plist_path = os.path.expanduser("~/Library/Preferences/com.apple.java.util.prefs.plist")

with open(plist_path, 'rb') as f:
    data = plistlib.load(f)

root = data.get("/", {})
jb = root.get("jetbrains/", "")
if not isinstance(jb, dict):
    jb = {}
if "region/" not in jb:
    jb["region/"] = {}

jb["region/"]["code"] = "americas"
root["jetbrains/"] = jb
data["/"] = root

with open(plist_path, 'wb') as f:
    plistlib.dump(data, f)

print("JetBrains Air region set to 'americas'. Restart Air to take effect.")
PYTHON
```

After running the script, restart JetBrains Air. If the onboarding region selector appears, choose any region **except** "China Mainland".

## Verification

To check current region value:

```bash
defaults read com.apple.java.util.prefs 2>/dev/null | grep -A5 "jetbrains/"
```

Expected output should show `code = americas` (or any non-china value).
