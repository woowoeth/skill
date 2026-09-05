---
name: iitd-mail
description: IIT Delhi CSE IMAP/SMTP. Use iitd_mail_* tools only. Search, fetch, send, reply, trash, classify. Never Gmail. Ask before send/delete.
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "📬",
        "always": true,
      },
  }
---

# IITD work email (not Gmail)

Use **plugin tools**, not `gmail_*`:

1. `iitd_mail_status` — LLM host/model + IMAP health
2. `iitd_mail_search` — find mail (`query`, optional `mailbox` / `sender` / `unseen` / `allFolders`)
3. `iitd_mail_fetch` — read one mail (`uid`+`mailbox` preferred)
4. `iitd_mail_recent` — last N INBOX headers
5. `iitd_mail_folders` — list IMAP folders
6. `iitd_mail_send` — new mail via campus SMTP. First call **without** confirm (draft). Show Ajay. Second call `confirm=true` only if he says send.
7. `iitd_mail_reply` — reply / `replyAll`. Same draft-then-confirm rule. Need `uid`+`mailbox`.
8. `iitd_mail_delete` — move one mail to Trash. `confirm=true` only after he names that mail to delete. Scan never auto-deletes.
9. `iitd_mail_scan` — classify + IMAP **move** into category folders (INBOX keeps Urgent)
10. `iitd_mail_digest` — daily summary
11. `iitd_mail_recategorize` — wrong folder → another category
12. `/llm` / `iitd_mail_llm` — pick which **local Ollama** model classifies IITD mail (radios). Does **not** change chat primary or compaction. Prefer a small pulled model (e.g. llama3.2:3b) so the 5-minute scan does not keep the chat model loaded.
13. `/calibrate` / `iitd_mail_calibrate` — one unseen mail, `ask_user` radios, Finish anytime, then accuracy
14. `iitd_mail_update_check` / `iitd_mail_update_apply` — GitHub Releases; apply only after yes

Ask Ajay for **N** before scanning. Never send or delete unless he just asked. Never Gmail tools for IITD.
