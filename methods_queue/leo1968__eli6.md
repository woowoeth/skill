---
name: eli6
description: Explain any topic like the user knows nothing about it, using a visual-first HTML page with big pictures, simple diagrams, flowcharts, and very few words. Trigger on eli6, /eli6, explain like Im 6, visual explanation, simple diagram explanation, or when the user wants a beginner-friendly visual breakdown of a concept, system, code module, decision, or incident.
---

# ELI6 — Visual Explain Like I'm 6

## Goal

Turn any complex topic into a beautiful, self-contained HTML page that a complete beginner can understand at a glance. Prioritize **big visuals + minimal text**. Assume the reader has zero background knowledge.

## When to activate

Activate when the user:
- Starts with `/eli6` or `eli6`
- Asks to "explain like I'm 6", "ELI6", "explain simply with pictures/diagrams"
- Wants a visual beginner-friendly breakdown of code, systems, trade-offs, incidents, or abstract concepts

## Core instructions

1. **Assume zero knowledge**  
   Pretend the reader is smart but has never heard of this topic before. No jargon unless immediately defined with a simple analogy.

2. **Output format — always produce a complete HTML file**  
   Create a single self-contained HTML page (save it as a `.html` file). The page must be:
   - Visually dominant (large diagrams, big icons, clear flow)
   - Minimal text (short sentences, big headings, plenty of whitespace)
   - Beautiful and readable on both desktop and mobile
   - Self-contained (inline CSS, no external dependencies except optional CDN for icons if needed)
   - Include a visible in-page “下载本页” / “Download this page” control that downloads the finished HTML itself. For a self-contained page, implement it with a Blob/object-URL download or an equivalent local mechanism; do not rely only on a chat message link.

3. **Page structure (follow this order)**

   - **Hero title** — Short, friendly title + one-sentence plain-English summary
   - **Big analogy** — A simple real-world metaphor that captures the essence (with a large visual if possible)
   - **How it works** — 3–7 numbered steps. Each step has:
     - Large number or icon
     - 1 short sentence
     - A clear visual (SVG diagram, flowchart box, simple illustration, or emoji composition)
   - **Key insight / Why it matters** — One memorable takeaway in a highlighted box
   - **Optional** — Tiny "Deeper if you want" section with slightly more detail (still simple)

4. **Visual style rules**

   - Use large, bold typography
   - Prefer diagrams over paragraphs
   - Use color purposefully (soft backgrounds, clear contrast)
   - Create flowcharts with pure CSS/SVG or simple nested boxes with arrows
   - Use generous spacing and rounded cards
   - Keep the color palette clean and friendly (avoid dark mode unless requested)
   - Make every important idea visible without reading walls of text

5. **Shared visual language**

   - Use a calm, premium Apple-like visual language without copying Apple's interfaces: generous whitespace, soft gray backgrounds, restrained blue accents, gentle shadows, translucent surfaces, and consistent rounded corners.
   - Keep the page content-first. Use one clear hierarchy, minimal decoration, and simple linear icons or SVG shapes.
   - Support desktop, tablet, and mobile layouts with responsive spacing and stacking.
   - Include natural, restrained hover, focus, active, and transition states. Respect `prefers-reduced-motion`.
   - Use the exact lowercase button label `download` for the in-page HTML download control.
   - Add a quiet footer reading `FoisonX Lab` to generated pages.

6. **Language rules**

   - Short sentences
   - Concrete words over abstract ones
   - Analogies from everyday life (toys, kitchen, traffic, school, animals, etc.)
   - Never say "as you know" or assume prior knowledge
   - If a technical term must appear, immediately follow it with a plain definition

7. **Special cases**

   - **Code / systems / modules**: Show the flow of data or control with a clear left-to-right or top-to-bottom diagram. Highlight the "main character" of the system.
   - **Technical trade-offs**: Frame as "We chose A instead of B because..." with simple pros/cons visuals.
   - **Incidents / postmortems**: Timeline style — what happened → why it broke → how it was fixed, with clear cause-effect arrows.
   - **Abstract concepts**: Always anchor to a physical or everyday analogy first.

8. **Image generation**
   When a custom illustration would significantly improve clarity (complex process, unique metaphor), generate a clean, simple, friendly illustration using the image generation capability and embed or reference it. Prefer lightweight SVG diagrams for most cases so the HTML stays fully self-contained.

9. **File delivery**
   Write the finished HTML to a file (e.g. `eli6-<short-topic>.html`) and present it to the user so they can open or download it.
   - After the HTML is successfully written and checked, always include a clickable Markdown link using the absolute file path, labeled clearly as “下载 HTML” or “打开 HTML”.
   - If a preview image or other requested companion file was created, provide a separate clickable link for it too.
   - A link makes the file available for the user to download or open; do not claim that an operating-system download was automatically triggered unless that action was actually performed and confirmed.
   - Before delivery, verify that the page contains the visible download control and that the generated HTML includes the download handler; the chat link and the in-page control are separate delivery paths.

## Quality bar

The final page should make someone say:  
"Ohhhh, *that's* how it works" within 10–20 seconds of looking at it — even if they previously understood nothing about the topic.
