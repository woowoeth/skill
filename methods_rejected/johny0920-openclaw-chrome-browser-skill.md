---
name: browser-use
description: Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, or extract information from web pages.
allowed-tools: Bash(browser-use:*)
---

# Browser Automation with browser-use CLI

> **Search Trigger:** When the user asks to "search" for information and the information cannot be provided from model knowledge, **automatically use `web_fetch`** to retrieve current results from search engines or websites. Prefer `web_fetch` over browser automation for simple information retrieval tasks.

## Quick Search Workflow

For search queries, use this pattern:

```bash
# DuckDuckGo HTML (works without JS)
web_fetch "https://duckduckgo.com/html/?q=YOUR+QUERY"

# Or direct site search
web_fetch "https://example.com/search?q=term"
```

Only use browser automation (`browser-use` or `browser` tool) when:
- The site requires JavaScript/interaction
- You need to fill forms or click elements
- You need screenshots or visual verification
- The page requires authentication

---

The `browser-use` command provides fast, persistent browser automation. It maintains browser sessions across commands, enabling complex multi-step workflows.

## Prerequisites

Before using this skill, `browser-use` must be installed and configured. Run diagnostics to verify:

```bash
browser-use doctor
```

For installation instructions, see https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md

## Core Workflow

1. **Navigate**: `browser-use open <url>` - Opens URL (starts browser if needed)
2. **Inspect**: `browser-use state` - Returns clickable elements with indices
3. **Interact**: Use indices from state to interact (`browser-use click 5`, `browser-use input 3 "text"`)
4. **Verify**: `browser-use state` or `browser-use screenshot` to confirm actions
5. **Repeat**: Browser stays open between commands

## Browser Modes

```bash
browser-use --browser chromium open <url> # Default: headless Chromium
browser-use --browser chromium --headed open <url> # Visible Chromium window
browser-use --browser real open <url> # Real Chrome (no profile = fresh)
browser-use --browser real --profile "Default" open <url> # Real Chrome with your login sessions
browser-use --browser remote open <url> # Cloud browser
```

- **chromium**: Fast, isolated, headless by default
- **real**: Uses a real Chrome binary. Without `--profile`, uses a persistent but empty CLI profile at `~/.config/browseruse/profiles/cli/`. With `--profile "ProfileName"`, copies your actual Chrome profile (cookies, logins, extensions)
- **remote**: Cloud-hosted browser with proxy support

## Essential Commands

```bash
# Navigation
browser-use open <url> # Navigate to URL
browser-use back # Go back
browser-use scroll down # Scroll down (--amount N for pixels)

# Page State (always run state first to get element indices)
browser-use state # Get URL, title, clickable elements
browser-use screenshot # Take screenshot (base64)
browser-use screenshot path.png # Save screenshot to file

# Interactions (use indices from state)
browser-use click <index> # Click element
browser-use type "text" # Type into focused element
browser-use input <index> "text" # Click element, then type
browser-use keys "Enter" # Send keyboard keys
browser-use select <index> "option" # Select dropdown option

# Data Extraction
browser-use eval "document.title" # Execute JavaScript
browser-use get text <index> # Get element text
browser-use get html --selector "h1" # Get scoped HTML

# Wait
browser-use wait selector "h1" # Wait for element
browser-use wait text "Success" # Wait for text

# Session
browser-use sessions # List active sessions
browser-use close # Close current session
browser-use close --all # Close all sessions

# AI Agent
browser-use -b remote run "task" # Run agent in cloud (async by default)
browser-use task status <id> # Check cloud task progress
```

## Commands Reference

### Navigation & Tabs
```bash
browser-use open <url> # Navigate to URL
browser-use back # Go back in history
browser-use scroll down # Scroll down
browser-use scroll up # Scroll up
browser-use scroll down --amount 1000 # Scroll by specific pixels (default: 500)
browser-use switch <tab> # Switch to tab by index
browser-use close-tab # Close current tab
browser-use close-tab <tab> # Close specific tab
```

### Page State
```bash
browser-use state # Get URL, title, and clickable elements
browser-use screenshot # Take screenshot (outputs base64)
browser-use screenshot path.png # Save screenshot to file
browser-use screenshot --full path.png # Full page screenshot
```

### Interactions
```bash
browser-use click <index> # Click element
browser-use type "text" # Type text into focused element
browser-use input <index> "text" # Click element, then type text
browser-use keys "Enter" # Send keyboard keys
browser-use keys "Control+a" # Send key combination
browser-use select <index> "option" # Select dropdown option
browser-use hover <index> # Hover over element (triggers CSS :hover)
browser-use dblclick <index> # Double-click element
browser-use rightclick <index> # Right-click element (context menu)
```

Use indices from `browser-use state`.

### JavaScript & Data
```bash
browser-use eval "document.title" # Execute JavaScript, return result
browser-use get title # Get page title
browser-use get html # Get full page HTML
browser-use get html --selector "h1" # Get HTML of specific element
browser-use get text <index> # Get text content of element
browser-use get value <index> # Get value of input/textarea
browser-use get attributes <index> # Get all attributes of element
browser-use get bbox <index> # Get bounding box (x, y, width, height)
```

### Cookies
```bash
browser-use cookies get # Get all cookies
browser-use cookies get --url <url> # Get cookies for specific URL
browser-use cookies set <name> <value> # Set a cookie
browser-use cookies set name val --domain .example.com --secure --http-only
browser-use cookies set name val --same-site Strict # SameSite: Strict, Lax, or None
browser-use cookies set name val --expires 1735689600 # Expiration timestamp
browser-use cookies clear # Clear all cookies
browser-use cookies clear --url <url> # Clear cookies for specific URL
browser-use cookies export <file> # Export all cookies to JSON file
browser-use cookies export <file> --url <url> # Export cookies for specific URL
browser-use cookies import <file> # Import cookies from JSON file
```

### Wait Conditions
```bash
browser-use wait selector "h1" # Wait for element to be visible
browser-use wait selector ".loading" --state hidden # Wait for element to disappear
browser-use wait selector "#btn" --state attached # Wait for element in DOM
browser-use wait text "Success" # Wait for text to appear
browser-use wait selector "h1" --timeout 5000 # Custom timeout in ms
```

### Python Execution
```bash
browser-use python "x = 42" # Set variable
browser-use python "print(x)" # Access variable (outputs: 42)
browser-use python "print(browser.url)" # Access browser object
browser-use python --vars # Show defined variables
browser-use python --reset # Clear Python namespace
browser-use python --file script.py # Execute Python file
```

The Python session maintains state across commands. The `browser` object provides:
- `browser.url`, `browser.title`, `browser.html` — page info
- `browser.goto(url)`, `browser.back()` — navigation
- `browser.click(index)`, `browser.type(text)`, `browser.input(index, text)`, `browser.keys(keys)` — interactions
- `browser.screenshot(path)`, `browser.scroll(direction, amount)` — visual
- `browser.wait(seconds)`, `browser.extract(query)` — utilities

### Agent Tasks (Remote Mode)

```bash
# Run task in cloud browser (async by default)
browser-use -b remote run "Search for AI news and summarize top 3 articles"

# Specify LLM model
browser-use -b remote run "task" --llm gpt-4o
browser-use -b remote run "task" --llm claude-sonnet-4-20250514

# Wait for completion
browser-use -b remote run "task" --wait

# Session reuse
browser-use -b remote run "task 1" --keep-alive # Keep session alive after task
browser-use -b remote run "task 2" --session-id abc-123 # Reuse existing session

# Task management
browser-use task list # List recent tasks
browser-use task status <task-id> # Get task status
browser-use task stop <task-id> # Stop a running task
browser-use task logs <task-id> # Get task execution logs
```

### Cloud Session Management
```bash
browser-use session list # List cloud sessions
browser-use session get <session-id> # Get session details + live URL
browser-use session stop <session-id> # Stop a session
browser-use session stop --all # Stop all active sessions
browser-use session create # Create with defaults
browser-use session create --profile <id> # With cloud profile
```

### Tunnels
```bash
browser-use tunnel <port> # Start tunnel (returns URL)
browser-use tunnel list # Show active tunnels
browser-use tunnel stop <port> # Stop tunnel
browser-use tunnel stop --all # Stop all tunnels
```

### Session Management
```bash
browser-use sessions # List active sessions
browser-use close # Close current session
browser-use close --all # Close all sessions
```

### Profile Management

#### Local Chrome Profiles (`--browser real`)
```bash
browser-use -b real profile list # List local Chrome profiles
browser-use -b real profile cookies "Default" # Show cookie domains in profile
```

#### Cloud Profiles (`--browser remote`)
```bash
browser-use -b remote profile list # List cloud profiles
browser-use -b remote profile create # Create new cloud profile
browser-use -b remote profile update <id> --name "New"
browser-use -b remote profile delete <id>
```

#### Syncing
```bash
browser-use profile sync --from "Default" --domain github.com # Domain-specific
browser-use profile sync --from "Default" # Full profile
```

## Common Workflows

### Basic Web Scraping
```bash
# Navigate and extract data
browser-use open https://example.com
browser-use state
browser-use get html --selector ".product-title"
browser-use screenshot products.png
browser-use close
```

### Form Filling
```bash
# Fill a form
browser-use open https://example.com/form
browser-use state
browser-use input 3 "John Doe"      # Name field (index 3)
browser-use input 4 "john@example.com"  # Email field (index 4)
browser-use click 7                 # Submit button (index 7)
browser-use wait text "Thank you"   # Wait for confirmation
browser-use close
```

### Authenticated Browsing with Profiles
```bash
# List available profiles
browser-use -b real profile list

# Browse with your logged-in Chrome profile
browser-use --browser real --profile "Default" open https://github.com
browser-use state
browser-use screenshot
```

### Running AI Agent Tasks
```bash
# Launch parallel research tasks
browser-use -b remote run "Research competitor A pricing"
browser-use -b remote run "Research competitor B pricing"
browser-use -b remote run "Research competitor C pricing"

# Check status
browser-use task list --status finished
```

### Exposing Local Dev Servers
```bash
# 1. Start your dev server
npm run dev & # localhost:3000

# 2. Create tunnel
browser-use tunnel 3000
# → url: https://abc.trycloudflare.com

# 3. Browse via cloud browser
browser-use --browser remote open https://abc.trycloudflare.com
```

## Global Options

| Option | Description |
|--------|-------------|
| `--session NAME` | Use named session (default: "default") |
| `--browser MODE` | Browser mode: chromium, real, remote |
| `--headed` | Show browser window (chromium mode) |
| `--profile NAME` | Browser profile (local name or cloud ID) |
| `--json` | Output as JSON |

## Tips

1. **Always run `browser-use state` first** to see available elements and their indices
2. **Use `--headed` for debugging** to see what the browser is doing
3. **Sessions persist** — the browser stays open between commands
4. **Use `--json`** for programmatic parsing
5. **Python variables persist** across `browser-use python` commands within a session
6. **CLI aliases**: `bu`, `browser`, and `browseruse` all work identically to `browser-use`

## Troubleshooting

**Run diagnostics first:**
```bash
browser-use doctor
```

**Browser won't start?**
```bash
browser-use close --all # Close all sessions
browser-use --headed open <url> # Try with visible window
```

**Element not found?**
```bash
browser-use state # Check current elements
browser-use scroll down # Element might be below fold
browser-use state # Check again
```

**Session issues?**
```bash
browser-use sessions # Check active sessions
browser-use close --all # Clean slate
browser-use open <url> # Fresh start
```

## Cleanup

**Always close the browser when done:**

```bash
browser-use close # Close browser session
browser-use session stop --all # Stop cloud sessions (if any)
browser-use tunnel stop --all # Stop tunnels (if any)
```

## Alternative: Using OpenClaw Built-in Browser Tool

If `browser-use` is not installed, you can use OpenClaw's built-in `browser` tool:

```javascript
// Navigate to a page
browser({ action: "navigate", targetUrl: "https://example.com" })

// Take a screenshot
browser({ action: "screenshot", fullPage: true })

// Get page state
browser({ action: "snapshot" })

// Click an element
browser({ action: "act", request: { kind: "click", ref: "element-id" }})

// Type text
browser({ action: "act", request: { kind: "type", ref: "input-id", text: "hello" }})
```

Note: The built-in `browser` tool is good for simple tasks, but `browser-use` provides more powerful automation capabilities.
