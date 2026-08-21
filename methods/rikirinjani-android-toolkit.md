---
name: adb-storage-inspector
description: Inspect Android phone storage over ADB. Lists storage hogs, analyzes WhatsApp/DCIM/app data, identifies cleanup opportunities, executes safe deletes, and debloats pre-installed apps. Inspired by SD Maid SE. Universal across brands. Requires USB debugging enabled and device connected.
---

# ADB Storage Inspector

Inspect, clean, and debloat Android phones over ADB. Works across all brands.

## Prerequisites

- ADB installed (`adb --version`)
- Device connected with USB Debugging ON
- `adb devices` shows `device`

## Quick Start

```powershell
adb devices                          # verify connection
adb shell df -h /sdcard              # storage overview
adb shell getprop ro.product.manufacturer  # detect brand
```

---

# PART 1: Storage Analysis

## Overall Usage
```powershell
adb shell df -h /sdcard
```

## Top-Level Folder Sizes
```powershell
adb shell du -h -d 1 /sdcard
```

## Android Media (WhatsApp, Telegram, etc.)
```powershell
adb shell du -h -d 1 /sdcard/Android/media
adb shell du -h -d 1 /sdcard/Android/media/com.whatsapp/WhatsApp
adb shell du -h -d 1 /sdcard/Android/media/com.whatsapp/WhatsApp/Media
```

## App Data Hogs
```powershell
adb shell du -h -d 1 /sdcard/Android/data
```

## Camera & Media
```powershell
adb shell du -h -d 1 /sdcard/DCIM
adb shell du -h -d 1 /sdcard/Pictures
adb shell du -h -d 1 /sdcard/Download
```

## SD Maid SE Feature Equivalents

| SD Maid Feature | ADB Equivalent |
|---|---|
| File Analysis | `du -h -d 1` per folder |
| Largest Files | `find /sdcard -type f -exec ls -lh {} \; \| sort -k5 -rh \| head -20` |
| Corpse Finder | `ls /sdcard/Android/data` cross-ref with `pm list packages` |
| App Cache Cleaner | `adb shell pm trim-caches 999G` |
| Empty Folder Finder | `find /sdcard -type d -empty` |
| WhatsApp Media Sizer | per-type breakdown |
| WhatsApp DB Cleanup | identify old `Databases/` backups, keep latest |
| Duplicate Finder | `md5sum` group-by-hash across DCIM/WhatsApp/Pictures |

---

# PART 2: Debloat (Universal)

## Architecture

```
 Detect brand (getprop)
       |
       v
 Apply brand-specific bloat list (MIUI / One UI / ColorOS / etc.)
       + Universal 3rd-party bloat (Facebook, Netflix, Amazon...)
       - Universal danger list (launcher, phone, SMS...)
       |
       v
 Present categorized list -> user confirms -> pm uninstall/disable
```

## 1. Detect Brand

```powershell
adb shell getprop ro.product.manufacturer  # Xiaomi, samsung, OPPO, vivo, Google...
adb shell getprop ro.build.version.release  # Android version
```

## 2. List All Packages

```powershell
adb shell pm list packages
```

## 3. Universal 3rd-Party Bloat (safe across all brands)

```
com.facebook.katana          - Facebook
com.facebook.appmanager
com.facebook.system
com.facebook.services
com.netflix.mediaclient      - Netflix
com.amazon.appmanager        - Amazon
com.reddit.frontpage         - Reddit
com.spotify.music            - Spotify
com.twitter.android          - Twitter/X
com.instagram.android        - Instagram
com.instagram.barcelona      - Threads
com.ss.android.ugc.trill     - TikTok
com.google.ar.lens           - Google Lens
com.google.android.apps.magazines - Google News
com.google.android.apps.wellbeing   - Digital Wellbeing
com.google.android.apps.googleassistant - Google Assistant
com.adobe.spark.post         - Adobe Express
com.microsoft.skype.teams    - Microsoft Teams
com.linkedin.android         - LinkedIn
```

## 4. Universal Danger List (NEVER remove)

```
com.android.launcher*        - Launcher (home screen)
com.android.phone            - Phone app
com.android.settings         - Settings
com.android.systemui         - System UI
com.android.providers.contacts - Contacts provider
com.android.providers.telephony - Telephony provider
com.android.providers.media   - Media provider
com.android.vending           - Play Store
com.google.android.gms        - Google Play Services
com.google.android.gsf        - Google Services Framework
com.sec.android.app.launcher* - Samsung launcher
com.xiaomi.account            - Xiaomi account
com.miui.securitycenter       - MIUI security
com.mi.android.globallauncher - MIUI launcher
```

## 5. Brand-Specific Bloat Lists

### MIUI / Xiaomi

```
com.miui.analytics              - Telemetry
com.miui.bugreport              - Bug reports
com.miui.msa.global              - MSA (ads engine)
com.miui.yellowpage              - Yellow Pages
com.miui.videoplayer             - Mi Video
com.miui.player                  - Mi Music
com.miui.fm                      - FM Radio
com.miui.screenrecorder          - Screen Recorder
com.miui.weather2                - Weather
com.miui.touchassistant          - Touch Assistant
com.miui.audiomonitor            - Audio Monitor
com.miui.cleaner                 - Cleaner
com.miui.powerkeeper             - Power Keeper
com.miui.phrase                  - Phrase shortcuts
com.miui.aod                     - Always-On Display
com.miui.miservice               - Mi Service
com.miui.freeform                - Freeform windows
com.miui.mishare.connectivity    - Mi Share
com.xiaomi.midrop                - Mi Drop
com.miui.backup                  - Local backup
com.miui.micloudsync             - Mi Cloud sync
com.xiaomi.payment               - Mi Pay
com.miui.notification            - Notification
com.miui.compass                 - Compass
com.duokan.phone.remotecontroller - IR Remote
com.xiaomi.discover              - App Vault / feed
```

### Samsung One UI

```
com.samsung.android.bixby.wakeup  - Bixby
com.samsung.android.bixby.agent
com.samsung.android.bixbyvision.framework
com.samsung.android.visionintelligence
com.samsung.android.app.spage     - Samsung Free
com.samsung.android.app.social    - Samsung Social
com.samsung.android.game.gametools - Game Tools
com.samsung.android.game.gos      - Game Optimizing Service
com.samsung.android.oneconnect    - SmartThings
com.facebook.appmanager           - Facebook suite
com.facebook.katana
com.facebook.system
com.facebook.services
com.microsoft.skype.teams         - Carrier bloat
com.samsung.android.app.notes     - Samsung Notes
com.samsung.android.calendar      - Samsung Calendar
com.samsung.android.forest        - Digital Wellbeing
com.samsung.kidsmode              - Kids Mode
com.sec.android.app.samsungapps   - Galaxy Store
com.samsung.android.app.reminder  - Reminder
```

### ColorOS / OPPO / Realme / OnePlus

```
com.heytap.market                 - App Market
com.heytap.browser                - Browser
com.heytap.cloud                  - HeyTap Cloud
com.coloros.filemanager           - File Manager
com.coloros.gamespace             - Game Space
com.coloros.weather               - Weather
com.coloros.video                 - Video player
com.coloros.music                 - Music player
com.coloros.compass               - Compass
com.coloros.soundrecorder         - Sound Recorder
com.coloros.assistantscreen       - Smart Sidebar
com.coloros.children              - Children's Space
com.opera.browser                 - Opera
com.opera.mini.native             - Opera Mini
com.facebook.katana               - Facebook suite
```

### vivo / Funtouch OS

```
com.vivo.weather                  - Weather
com.vivo.video                    - Video player
com.vivo.music                    - Music player
com.vivo.game                     - Game Center
com.vivo.vivokaraoke              - Karaoke
com.vivo.easyshare                - EasyShare
com.vivo.assistant                - Jovi assistant
com.facebook.katana               - Facebook suite
com.vivo.browser                  - Browser
com.vivo.appstore                 - App Store
com.vivo.digitalwellbeing         - Digital Wellbeing
```

### Nothing OS

```
com.nothing.weather               - Nothing Weather
com.nothing.recorder              - Nothing Recorder
com.facebook.katana               - Facebook (if present)
```

## 6. Debloat Commands

### Uninstall
```powershell
adb shell pm uninstall -k --user 0 <package.name>
```

### Disable (fallback if uninstall fails)
```powershell
adb shell pm disable-user --user 0 <package.name>
```

### Re-enable
```powershell
adb shell pm enable <package.name>
```

## 7. Android Version Compatibility

| Feature | Min Android | Notes |
|---|---|---|
| `pm list packages` | 1.0 | Universal |
| `pm uninstall -k --user 0` | 4.0 | Some OEMs block on newer Android; fallback to disable |
| `pm disable-user --user 0` | 5.0 | Reliable fallback when uninstall fails |
| `df -h /sdcard` | 1.0 | Universal |
| `du` on `/sdcard/` | 1.0 | Universal |
| `getprop ro.product.manufacturer` | 1.0 | Universal |
| WhatsApp at `Android/media/` | 11+ | Pre-11: at `/sdcard/WhatsApp/` root |
| `pm trim-caches` | 7.0+ | Ignores large app data, only cache |
| Scoped storage restrictions | 11+ | Can't read other apps' `Android/data/` dirs |

**Version-specific gotchas:**
- **Android 14+** — Some brands restrict `pm uninstall` for system apps more aggressively
- **Android 11+** — Scoped storage hides `/sdcard/Android/data/` contents of other apps via `ls`; `du` still works
- **MIUI 14+** — Some packages flag `Failure [-1000]` on uninstall but accept `disable-user`
- **Samsung One UI 6+** — Bixby packages may be protected; try disable first

## 8. Debloat Safety Rules

1. Never remove the launcher
2. Never remove Play Services (com.google.android.gms)
3. Never remove the keyboard
4. Never remove Phone / SMS / Contacts providers
5. Disable instead of uninstall if unsure
6. All changes are user-level - factory reset restores everything
7. Debloating frees RAM/CPU/ads, not significant storage (typically <500 MB)

---

# PART 3: Cleanup Actions

## WhatsApp Database backups
```powershell
adb shell ls -lh /sdcard/Android/media/com.whatsapp/WhatsApp/Databases/
adb shell rm /sdcard/Android/media/com.whatsapp/WhatsApp/Databases/msgstore-OLD.db.crypt14
```

## WhatsApp Images
```powershell
adb pull "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images" C:\backup
adb shell rm -rf "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images"
```

## Camera roll
```powershell
adb pull /sdcard/DCIM/Camera C:\backup\DCIM
adb shell rm -rf /sdcard/DCIM/Camera
```

## App caches
```powershell
adb shell pm trim-caches 999G
```

## Empty folders
```powershell
adb shell find /sdcard -type d -empty -delete
```

## Corpse data
```powershell
adb shell pm list packages > installed.txt
adb shell ls /sdcard/Android/data > data_dirs.txt
```

---

# Safety Rules

1. Always backup before delete
2. WhatsApp Databases - keep the most recent
3. Games - ask user before touching
4. System apps - never touch
5. Verify - `adb shell df -h /sdcard` after each action

---

# Verdict

```powershell
adb shell df -h /sdcard
```
