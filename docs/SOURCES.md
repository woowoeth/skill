# 品味信源

口号：帮你发现有品位的 Skills。
进货对标原声：**进货和上架同一轮**。过门禁的当场写文案、hide:false、进 feed；过不了的留库房。

## 不当主源（对照用）

| 源 | 为什么不进货 |
|---|---|
| `topic:claude-skills` 全网扫描 | 召回优先，货是目录站同款 |
| LinklyAI/best-skills 安装量榜 | 官方四件套 + 通用开发件占满 Top |
| Anthropic / Vercel / Microsoft 官方目录 | 用户自己会去官网 |
| claudskills.com 6 万件镜像 | 数量堆 |
| swaylq/master-skill 72 行业蒸馏 | 一台机器量产行业包，没有单件立场 |

伊恩日刊、HelloGitHub 是**口味校准**，不是 SKILL.md 矿。看见对得上的单件再收。

## T1 必盯

中文创作者（国外目录站没有的理由）：

- `op7418` 歸藏 — 瑞士风 / 材质插画 / 社交卡片
- `alchaincyf` 花叔 — 设计哲学写进原型
- `JimLiu/baoyu-skills` 宝玉 — 中文写作与小红书图卡
- `worldwonderer` — 小说变成能玩的游戏、网文拆解
- `5tldr` · `laolaoshiren` — 中文现场单件
- `KKKKhazix` 卡兹克 — 活人感长文，合集只抽 `khazix-writer` 这一档
- `BigPengSays` — 从爆款公号蒸馏出的选题公式
- `tjxj` — 手写幻灯片、四格漫画
- 在架已验证作者继续盯：侨批、蒸馏海报、假崔玉涛、湿球、SHA-256 审讯、花粉、赶海、起名、风水先声明不算命、Bluey、冰箱过敏原、龙猫禁洗澡、纸面桌游、父母口述史、家长配音绘本、三盘星历、定金订金、克苏鲁 KP、剧本杀、草间壁纸、本地线稿白板、NURBS 滑块、禁 AI 插图路书

有立场的英文单品作者：

- `Nutlope/hallmark` — 把一眼 AI 的页面改回人做的
- `JuliusBrussee` caveman
- `blader` humanizer
- `tjxj/z-skills` — 手写幻灯片、四格漫画，HelloGitHub 同属
- `obra/superpowers` — 只抽能单独成件的方法，不整库上架
- `mattpocock/skills` — 同上

## T2 热门榜（监视 + 筛选，整榜不上架）

每天从这些榜抽 `owner/repo`，过 `_admit` 和官方厂牌黑名单，再 clone 看有没有正经 `SKILL.md`。每天最多试 3 个新仓。

| 榜 | 取什么 |
|---|---|
| LinklyAI rising-stars / trending-7d / social-buzz | 新而热，不取 official-100 |
| LinklyAI top-repos | 只当对照，官方厂牌丢掉 |
| GitHub search `topic:claude-skills created:>14d sort:stars` | 近两周新星 |

直接扔掉的厂牌：`anthropics` `vercel` `microsoft` `google` `github` `huggingface` `shadcn-ui` `cursor`。
`awesome-`、vscode、空壳 `skills` 仓同样丢掉。

HelloGitHub 近刊里带正经 `SKILL.md` 的单件、伊恩日刊近两周能对上 GitHub 且装完手上有物件的，仍走这一档。

## T3

极强才收。合集只抽招牌件。

## 店主 09-07 名单（另一台 bot 按门闸过完的货，店主转来）

定位一句话（店主原话）：**帮你发现有品位的 Skill。一件一装，风格写死，有样图。20 种风格箱、工程全能包、落地页生成器不进。**

### 钉在每日扫描里的仓（已进 `scouts/skill_scout.py` 的 T1_REPOS / T1_AUTHORS）

图册 / 海报：LiamGvchi/gc-minimal-zine-poster · Zeejay0/gathered-scenes-zine-skill · wnby/paper-spirit-zine · yanliudesign/french-illustration-skill · yanliudesign/mono-color-skill · Kimberlying/watercolor-memory-poster · kennyleung123/photo-paper-scene-zine-v1 · Hiseaa/eastern-ink-photo-diptych · TwentyfiveBTea/ink-wash-poster · N1kO724/kodak-2383-film-look · luji12/handdrawn-photo-poster · luckdvr/photo-riso-poster · iamkong/photo-to-minimal-illustration · liuzihe849-png/ai-editorial-print-studio · yangcodingmaster/photo-distill · haorantang97/antibes-holiday · op7418/guizang-yingzao-skill · leishifu666/lsf-trend-merch-poster · xianxie6/algorithmic-sublime-poster · zhu930824/photo-animal-transposition-poster · dse120071750/paper-collage-design-skill · cxcxy/dy-travel-ticket-poster · taxueseek/taxue-solar-polaroid · swping999/scene-card-studio

插画 / IP / 配图：helloianneo/ian-xiaohei-illustrations · helloianneo/ian-xiaohei-scenes · orange2ai/orange-line-illustration · s1dashu/ip-as-logo-skill · EverettFish/ip_illustration_for_yourself · TaiT-tt/tait-crt-interface-skill · op7418/guizang-material-illustration · op7418/guizang-social-card-skill · op7418/logo-generator-skill

文字：orange2ai/renwei-writing · op7418/Humanizer-zh
工作向还过得去：lazypay/Archscribe（手绘技术图）· JimLiu/baoyu-skills · op7418/guizang-ppt-skill

09-07 对账：38 仓里 17 在架；7 在库房有源文件从没进过门闸日志；3 在阅读队列；10 全新；**3 在拒收榜**（taxueseek/taxue-solar-polaroid、orange2ai/renwei-writing、op7418/logo-generator-skill，都是问二「同类已有」）—— 店主名单高于机器判据，这 3 件重读，收就在 `rejected.json` 的 `_翻案记录` 里记一条。

### X 上盯的人（发新仓比任何商店都准）

@yanliudreamer（yanliudesign）· @op7418 · @AdrianPunk115（adrianpunk）· @LeiShifu79071（leishifu666）· @Xian0063（xianxie6）· @dotey（宝玉 JimLiu）· @cxcx_cxy（cxcxy）· @BTCqzy1

### 商店结论

- Atlasnote：87 件里约 12 件过门闸，上面那些已收完
- Agensi：付费落地页，没开源仓
- Linkly / skills.sh：安装量榜，工程件。当热度雷达，不当货架
- Zeejay 站：试玩页，仓已跟

### 明确不收

李岳写真导演箱、20 种海报生成器（howardz27 那类）、手绘视频风格选择器、仙侠美女箱、全栈 Design Skill。**共同点：风格箱 / 全能包 —— 「一件一装、风格写死」的反面。**
