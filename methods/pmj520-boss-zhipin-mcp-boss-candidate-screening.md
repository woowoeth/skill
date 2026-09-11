---
name: boss-candidate-screening
description: BOSS 直聘招聘者侧「搜索 + 收藏」工作流：关键词搜索 → 硬条件过滤 → 评估打分 → UI 免费收藏 → 输出报告。当用户说"按招聘工作流找人 / 搜候选人并收藏 / 出候选人报告 / 筛选 N 份简历"时应用。纯筛选，不含触达动作。
---

# BOSS 候选人筛选工作流（搜索 → 评估 → 收藏 → 报告）

**版本 1.0.0**

执行前必须先加载并遵守 `boss-agent-cli-ops`（环境、安全红线、通用约定、宿主能力对照）。
本 SOP 只写与其他流程的差异部分。

## 参数（可被用户指令覆盖）

- `KEYWORDS`：搜索关键词。默认从当前职位 JD 提炼；可多组关键词各搜一页后合并去重。
- `CITY_CODE`：**由任务指定**，取自目标职位所在城市。未指定时先用 `boss cities` 查询确认，
  不要假设默认城市。
- `N`：目标人数，默认 3。
- `JOB`：**不写死**。执行时从后台读取（见步骤 1），用户可用职位名或 encryptJobId 指定。
- `REPORT_FORMAT`：默认 Markdown；宿主具备 PDF 能力时附带 PDF。
- 硬过滤条件：由任务指定，跟当前 JD 走。口径与性别相关限制见 ops「硬过滤条件口径」
  与「安全红线」第 5 条。

## 步骤

### 1. 前置体检 + 确定目标职位

先做 ops 的**前置体检四连**。通过后读取当前在招职位：

```bash
boss --json --cdp-url http://127.0.0.1:9222 --role recruiter hr jobs list
```

- 只有一个在招职位 → 直接采用，向用户复述职位名确认。
- 多个 → 列出职位名 + encryptJobId 让用户选，**不要替用户猜**。
- 记下选中的 `encryptJobId` 与 `jobId`，后续步骤复用；城市未指定时取职位所在城市。

### 2. 取 JD 建评分基准

`hr jobs detail <encryptJobId>` → 提取 `/job/postDescription`、`skillList`、薪资、城市 →
归纳 5-6 条评分维度（核心客群 / 场景经验、行业匹配、量化业绩、稳定性与年限、
薪资带与班次匹配等）。硬条件同时从 JD 原文归纳，交用户确认后固化为本轮过滤规则。

### 3. 搜索与初筛（API，只读）

```bash
boss --json --cdp-url http://127.0.0.1:9222 --role recruiter hr candidates "<KEYWORDS>" --city <CITY_CODE>
```

- 多关键词循环，间隔 ≥ 4 秒。
- 解析 `data.geeks[].geekCard`：`name`、`ageDesc`、`workYear`、`highestDegreeName`、
  `salary`、`activeDesc`、`matches`、`eduSchool`。
- 先按已确认的硬条件过滤，再按评分维度对卡片打分排序，取 Top N（另备 2 名替补）。

### 4. 深度评估（API，只读）

- 每人 `hr resume <encryptGeekId> --security-id <securityId> --job-id <jobId>`，间隔 ≥ 5 秒。
- 输出：评分 x/100、3-5 条优点、2-4 条缺点或风险、面试追问清单。
- 排除：明显超配（管理岗 / 期望薪资远超职位带）、画像不符、硬条件不过者。

### 5. 收藏（UI 免费通道）

**浏览器必须已停在搜索牛人页**，自动化不做页面导航（冷启动会触发鉴权握手，实测可能掉线）。

```python
from boss_agent_cli.automation.boss_browser import SURFACE_SEARCH, attach_recruiter_surface

session = attach_recruiter_surface(cdp_url="http://127.0.0.1:9222", surface=SURFACE_SEARCH)
report = session.health_report()
if not report.ok:
    raise SystemExit(report.reason)   # 风控 / 掉线 / 页面结构变化，停手
```

页面没开会抛 `BossUiSurfaceUnavailable` —— 提示用户手动点开搜索牛人页，不要绕过。
选择器取自 `session.selectors`（`search_card` / `favorite_button`），不要另写一套。

- **定位铁律**：UI 列表非确定性、同姓氏会重复 —— 用「姓氏 + 年龄 + 学历 + 1 个独有特征词」
  四重校验；搜索框输入独有特征词组合再匹配；命中失败换备用关键词（公司名 / 项目名 /
  技能短语）重试，仍失败则用替补。
- 操作：`session.human_click(卡片)` → 抽屉 → `session.human_click(收藏按钮)` →
  断言「收藏 → 已收藏」+ toast「收藏成功」。误收藏立即用同一按钮撤销。
- **一律用 `human_click`，不要 `locator.click()`**：它内部已含 `guard()`、节律等待、
  指针轨迹与随机落点。收藏不是触达，用默认的 `click` 档即可。
- 每人操作后按 `Escape` 关抽屉（残留的 c-resume iframe 会挡住搜索框）；
  间隔由节律器保证，不要自己 sleep。
- **绝不点「联系Ta」**（付费畅聊卡收银台）。

### 6. 报告

生成 `候选人筛选报告_YYYY-MM-DD.md`：职位与评分基准、筛选链路（搜索量 → 过滤 → 初筛 →
深评 → 收藏）、Top N 对比表（评分 / 基本信息 / 核心命中 / 风险）、逐人详评（优缺点 +
面试追问）、建议。

需要 PDF 时按 ops「宿主能力对照」调用当前宿主的 PDF 生成能力；无可用能力则只交付
Markdown 并说明原因。产物写入工作目录后把路径告知用户。

### 7. 核验收尾

- 打开 `/web/chat/interaction?status=9`（互动 → 收藏牛人），在 frame
  `/web/frame/recommend/interaction` 内断言 N 位目标全部可见。
- 汇报：收藏清单 + 报告路径 + 声明「未发送任何消息、未支付任何费用」+ 数据留存位置。

## 相关流程

推荐牛人流（筛选 + 打招呼）见 `boss-recommend-greet`；
附件简历接收见 `boss-resume-intake`。

## 验证

① 体检四连通过；② `health_report().ok` 为真；③ 目标职位已与用户确认；④ N 份 resume JSON 均 `ok:true`；
⑤ 收藏断言 N/N；⑥ 收藏页 N 位可见；⑦ 报告已交付并告知路径；⑧ 零消息、零付费。
