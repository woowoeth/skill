---
name: luma
description: "Manage Luma events: discover local events, view your calendar, check guest lists, RSVP, and create events. Use when: user asks about events, meetups, RSVPs, or anything related to luma.com / lu.ma / Luma."
homepage: https://luma.com
requires:
  bins:
    - curl
  env:
    - name: LUMA_AUTH_SESSION_KEY
      description: >-
        Luma session cookie (the `luma.auth-session-key` value copied from the
        browser). Luma issues no public API keys — this cookie is the only
        credential, and it authenticates every read and write. Shaped
        `usr-<id>.<secret>`; the part before the dot matches the account's
        `api_id`, so a value that looks truncated there was mis-copied. Expires
        with the browser session and must be re-copied when it does.
      sensitive: true
---

# Luma Skill

Manage events on [Luma](https://luma.com) (luma.com, formerly lu.ma) — discover, list, RSVP, check guests, and create events.

## When to Use

- "What events are happening in <city name>?"
- "Show my upcoming events"
- "Who's going to [event]?"
- "RSVP me to [event]"
- "Create an event for Friday"
- "Show me tech meetups near me"

## When NOT to Use

- Eventbrite, Meetup.com, or other event platforms
- Google Calendar management (use a calendar skill)

## Authentication

All requests require the `LUMA_AUTH_SESSION_KEY` env var (Luma session cookie).

Set it:
```bash
export LUMA_AUTH_SESSION_KEY="usr-..."
```

To get it: open luma.com in browser, open dev tools, Application > Cookies > `https://luma.com`, copy the `luma.auth-session-key` value.

## API Base

All endpoints use `https://api.luma.com` with the cookie header:
```
Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY
```

> **Host migration (Aug 2026).** Luma moved its API from `api.lu.ma` to `api.luma.com`, and the site from `lu.ma` to `luma.com`. Three things to know:
>
> - The **old API host still answers read endpoints**, so a stale integration looks healthy right up until it tries to write.
> - `POST api.lu.ma/event/create` now returns `400 {"message":"Invalid request.","code":null}` for **every** payload — including an empty body and unauthenticated requests. If create fails with a bare "Invalid request." and no field-level detail, check the host before you touch the payload.
> - The **session cookie is unchanged** — same `luma.auth-session-key` name, same value, accepted by both hosts. Migrating does not require re-authenticating.
>
> Old event links still work: `lu.ma/<slug>` 301-redirects to `luma.com/<slug>`.

## User Info

Call `/user` to learn who the session belongs to. Useful fields:

- `personal_calendar_api_id` — the calendar to create events on by default
- `timezone` — the viewer's timezone, e.g. `"America/Vancouver"`
- `geo_city`, `geo_region`, `geo_country` — used to scope local event discovery

Note that `/user` returns a **city, not coordinates**. The discover endpoint wants either `geo_latitude`/`geo_longitude` or a `discover_place_api_id`, so resolve the city through `/url?url=<city>` to get its place ID rather than expecting lat/long on the profile.

## Timezones

All timestamps on the wire are UTC ISO-8601 (`2026-09-10T01:00:00.000Z`). Never show a raw `start_at` to a user.

Two different timezones matter here, and picking the wrong one is the easy mistake:

- **The event's timezone.** Every event object carries its own `timezone` field. This is where the event physically happens, and it is the right one for rendering that event's start time. A 7pm meetup in Berlin should read `7:00 PM CEST` regardless of who is asking.
- **The viewer's timezone.** `/user` returns `timezone` for the signed-in account. Use it when the answer depends on the viewer's own clock — "what's on tonight", "this weekend", or any relative phrasing like "in 2 hours". Fall back to the system timezone if the field is missing.

When the two differ, show both rather than silently picking one: `7:00 PM CEST (10:00 AM PDT)`.

On create, the `timezone` field in the payload sets the event's timezone; `start_at` stays UTC regardless.

## Commands

### Search Events

```bash
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/search/get-results?query=SEARCH_TERMS"
```

Returns: `events[]` (direct matches), `calendars[]`, `discover_entities[]` (places and categories), `help_pages[]`.

- `events[]` contains full event objects with `event`, `calendar`, `hosts[]`, `ticket_info`, and `guest_info` (if user is registered).
- `discover_entities[]` includes `type: "discover-place"` (cities) and `type: "discover-category"` (topics) with `api_id` values like `cat-crypto`, `discplace-4fa7ldlAkBTTivm`.

**Search workflow:**
1. Call `search/get-results?query=...` — check `events[]` first for direct hits.
2. If no direct events but `discover_entities[]` has a relevant category, use it to browse:

```bash
# Events by category near a location (e.g. crypto events near Vancouver)
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/discover/get-paginated-events?discover_category_api_id=cat-crypto&geo_latitude=49.2827&geo_longitude=-123.1207&pagination_limit=20"

# Events by place (city discover feed — only shows city-tagged events)
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/discover/get-paginated-events?discover_place_api_id=discplace-4fa7ldlAkBTTivm&pagination_limit=20"
```

**Tips:** Use specific terms (organizer names, event titles) for direct event hits. Generic terms (like "crypto") tend to return categories instead. Combine both: search for direct matches, then browse the returned category near the user's location.

### Get Current User Profile

```bash
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/user" | python3 -m json.tool
```

Returns: user profile with name, email, avatar, timezone, social handles, personal calendar ID.

### Discover Events by City

```bash
# First resolve the city to a discover place
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/url?url=vancouver"

# Then get paginated events for that place
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/discover/get-paginated-events?discover_place_api_id=discplace-XXXX&pagination_limit=10"
```

The `url` endpoint returns `kind: "discover-place"` with `data.place.api_id` and `data.place.featured_event_api_ids`.


### Get Event Details

```bash
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/event/get?event_api_id=evt-XXXX"
```

Returns: full event details including name, start/end times, location, calendar info, cover image, visibility, waitlist status.

### Get Event Guest List

```bash
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/event/get-guest-list?event_api_id=evt-XXXX"
```

Returns: `entries[]` with user profiles (name, avatar, social handles, tickets registered). Supports `next_cursor` pagination.

Only works for events you host or events with public guest lists (`show_guest_list: true`).

**Guest entry shape:** each entry has two distinct api_ids — a guest-registration ID at the root, and a user ID under `user`. They are *not* interchangeable.

```json
{
  "entries": [
    {
      "api_id": "gst-xxx",
      "num_tickets_registered": 1,
      "user": {
        "api_id": "usr-xxx",
        "name": "...",
        "first_name": "...",
        "last_name": "...",
        "email": "..."
      }
    }
  ]
}
```

Use the root `api_id` as a stable key for a specific signup (e.g. for diffing to detect cancellations). Use `user.api_id` to reference the person. Not every entry has the root `api_id` populated — fall back to `user.api_id` when it's missing.

**Detecting new signups / cancellations:** the endpoint returns the current snapshot only — there is no per-guest timestamp and no "new" marker. To build a signup notifier, persist the previous set of guest IDs and diff across polls:

- IDs present now but not before → new signups
- IDs present before but not now → cancellations

### User Profile Events

```bash
# Overview: hosting, past, and events-together for a user (by username)
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/user/profile/events?username=USERNAME"
```

Returns: `events_hosting[]`, `events_past[]`, `events_together[]` — a snapshot of the user's event history and overlap with you.

```bash
# Paginated list of events a user is hosting (by user_api_id)
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/user/profile/events-hosting?user_api_id=usr-XXXX&pagination_limit=10"
```

Returns: `entries[]` with full event objects. Supports `has_more` / cursor pagination.

```bash
# Paginated list of events in common with the authenticated user (by user_api_id)
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/user/profile/events-together?user_api_id=usr-XXXX&pagination_limit=10"
```

Returns: `entries[]` of events both you and the target user have attended or are registered for.

**Note:** `/events` requires `username`, while `/events-hosting` and `/events-together` require `user_api_id`. Get `user_api_id` from the `/user` endpoint or from event guest lists.

### List Your Calendar Events

```bash
# Past events on your personal calendar
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/calendar/get-items?calendar_api_id=YOUR_CALENDAR_API_ID&period=past&pagination_limit=10"

# Future events on your personal calendar
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/calendar/get-items?calendar_api_id=YOUR_CALENDAR_API_ID&period=future&pagination_limit=10"
```

Returns: `entries[]` with event details, cover images, calendar info. Supports `has_more` pagination.

**Response shape:** each entry wraps the actual event object one level deep under `event` — access fields like `entry.event.api_id`, not `entry.api_id`.

```json
{
  "entries": [
    {
      "event": { "api_id": "evt-xxx", "name": "...", "start_at": "...", "cover_url": "..." },
      "calendar": { "api_id": "cal-xxx", "name": "..." },
      "hosts": [ ... ]
    }
  ]
}
```

### Resolve URL / Event Slug

```bash
curl -s -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  "https://api.luma.com/url?url=EVENT_SLUG_OR_CITY"
```

Returns: `kind` (`"event"`, `"discover-place"`, `"calendar"`, `"user"`) and `data` with the resolved object. Use this to look up events by their luma.com URL slug.

### Create Event (single call)

`/event/create` takes the **whole event definition in one request** — name, schedule, location, description, visibility and ticketing. The older two-step flow (create a shell, then fill it in via `/event/admin/update`) is no longer needed; `admin/update` is now only for editing an event after it exists.

```bash
curl -s -X POST \
  -H "Cookie: luma.auth-session-key=$LUMA_AUTH_SESSION_KEY" \
  -H "Content-Type: application/json" \
  -H "Origin: https://luma.com" \
  -H "x-luma-client-type: luma-web" \
  "https://api.luma.com/event/create" \
  -d @event.json
```

Returns: `{ "api_id": "evt-xxx", "url": "slug", "calendar_event_api_id": "calev-xxx" }`. The public event URL is `https://luma.com/<url>` — the `url` field is the slug, not the `api_id`.

**The create validator is strict and silent.** Every rejection — missing field, malformed value, wrong host — comes back as the same flat `400 {"message":"Invalid request.","code":null}`, with no indication of which field is at fault. Because of that, send the full payload template below and vary only the values.

Verified behaviour:

- The template below is accepted **exactly as written** (only the values swapped).
- A trimmed 8-field subset (`name`, `start_at`, `duration_interval`, `timezone`, `calendar_api_id`, `visibility`, `description_mirror`, `ticket_types`) is **rejected**.
- `cover_url: null` is **rejected** — see the field notes.

Which of the remaining fields are strictly required has not been isolated one by one, so treat the template as the contract rather than trying to guess a minimum.

**Payload template:**

```json
{
  "name": "Event Name",
  "start_at": "2026-09-10T01:00:00.000Z",
  "duration_interval": "PT1H",
  "timezone": "America/Vancouver",
  "calendar_api_id": "cal-xxx",
  "visibility": "public",

  "description_mirror": {
    "type": "doc",
    "content": [
      { "type": "paragraph", "content": [{ "type": "text", "text": "Event details here." }] }
    ]
  },

  "location_type": "offline",
  "geo_address_visibility": "public",
  "geo_address_json": {
    "type": "google",
    "place_id": "ChIJ...",
    "address": "Venue Name",
    "full_address": "756 Davie St, Vancouver, BC V6G 1B6, Canada",
    "short_address": "756 Davie St, Vancouver",
    "city_state": "Vancouver, BC",
    "city": "Vancouver",
    "region": "British Columbia",
    "region_short": "BC",
    "country": "Canada",
    "country_code": "CA",
    "place_coordinate": { "latitude": 49.2774788, "longitude": -123.1272636 }
  },
  "coordinate": { "latitude": 49.2774788, "longitude": -123.1272636 },

  "ticket_types": [
    {
      "type": "free",
      "currency": null,
      "cents": null,
      "min_cents": null,
      "is_flexible": false,
      "require_approval": false,
      "is_hidden": false,
      "ethereum_token_requirements": []
    }
  ],

  "max_capacity": null,
  "waitlist_status": "disabled",
  "calendar_to_submit_to_api_id": null,
  "grant_manage_access": false,
  "_calendar_requires_manage_access": false,
  "supports_members_only": false,

  "zoom_meeting_url": null,
  "zoom_meeting_id": null,
  "zoom_meeting_password": null,
  "zoom_session_type": null,
  "zoom_creation_method": null,

  "cover_url": "https://images.lumacdn.com/gallery-images/2b/9d9ee6ac-3d35-4fce-ade7-3f0ee7216dac",
  "theme_meta": { "theme": "legacy" },
  "tint_color": "#4ab2ea",
  "font_title": "ivy-mode"
}
```

**Field notes:**

- **`duration_interval` replaced `end_at`.** It is an ISO-8601 duration — `"PT1H"`, `"PT90M"`, `"P1D"`. You no longer send an end time; Luma derives it and still returns `end_at` when you read the event back.
- **`start_at`** is ISO-8601 UTC with milliseconds (`2026-09-10T01:00:00.000Z`).
- **`calendar_api_id`** picks the target calendar. Get your own from `/user` → `personal_calendar_api_id`. This is now honoured on create (it used to be silently dropped).
- **`visibility`** is `"public"` or `"private"`.
- **`description_mirror`** is accepted on create — see the ProseMirror section below.
- **`geo_address_json`** takes a Google Places result. `place_id` alone may not be enough; the web app sends the full resolved address block shown above. Plain address strings are rejected with `"That doesn't look like a valid address"`.
- **`ticket_types`** — the free-ticket object above is what the web app sends for a no-cost event.
- **`cover_url` is required and must be a non-null string.** Passing `null` fails with the same undifferentiated 400 — this is an easy one to lose an afternoon to, since a cover image feels optional. Luma's own gallery images live at `https://images.lumacdn.com/gallery-images/<xx>/<uuid>`; the value in the template is a known-good default you can reuse if the user has no artwork of their own.

**Editing an existing event:** `POST https://api.luma.com/event/admin/update` with `event_api_id` plus the fields to change. Do **not** POST to `/event/update` — it redirects.

### Event Descriptions — `description_mirror` (ProseMirror)

Luma stores rich descriptions in the `description_mirror` field using **ProseMirror / TipTap JSON document format**. The plain `description` string field is effectively write-nothing / read-null: setting it on create or update has no visible effect, and it always returns `null` when you fetch the event. Always write rich content to `description_mirror` — on `/event/create` directly, or via `/event/admin/update` when editing an existing event.

**Structure:** a `doc` with a `content` array of block nodes (paragraphs, headings, lists). Each paragraph has its own `content` array of text nodes. Links are applied as `marks` on text nodes.

```json
{
  "type": "doc",
  "content": [
    { "type": "paragraph", "content": [{ "type": "text", "text": "First paragraph." }] },
    { "type": "paragraph", "content": [] },
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Register here: " },
        {
          "type": "text",
          "text": "https://luma.com/abc",
          "marks": [{ "type": "link", "attrs": { "href": "https://luma.com/abc", "target": "_blank" } }]
        }
      ]
    }
  ]
}
```

An **empty paragraph** (`{"type": "paragraph", "content": []}`) is how you insert a blank line between blocks — putting `\n\n` inside a text node does not render as a blank line.

**Reading descriptions back:** on the `GET /event/get?event_api_id=...` response, `description_mirror` sits at the **root** of the response object, not nested under `event`. The nested `event.description` (plain-text) field is always `null`.

## Response Formatting

When showing events to the user, format them clearly:

**Event listing:**
```
- **Event Name** — Apr 1, 6:00 PM PDT
  Location: Venue Name, City
  URL: https://luma.com/SLUG
  Guests: 25 registered
```

Render the time in the **event's** timezone and label it, so a listing that spans cities stays unambiguous.

**Guest list:**
```
- **Name** (@twitter) — Company
```

## Notes

- Session cookies expire; if you get auth errors, the user needs to refresh the cookie
- A bare `400 {"message":"Invalid request.","code":null}` on create means either a bad payload or the retired `api.lu.ma` host — the error text is identical for both, so rule out the host first
- Rate limit: don't spam requests; batch where possible
- Event times are UTC on the wire; always convert before display — see [Timezones](#timezones) for which timezone to convert *to*
- Pagination: use `pagination_limit` and `next_cursor` / `after` params
- The `url` endpoint is versatile — use it to resolve event slugs, city names, calendar slugs, and usernames
