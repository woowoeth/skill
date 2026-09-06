---
name: post
description: Take one opportunity through plan, render and delivery as a draft, quoting the cost before every charged call.
disable-model-invocation: true
argument-hint: '[what to post about]'
---

# Post something

Read `layers://skills/v1/what-to-post` first. That body carries the judgment.
This file says which tool to call and in what order.

Quote before you spend. Every charged tool takes `quoteOnly`, which returns the
exact maximum credits, calls no provider and runs no model. Say the quote and
the balance from `layers://account` out loud, then make the call.

## Order

1. `find_growth_opportunities`, 0 credits. The ranked queue with the source
   evidence behind each entry. When the person named a subject in
   "$ARGUMENTS", pick the entry that matches it and say why. A queue that
   comes back empty with `connect_social_account` as the next step means no
   social account is connected yet: hand over the connect link as a markdown
   link and stop there.

2. `plan_content_experiment`, 6 credits for a new plan or a format change and 0
   to rewrite the opening or the caption. One hypothesis, one controlled
   variable, the target account, the effort and the success gate. Show the plan
   and let the person edit it before anything is rendered.

3. `render_content`, 200 credits per 10-second video, 400 per 20-second video,
   85 per slideshow and 25 per output image, each per usable variant. Quote it,
   say the number, then render. An unusable output is refunded. The finished
   job names `layers://artifacts/<id>`, which holds the CDN addresses and the
   measured bytes.

4. `deliver_content_experiment`, 0 to prepare and 5 per target. Send it to the
   draft inbox unless the person asked for a direct post. Never call a post
   public until the platform post id and the URL come back.

## While it runs

`layers://jobs` holds state, progress and errors for anything running.

`halt`, 0 credits, stops queued and running work in the scope you name: one
job, one experiment, one account, one campaign, or the whole project. Reach for
it first when the person says stop.

On a refusal, read `layers://skills/v1/refusals` before retrying anything. On
`OUT_OF_CREDITS`, read the message: it states how many credits short the
balance is and links the checkout for the pack that covers it. Give that link
as a markdown link.
