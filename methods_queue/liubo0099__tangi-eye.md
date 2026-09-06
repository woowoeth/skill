---
name: tangi-eye
description: >-
  Give an agent eyes on the physical world: capture a USB camera, HTTP snapshot,
  MJPEG or RTSP frame, trigger an authorized Android camera via ADB, or import an existing JPEG/PNG locally or through Android ADB.
  Examine the overview first,
  then crop native-resolution evidence for embedded hardware, wiring and headers,
  chip markings, suspected component damage, indicator LEDs, multimeter readings,
  and supplied software screenshots. Use when physical or image evidence is
  needed; not for code-only debugging or operating a computer interface.
license: MIT
metadata:
  version: "0.2.0"
  display-name: "TangiEye | 实界之眼"
---

# TangiEye | 实界之眼

Give your agent eyes on the physical world. 让 Agent 看见物理世界。

## Requirements and routing

Use a host that can execute local commands **and actually read local images**.
Use the user's configured language. This Skill supplies images, not a vision model.
Windows is the initial target; read `VALIDATION.md` before claiming a tested host,
platform, camera, or protocol. Python 3.11+ and `requirements.txt` are required.

Resolve all Skill scripts relative to this `SKILL.md` directory. The examples below
assume that directory is the current working directory; elsewhere use absolute paths.
Use a project virtual environment, not a global package installation. Run:

```powershell
python scripts/tangi_eye.py doctor
```

`doctor` does not open cameras unless given `--source`. A source probe captures and
discards a frame; do not describe it as passive device discovery. Exception: ADB
`doctor --source adb` checks authorization, lock state, camera package and folder
access without launching the camera or sending a shutter.

Use the image or camera source specified by the user or already established in
the session. If none is known, ask which camera/image to inspect. Do not enumerate
the network or silently switch to another camera. Keep an established source for
the task; do not repeatedly ask permission for already authorized captures.

## Observe, then inspect

1. **Acquire one observation.** Existing photos/screenshots use `ingest`; cameras
   use `capture`. Specify a workspace output directory, normally `work/tangi-eye`.
   Camera output records the delivered dimensions, which may differ from a request.

   ```powershell
   python scripts/tangi_eye.py capture --source usb --device 0 --width 1920 --height 1080 --output work/tangi-eye
   python scripts/tangi_eye.py ingest --input "board.jpg" --output work/tangi-eye
   ```

   For HTTP/MJPEG/RTSP setup, credentials and USB backend options, read
   [references/cli.md](references/cli.md). Do not put secret URLs in commands or chat;
   use an existing environment variable with `--url-env`.

   For an Android phone, read [references/android-adb.md](references/android-adb.md).
   For a fresh observation, use `capture --source adb --adb-serial SERIAL
   --camera-package CAMERA_PACKAGE --timeout 30`. The user unlocks and aims the
   phone; the script opens the selected camera, sends one shutter, verifies one
   newly saved photo and its transfer hash, then backgrounds the camera if still
   in focus. Use the established device/package; only the documented Huawei setup
   has real acceptance. Keep the camera app's current lens and settings.
   No new photo or multiple new photos means failure, never an old-photo fallback.
   Do not blindly retry after a timeout: a photo may already have been saved.
   For an explicitly selected existing photo, use `ingest --remote-path` instead;
   its capture time is unknown. `screencap` is a screenshot, not a camera photo.

2. **Read the returned `overview_path` using the host's image-reading tool.**
   File existence or JSON metadata is not visual evidence. Establish orientation,
   the target component, and the context needed to interpret it. If the host cannot
   read images, explain the limitation and request an image-capable host; do not guess.

3. **Crop a relevant region from that observation.** Use normalized coordinates
   `[x0, y0, x1, y1]` in the **entire orientation-corrected image**, not coordinates
   in a letterboxed viewer, a previous crop, or the unrotated input. Divide target
   positions by the displayed image's actual width and height, excluding UI margins.
   Leave enough context to retain pin numbers, polarity, units, or component references.

   ```powershell
   python scripts/tangi_eye.py crop --manifest "ABSOLUTE_PATH_FROM_CAPTURE_OR_INGEST" --bbox 0.25 0.2 0.65 0.6
   ```

   Read `crop_path` with the host image tool. Further regions must use the same
   observation manifest and original coordinate space. Never crop the overview.

4. **Report only what the images support.** Separate visible facts, possible
   explanations, missing evidence, and the next useful action. Link to the overview
   and relevant crop. For task-specific interpretation, read
   [references/inspection.md](references/inspection.md).

## Evidence quality

- Original file bytes remain unchanged. Canonical PNG corrects EXIF orientation;
  CMYK input is converted for PNG. Native crop pixels equal the canonical region.
  JPEG/camera transport may already be lossy. “Lossless crop” does not mean optical
  magnification or recovery of absent detail.
- No generated repair, super-resolution, sharpening, or inferred character completion
  may serve as diagnostic evidence. Do not infer missing digits from a likely part name.
- When focus, glare, angle, or pixel count prevents a conclusion, request a specific
  better view (move closer, refocus, light from the side, include the meter mode).
  Repeating crops of the same insufficient pixels is not progress.
- After rewiring or another state change, acquire a new observation. Import time is
  not capture time. Acquisition timestamps indicate local receipt, not verified
  sensor exposure time or server freshness.
- A still LED image cannot establish a blink pattern. Visible discoloration cannot
  establish an electrical failure, and a photo cannot prove continuity or voltage.
- Source failure, timeout or an unreadable image must remain a failure. Do not
  substitute an earlier observation without explicitly identifying it as old evidence.

## Boundaries

The scripts perform local image processing and contact only the supplied source.
They do not upload images to a recognition API; the host agent's image processing
still follows that host's settings. No automatic publication or telemetry is included.

This Skill does not manipulate wiring, energize hardware, operate desktop mouse/keyboard,
record ongoing video, or recognize arbitrary proprietary camera APIs. Software UI
inspection accepts provided screenshots. Android control is limited to the selected
camera launch, one shutter, and conditional Back cleanup; no unlocking, permission
bypass, app installation or general UI automation. High-voltage work, changing connections,
and electrical measurement procedures require their own appropriate context.
