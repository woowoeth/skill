<p align="center">
  <b>🏪 Skill 商店 · Skill Store</b><br>
  <i>每天上新的好玩 Agent Skill 精选店 — a corner store of fun agent skills, restocked daily.</i>
</p>

<p align="center">
  🌐 <a href="https://ourword.ai/skill-store/">进店逛逛 / Live store</a> ·
  🤖 <a href="./llms.txt">llms.txt (for AI agents)</a> ·
  📦 <a href="./skills/feed.json">feed.json</a> ·
  📄 <a href="./docs/PROTOCOL.md">进货协议 / Protocol</a>
</p>

---

## 这是什么 / What this is

**Skill 商店**只做一件事：把 GitHub 上**好玩、值得一装**的 Agent Skills（`SKILL.md` 那种）挑出来，配上中英双语导购文案，摆上货架。不追求大而全 —— 全网索引已经有人做了；这里是一家有店长口味的小店，**每天进货，只上架有意思的**。

**Skill Store** does one thing: it picks the **fun, worth-installing** Agent Skills (the `SKILL.md` kind) off GitHub, writes bilingual shelf copy for them, and puts them on display. It is not an exhaustive index — those exist. It's a small shop with a shopkeeper's taste, **restocked daily, fun items only**.

界面极简、内容优先：卡片带仓库封面，点开任何一件是安装说明。
Minimal, content-first UI: cards carry repo covers; clicking any item shows install instructions.

## 怎么运转 / How it works

```
GitHub (topics · search · tracked repos)
      |  daily GitHub Actions scout（进货员）
      v
shallow clone → parse SKILL.md frontmatter
      |            - 分类上架（8 排货架 / 8 shelves）
      |            - fun_score 好玩度打分
      |            - 大合集折叠成一张「合集」卡（no dumping）
      v
skills/*.json（repo 即数据库 / repo is the database）
      + editorial/curation.json（店长手写中文文案与推荐，永不被机器覆盖）
      v
skills/feed.json → GitHub Pages 静态店面（this site）
```

- **Runs entirely on GitHub.** Actions 是进货员，repo 是数据库，站点是一个读 `feed.json` 的静态页。No server.
- **Editorial layer wins.** `editorial/curation.json` 里的人写文案在每次重建 feed 时覆盖机器字段；scout 永远不会碰它。
- **Collections stay tidy.** 一个仓库塞几十个 skill 时，货架上只放一张「合集 ×N」卡 + 最多 3 件样品。

## 货架 / Shelves

🎨 创意画室 · 🎮 玩乐杂货 · ✍️ 文房小铺 · 🧺 生活日用 · 📄 文档柜台 · 💼 打工必备 · 🔧 开发五金 · 🧬 元技能

## 进货来源 / Sources

| Source | Status |
|---|---|
| `anthropics/skills` 官方专柜 | live |
| GitHub topics: `claude-skills` `claude-code-skills` `agent-skills` | live |
| GitHub search（fun/game/creative 关键词） | live |
| 已上架仓库的星数/更新回访（restock） | live |

> 选品标准见 [docs/CURATION.md](./docs/CURATION.md)。

## 日常巡货 / Daily curation

进货员（GitHub Actions）每天自动上货，新货先挂**占位文案**（形如「写代码的顺手工具：xxx。英文简介见下」）。把占位货变成正式商品这一步是人工巡货：挑出值得留的写钩子+点评、该下架的置 `hide`。

**触发方式**：在对话里说一句「今天巡货」，即对当天（或积压）的占位新货做一次编辑过堂。攒几天一起补也行——占位文案在信息流里一眼可辨，不会遗漏。

> 想省掉人工这步？配一个 `LLM_API_KEY`（见下），进货当刻即自动出文案。

## 新货自动文案 / Auto copy for new stock

每日进货的新商品会先套用占位文案；在仓库 Settings → Secrets 配置以下三项后，scout 会用 LLM 按「钩子 + 点评」的店内风格自动写中英文案（editorial 层始终优先）：
只需 `LLM_API_KEY` 一项（可选 `LLM_BASE_URL`、`LLM_MODEL`），OpenAI 兼容协议与 Anthropic 原生协议自动识别：
- Anthropic：`LLM_API_KEY=sk-ant-…`（默认模型 claude-haiku-4-5）
- DeepSeek：`LLM_API_KEY=sk-…` + `LLM_BASE_URL=https://api.deepseek.com` + `LLM_MODEL=deepseek-chat`
- OpenAI / OpenRouter 等：填对应 base 与 model 即可

New items get placeholder copy by default. Set the three secrets above and the daily scout writes bilingual hook + review copy for them (the editorial layer always wins).

## 本地跑 / Run locally

```bash
python3 scouts/skill_scout.py            # daily mode: restock + discover (uses GH_TOKEN if set)
python3 scouts/scout_lib.py              # rebuild skills/feed.json only
python3 -m http.server 8080              # open http://localhost:8080
```

## 安全提示 / A word on safety

Skill 会在你的环境里执行指令。**装之前先读 `SKILL.md`**，只装你看得懂、信得过的。
Skills run instructions in your environment. **Read the `SKILL.md` before installing**; every receipt says so.

## License

Code, scouts, editorial copy and the site: [MIT](./LICENSE). 各 Skill 版权归原作者，以其仓库 License 为准。
