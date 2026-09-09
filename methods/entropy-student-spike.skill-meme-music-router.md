---
name: meme-music-router
display_name: Meme Music Router（热梗音乐路由器）
description: 一个 Meme-first 创意编排器。先现场调用 Entertainment Rander 找到值得玩的热梗并锁定梗核，再确定作品名与最有趣的演绎方式；图片、台词、歌曲、短视频都只是放大原梗的工具。进入标准 Meme Music Episode 后，固定交付：名称、带标题图片、歌词、旋律/曲风提示词。
version: 0.4.1
language: zh-CN
status: calibrating
---

# Meme Music Router（热梗音乐路由器）

## 1. 总目标

> **找到真正值得玩的热梗 → 锁定梗核 → 给这一期定一个不跑偏的作品名 → 选择最好玩的演绎方式 → 把原梗放大。**

热梗是主角。图片、台词、歌曲、短视频只是演绎工具。

> **Meme first. Name locks the concept. Format amplifies it. Quality comes last.**

创作核心规则：

- `references/MEME_AMPLIFICATION_RULES.md`
- `references/IMAGE_REFERENCE_RULES.md`
- `references/MUSIC_OUTPUT_RULES.md`
- `references/LANGUAGE_FLEXIBILITY_RULES.md`

---

## 2. Router 的职责

Router 负责：

- 现场调用正确的上游 Skill；
- 锁定本期 `meme_core`；
- 区分 parent meme / child unit；
- 形成 `episode_name`；
- 判断哪种创意演绎最能放大梗；
- 保证图片、歌词、音乐提示词都围绕同一梗核与同一作品名；
- 管理用户确认和下游交付；
- 阻止 Theme Drift。

Router 不负责自行定义热梗、热歌或好音乐的专业标准。

---

## 3. 上游调用契约

### 3.1 Entertainment Rander｜默认第一入口

需要选题 / 热梗判断时：

```text
Router
→ LIVE 读取 entertainment-rander 当前版本
→ 接收候选、等级、证据、对象层级
```

默认主制作池优先使用上游返回的 `S+ / S`。

### 3.2 Music Trend Radar｜按需

只有在以下情况调用：

- 近期热歌本身参与创意；
- 需要确认某首歌当前是否仍热；
- 准备用近期热歌做改编。

不依赖当前歌曲热度时跳过。

### 3.3 Music Quality Radar｜进入歌曲节点才调用

当需要正式生成 / 改编歌词、旋律 / 曲风 / 编曲提示词或审查音乐时，现场读取当前 `music-quality-radar`。

它只能优化 **HOW**，不能改变已经锁定的 **WHAT**。

---

## 4. LIVE Skill 规则

遵循：

`references/LIVE_SKILL_INVOCATION_RULES.md`

每次实际调用前重新读取 GitHub 当前版本；历史读取、聊天记忆、摘要和缓存都不能替代。

读取失败：`LIVE_SKILL_READ_FAILED`。

---

## 5. Meme Core Lock｜先锁梗核

Entertainment 结果进入 Router 后先记录：

```yaml
meme_core:
  source_meme:
  parent_meme_or_ecosystem:
  parent_tier:
  selected_child_unit:
  child_tier_if_separately_rated:
  gate_basis: parent | child
  core_person_or_character:
  core_action_or_conflict:
  iconic_line_or_object:
  why_it_is_funny:
  must_not_drift:
```

Parent 与 child 不得混级。

如果 `core_action_or_conflict` 与 `why_it_is_funny` 说不清楚，不进入创作阶段。

---

## 6. Creative Name Lock｜选题阶段就定作品名

每个进入候选池的创意，在用户确认前就生成：

```yaml
creative_lock:
  episode_name:
  meme_core:
  selected_derivative:
  one_sentence_play:
  must_preserve:
```

`episode_name` 不是装饰标题，而是整期作品的统一创意锚点。

固定要求：

1. 名称必须直接绑定原梗人物 / 原句 / 动作 / 冲突，或非常明显地指向它；
2. 名称同时要体现本期创意玩法或二创版本；
3. 禁止把梗抽象成泛主题，例如原梗是“找凌玲 / 手撕小三”，却起成《把话摊开》；
4. 名称一旦用户确认，图片标题、歌词主题、Hook 与音乐提示词都必须继续使用同一创意锁；
5. 如果后续确实要改名，必须重新检查图片 / 歌词 / 音乐是否一起同步，不能只改一个节点。

示例：

```text
原梗：薛甄珠冲进办公室找凌玲 / 手撕小三
玩法：印度电影歌舞版

可用方向：
《凌玲你出来》
《我今天就是来找凌玲》
《找小三·印度歌舞版》

错误方向：
《把话摊开》
```

---

## 7. Presentation Router｜形式服从梗

锁定梗核与作品名后，再比较：

- 图片 / 梗图
- 台词 / 对话 / 小剧场
- 歌曲
- 短视频 / 剧情演绎
- Mixed

核心判断：

> **哪种形式能让这个梗更好笑、更荒诞、更爽、更容易理解和传播？**

音乐不是所有热梗的默认终点。

### 标准 Meme Music Episode

只有当“图片 + 音乐”确实能放大这个梗，或用户明确选择这一生产模式时，才进入标准四件套。

进入后固定最终交付：

1. **名称 `episode_name`**
2. **图片**：必须包含该标题，并体现原梗 + 本期创意
3. **歌词**：必须锁定同一梗核
4. **旋律 / 曲风提示词**：指导音乐模型如何演绎这个梗

不适合音乐化的梗应被 Router 跳过或改走其他形式，不为了凑四件套强行做歌。

---

## 8. Meme Amplification Gate｜形式不能改变梗

所有输出遵循：

`references/MEME_AMPLIFICATION_RULES.md`

最终作品主题必须直接继承：

- `core_action_or_conflict`；或
- `iconic_line_or_object`。

### 薛甄珠校准

```text
WHAT：找凌玲 / 找小三 / 冲进办公室手撕 / 护女儿上门算账
HOW：印度电影式高能歌舞
```

“印度电影歌舞”负责怎么演，不负责把“演什么”改成沟通、体面、成长等新主题。

---

## 9. 图片节点

遵循：

- `references/MEME_AMPLIFICATION_RULES.md`
- `references/IMAGE_REFERENCE_RULES.md`
- `references/LANGUAGE_FLEXIBILITY_RULES.md`

固定要求：

- 明确人物 / 名场面先找真实参考；
- 同时保留原梗 + 本期二创版本；
- 图片必须出现已锁定的 `episode_name` 作为主标题；
- 除标题外不默认塞大量文字；
- 最终生图 Prompt **硬上限 200 字**，推荐 80–160 字；
- 参考图承担身份细节；
- 图片必须让人一眼看出“哪个梗 + 我们怎么重新玩它”。

---

## 10. 歌曲节点

只有歌曲被判定为合适的放大形式时进入。

进入前固定生成：

```yaml
music_meme_lock:
  episode_name:
  meme_core:
  selected_derivative:
  music_role: amplifier
  music_type: original | adaptation
  song_theme:
  required_meme_anchor:
  forbidden_theme_drift:
```

然后 LIVE 调用 `music-quality-radar`。

固定原则：

> **Music Quality Radar 优化“怎样把这个梗写成好歌”，不能把梗和作品名背后的主题改掉。**

最终交付：

- 完整歌词；
- 旋律 / 曲风 / 编曲提示词，推荐 200–350 字，硬上限 500 字。

---

## 11. 输出语言

最终呈现不固定中文。

名称、图片标题、台词、歌词、Hook 可根据原梗、二创版本、人物身份、节奏和笑点选择中文、英文、中英混合、方言或其他更有效表达。

> **Language serves the meme.**

---

## 12. 默认完整流程

```text
用户发起一期
↓
LIVE Entertainment Rander
↓
得到 S+/S 热梗候选
↓
Meme Core Lock
↓
为候选生成 episode_name + one_sentence_play
↓
Router 判断最有趣的演绎方式
↓
如需要当前热歌 → LIVE Music Trend Radar
↓
用户确认“选题 + 名称 + 创意玩法”
↓
进入标准 Meme Music Episode（仅适合时）
↓
① 名称：沿用已锁定 episode_name
↓
② 图片：reference-first + 必须带标题 + Prompt ≤200字
↓
③ 歌词：music_meme_lock + LIVE Music Quality Radar
↓
④ 旋律 / 曲风提示词：围绕同一梗核与玩法
↓
Meme Recognition / Binding / Amplification / Name Consistency Test
↓
交付四件套
```

---

## 13. 最终四项测试

### Meme Recognition Test
去掉解释，熟悉原梗的人还能认出在玩什么吗？

### Meme Binding Test
只换人物名字，作品是否几乎可以原样套给大量无关梗？

- 是 → 太泛，重做。

### Amplification Test
图片 / 音乐有没有真正把原梗变得更有趣，而不只是更漂亮、更像歌？

### Name Consistency Test
名称、图片标题、歌词主题、Hook、音乐提示词是否仍然在讲**同一个梗 + 同一个创意玩法**？

- 任一节点漂移 → 回退重做。

---

## 14. Kill Rules

出现以下情况视为执行错误：

1. 需要上游判断却未 LIVE 调用；
2. 用记忆 / 摘要代替 LIVE Skill；
3. Parent / Child 等级污染；
4. 未锁定 `meme_core` 就开始创作；
5. 候选没有 `episode_name` 就进入正式制作；
6. 名称变成与原梗无直接关系的泛主题；
7. 默认强行把所有梗做成歌曲；
8. 图片 / 音乐 / 台词反过来改写原梗；
9. 图片没有展示已锁定标题；
10. 生图 Prompt 超过 200 字；
11. 歌曲节点没有 LIVE 调用 Music Quality Radar；
12. 歌曲发生 Theme Drift；
13. 曲风 / 编曲提示词超过 500 字；
14. 四个交付物彼此主题不一致；
15. 为了统一中文或国际化而破坏梗。

---

## 15. 核心原则

> **Meme first. Name locks the concept. Format amplifies the meme. Quality optimizes the execution.**

最终目标：

> **找到热梗 → 锁住它真正好玩的地方 → 先给这期一个准确有梗的名字 → 用最有趣的图片与音乐方式演绎 → 四个交付物始终讲同一件事 → 用真实反馈继续校准。**