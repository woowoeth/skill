---
name: podcast-finder
description: 按关键词检索中文播客的节目和单集，一次搜索同时覆盖小宇宙和喜马拉雅，输出可点击的平台链接。基于 Apple 公开的 iTunes Search API，零登录、零 API Key、零爬虫。当用户说「找播客」「搜播客」「有没有讲 XX 的播客」「找几期关于 XX 的单集」「看看别人怎么聊 XX」「播客素材」「找对标播客」「某播客最近更新了什么」时使用；即使用户没说「播客」二字，只要是想找音频节目素材，也应触发。搜到小宇宙链接后，可与 xiaoyuzhou-podcast-notes 串联，直接生成逐字稿和结构化笔记。
---

# 播客检索器

用关键词找中文播客。一个接口打通小宇宙和喜马拉雅，不用登录、不用 Key、不用爬网页。

## 它解决什么问题

跟播客相关的需求分两段：

| 环节 | 工具 | 状态 |
|---|---|---|
| **找**——关键词搜节目 / 搜单集 | 本技能 | 本技能 |
| **吃**——给链接出逐字稿和笔记 | `xiaoyuzhou-podcast-notes` | 用户已装 |

市面上绝大多数播客工具只做「吃」，不做「找」。本技能补的是上游这一段。

## 数据从哪来

Apple 的公开搜索接口：

```
https://itunes.apple.com/search?term=<关键词>&entity=podcastEpisode&country=CN&limit=N
```

为什么它能同时覆盖两个平台：国内播客基本都向 Apple Podcasts 提交过 RSS。
小宇宙的 feed 托管在 `feed.xyzfm.space`，喜马拉雅的直接是 `ximalaya.com/album/*.xml`。
所以搜一次，两个平台的单集一起回来。

## 怎么用

脚本在 `scripts/search.py`，只用 Python 标准库，无依赖。

### 搜单集（最常用）

```bash
python3 scripts/search.py "AI 出海"
python3 scripts/search.py "出海" --limit 20
python3 scripts/search.py "独立开发者" --platform xyz      # 只要小宇宙
python3 scripts/search.py "访谈" --min-minutes 40          # 只要 40 分钟以上的
python3 scripts/search.py "SaaS" --country US              # 搜英文播客
```

### 搜节目（想找一档值得长期跟的播客）

```bash
python3 scripts/search.py "商业访谈" --mode podcast
```

### 列某档播客的最新单集

```bash
python3 scripts/search.py --feed https://feed.xyzfm.space/xxxxx --limit 20
```

RSS 地址从上面任意一次搜索结果里就有（`RSS :` 那一行）。

### 给程序用

```bash
python3 scripts/search.py "AI 出海" --json
```

## 输出长什么样

```
 1. [小宇宙] Manus收购被叫停：技术主权与AI出海的「中国红线」
    节目: AI圆桌π | 16 分钟 | 2026-04-29
    链接: https://www.xiaoyuzhoufm.com/episode/69f20bedfbed7ba9411f6099
    简介: 近日，中国政府依法依规对Meta收购Manus项目作出禁止投资决定……

 2. [喜马拉雅] 揭秘近百家AI出海营销真相：Go Viral or Go Home
    节目: AI炼金术 | 71 分钟 | 2025-06-24
    链接: https://www.ximalaya.com/sound/875815634
```

链接还原规则（脚本已实现，无需手动处理，按优先级依次尝试）：

1. **直链解析**：小宇宙音频直链形如 `/track/<播客ID>/<单集ID>/...`，取第二个 ID →
   `https://www.xiaoyuzhoufm.com/episode/<单集ID>`；
   喜马拉雅直链参数里有 `track_id=<数字>` → `https://www.ximalaya.com/sound/<数字>`
2. **RSS 反查**：有些播客（如疯投圈）音频不托管在小宇宙，第 1 步拿不到 ID。
   此时抓该播客的 RSS，按标题匹配对应的 `<item>`，取其 `<link>`。并发执行，有缓存。
3. **兜底**：退化成 Apple Podcasts 页面链接。

只有第 1、2 步成功的结果会带 `← 可直接转笔记` 标记。**认这个标记挑，别自己猜。**
嫌 RSS 反查慢可以加 `--no-resolve`，但会多出几条退化的 Apple 链接。

## 与 xiaoyuzhou-podcast-notes 串联

这是本技能最大的价值点。完整链路：

```
关键词 → 本技能搜到小宇宙链接 → xiaoyuzhou-podcast-notes 出逐字稿+笔记 → 落 Obsidian
```

操作上：搜完之后挑带 `← 可直接转笔记` 标记的结果，把链接丢给
`xiaoyuzhou-podcast-notes`，它会解析元数据、转录音频、按类型套模板、
笔记和逐字稿成对落进你的 Obsidian 库。

**这条链路已实测跑通**：搜「独立开发者」→
拿到 `xiaoyuzhoufm.com/episode/6a81707a36641f136d88f41c` →
笔记技能成功解析出标题、节目名、时长 56.3 分钟、shownotes 和音频直链。

喜马拉雅的结果没有配套的笔记技能，只能拿到链接和简介，想深挖得人工处理。

## 边界和坑

- **搜的是标题和简介，不是音频内容。** iTunes 不索引音频里的对话，所以「谁在哪期聊过 X」
  这种问题搜不准，只能靠标题/简介命中。这是本技能最主要的局限，跟用户说清楚。
- **时效性不保证。** Apple 的索引可能滞后几天到几周，最新一期不一定能搜到。
  追更请用 `--feed` 直接解析 RSS，那是实时的。
- **结果按发布日期倒序**，不是按相关度。要更准就换更具体的关键词。
- **偶尔返回空。** 中文分词不如原生搜索聪明，一个词搜不到就换同义词再试。
- **证书校验**失败时脚本会自动降级重试一次，不用管。
- 本技能只做检索，不下载音频、不转写。要转写走 `xiaoyuzhou-podcast-notes`。

## 典型话术

| 用户说 | 怎么跑 |
|---|---|
| 找几期讲出海的播客 | `search.py "出海" --limit 15` |
| 有没有聊 AI 创业的单集 | `search.py "AI 创业"` |
| 找一档值得长期跟的商业播客 | `search.py "商业" --mode podcast` |
| 某某播客最近更新了啥 | `search.py --feed <该播客RSS>` |
| 找点播客当写作素材 | 先问清主题，再 `search.py "<主题>" --min-minutes 30` |
