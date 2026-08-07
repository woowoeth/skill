# 进货协议 / Restock Protocol

The repo is the database. One JSON per shelf item in `skills/`, aggregated into `skills/feed.json`.

## Item schema (informal)

| field | meaning |
|---|---|
| `id` | slug of repo (+skill dir). stable, filename = `<id>.json` |
| `kind` | `skill` 单品 / `collection` 合集 |
| `name` / `title_zh` | frontmatter name / 店长起的中文名 |
| `tagline_zh` / `tagline_en` | 货架一句话导购 |
| `why_zh` / `why_en` | 店长推荐理由（picks only） |
| `desc_en` | SKILL.md frontmatter description（原文） |
| `repo` `path` `url` `homepage` | provenance |
| `stars` `pushed_at` | refreshed daily by restock |
| `category` | one of 8 shelves |
| `fun_score` | keyword + stars + freshness heuristic（排序用） |
| `pick` | ★ 店长推荐 |
| `hide` | 下架但保留记录 |
| `skill_count` | 合集里有几件 / 单品附带几个子技能 |
| `cover` | 封面图 URL：作者社交预览图 > README 首张真实截图 > 空（前端回退 GitHub 信息卡）。店长可在 editorial 置空否决 |
| `install` | `{clone, copy, dir}` — 安装命令 |
| `source` `added_at` | who stocked it, when |

## Ingest rules（防止倾倒）

1. `anthropics/skills` → 官方专柜：全部单独上架，不出合集卡。
2. 仓库根目录有 `SKILL.md` → 一件商品（单品卡，`skill_count` = 仓库内 SKILL.md 总数）。
3. 有一个子技能与仓库同名（flagship）→ 视为「一件商品带配件」，只上 flagship 单品卡。
4. 其余：≥6 个 skill 出一张合集卡；<26 个再抽 fun_score 最高的 ≤3 件当样品；≥26 个只上合集卡。
5. 名字为 template/example/sample 或 `-v数字` 结尾的跳过。
6. 新仓库准入线：≥40 星，非 fork，名字不含 awesome-/dotfiles/demo。
7. 每次进货最多 10 个新仓库 —— 小店每天上新几件，不是倒货车。

## Editorial layer

`editorial/curation.json` 的字段在每次 `feed.json` 重建时覆盖同 id 抓取项。
机器只补货，**不改店长写过的任何字**。下架 = `"hide": true`。

## Conflict-safe commits

Per-item files commit first（文件名唯一，rebase 永不冲突）；`feed.json` 永远从合并后的全量重建再推送，失败则 reset → 重建 → 重试（同 ourword-ai/idea 的成熟套路）。
