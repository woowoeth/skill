---
name: pinit-veroeffentlichen
description: Veröffentlicht oder aktualisiert Pinit-Bretter (Whiteboard-Artifact aus pinit.html, db-Capability) — ohne Angabe ALLE Bretter aus der Liste `bretter.json`, mit Name oder URL nur eins, mit „neu <Name>“ ein neues Brett für ein Projekt (eigener Artifact-Name, eigene Datenbank). Nutze diesen Skill bei „veröffentliche Pinit“, „update alle Bretter“, „leg ein Pinit-Brett für <Projekt> an“, „publish das Brett“, „neue Fassung hochladen“. Funktioniert in jedem Projekt.
---

# Pinit veröffentlichen

Die eine Quelle ist `C:\Users\luish\Documents\claude\pinit\code\pinit.html` (falls der Ordner
noch nicht umbenannt ist: `…\claude\reissbrett\code\pinit.html`). Sie wird **nie** verändert.
Jedes Brett ist ein eigenes Artifact mit eigenem Namen und eigener Datenbank; die Liste aller
Bretter liegt neben diesem Skill in `bretter.json`.

## 0. Aufruf verstehen
- **Ohne Angabe** („veröffentliche Pinit“, „update alle“): **alle** Einträge aus `bretter.json`
  aktualisieren.
- **Mit Name oder URL**: nur dieses Brett. Name = `name` aus der Liste (Teilstring reicht, bei
  mehreren Treffern nachfragen).
- **„neu <Name>“** (oder „leg ein Brett für <Projekt> an“): neues Brett anlegen, in die Liste
  eintragen, URL in die `CLAUDE.md` des aktuellen Projekts schreiben (Abschnitt „Pinit-Brett“,
  eine Zeile mit URL), damit `pinit-lesen`/`pinit-schreiben` sie finden.
  **Fehlt der Name, fragen** (AskUserQuestion, Vorschlag „Pinit · <Name des Projektordners>“).
  Nie einen Namen raten.

**Konten-Regel (wichtig, weil Luis zwei Konten hat — Arbeit und privat):** Ein Artifact kann
nur das Konto aktualisieren, das es veröffentlicht hat. Darum trägt jeder Eintrag in
`bretter.json` ein Feld `konto`. **Vor jedem Update** `action: "read"` mit der URL: kommt
„artifact not found“, gehört das Brett dem anderen Konto — dann **nicht** weiter probieren,
sondern dem Nutzer sagen, welches Konto es besitzt, und anbieten: (a) hier ein **neues** Brett
anlegen (Name erfragen), (b) auf dem anderen Rechner veröffentlichen. Bei „alle“ werden
Bretter fremder Konten übersprungen und in der Ergebnis-Tabelle als „anderes Konto“ gelistet,
nicht als Fehler. Welches Konto gerade aktiv ist, steht im Systemkontext (`userEmail`);
beim Anlegen eines neuen Bretts diese Adresse als `konto` eintragen.

## 1. Vorbereiten
1. Quelle lesen, `var FASSUNG = "x.y"` herausziehen — das wird das `label`.
2. `bretter.json` lesen. Format:
   ```json
   [ { "name": "Pinit · Smartvillage", "url": "https://claude.ai/code/artifact/…", "favicon": "📌", "projekt": "C:\\…" } ]
   ```
3. **Je Brett eine Wegwerf-Kopie** im Scratchpad: `pinit-<slug>.html`, in der **genau eine**
   Zeile anders ist: `<title>Pinit</title>` → `<title><name></title>`. Der Galerie-Name kommt
   aus dieser Zeile; der `title`-Parameter greift nur ohne Title-Tag. Vor dem Publish prüfen,
   dass sich Kopie und Quelle in genau einer Zeile unterscheiden (`diff | wc -l`).
   **Denselben Kopie-Pfad je Brett wiederverwenden** — ein anderer Pfad wäre für das
   Werkzeug ein anderes Artifact.

## 2. Veröffentlichen
Artifact-Werkzeug, je Brett ein Aufruf:
- **Update:** `file_path` = Kopie, `url` = URL aus der Liste, `label` = „Fassung <FASSUNG>“.
  `capabilities` **weglassen** (die gespeicherte `{db:{}}` bleibt), `favicon` **weglassen**.
  Wird das Artifact in dieser Sitzung noch nicht gelesen/veröffentlicht, verlangt das Werkzeug
  erst ein `read` — dann `action: "read"` mit der URL, danach erneut publishen. Bei einem
  Versions-Konflikt **nicht** `force`: die Seite selbst schreibt sich nie neu, ein Konflikt heißt
  eine andere Sitzung hat veröffentlicht — kurz lesen, dann erneut.
- **Neu:** `file_path` = Kopie, **kein** `url`, `capabilities: { db: {} }`, `favicon` (Emoji,
  Vorgabe 📌), `label` = „Fassung <FASSUNG>“, `description` = „Pinit-Brett für <Projekt>“.
  Die zurückgegebene URL in `bretter.json` eintragen (name, url, favicon, projekt = aktuelles
  Arbeitsverzeichnis) und in die Projekt-`CLAUDE.md`.

## 3. Danach
Im Chat: Tabelle mit Name · Fassung · URL · Ergebnis je Brett. Fehlgeschlagene einzeln nennen,
nicht verstecken. Bei „alle“ auch die Zahl: „3 von 3 aktualisiert“.

## Grenzen
- Der Inhalt liegt in der Datenbank des Artifacts und übersteht ein Update — ein Update ist
  gefahrlos. Ein Publish **ohne** `url` erzeugt dagegen immer ein neues, leeres Brett.
- Nie die Quelle `pinit.html` umschreiben, um einen Namen zu setzen. Nur die Kopie.
- Ein Brett aus der Liste nehmen = Zeile in `bretter.json` löschen; das Artifact selbst löscht
  nur Luis in der Galerie (claude.ai/code/artifacts).
