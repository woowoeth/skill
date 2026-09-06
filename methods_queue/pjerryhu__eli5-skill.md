---
name: eli5
description: Explain a topic to someone who knows nothing about it, as an HTML artifact with big pictures and few words. Use when the user runs /eli5 <topic> or asks for a beginner-friendly visual explanation.
argument-hint: <what you want explained>
---

# ELI5

Explain the topic in `$ARGUMENTS` like the reader knows **nothing** about it, as an HTML artifact with big pictures and few words.

If no topic was given, ask the user what they want explained. If the topic is something in the current conversation or codebase (e.g. "this function", "our auth flow"), read the relevant code first so the explanation is accurate.

## How to build it

1. Load the `artifact-design` skill before writing the page (required by the Artifact tool).
2. Write the explanation as a single HTML file in the scratchpad directory, then publish it with the Artifact tool.

## Rules for the explanation

- **Pictures carry the story, words support it.** Every major idea gets a big, friendly inline SVG diagram: simple shapes, labeled arrows, stick-figure-level characters (a person, a robot, a box, a database cylinder). No decorative clip art — every element in a diagram must mean something.
- **Few words.** One short caption sentence under each picture. Short headings. No paragraphs longer than 2 sentences. If a sentence can be cut, cut it.
- **Zero jargon.** Assume the reader has never heard any term of art for this topic. When a technical word is unavoidable, introduce it *after* the plain-language idea, in parentheses: "the bot writes down the card's id (msgId)".
- **Concrete over abstract.** Use a running example with named things ("an admin", "the bot", "the notebook") instead of generic descriptions. Analogies to everyday objects beat precise definitions.
- **One idea per section.** Number the steps (1, 2, 3…) so the reader always knows where they are in the story. Each numbered step = one heading + one big diagram + one caption.
- **Progressive**: start with the one-sentence "what is this and why should I care", then walk through the mechanism step by step, and end with a small "so, to recap" picture or 3-bullet summary.

## Page style

- Big type, generous whitespace, diagrams that fill most of the content width.
- Diagrams as inline SVG (theme-aware per the artifact rules), never external images.
- Give the artifact a short, friendly `<title>` naming the topic, and a fitting emoji favicon.

When done, give the user the artifact link.
