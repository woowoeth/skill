---
name: journal-archaeology
description: 日记自我考古 skill。把多年日记语料（备忘录/Apple Journal/Day One/Notion/手写转录等导出）变成分层知识库和单文件交互式年鉴网站：摄取核验 → 通读建知识层 → 词典量化分析 → 五问综合（我怎么变的/我关注什么/什么改变了我/我的底色是什么/谁在我生命里）→ 滚动博物馆式 HTML 展示。触发词：分析我的日记、日记考古、自我考古、思维年鉴、journal analysis、diary archaeology、把日记给 AI、用日记了解我、日记做成网站、日记年鉴。即使用户只说"我有几年的日记想让你分析"或"把我的日记做成一个回顾"，也应触发。全程本地处理；这是自我反思工具，不是心理诊断。
---

# Journal Archaeology · 日记考古

把一个人多年的日记变成 TA 的思维年鉴。**核心原则：不是摘要，是考古**——
提取作者*相信/主张/执念*的东西，而不是发生了什么事。

## 开场原则（不可跳过）

**分工铁律：确定性工作交脚本，判断力工作交阅读。**
数数、词频、密度、共现 = `scripts/` 下的脚本；转折点认定、执念命名、引语精选、
叙事撰写 = 通读原文。词典法输出只是线索，结论必须由深读确认。

**伦理边界（日记是一个人最裸的东西）：**

- 全程本地文件处理，语料不上传任何外部服务
- 单被试纵向数据：相关不等于因果，所有图表带方法边界脚注
- 这是自我反思工具，**不是心理诊断**——不使用诊断性语言，不下临床结论
- 所有 quote 原文照录（`assemble_datajson.py` 机器校验逐字命中），所有论断带日期出处
- **人的重要性永远不打分**：关系层只报客观文本计数，"TA 对我是谁"由用户亲自填写
- 分析会触及沉重内容（丧失、危机、感情）。每个检查点都是用户的退出口；
  用户可随时终止，或指定某段时期/某个人不进入分析。呈现沉重发现前先问"要不要展开"
- **"和用户聊发现"是正式阶段（CP3），不是吐一份报告完事**——
  最好的洞察来自对话，用户的亲历语境是任何分析替代不了的证据层

**MVP 范围**：打字语料、中文优先。手写笔记本是高级路线（人工转录，成本高，
见 references/ingestion.md），多语言界面是 v2。

## 工作目录约定（用户项目内）

```
<用户项目>/
├── journal-analysis.config.json   唯一配置(CP2 诞生,用户校订过)
├── PROJECT.md                     语料档案 + 决策日志(跨会话记忆)
├── import/                        原始导出 + 一次性提取脚本 + 转录底稿(只进不删)
├── corpus/                        规范化语料 YYYY-MM-DD_来源.txt(建成后只读)
├── knowledge/
│   ├── stats.json / timeline.md / verify_report.md / config_suggestions.md   脚本生成
│   ├── digests/YYYY.md            P2 通读产物(纵轴)
│   ├── profile/NN_维度.md         P2 通读产物(横轴十维)
│   ├── annual/YYYY.json + cross_year.json   P4 结构化中间层
│   └── findings/01-05_*.md + data/*.json    P4 五章 + P3 量化数据
└── output/
    ├── data.json                  assemble_datajson.py 校验汇总产物
    ├── site.json                  P5 叙事文案层(经 CP4 签字)
    └── index.html                 build_html.py 产物,唯一交付物,永不手改
```

所有脚本用法：`python3 <skill目录>/scripts/<脚本>.py --config <项目>/journal-analysis.config.json`。
skill 目录只读，产物全部落用户项目。开始前把 `assets/config.template.json` 复制为
项目根的 `journal-analysis.config.json`（lexicons 有中文默认值，其余空壳在 P2 填）。

## 五阶段流程

### P1 摄取与核验 → 检查点 CP1（强制停）

1. 问清用户语料来源与形态，读 `references/ingestion.md` 选对应模式
2. 写一次性提取脚本（放 `import/`），把一切切成 `corpus/YYYY-MM-DD_来源.txt`
3. 跑 `verify_corpus.py`（命名/日期/星期/重复五项机械检查 + 抽样清单）和 `build_stats.py`
4. **CP1**：向用户呈现——逐年逐源篇数字数表、星期不符等异常清单及处置建议、
   随机 5 篇与原始导出的比对结果。**用户确认前不进 P2**。缺失时段要问清是真没写还是漏导

### P2 通读与知识层 → 检查点 CP2（强制停）

1. 按年分批通读 corpus（用 `build_timeline.py` 的索引辅助定位），按
   `references/analysis-spec.md` 写 `digests/YYYY.md` 和 `profile/` 十维
2. 通读中记录：人名与别名线索、主题词线索、作者的独有对比句式
3. 跑 `suggest_config.py` 得宽网候选，结合通读印象起草 config 的
   `topics` / `invariants`（候选+对照组）/ `people.registry`
4. **CP2**：把 config 草稿逐块摆给用户校订。**词典和人物表不出厂预装，这里是唯一出生点**：
   - 人物表逐人确认：别名合并（"k 是谁？"）、归类、歧义符号的生效年份
   - 主题词典：主题划分对不对、词表有没有明显误命中源
   - 不变量候选：这些"底色假设"像不像 TA；对照组选哪两个
   校订质量直接决定 P3 一切输出的质量——这轮对话值得慢慢聊

### P3 量化分析 → 软检查点（异常才停）

1. 跑量化脚本：`topic_shares.py`、`relationships.py`、`extract_self_compare.py`、
   `build_timeline.py`（幂等，P2 跑过也重跑无害）；`invariants.py` 仅在语料
   ≥100 篇且 ≥2 年时跑（体量门槛见 analysis-spec.md）
2. 逐个 sanity check 输出：份额突变月先查词典误命中；CV 自检按
   "对照组最小 CV ≥ 候选组最大 CV × 1.5"判定，不过则发现四不产出；
   人名明显误命中（如常用词撞名）回 CP2 修 config 重跑
3. 无异常则直接进 P4，有异常向用户报告并修正

### P4 五问综合 → 检查点 CP3（强制停，正式对话阶段）

1. 按 `references/analysis-spec.md` 写 `knowledge/annual/YYYY.json` 逐年 +
   `cross_year.json`（评分标准/三判据/宁缺毋滥全在手册里）
2. 写 `findings/01-05.md` 五章，对应五问：
   01 自我认知时间线（今昔对比句法）/ 02 关注点迁移（主题份额）/
   03 转折点解剖（得失×在场者编码）/ 04 人格底色（不变量 CV）/
   05 人际关系客观层（五信号，无公式）
3. 跑 `assemble_datajson.py`——quote 校验不过就回原文修正再跑，**不许绕过校验**
4. **CP3——和用户聊发现**：逐个发现给出"一句话结论 + 最强证据（带日期原文）+ 方法边界"，
   然后听：用户可以否决、修正、补充亲历语境；人物档案的 role 字段邀请用户命名；
   沉重的发现先问"这部分要不要展开"。把用户的修正回写进 findings 和 annual JSON

### P5 展示与交付 → 检查点 CP4（强制停）

1. 读 `references/presentation.md`，写 `output/site.json`（全部叙事文案：
   序厅大标题、五厅"标题即结论"、footnote 方法边界、尾厅收束句）
2. **CP4（构建前）**：把文案清单给用户签字——序厅大标题、尾厅收束句、五厅标题、
   精选引语。这些是年鉴里最重的话，必须是用户认可的话
3. 跑 `build_html.py`，让用户本地打开 `output/index.html` 验收
   （交互全项过一遍，见 presentation.md 的 CP4 检查单）

## 语料不足时的降级

语料 < 100 篇或不足 2 年：只做长廊 + 对比句 + 星图，跳过 CV 和转折编码
（详见 analysis-spec.md 体量门槛）。site.json 少写对应展厅，模板自动隐藏，无需改模板。

## 增量更新（新语料进来时）

P1 局部（增量核验）→ 只重读新增部分、更新受影响年份的 digests/annual →
重跑 P3 全部脚本 → assemble → 必要时补 CP3 聊新发现 → 更新 site.json → build。
详见 references/ingestion.md 增量流程。

## 参考文件

- `references/ingestion.md` — P1 详规：按来源的 playbook、核验协议、PROJECT.md 模板
- `references/analysis-spec.md` — P2/P4 编码手册：评分标准、四个分析方法、annual schema、体量门槛
- `references/presentation.md` — P5 详规：五展厅映射、site.json schema、文案规范、CP4 检查单
- `assets/config.template.json` — 配置模板（中文 lexicons 默认值内置）
- `assets/template.html` — 年鉴模板（渲染器，勿改副本，文案走 site.json）
