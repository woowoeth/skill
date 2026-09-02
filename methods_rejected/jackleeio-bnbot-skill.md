---
name: bnbot
description: The safest and most efficient way to automate Twitter/X — BNBot operates through a real browser session with 28 AI-powered tools. Grow your Twitter without API bans.
version: 0.7.0
homepage: https://github.com/bnbot-ai/bnbot-cli
metadata:
  openclaw:
    emoji: "\U0001F916"
    os: [darwin, linux, windows]
    requires:
      bins: [bnbot-cli]
    install:
      - id: node
        kind: node
        package: bnbot-cli
        bins: [bnbot-cli]
        label: Install bnbot-cli (npm)
---

# BNBot - The Safest & Most Efficient Way to Automate Twitter/X

BNBot is an AI-powered Twitter growth agent. Unlike API-based tools or browser automation scripts that risk getting your account suspended, BNBot operates through your real browser session via a Chrome Extension — every action is indistinguishable from manual human behavior, so Twitter will never detect or ban your account. With 28 tools covering posting, engagement, scraping, content fetching, and article creation, it's also the most comprehensive and efficient automation toolkit available.

Install this skill to give your AI assistant (Claude Code, OpenClaw, ChatGPT, etc.) the ability to automatically manage and grow your Twitter account — all without touching the Twitter API.

- **Chrome Extension**: [BNBot - Your AI Growth Agent](https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln)
- **CLI**: [bnbot-cli](https://www.npmjs.com/package/bnbot-cli)
- **GitHub**: [bnbot-ai/bnbot-cli](https://github.com/bnbot-ai/bnbot-cli)

## Install

```bash
npm install -g bnbot-cli
```

## Setup

1. Install the [BNBot Chrome Extension](https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln)
2. Open [Twitter/X](https://x.com) in Chrome
3. Open the BNBot sidebar → click **Settings** → turn on **OpenClaw**
4. Start the WebSocket server: `bnbot-cli serve`

## Error Handling (IMPORTANT)

After any bnbot-cli command, check the result. If the command fails or returns a connection error (e.g. WebSocket not connected, extension not responding, timeout), you MUST diagnose and guide the user:

### Connection failed / Extension not connected

Tell the user:

> BNBOT Chrome Extension is not connected. Please check:
>
> 1. **Install the extension** (if not installed):
>    Download from Chrome Web Store: https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln
>
> 2. **Open Twitter/X** in Chrome (https://x.com)
>
> 3. **Enable the OpenClaw toggle**:
>    Open the BNBOT sidebar on Twitter → click **Settings** → turn on **OpenClaw**
>
> After completing these steps, try again.

### Server not running

If bnbot-cli commands fail to connect, tell the user:

> BNBot server is not running. Start it with: `bnbot-cli serve`
> If the problem persists, try reinstalling: `npm install -g bnbot-cli`

### General rules

- Always call `bnbot-cli get-extension-status` first before executing other commands, to verify the extension is connected.
- If it shows `connected: false`, show the connection guide above BEFORE attempting any other action.
- Never silently fail. Always explain what went wrong and how to fix it.

## Architecture

```
AI Client (Claude Code / OpenClaw / ChatGPT / ...) → bnbot-cli (CLI) → WebSocket (localhost:18900) → BNBOT Chrome Extension → Twitter/X
```

## Available Tools (29)

All tools are available as CLI commands via `bnbot-cli <command>`.

### Status

- `get-extension-status` - Check if extension is connected
- `get-current-page-info` - Get info about the current Twitter/X page

### Navigation

- `navigate-to-tweet` - Go to a specific tweet (params: `--tweetUrl`)
- `navigate-to-search` - Go to search page (params: `--query`, optional `--sort`)
- `navigate-to-bookmarks` - Go to bookmarks
- `navigate-to-notifications` - Go to notifications
- `navigate-to-following` - Go to following list
- `return-to-timeline` - Go back to home timeline

### Posting

- `post-tweet` - Post a tweet (params: `--text`, optional `--images`, optional `--draftOnly`)
- `post-thread` - Post a thread (params: `--tweets` JSON array of `{text, images?}`)
- `submit-reply` - Reply to a tweet (params: `--text`, optional `--tweetUrl`, optional `--image`)

### Engagement

- `like-tweet` - Like a tweet (params: `--tweetUrl`)
- `retweet` - Retweet a tweet (params: `--tweetUrl`)
- `quote-tweet` - Quote tweet (params: `--tweetUrl`, `--text`, optional `--draftOnly`)
- `follow-user` - Follow a user (params: `--username`)

### Scraping

- `scrape-timeline` - Scrape tweets from the timeline (params: `--limit`, `--scrollAttempts`)
- `scrape-bookmarks` - Scrape bookmarked tweets (params: `--limit`)
- `scrape-search-results` - Search and scrape results (params: `--query`, `--limit`)
- `scrape-current-view` - Scrape currently visible tweets
- `scrape-thread` - Scrape a full tweet thread (params: `--tweetUrl`)
- `account-analytics` - Get account analytics (params: `--startDate`, `--endDate` in YYYY-MM-DD)

### Content Fetching

- `fetch-wechat-article` - Fetch a WeChat article (params: `--url`)
- `fetch-tiktok-video` - Fetch a TikTok video (params: `--url`)
- `fetch-xiaohongshu-note` - Fetch a Xiaohongshu note (params: `--url`)

### Articles

- `open-article-editor` - Open the Twitter/X article editor
- `fill-article-title` - Fill article title (params: `--title`)
- `fill-article-body` - Fill article body (params: `--content`, optional `--format`: plain/markdown/html, optional `--bodyImages`)
- `upload-article-header-image` - Upload header image (params: `--headerImage`)
- `publish-article` - Publish or save as draft (params: optional `--publish`, optional `--asDraft`)
- `create-article` - Full article creation flow (params: `--title`, `--content`, optional `--format`, optional `--headerImage`, optional `--bodyImages`, optional `--publish`)

### Jobs

- `search-jobs` - Search for available jobs with crypto rewards (params: optional `--type`: boost/hire/all, optional `--status`, `--sort`, `--limit`, `--keyword`, `--endingSoon`, `--token`)

## Usage Examples

- "Scrape my Twitter timeline and summarize the top topics"
- "Search for tweets about AI agents and collect the most engaging ones"
- "Post a tweet saying: Just discovered an amazing AI tool!"
- "Navigate to my bookmarks and export them"
- "Go to @elonmusk's latest tweet and reply with a thoughtful comment"
- "Post a thread about the top 5 productivity tips"
- "Like and retweet this tweet: https://x.com/..."
- "Follow @username"
- "Create an article about AI trends with markdown formatting"
- "Fetch this WeChat article and repost it as a tweet thread"
