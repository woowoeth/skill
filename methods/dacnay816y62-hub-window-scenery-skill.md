---
name: window-scenery
description: Generate photorealistic travel images from inside vehicles looking out through windows, with a consistent lower-left location badge. Use when the user asks for "车窗里的风景", "车窗美景", window-view scenery, travel photos from a car/train/boat/plane/cable-car window, or batch image prompts for locations viewed from transportation.
---

# 车窗里的风景

Create one independent vertical 3:4 travel photograph per requested location. The image must look as if the viewer is inside a moving vehicle, vessel, aircraft, train, or cable car, looking outward through a visible window frame.

## Core Rules

- Treat the window frame as the composition frame and the journey as the narrative.
- Make the exterior landscape the subject; keep the interior as foreground framing.
- Show a clear car window, train window, cabin window, porthole, plane window, ferry window, or cable-car glass.
- Match the landscape, architecture, weather, season, and light to the real location.
- Add "in transit" cues such as passing road edges, guardrails, wake, glass reflection, motion blur, ropes, handles, seats, curtains, or cabin trim.
- Output single images only. Never combine multiple locations into a collage.
- Avoid travel-advertising gloss, excessive HDR, fake skies, over-saturation, watermarks, extra titles, social UI, and unrelated text.
- If reference images are provided, use them only to infer abstract visual DNA. Do not directly use them as image-to-image inputs unless the user explicitly requests it, and do not copy exact people, scene relationships, composition skeletons, or signature color combinations.

## Request Parsing

Parse each request into:

```yaml
location:
landscape_type:
transport:
time:
weather:
landmark_or_natural_motif:
composition_mode:
coordinates:
badge_enabled:
aspect_ratio:
```

Defaults:

- `aspect_ratio`: vertical 3:4
- `transport`: auto-select by location type
- `time`, `weather`, `composition_mode`: auto-select for realism and variety
- `badge_enabled`: on unless the user disables it

For batch requests, the number of numbered locations equals the number of output images. Generate and save each location separately.

## Transport Matching

Use `references/style-guide.md` for detailed mappings, but keep these defaults:

- Cities and urban landmarks: car, taxi, bus, tram, double-decker bus, or city train.
- Plateaus, grasslands, mountains, and road trips: SUV, off-road vehicle, long-distance train, sleeper train, or scenic train.
- Coasts, islands, fjords, and harbor cities: ferry, boat cabin, passenger ship, speedboat, water bus, or water taxi.
- Glaciers, polar regions, and snowfields: train, icebreaker, cruise ship, ferry, or airplane.
- Tropical archipelagos and coral seas: speedboat, seaplane, ferry, or small passenger plane.
- Deserts, wilderness, and wildlife regions: off-road vehicle, Safari Jeep, or desert bus.
- Mountain cable areas: cable car, gondola, or scenic mountain vehicle.

## Prompt Template

Compile a final image prompt in English:

```text
Create one single photorealistic vertical 3:4 travel photograph viewed from inside a [TRANSPORT].

The camera is positioned inside the vehicle or vessel, looking outward through a clearly visible [WINDOW TYPE]. The window frame, door edge, cabin trim, seat edge, curtain, handle, mirror, rope, sill, or glass reflection appears naturally as foreground framing, occupying about 15% to 35% of the image.

Outside the window, show [LOCATION] through accurate, recognizable, non-cliche visual characteristics: [LANDSCAPE / ARCHITECTURE / CLIMATE DETAILS].

The image must feel like a real journey in progress. Include subtle motion cues such as passing road edges, gentle foreground blur, bridge railing, shoreline wake, distant traffic, glass reflection, or changing light.

Keep the scene realistic, calm, restrained, transparent, and lightly cinematic. The landscape is the protagonist. No collage, no poster layout, no advertising style, no extra text, no social-media UI, no watermark, no excessive HDR, no fake sky, no over-saturated tourism aesthetic.
```

If generating with an image backend, generate the base image without any text first. Add the location badge afterward with `scripts/overlay_badge.py` unless the user explicitly wants no badge.

## Location Badge

Place a small, consistent badge in the lower-left corner. Use the current system or conversation language for the place label so the user can immediately understand the location. If the user is writing in Chinese, use a concise Chinese place label.

```text
地点名 / PLACE LABEL IN CURRENT LANGUAGE
LATITUDE   LONGITUDE
```

Badge styling:

- Position: about 4% from the left and bottom.
- Width: 12% to 18% of image width.
- Height: 4% to 6% of image height.
- Background: semi-transparent dark gray/black.
- Border: very thin gray-white.
- Radius: subtle.
- Place text: concise local-language label; use uppercase only for Latin-script labels.
- Coordinates: smaller and lighter, 4 decimal places, using N / S / E / W.
- Do not place dash-like marks directly before coordinates; they can be mistaken for negative latitude or longitude signs.

Use user-provided coordinates first. If coordinates are missing, use the location center or main landmark coordinates; verify with a reliable source when uncertain or when precise coordinates matter.

Overlay command:

```powershell
python "D:\Codex_Moved_From_C\.codex\skills\window-scenery\scripts\overlay_badge.py" `
  --input "D:\Codex_Outputs\images\base.png" `
  --output "D:\Codex_Outputs\images\final.png" `
  --place "北京 · 天安门" `
  --coords "39.9087°N   116.3975°E"
```

## Workflow

1. Parse the user request and split batch locations.
2. Classify each location type.
3. Select a plausible transport and window type.
4. Extract 2 to 4 visual motifs tied to the location.
5. Choose composition, light, time, and weather; avoid repeating the same composition across adjacent batch outputs.
6. Generate a no-text base image.
7. Add the badge with `scripts/overlay_badge.py` if enabled.
8. Save generated images under `D:\Codex_Outputs\images` unless the user specifies another output directory.
9. Quality-check the result before delivery.

## Quality Check

Reject and redo when any of these fail:

- Viewpoint is not clearly inside transportation.
- Window frame or cabin edge is missing.
- Location features are inaccurate or generic.
- Transport does not fit the location.
- Image lacks a journey-in-progress feeling.
- Interior overwhelms the exterior; target 15% to 35% interior and 65% to 85% exterior.
- Image looks like a tourism advertisement, poster, collage, or ordinary landscape photo.
- Badge is too large, too bright, misplaced, text-wrong, or inconsistent.
- Extra text, watermark, social UI, fake sky, excessive HDR, muddy color, or over-saturation appears.

For additional composition modes, location categories, and test prompts, read `references/style-guide.md`.
