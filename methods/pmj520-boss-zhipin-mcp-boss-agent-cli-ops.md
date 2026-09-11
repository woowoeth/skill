---
name: boss-agent-cli-ops
description: boss-agent-cli（命令 `boss`）的安装部署、登录验证与安全红线，Windows / macOS / Linux 通用。当用户要求"安装 boss-agent-cli / 配置初始化约束 / 重装环境 / 登录 BOSS"时应用，也作为三条招聘 SOP（screening、recommend-greet、resume-intake）的共同前置。
---

# boss-agent-cli 环境与安全边界

**版本 1.0.0**

本 Skill 管**环境与安全**：安装、登录、CDP、安全红线，以及三条业务 SOP 共享的通用约定。
业务流程见 `boss-candidate-screening` / `boss-recommend-greet` / `boss-resume-intake`。

不改动 boss-agent-cli 原生能力；CLI 未实现的功能走平台 UI 的免费通道，不绕平台风控。
**命令报错或行为异常先查 `docs/field-notes-2026-09.md`**（10 项实测记录与补丁说明）。

## 平台与路径约定

CLI 自身跨平台，数据目录统一是 `~/.boss-agent/`（Windows PowerShell 下等价写法
`$env:USERPROFILE\.boss-agent\`）。本 Skill 下文一律用 POSIX 写法。

| 用途 | 路径 |
|---|---|
| 数据 / 配置 | `~/.boss-agent/` |
| 调试浏览器 Profile | `~/.boss-agent/manual-browser-profile` |
| uv 工具根目录 | `uv tool dir` 的输出（不要写死） |
| CLI 所在虚拟环境 | `$(uv tool dir)/boss-agent-cli/bin`（Windows 为 `\Scripts`） |

## 一站式安装（AI 全自动执行）

用户说「帮我安装并配置初始化约束」时按序执行，**每步验证通过再进行下一步**，
用户全程只需完成第 8 步的登录。

1. **获取仓库**：`git clone <仓库地址> <本地目录>`（git 直连受限时改用
   `curl -sL https://codeload.github.com/<owner>/<repo>/tar.gz/refs/heads/master` 下载解压）。
2. **环境探测**（只读）：`python --version`（需 ≥ 3.10）、`python -m uv --version`。
3. **安装 CLI**：无 uv 则 `python -m pip install --user uv`；优先装仓库版
   `python -m uv tool install --force <仓库目录>`（含实测修复），失败回落
   `python -m uv tool install boss-agent-cli`；`python -m uv tool update-shell` 写 PATH
   （提示重启终端生效）。
4. **浏览器内核**：
   - macOS / Linux：`"$(uv tool dir)/boss-agent-cli/bin/patchright" install chromium`
   - Windows：`& "$(uv tool dir)\boss-agent-cli\Scripts\patchright.exe" install chromium`
5. **部署 Skill**：`python scripts/install_skills.py`（自动探测 Claude Code / 千问办公 /
   Codex 等宿主；`--list` 先看探测结果，`--host` 指定单个宿主）。
6. **启动调试浏览器**：`python scripts/launch_boss_browser.py`
   （专用持久 Profile；CDP 仅绑 `127.0.0.1:9222`；端口已监听则复用不重复启动）。
   已有多个子 profile 时脚本会列出让用户选；需要一个干净登录态时用 `--new-profile`
   （各 profile Cookie 独立，但共用同一 user-data-dir 与同一个 CDP 端口）。
7. **验证 CDP**：`curl http://127.0.0.1:9222/json/version` 返回浏览器版本即就绪。
8. **登录（唯一需用户参与的一步）**：请用户在弹出的浏览器里登录 BOSS，切换到招聘者
   身份并打开在招职位页；用户确认后执行三连验证：
   `boss --cdp-url http://127.0.0.1:9222 login --cdp` → `boss status --live` →
   `boss --role recruiter hr jobs list`（能列出职位 = 招聘者身份确认）。
9. **收尾报告**：安装版本（仓库版 / PyPI 版）、体检结果、部署清单、已生效的初始化约束，
   以及三条 SOP 的触发语。

任一步失败按 `docs/field-notes-2026-09.md` 排障；不硬重试，向用户报告具体错误。

## 环境自检（安装后 / 日常）

- `boss doctor`：环境体检；`boss status` / `boss status --live`：登录态。
- 装的是仓库版时注意：`uv tool upgrade boss-agent-cli` 会用 PyPI 版覆盖，
  恢复方式是对仓库目录重新 `uv tool install --force .`。

## 初始化约束

1. 只用专用持久 Profile，不接管系统默认浏览器或日常主 Profile；CDP 只绑 `127.0.0.1`，
   绝不暴露到局域网。
2. 登录链路必须走完三连验证，不能只看「已登录」——要确认招聘者身份。
3. stoken 缺失（auth degraded）时只读可用；缺二级令牌时不要高频重试平台请求。

## 安全红线（每次操作前自检）

1. 默认只读；写动作（发消息 / 同意 / 上下架 / 改配置 / 付费）逐次获得用户明确授权。
2. **绝不付费代购**：搜索页「联系Ta」会弹畅聊卡付费收银台，与 VIP 额度是两套权益；
   绝不绕验证码或风控。
3. 每次招聘查询前验证登录态 + 招聘者身份；身份错误 / 登录异常 / 出现验证页 →
   立即停手交人工。
4. 只收集当前招聘任务必需的信息；未经要求不关用户浏览器、不切账号。
5. **不得设置歧视性筛选条件**：性别、年龄、民族、婚育状况等不作为默认过滤项。
   仅当用户显式提出、且属于国家规定的例外岗位时才可执行，执行前需用户书面确认依据。
6. `hr reply` 假失败陷阱：报 `no confirmed chat websocket send detected` 时消息
   **可能已送达**；重试前必须核验（见下「防重复铁律」）。

## 通用约定（三条 SOP 共享）

### 前置体检四连
CDP 存活（`curl http://127.0.0.1:9222/json/version`，不通则跑启动脚本）→
`boss status --live` 登录态 → `boss --role recruiter hr jobs list` 招聘者身份 →
**风控页三查**（页面出现 `verify.html` 或 URL 带 `_security_check` → 本轮立即中止转人工）。
任一失败不硬重试。

### 硬过滤条件口径
硬条件（学历、年限、行业等）一律**由任务指定、跟当前 JD 走**，不写死在 SOP 里。
执行前先从 JD 原文归纳并与用户口头确认。性别相关约束见「安全红线」第 5 条。
若确有合规依据需要按性别筛选，字段口径为：
- API 卡片 / 简历：`gender` 字段，`0` = 女，`1` = 男
- 推荐流 UI：卡片头像 `<use xlink:href="#icon-icon-woman|man">`，**不凭姓名猜测**

### UI 自动化一律走 `boss_browser`，不要手写 patchright

三条 SOP 的浏览器动作**必须**通过 `boss_agent_cli.automation.boss_browser`：

```python
from boss_agent_cli.automation.boss_browser import (
    SURFACE_CHAT, SURFACE_RECOMMEND, SURFACE_SEARCH, attach_recruiter_surface,
)

session = attach_recruiter_surface(cdp_url="http://127.0.0.1:9222", surface=SURFACE_RECOMMEND)
```

它固化了三条「写错就掉线」的规则，自己写 patchright 极易漏掉：

1. **只复用，不导航。** 取用户已登录 context 里已打开的页签。
   `new_context()` 不共享 Cookie（在里面开招聘页 = 未登录会话）；`page.goto()`
   是整页冷启动，会触发完整鉴权握手 —— **实测：手动点侧边栏正常，自动导航必掉线**。
   页面没开时抛 `BossUiSurfaceUnavailable`，**请用户手动点开目标页**，
   不要传 `allow_open=True`（那只给无人值守的定时任务用，且仍在同一 context 内开页签）。
2. **动作前后检风控与掉线**：`session.guard()` 命中即抛
   `BossRiskPageDetected` / `BossSessionLoggedOut`，必须停手转人工。
   `BossRiskPageDetected` 继承 API 通道的 `PlatformRiskError`（`code = ACCOUNT_RISK`），
   所以两条通道的风控走同一条终止分支；给用户的恢复动作用
   `display.risk_error_contract(exc.code)` 取，与 CLI 命令逐字一致。
   **平台响应码侧**：`code 36` = 账号风控，`code 37` 按文案分类 ——
   只有明确指向 token 过期才刷新，其余（含语义不明）一律 `ENVIRONMENT_RISK`，
   `recoverable=false`，**不刷新、不重试、不重新登录**。
3. **滚动走节流、距离随机、有上限**：`collect_recommend_cards(max_cards=N)`。
   用的是真实滚轮事件（`mouse.wheel`）而不是 `window.scrollBy`——后者直接改
   scrollTop、不产生 wheel 事件序列，页面侧能分辨。位移随机且偶尔回滚。
4. **点击一律用 `session.human_click(locator, kind=...)`，不要直接 `locator.click()`。**
   它会把指针沿带抖动的轨迹移过去、落点在元素框内随机偏移（不是正中心）、
   按下前有瞬时停顿。零位移的点击是最廉价的自动化破绽。
   `kind` 决定节奏档位：`read`（2-8s）< `click`（5-12s）< `write`（8-20s）——
   打招呼、发消息这类**触达一律用 `write`**，不可撤回的动作慢比快值钱。
   两个动作之间要留白时用 `session.pause("read")`，不要自己 `time.sleep`：
   各档位有独立的高斯延迟 + 突发惩罚，自己 sleep 等于绕过节律器。

选择器全部外置在 `automation/boss_selectors.py`。页面改版 → 改那里的
`SelectorGroup`（每组支持多个备选），**不要在 SOP 或临时代码里另写一套**。
开工前 `session.health_report()` 会把「结构变了」提前暴露成红灯。

### 防风控节奏
动作间隔由 `boss_browser` 的节律器保证（见上：`read` / `click` / `write` 三档，
各自独立的高斯延迟 + 突发惩罚），**不要自己 sleep、也不要靠记住某个秒数**。
仍需由任务约束的是**数量**：每轮写操作 ≤ 3 次、推荐流单轮打招呼 ≤ 5 个、
抓取要有上限，不为"抓全"翻完整个列表。
过程中出现验证页或异常，立即停止剩余操作转人工。

### 防重复铁律
`hr reply` 发送后**即使命令报错**，也必须用 `hr chatmsg <friend_id>` 按消息内容计数核验，
存在即视为已发，**严禁重发**（平台消息不可撤回）。
仓库版已自动仲裁，PyPI 版仍需手动核验。

### 付费边界
免费通道 = 收藏 / 推荐流打招呼（VIP 额度）/ 已建会话的 `hr reply`。
付费入口 = 搜索页「联系Ta」（畅聊卡收银台）—— 绝不触碰、绝不代付。

### 候选人数据留存
简历与评估产物只保存在用户指定目录；任务结束时向用户汇报留存位置，
并提示可用 `boss clean --privacy` 清理。默认不长期保留，超出当前招聘任务需要即删除。

## 宿主能力对照（Skill 跨 AI 环境通用）

SOP 中出现的辅助能力按「能力」描述，各宿主按下表取用；**不要写死某个宿主的工具名**。

| 能力 | Claude Code | 千问办公 | 通用回落 |
|---|---|---|---|
| 从 PDF 提取文本 | `pdf` skill | `extract_content.py` | `pdftotext`（poppler）或 `python -m pypdf` |
| 生成 PDF 报告 | `pdf` skill | `generate_mdx_pdf.py` | `pandoc`；都不可用时只交付 Markdown |
| 浏览器自动化 | `boss_browser`（见上，勿手写 patchright） | 同左 | 同左 |
| 交付文件给用户 | 写入工作目录并告知路径 | 同左 | 同左 |

运行 `boss_browser` 的解释器用 CLI 所在环境：
`$(uv tool dir)/boss-agent-cli/bin/python`（Windows 为 `\Scripts\python.exe`），
CDP 连接由 `attach_recruiter_surface` 内部完成。

## 快速排障索引（详见 docs/field-notes-2026-09.md）

- reply 假失败 / request-resume 不可用 / RECRUITER_CHAT_TAB_REQUIRED → §一
- 安全验证页挂起（verify.html）→ §二 #5（停手转人工，绝不绕过）
- 全局参数位置 / 临时目录 / PowerShell 编码 / 列表非确定性 → §二 #6-#10
- 通道费用边界 / 数据口径（gender、bizType=14、flag=65537）→ §三 / §四
