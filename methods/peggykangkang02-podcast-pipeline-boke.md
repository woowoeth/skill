---
name: boke
description: 中文播客「找→转→总→落→归」一条龙总指挥。串起 podcast-finder（检索）、podcast-transcribe-local（本地转录+标点）、总结写作、落库 Obsidian（xiaoyuzhou-podcast-notes）、按主题归类子文件夹。当用户说「找一期关于 XX 的播客然后整理进我的知识库」「把这几期播客转成逐字稿+总结放进 Obsidian 播客干货」「按类型给播客笔记分类」、或想批量沉淀播客素材时使用。产出：每期「逐字稿+总结」两份，笔记与逐字稿成对落库、按主题自动归入子文件夹、双向双链，可长期当选题素材库检索。
---

# 中文播客一条龙：找 → 转 → 总 → 落 → 归

把一期（或多期）中文播客从「发现」一路做到「躺在 Obsidian 选题库里，按主题归类好、可检索」。全流程零云端 ASR、零 API 成本、本地跑。

## 为什么要有这个总指挥

播客素材处理被拆在好几个 skill 里，单独用记不住顺序和参数。这个 skill 是**总入口**，把下面已有的能力串成一条稳定流水线，并把这几轮打磨沉淀的**内容标准**固化：

| 环节 | 用的能力 | 属于 |
|---|---|---|
| ① 找：关键词搜节目/单集 | `podcast-finder` | 已有 |
| ② 转：出逐字稿 | `podcast-transcribe-local` (SenseVoice 离线) | 已有 |
| ③ 标点 | 同上的 `punctuate.py` (CT-Transformer 离线) | 已有 |
| ④ 总结 | 按下方「总结标准」由 agent 写 | 本 skill 固化 |
| ⑤ 落库+归类 | `xiaoyuzhou-podcast-notes` 落库 + 本 skill 的 classify/organize/sync | 已有+本skill |

## 一条命令跑通（速查）

假设已有一期链接，按顺序执行（每个等上一步产物出来）：

```bash
PY=~/.workbuddy/binaries/python/envs/default/bin/python   # WorkBuddy 受管 Python；没装 WorkBuddy 就换成你的 python3 路径
SK=~/.workbuddy/skills/boke
TR=~/.workbuddy/skills/podcast-transcribe-local/scripts

# 建工作目录（按 平台-节目-主题 命名）
D="播客转录/喜马拉雅-XX节目-主题"; mkdir -p "$D"

# ② 转录（出 transcript.txt / transcript.srt / meta.json）
cd "$D" && $PY $TR/transcribe.py "<小宇宙或喜马拉雅链接>" --out ./_work

# ③ 加标点 + 章节标记（出 punctuated.txt）
$PY $TR/punctuate.py --work-dir ./_work

# ④ 读 punctuated.txt 全文，按下方标准写 总结.md
#    （这是最花功夫的一步，agent 必须读全稿、引用原话）

# ⑤ 判断该归哪类（决定落库 --subfolder）
$PY $SK/scripts/classify.py --title "<单集标题>" --desc "<节目简介>" --json
#   → 读返回的 folder，形如 "播客干货-夏林果/Agent与智能体"

# ⑤ 落库 Obsidian（成对笔记+逐字稿，双向双链）。--subfolder 传完整库路径+子类
$PY ~/.workbuddy/skills/xiaoyuzhou-podcast-notes/scripts/publish_to_vault.py \
    --meta ./_work --note ./总结.md --transcript ./_work/punctuated.txt \
    --slug "<主题>" --subfolder "播客干货-夏林果/Agent与智能体"

# 若笔记正文后续有改动，用 sync_vault.py 同步进 Obsidian（保留 frontmatter）
$PY $SK/scripts/sync_vault.py --work "$PWD"
```

注意：落库时的 `--subfolder`（子文件夹）在 publish_to_vault.py 里传，或在其 config 设 default_subfolder。归类逻辑见下方第五节。

---

## ① 找播客

用 `podcast-finder` skill。按关键词一次搜小宇宙+喜马拉雅，零登录零 Key。搜到链接交给下游。

- 触发词：找播客、搜 XX、有没有讲 XX 的、找几期关于 XX 的
- 产出：一批含 平台链接/标题/时长/发布日期 的清单，存 `播客选题/`，再挑要深挖的进流水线

## ② 转录（本地离线，60-70 倍实时）

用 `podcast-transcribe-local` skill。双平台（小宇宙/喜马拉雅）+ 本地音频 + 直链都能喂。产物：

- `_work/transcript.txt` 无标点纯文本（原始）
- `_work/transcript.srt` 带时间戳
- `_work/meta.json` 节目名/标题/时长/播放量/转录耗时/real-time factor

> 踩坑红线（别改回去，详见 podcast-transcribe-local/SKILL.md）：用固定 20 秒窗口切分，别用 VAD（长音频丢 90% 内容）；整文件下载别 Range；转完别跳过片头 30 秒音乐段的噪声。

## ③ 标点（本地离线，免费）

用同技能的 `punctuate.py`（CT-Transformer 标点模型，282MB 随技能自带）。输出 `_work/punctuated.txt`（带标点+章节标记，可读）。标点这步是这几轮补的：之前 SenseVoice 只出无标点连续文本，现在本地模型直接补上，零成本不联网。

## ④ 总结（内容标准，最花功夫）

agent **必须读 `_work/punctuated.txt` 全稿**（2-3 万字），引用原话和案例，按下面标准写 `总结.md`。标准经过康康六轮反馈打磨，详见项目记忆 MEMORY.md，核心如下：

### 总结结构（五模块）

1. **知识概览 + 适合谁听**：分块列这期讲了哪几方面知识；标「谁该听、谁可跳过哪段」。开头给小白视角一句话整体翻译
2. **重要观点**（5-6 条）：每条 = 观点句加粗 + **原话引用** + **具体案例**（播客里或自己举例）+ **小白视角解读**。解读要落结论：干货是什么、接下来该怎么做、什么样才是对的。叙述高级但把事说明白。不写「我的解读」字样，统一「小白视角解读」
3. **信息差/反直觉**（3-5 条）：同样必须带案例 + 小白视角 + 结论，不能光列观点
4. **章节纪要**：分点列每章**具体讲了什么**（细节级），不写大段。每章 3-5 个要点
5. **思考**（≥7 条）：每条 = **观点句加粗作标题** + 一段剥到里层的高阶解读

### 思考模块写法（v7，康康最在意）

- 每条 = 加粗观点标题 + **只有正文段**，**不要任何「解读：/成稿：/案例：」标签**，不要引用块
- 解读要高阶有沉淀：不是复述观点，而是**往上一层抽象出可迁移的判断框架/规律**，给明确**结论**（所以该怎么做），有**认知增量**（看完能带走一个东西）
- 结论化在叙述里自然收束，**不要用「给你的结论：」这类统一标签句式**（会变新模板腔）
- 语调是「这个人真的听懂了、想明白了」，不是百科复述，也不是发社媒的营销腔
- 至少 7 条

### 文字红线（机械检查必须过）

- 全文**禁英文直引号** `"`（用中文弯引号「」/"" 或加粗）
- 正文**禁破折号 `——`**（只能当独立段落分隔符），一律用逗号/冒号
- 检查命令：
```bash
grep -c '"' 总结.md; grep -c '——' 总结.md   # 都应为 0
```

### 终审（写完全部跑）

1. dbs-content 终审：结构/可读性/干货精准度/逻辑闭环
2. 禁用符号机械检查（上面命令）
3. 定稿后 `sync_vault.py` 同步进 Obsidian

## ⑤ 落库 + 归类（Obsidian「播客干货-夏林果」）

### 落库

用 `xiaoyuzhou-podcast-notes` 的 `publish_to_vault.py`。它把「笔记 md + 逐字稿 md」成对落库，**逐字稿从 txt 转 md**（Obsidian 不索引 txt），自动补 frontmatter + 双向双链。落库目录由其 config 的 `default_subfolder` 控制。

### 分类法（一级 6 类，按单集主题）

Obsidian 子文件夹，见 `categories.json`：

| 子文件夹 | 收什么 |
|---|---|
| `AI工具与用法` | 某个/某类 AI 工具怎么用、搭工作流提效、保姆级教程 |
| `AI认知与商业` | AI 行业趋势/商业化/变现、认知刷新、反直觉洞察 |
| `Agent与智能体` | Agent 产品形态、办公 Agent、架构生态、入口与上下文之争 |
| `产品与创业` | 做产品、创业、出海、SaaS 增长获客变现 |
| `自媒体与内容` | 自媒体运营、内容创作、个人 IP、涨粉变现 |
| `职场与个人成长` | 职场组织、个人成长、效率学习方法、思维认知 |

**判定**：落库前用 `classify.py --title/--desc` 打标建议子文件夹；关键词匹配有歧义时，agent 结合全稿内容定夺（拿不准就用 `organize.py --move-file ... --to-folder ...` 手动归）。新建子文件夹名随手建，classify 的 folder 字段与 publish_to_vault 的 --subfolder 保持一致。

### 归类工具

- `classify.py`：给单期打类别 + 建议子文件夹（JSON 或可读）
- `organize.py`：把平铺在库根的旧笔记按主题批量搬进子文件夹（`--dry-run` 先看再 `--apply`）；`--move-file --to-folder` 手动归单篇
- `sync_vault.py`：定稿后把工作区总结正文同步进 Obsidian 笔记（保留 frontmatter）

---

## 触发场景 & 一口价交付

当用户说「整理一期/几期播客进我的库」，默认交付：

1. `播客转录/<案例>/` 下：逐字稿（带标点）+ 总结.md
2. Obsidian `播客干货-夏林果/<子文件夹>/` 下：笔记 + 逐字稿 成对、双向双链、已按主题归类
3. 提醒已进哪类，方便日后按主题钻文件夹找素材

## 相关 skill

- 上游检索：`podcast-finder`
- 转录+标点：`podcast-transcribe-local`
- 落库模板/脚本：`xiaoyuzhou-podcast-notes`
- 终审：`dbs-content`
