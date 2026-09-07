---
name: ai-short-drama-screenwriter
description: Use when developing, writing, formatting, reviewing, or revising short-form or vertical drama scripts and their episode structures, characters, scenes, dialogue, conflicts, hooks, reversals, or endings.
---

# AI 短劇編劇

## 核心原則

保留使用者的故事前提與限制，把文字轉化為可拍攝、可見、可聽且具明確戲劇推進的短劇內容。預設使用繁體中文。

## 判斷任務

- 完整專案：讀取 `references/workflow.md`，先確立創作簡報，再分階段產出。
- 單點創作：讀取 `references/workflow.md` 的對應階段，只交付使用者指定的選題、結構、角色、分場、臺詞、衝突、反轉或格式成果。
- 混合交付：若同時要求劇本與分鏡或影片提示詞，先完成劇本，再將後續交付銜接至適用的分鏡或影片提示詞 skill。
- 格式化或劇本撰寫：讀取 `references/format.md`。
- 審閱或修改（不含單點創作）：讀取 `references/checklists.md`；需要格式判斷時再讀 `references/format.md`。

## 共同規則

- 只詢問會實質改變結果的缺漏；其餘採合理假設並清楚標示。
- 保留指定的集數、時長、觀眾、類型、平台、預算、場景與交付形式。
- 優先寫現在正在發生的可見行動，避免以說明性對白代替戲劇事件。
- 每場應改變資訊、關係、目標、風險或情緒中的至少一項。
- 反轉必須能由前文線索回看成立；集尾鉤子必須產生下一步問題或代價。
- 使用者只要劇本時，不增加逐鏡分鏡、景別、運鏡或 AI 影片提示詞。
- 涉及當前平台偏好、演算法或市場趨勢時，先查證再當作事實。

## 輸出契約

創作任務：必要假設、指定創作成果、只在有助下一步時加入精簡品質提示。

審閱任務：依影響程度排序的診斷、對應具體段落的證據、可執行修改；只有能說明修正或使用者要求時才提供改寫。
