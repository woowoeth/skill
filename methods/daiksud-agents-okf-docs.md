---
name: okf-docs
description: 文書を作成・更新するときに使用し、docs以下の文書をOKF v0.2で整理・検証する。Markdown with Gherkinのfeature文書も対象とし、読み取り・説明だけでは使用しない。
---

# OKFで文書を作成する

文書作成・更新では `task-workflow` も適用する。以下の `docs/` は作業対象リポジトリのパスを指す。

GitHubに投稿するIssue・PR本文・コメントにはOKFやYAML frontmatterを適用しない。投稿の構成・整形は依存スキル `task-workflow` の手順に従う。

## 文書の形式

- `docs/` をKnowledge Bundleとして扱い、文書の作成・更新時は [Open Knowledge Format（OKF）](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) v0.2に従う。
- 通常の文書は1ファイル1概念とし、UTF-8のMarkdown本文と、`---` で囲んだYAML frontmatterで構成する。
- frontmatterには文書の種類を表す `type` を必ず記載し、`title` と `description` を付ける。
- `index.md` はディレクトリの索引、`log.md` は更新履歴にのみ使用し、通常の概念文書には使わない。作成する場合はOKFの各形式に従う。
- 出典・検証・履歴などの任意メタデータを記載する場合は、OKFのフィールド定義に従い、確認できた事実だけを書く。
- `*.feature.md` もOKFのfrontmatterを付け、本文はMarkdown with Gherkinで記述する。

## 配置と記法

- 文書の目的に応じて `docs/` 以下にディレクトリを作成し、分類する。設計判断は `docs/adr/`、ふるまいの定義は `docs/behavior/` に配置する。
- 既存の分類に該当する文書はそのディレクトリに追加し、新しい分類が必要な場合にディレクトリを作成する。
- ページは `docs/<分類>/<page-name>.md` に作成する。全体の案内など、分類に属さない文書は `docs/<page-name>.md` に配置する。
- 画像など Markdown に含められない外部アセットは使用しない。
- GitHub Flavored Markdown（GFM）を積極的に活用し、見出し、リスト、タスクリスト、表、コードブロックで情報を読みやすく整理する。
- Emojiは見出しや状態の識別に、GitHub Alertsは注意事項や重要な制約の強調に使用する。

## 検証

- 依存スキル `task-workflow` の[GitHub向けMarkdownの品質](../task-workflow/references/markdown-quality.md)に従い、Markdown全体を保存前にrumdlで整形・チェックする。共通設定は同スキルの `assets/rumdl.toml` を参照し、既存プロジェクト設定を無断で上書きしない。
- rumdl未導入・旧版の場合の導入・更新やダウンロードを伴う一時実行は、同資料に従ってユーザーの事前許可を得る。実行不能を検証合格と扱わない。
- frontmatterの形式・必須項目、文書の分類、用語、相対リンク、記載したコマンドと差分の体裁を確認する。
- feature文書は `bdd-tdd` の記法に従い、rumdlで整形後も見出し・ステップの構造を確認する。
- 確認できなかった出典や検証結果を、確認済みとして記載しない。
