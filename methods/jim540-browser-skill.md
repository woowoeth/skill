---
name: browser
description: |
  Drive a real browser for any web task: read pages, click, fill forms, screenshot, log in,
  sign up. Default is "live" mode, the user's own running browser with their logins, driven in
  the BACKGROUND, so it never steals focus and many sessions run in parallel without fighting.
  Each session owns a group of tabs it can open, switch between and juggle.
  Also "headless" (invisible Chrome, fast bulk work) and "incognito" (a visible window, logged
  out, the "show me" mode).
allowed-tools:
  - Bash
  - Read
---

# browser

`ab` is the wrapper. **Call it by its full path, one command per Bash call**, never as a `$AB`
variable and never chained with `;` or `&&`: permission rules match on the literal command
prefix, so `AB=...; $AB click @e5` matches nothing and gets stopped by the auto-mode classifier
mid-task. The allow rule is `Bash(~/.claude/skills/browser/ab:*)` in `~/.claude/settings.json`.

Three modes, picked from the request.

| Say | Mode | What runs |
|---|---|---|
| default; "my browser", "logged in as me" | `live` | the user's running browser, their profile and logins, driven in the background |
| "headless", "fast", bulk scraping/QA over many pages | `headless` | Chrome for Testing, no window |
| "show me", "watch it", "incognito", "as a new visitor" | `incognito` | a visible window, throwaway profile |

```bash
~/.claude/skills/browser/ab start live https://example.com   # background tab in the user's browser
~/.claude/skills/browser/ab snapshot                         # interactive elements as @e1, @e2...
~/.claude/skills/browser/ab click @e5
~/.claude/skills/browser/ab fill @e3 "you@example.com"
~/.claude/skills/browser/ab screenshot /tmp/shot.png         # then Read the file
~/.claude/skills/browser/ab tab new https://example.com/pricing   # a second tab, same session
~/.claude/skills/browser/ab in t1 text                       # read t1 without leaving t2
~/.claude/skills/browser/ab stop                             # closes every tab this session opened
```

## Live mode is background, and that's the whole point

Live is driven over CDP by `cdp.js`, operating this session's own tabs **by id, without ever
making one the foreground**. Consequences:

- **It never steals focus.** The user stays in their editor; the browser never jumps in front.
  Verified across start, read, navigate, click, fill, screenshot.
- **Truly parallel.** Run as many live sessions as you like, each owns its own group of tabs
  and can't see or disturb the others: `ab in t3 ...` in one session refuses to touch another
  session's t3, and `ab stop` closes only what that session opened. Two sessions clicking
  through different pages at once don't fight. State is keyed by `CLAUDE_CODE_SESSION_ID`
  (override with `AB_INSTANCE`).
- **There is no debug port.** The browser runs with `--remote-debugging-pipe` and CDP travels
  over a pipe held by a broker (`abd.mjs`, node), which re-exposes it on `~/.agent-browser/cdp.sock`
  (mode 600) behind a token in `.cdp-token` (mode 600). Nothing listens, so no other local process
  can drive the logged-in browser. `ab start live` starts the broker if it isn't up. The broker
  must launch the browser to own the pipe, so if the browser was started some other way (the Dock,
  a link from another app, it being the default browser) there is no pipe. Then `ab relaunch` quits
  it and brings it straight back on the pipe, in one step. Needs `bun` (driver) and `node` (broker).
- Background tabs are render-throttled by Chromium, so `ab` turns focus emulation on for the
  duration of each command and **off again before disconnecting**. Leaving it on costs ~0.14 cores
  per idle tab; released, an agent tab costs the same as any background tab.

Live commands (this is the full set; anything else: use `eval`, or ask):

```
open <url>   url   title   text   html   snapshot   click @ref   fill @ref <text>
screenshot [path]   eval <js>   back   forward   reload   wait <sel|ms>
tab [new|close|t2]   in t2 <command>          # the tab group, next section
```

`start`, `open` and `tab new` return once the page has actually loaded, so the next `title`,
`text` or `snapshot` reads a real page: no manual pause needed. `wait <css>` is for content that
arrives later (it fails loudly on an invalid selector), `wait <ms>` for a blunt pause.

`snapshot` returns only interactive elements, each labelled `@e1`… Refs come from the last
snapshot; after a navigation or DOM change, snapshot again before clicking. To read the page
prose use `text`; to see how it renders use `screenshot` then Read the file.

## A group of tabs, all yours

One session can open several tabs and work them in any order. They're labelled `t1`, `t2`… per
session, so two sessions each have their own `t1`.

```
ab tab                  list this session's tabs (* marks the current one, with live URL + title)
ab tab new [url]        open another background tab and make it current
ab tab t2               make t2 current (still no window comes forward)
ab tab close [t2]       close one tab; default is the current one
ab in t2 <command>      run a single command against t2 without switching
```

Everything else runs against the current tab. Use `ab in` for a quick read elsewhere
(`ab in t1 title`), and `ab tab t1` when you're about to do several things there. Refs are
per-tab: `@e5` in t2 means whatever t2's own last `snapshot` labelled, so snapshot the tab you're
about to click in. Comparing pages, keeping a doc open while filling a form on another site, or
running a search in one tab and opening results in others all work; the cap is 10 tabs a session
(`AB_MAX_TABS`), which is about restraint in a real browser, not a technical limit.

## The user can see which tabs are yours

Every live tab is marked, so they know not to touch it. In the **tab strip** (visible without
opening the tab) the title gets a `● <TAG> ` prefix and the favicon becomes a coloured dot with the
tag in it. **Inside the page**: a coloured frame around the viewport, a pill in the bottom-right
reading `Claude <TAG> · <status>` (reading, clicking, typing, idle…), and a cursor dot that moves to
an element just before a click, so a click is visible if they're watching.

Tag and colour come from the session, so two sessions look different. Set `AB_TAG=RESEARCH` for
something meaningful, `AB_COLOR=#ff6b35` to force a colour, `AB_BADGE=0` to turn it off entirely.

The overlay lives in a shadow root, so it never appears in `snapshot`, `text` or `html`, never
affects layout, and it's hidden automatically during `screenshot`. It does write to `document.title`
and swap the favicon on a real page, which is reversible:

```
ab tab release [t2]     hand the tab back: marker off, tab stays open, leaves the group
```

Use that when the user asks to keep a page you opened, instead of `ab tab close`.

## Look at the page when looks matter

`snapshot`/`text` tell you what's on the page, not how it renders. When the decision depends on
appearance (does it look right, is anything overlapping or cut off, did the layout hold), take a
`screenshot` and Read it. The screenshot is captured from the background tab, so it costs no
focus either.

## Logins and signups: do them

Fill the form, click "Sign in with Google", finish the flow. One confirmation before the click
that creates an account or commits the user to something ("this creates an account at X via
Google, go?"), then run it end to end. In live mode they're already signed into most sites, so
this usually just works. Ask only for what only they have: a 2FA code, a CAPTCHA, a passkey or
Touch ID, or a password (have them type it in a visible window, or read it from their password
manager's CLI; never put a password in the chat). To a page, live mode is an ordinary browser:
real profile, real cookies, `navigator.webdriver` false, so it isn't seen as a bot. Keep volume
and pacing human on sites that rate-limit (LinkedIn, Google) and ask before anything that looks
like bulk automation on real accounts.

## headless and incognito

These run on `agent-browser` (they don't have the focus problem: headless has no window,
incognito is a separate window the user is watching on purpose). Same command surface as
agent-browser (`snapshot -i`, `find role button click --name Submit`, `console`, `network
requests`, `vitals`, `tab`, `back`, `eval`). Incognito is logged into nothing, every time. If a
task needs a login, it belongs in `live`. `ab dashboard` opens agent-browser's viewer on :4848
for those modes.

## Gotchas

- **Tabs the user closes.** The group is re-checked before every command, so a tab they closed
  just drops out of the list. If it was the current one, `ab` switches to another of ours and says
  so; if they closed them all (or the browser restarted), the next command says to run
  `ab start live` again rather than driving something random.
- **Never touch a tab we didn't open.** Only tabs in this session's group are ours. The user's own
  tabs, and other sessions' tabs, are off limits.
- **No visual grouping in the tab strip.** The group is `ab`'s bookkeeping; the browser shows our
  tabs as ordinary tabs mixed in with the user's. CDP has no tab-group commands, and a window per
  session can't hold more than one tab without stealing focus, so this is a real limit, not a
  to-do.
- **Chromium 136+ and the default profile.** Chrome refuses the remote-debugging switches when the
  default user data directory is in use, which is why the default browser here is Comet (it does
  not enforce that) and why pointing `AB_BROWSER` at Chrome needs `AB_USER_DATA_DIR` and a
  logged-out profile. See "Using a different browser".
- **The port fallback.** If a browser is already up serving a debug port, the broker attaches to
  that instead of launching its own; that's a transition path, not the normal one, and it's off
  whenever `AB_BROWSER`, `AB_USER_DATA_DIR` or `AB_NO_PORT=1` is set. Normal operation opens no
  TCP port at all.

## Using a different browser

`cdp.js` speaks plain CDP, so any Chromium works. `AB_BROWSER` picks the binary the broker
launches:

```bash
AB_BROWSER="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
AB_USER_DATA_DIR="$HOME/.agent-browser/profiles/chrome" ab start live https://example.com
```

The catch is the profile, not the protocol. Chrome, Brave and Edge on 136+ refuse remote
debugging against the default user data directory, so a separate `AB_USER_DATA_DIR` is required,
and that profile starts logged out, which is the point of live mode gone. Comet 152 does not
enforce the restriction, so it can attach to the real, logged-in profile. That's the only reason
it's the default. `incognito` mode hardcodes the Comet path in `ab` (`COMET_APP`), which is a
one-line edit since it uses a throwaway profile anyway.
