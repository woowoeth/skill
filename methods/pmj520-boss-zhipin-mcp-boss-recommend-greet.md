---
name: boss-recommend-greet
description: BOSS 直聘「推荐牛人」信息流的筛选 + 触达工作流：抓取推荐卡片 → 硬条件过滤 → 卡片评估 → 达阈值点「打招呼」（VIP 免费额度）→ 核验会话。当用户说"看下推荐牛人 / 从推荐流找人 / 推荐流筛选并打招呼 / 达到 85 分的直接打招呼"时应用。含触达动作，执行前须用户授权。
---

# BOSS 推荐牛人流工作流（推荐 → 评估 → 打招呼）

**版本 1.0.0**

执行前必须先加载并遵守 `boss-agent-cli-ops`（环境、安全红线、通用约定）。

> **本流程含触达动作。** 开始前需用户明确授权本轮打招呼，并确认四件事：
> 分数阈值、本轮打招呼上限、抓取上限、硬过滤条件。未获授权只做评估、不点任何按钮。

> **浏览器必须已停在推荐牛人页。** 自动化**不做页面导航** —— 整页冷启动会触发一次
> 完整鉴权握手，实测会导致掉线（手动点侧边栏正常，自动导航必掉）。页面没开就
> 请用户手动点开，不要自己跳转。

## 参数

- `THRESHOLD`：打招呼分数线，默认 **85**
- `MAX_GREET`：单轮打招呼上限，默认 **5**
- `MAX_CARDS`：抓取卡片上限，默认 **60**。挑几个人不需要翻完整个推荐池 ——
  一次拉全量是采集行为，不是浏览行为，也是最容易触发风控的动作
- 硬过滤条件：由任务指定，跟当前 JD 走（口径见 ops）。**性别不作为默认过滤项**
- `JOB`：推荐流按当前默认职位出人；开工前用 `hr jobs list` 复述当前职位与用户确认，
  避免对错职位打招呼
- 打招呼内容：平台默认招呼语（点按钮即发送，无自定义输入框）

## 步骤

### 1. 前置体检

执行 ops 的**前置体检四连**，然后挂载 UI 会话并做选择器体检：

```python
from boss_agent_cli.automation.boss_browser import (
    SURFACE_RECOMMEND, attach_recruiter_surface,
    BossRiskPageDetected, BossSessionLoggedOut, BossUiSurfaceUnavailable,
)

session = attach_recruiter_surface(cdp_url="http://127.0.0.1:9222", surface=SURFACE_RECOMMEND)
report = session.health_report()
if not report.ok:
    # 风控页 / 掉线 / 页面结构变化 —— 停手，把 report.reason 报给用户
    raise SystemExit(report.reason)
```

`attach_recruiter_surface` 复用用户已登录的 context 和已打开的推荐页页签；
页面没开会抛 `BossUiSurfaceUnavailable`，此时**提示用户手动点开推荐牛人页**，
不要传 `allow_open=True` 绕过（那是给无人值守的定时任务用的）。

### 2. 抓取推荐卡片（只读）

```python
cards = session.collect_recommend_cards(max_cards=MAX_CARDS)
```

返回每张卡片的 `id`（encryptGeekId）、`name`、`gender`、`text`（含薪资 / 年龄 /
工龄 / 学历 / 期望 / 优势 / 标签 / 工作经历时间线）。滚动节奏、距离随机化、
按 id 去重、frame 选择、每轮风控检查都在函数内部处理，**不要自己写滚动循环**。

### 3. 评估（卡片即证据，无需拉简历）

- 推荐流卡片**无 securityId**，`hr resume` 不可用；卡片文本已含工作经历与标签，足够评估。
- 先按已确认的硬条件过滤，再按 JD 维度打分（核心客群 / 场景经验、行业匹配、
  量化业绩、稳定性与年限、薪资带、活跃度）。
- **注意**：点头像是照片预览、不是简历抽屉，不要点。

### 4. 打招呼（≥ THRESHOLD 分，逐个慢速）

```python
button = card.locator("button:has-text('打招呼')")
session.human_click(button, kind="write")   # 触达档：指针轨迹 + 8-20 秒间隔
```

- `human_click` 内部已经做了：动作前后 `guard()`、节律等待、指针移动、随机落点。
  **不要用 `locator.click()`，也不要自己 `time.sleep`** —— 都会绕过这些。
- **成功标志**：按钮变为「继续沟通」；侧边「沟通」角标数 +1。
- **免费通道**：推荐流打招呼走 VIP 免费额度，不会弹付费墙。
- **单轮总数 ≤ `MAX_GREET`**；间隔由 `write` 档位保证，不需要手写。
- 跳过按钮不是「打招呼」的卡片（已沟通过的显示「继续沟通」）。

捕获到 `BossRiskPageDetected` 或 `BossSessionLoggedOut` 时：**立即停止剩余操作**，
汇报已完成的部分并转人工，绝不重试、绝不绕过。

### 5. 核验与汇报

- `hr chat --label-id 0` 拉最新会话，对新增 friend_id 逐个 `hr chatmsg` 识别归属。
- 汇报：打招呼名单（姓名 / 评分 / 核心命中 / 新 friend_id）、未达线名单简述、
  剩余可跟进建议。
- 收尾 `session.close()`（只断开自动化连接，不关用户浏览器）。

## 选择器失效时

`health_report()` 报「选择器体检未通过，缺失 X」= 页面结构变了。
改 `src/boss_agent_cli/automation/boss_selectors.py` 里对应的 `SelectorGroup`
（每组支持多个备选，加一个新的即可），**不要在 SOP 里另写一套选择器**。

## 验证

① 体检四连通过；② `health_report().ok` 为真；③ 目标职位已与用户确认；
④ 抓取量 ≤ `MAX_CARDS`；⑤ 触达对象全部满足已授权的硬条件；
⑥ 每个打招呼按钮变「继续沟通」；⑦ 会话核验 N/N；⑧ 全程零付费、无风控页触发。
