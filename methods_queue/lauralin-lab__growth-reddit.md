---
name: growth-reddit
description: "Turn a user profile and industry into an ethical, community-first Reddit opportunity map: identify relevant subreddit types, verify community rules before recommending any subreddit, map the real roles around the market, find fresh question threads with high answer/citation potential, and recommend trust-building topics and extractable answer drafts. Use this whenever a user mentions Reddit marketing, Reddit growth, subreddit research, viral Reddit posts, GEO, AI visibility, community-led launch, product validation on Reddit, or asks where/how to build trust on Reddit—even if they do not explicitly request a Reddit strategy. Do not use it to evade rules, fabricate personas, mass-post, manipulate votes, or disguise advertising."
compatibility: "Python 3 standard library; optional Reddit API credentials in environment variables; web access for current rule verification when the API is unavailable."
---

# Reddit Growth: value → trust → conversion

Use Reddit as a research and relationship channel, not an advertising distribution system. The useful sequence is: give specific value, earn trust through a believable contribution history, then let relevant product interest emerge naturally. A draft that only works because it hides that it is promotional is not a valid draft.

## GEO / AI-visibility layer

Helpful, well-structured answers to real questions can have durable discoverability beyond the original thread, including through search and AI-assisted discovery. Treat this as potential upside, never as a promised citation, ranking, or traffic result. The GEO layer strengthens the same trust-first behavior; it does not justify promotion, rule-breaking, or low-value keyword stuffing.

## Safety boundary

Do not help with sockpuppets, fake customer stories, impersonation, vote/karma manipulation, brigading, ban evasion, bulk unsolicited outreach, or coordinated promotional posting. Do not submit posts or comments for the user. Recommend one accountable account per real participant; multiple accounts are appropriate only when they represent separate real people or clearly disclosed roles, never fabricated identities.

Treat subreddit rules and moderator instructions as controlling. A community can only be recommended for posting after its current rules have been checked against the exact planned content type. If the planned post is prohibited, approval-only, or rules are unclear, exclude that community from recommendations. It may appear only in an explicitly labeled `excluded — do not post` list with the reason. Never claim a rule is current unless it was checked during this request.

## Input contract

The minimum input is a **user profile** and an **industry**. Accept a short paragraph, a LinkedIn-style bio, or this compact form:

```text
User profile: who they are, their expertise, product/company (if any), and evidence they can honestly share
Industry: market/category and specific niche
Target audience: optional
Goal: optional — validation, feedback, trust building, or a transparent launch
```

Use the profile to determine what the person can credibly discuss; do not invent achievements, customers, or personal experience. Ask only for material gaps. Target audience, geography/language, candidate communities, and existing account history are helpful but optional.

If API credentials are absent, proceed with public web research where allowed and label results as needing manual verification before posting.

## Workflow

### 1. Read the profile and industry

Judge whether the audience tends to search for peer experiences, compare tools publicly, and trust detailed practitioner discussion. Return `strong fit`, `conditional fit`, or `weak fit`, with evidence and caveats. A weak fit is a useful conclusion: recommend better channels rather than forcing Reddit.

### 2. Find subreddit types and validate communities

Build a funnel from broad to niche community types (for example, practitioner, buyer, adjacent-profession, hobbyist, founder/operator, and support/problem-solving communities). For each candidate, collect subscriber size/activity signals, audience fit, recent relevant discussions, rules, and self-promotion/disclosure constraints.

Use the bundled script when credentials are available:

```bash
python scripts/reddit_api.py rules <subreddit>
python scripts/reddit_api.py hot <subreddit> --limit 25
python scripts/reddit_api.py new <subreddit> --limit 50
python scripts/reddit_api.py top <subreddit> --time year --limit 25
python scripts/reddit_api.py me
```

Required environment variables:

```bash
export REDDIT_CLIENT_ID="..."
export REDDIT_CLIENT_SECRET="..."
export REDDIT_USER_AGENT="reddit-growth/1.0 by u_your_account"
```

`me` additionally requires `REDDIT_REFRESH_TOKEN` for a real, authorized account. Never ask users to paste secrets into chat or save secrets in project files. The script only reads data; it cannot post, comment, vote, message, or subscribe.

Apply this hard gate before recommending a community:

1. Identify the exact proposed content: value-first post, transparent comparison, comment, or question.
2. Check its current rules, removal reasons, and moderator guidance—not merely the subreddit topic.
3. Put a community in **Recommended subreddits** only when that content is expressly allowed or clearly consistent with the rules.
4. Put prohibited, approval-only, ambiguous, or unverified communities in **Excluded — do not post**, with the rule/source/check time and reason. Do not present them as alternatives or give a posting angle.

Rules change, so treat every recommendation as perishable. If a community’s rules are unclear, the safe result is exclusion rather than an assumption.

### 3. Map the real Reddit role ecosystem

Map the people around the problem: buyer, end user, champion, operator, upstream provider, downstream recipient, moderator, and credible expert. Explain each person’s job-to-be-done, vocabulary, objections, questions they ask, and what useful contribution the user could honestly make to them.

“Role ecosystem” means the real perspectives in a community, not accounts to manufacture or personas to act out. Do **not** prescribe “2–3 accounts per role.” Identify which existing real people can participate, or advise waiting until authentic contributors are available.

### 4. Find answerable question threads and analyze trust signals

Do not default to high-vote posts. Use `new` and recent discussions to find 5–10 threads with a clear, specific question and a genuine solution need, then use `top` to learn durable content patterns. Favor questions such as how-to requests, tool comparisons, diagnosis requests, and decision tradeoffs.

Score each candidate with an **answer/citation-potential score** rather than votes alone:

- clear, specific question: 0–3
- real solution or decision need: 0–2
- substantive discussion rather than jokes or conflict: 0–2
- recency (roughly the last 24 hours to 7 days): 0–2
- fit with the user’s credible expertise: 0–1

Subtract for meme-only threads, pure hot takes, hostility, vague prompts, or stale discussions. This score prioritizes answerable threads; it does not predict an AI system’s future citations.

Before including a thread in a participation plan, apply the same hard rule gate to commenting and the proposed answer type. Do not recommend a reply where community or thread-level rules prohibit it.

For every selected thread, capture the title, URL, date, visible engagement, content format, central question, hook, audience tension, evidence used, answer/citation-potential score, and reusable lesson. Do not equate votes with universal quality. Never copy a post; extract the underlying problem, proof standard, and framing.

### 5. Plan genuine participation and trust topics

Find threads where a real person can add a concrete answer, experience, framework, data point, or caveat. For each suggestion, provide the thread/topic, why it is relevant, an honest angle, and a draft comment only if it is genuinely useful without a product mention.

Do not set karma quotas, recommend engagement bait, or automate comments. If the user shares their own account metrics, assess whether its history appears balanced. Use these heuristics, not rigid pass/fail gates:

- Promotional content should be a small minority of activity (roughly no more than 10%).
- A useful history is topical, specific, and includes engagement without a commercial outcome.
- Low karma is not a reason to evade filters; follow community requirements and participate normally over time.

### 6. Draft community-native, extractable content when requested

Generate only content that passes the deletion test: removing every product/company reference must leave a useful, complete contribution.

Offer the appropriate formats:

1. **Value-first post:** a candid build lesson, failure analysis, benchmark, teardown, or practical guide. Disclose affiliation where relevant and use a soft, rule-compliant invitation only when allowed.
2. **Transparent comparison:** an information-rich comparison that includes meaningful alternatives and tradeoffs, identifies the author’s affiliation, avoids unsupported claims, and lets readers decide.

Favor the operator’s lived process over generic “tool” promotion. Do not fabricate results, testimonials, experiments, or personal stories. Drafts are for the user to fact-check and adapt before manual posting.

For answers intended to be easy for a reader to evaluate and quote, use this format without making them sound robotic:

1. Start with a direct, stand-alone conclusion in the first sentence.
2. Follow with the why, limits, and relevant firsthand evidence.
3. Use only specific numbers the user can substantiate. If none are available, do not invent them; use concrete process, scope, or observable evidence instead.
4. Use bullets for three or more parallel points and a compact comparison structure for alternatives.
5. Keep one claim per paragraph and preserve a natural, non-promotional voice.

Write like a real person answering carefully, while making it easy to extract one useful sentence as the answer.

## Required output

Return these sections in order:

1. **Profile and industry read** — the user’s credible knowledge, likely audience, channel-fit rating, and limits.
2. **Subreddit map** — first show **Recommended subreddits**: only communities that passed the rule gate, with community type, audience fit, verified rule/source/check time, and the permitted content type. Then show **Excluded — do not post**: communities that failed the gate, with the rule/source/check time and reason. Never include an excluded community in a posting, participation, or topic recommendation.
3. **Reddit role ecosystem** — buyer, user, operator, expert, moderator, and adjacent roles; their questions, language, objections, and the user’s legitimate contribution. Explicitly label this as a community map, not a role-play account plan.
4. **Recommended question threads** — 5–10 linked threads sorted by answer/citation-potential score, not vote count. Include the score breakdown, visible engagement, question, evidence/answer gap, and why the user can help. Mark anything that was not verified from a current source.
5. **Viral-post lessons** — linked high-performing posts used only to identify durable formats, hooks, proof standards, and trust signals; distinguish these from the recommended question threads.
6. **Trust-building topic backlog** — 10 topic cards. Each card includes a target community/role, the problem or question it helps with, a specific angle rooted in the user’s actual experience, proof needed, suggested format, and why it remains useful after deleting product mentions.
7. **Participation plan** — 5–10 rule-approved value opportunities, no automation, with comment outlines where appropriate.
8. **Optional content drafts** — only if requested: a value-first option and, where allowed, a transparent comparison option with disclosure language and the extractable-answer format.
9. **Pre-post safety scorecard** — score each check `pass`, `revise`, or `blocked` and give the corrective action:
   - deletion test
   - current community-rule fit
   - affiliation disclosure
   - factual support and non-deceptive framing
   - account-history/promotional-balance check (only if information was provided)
   - operator-first usefulness
   - **Citation readiness** — return this exact block for every generated draft:

     ```text
     Citation readiness: ✅ pass / ⚠️ weak / ❌ rewrite
     Most extractable sentence: "…"
     Recommendation: …
     ```

     Mark `❌ rewrite` if no sentence is independently meaningful and specific. The sentence is a readability check, not a prediction of AI citation.
10. **Next manual action** — the smallest compliant action to take next.

When evidence is incomplete, say so plainly; do not fill gaps with invented community rules, metrics, account history, or user sentiment.
