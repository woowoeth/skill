---
name: listful-personal-home
description: Read a user's local Google Chrome bookmarks and browsing history, infer recurring browser-based workflows, and generate a validated listful.content-bundle.v1 JSON file for a personalized Listful Home. Use when the user asks to analyze Chrome activity, organize bookmarks or history into Listful collections and lists, or create a personal new-tab launchpad. Run only in a local environment with explicit authorization to read the selected Chrome profile; never use in a cloud task or modify Chrome's Bookmarks, History, or extension storage files.
---

# Listful Personal Home

Create a private, importable Listful Home from one local Google Chrome profile. Use this open Agent Skills workflow with a compatible local Agent such as Codex or Claude Code. Extract browser data deterministically, curate it with the agent, validate the result, and leave the final write to Listful's existing import flow.

## Workflow

1. Confirm that the task is running locally. Stop if the task is cloud-hosted or cannot access the user's Chrome profile.
2. Treat an explicit request to analyze bookmarks and history as authorization for this run. Otherwise, tell the user that selected bookmark titles, URLs, folder paths, and recent history will be processed in the current local Agent task, then ask for confirmation before reading them.
3. Locate this skill directory and run:

   ```bash
   python3 scripts/extract_chrome_activity.py --list-profiles
   ```

4. If more than one profile is available, ask the user which profile to use. Do not infer identity from profile contents.
5. Create a dedicated system temporary directory. Extract 90 days of activity unless the user requested another window:

   ```bash
   python3 scripts/extract_chrome_activity.py \
     --profile "Default" \
     --history-days 90 \
     --output "/absolute/private/temp/listful-chrome-activity.json"
   ```

   The script reads Chrome data only. Do not add `--include-query` or `--include-local` unless the user explicitly requests those more sensitive inputs.
6. Inspect the extracted JSON without dumping the complete dataset into user-facing messages. Do not visit any extracted URL or fetch external metadata unless the user separately authorizes network access.
7. Infer recurring workflows using bookmark placement as strong intent and recent visit frequency as supporting evidence. Prefer durable tools, references, libraries, generators, inspectors, converters, and asset sources. Exclude login, authentication, checkout, account-management, transient search-result, and one-off article pages.
8. Read [references/listful-bundle.md](references/listful-bundle.md) before composing the output. Generate an additive bundle with an empty top-level `lists` array and personalized wrappers in `collections`.
9. Write the bundle to a new `.json` file, preferably in the user's Downloads directory. Never overwrite an existing file.
10. Validate it:

    ```bash
    python3 scripts/validate_listful_bundle.py "/absolute/path/listful-personal-home-YYYY-MM-DD.json"
    ```

11. Remove only the dedicated temporary directory created in step 5, then tell the user the raw activity export was removed. Keep the validated bundle.
12. Return the exact bundle path and instruct the user to open Listful, choose **Customize → Import from JSON**, and select the file. Do not directly edit Chrome's LevelDB files or Listful's `chrome.storage.local` backing files. Use Chrome UI control only when the user explicitly asks for import automation and the user's actual Chrome control tool is available.

## Curation rules

- Create 2–6 collections when the evidence supports them; use fewer rather than inventing weak themes.
- Create 2–8 lists per collection and 4–10 items per list. A Listful list must never exceed 10 items.
- Organize around repeated workflows rather than generic professional labels.
- Prefer a URL once across the entire bundle unless it genuinely serves two distinct workflows.
- Give every collection, list, and item a concise authored title or description in the user's language.
- Write each item recommendation specifically for that site: roughly 4–8 English words or 10–15 Simplified Chinese characters.
- Use only HTTP(S) URLs produced by the extractor. Do not invent URLs.
- Preserve source evidence in working notes, but do not include browsing counts, folder paths, or provenance fields in the portable bundle.

## Failure behavior

- Fail visibly when Chrome is missing, a selected profile is ambiguous or absent, Bookmarks or History cannot be read, the SQLite schema is unsupported, or the output is invalid.
- Never silently switch profiles, shorten the requested history window, substitute another Chromium browser, or fall back from combined bookmarks and history to a single source.
- If permissions block access, report the exact profile path that needs read access. Do not request write access to the Chrome profile.
