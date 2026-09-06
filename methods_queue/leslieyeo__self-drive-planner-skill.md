---
name: self-drive-planner
description: 为中国境内自驾旅行生成真实、低疲劳、以当地美食和顺路游玩为核心的完整行程。用于已知起终点和天数的往返/单程规划，或从起点、天数和偏好推荐 2–3 个方向；结合高德路线、天气及小红书/B站社区证据，输出交互地图和逐日路书。办事、探亲、购物等只作为可选任务插入已有停留日。
---

# 通用自驾规划

生成一条可执行的完整行程，而不是景点清单。始终按以下优先级决策：

1. 驾驶安全和每日硬上限。
2. 顺路、少折返和充足休整。
3. 当地代表美食与真实社区体验。
4. 小范围、低拥挤的游玩组合。
5. 用户主动提出的可选事务。

不得为了增加城市数量牺牲体验。跨城驾驶日不叠加正式景点；停留日默认只安排一个主要区域。

## 首次使用与本地边界

区分两个目录：

- **Skill 源码目录**：包含本文件、`scripts/`、`templates/` 和静态页面模板；可以位于 SkillSource，按只读代码原件维护。
- **私人工作区**：调用 Skill 的当前项目根目录；保存密钥、行程、状态和生成结果。

先确认私人工作区有以下本机文件；它们不得提交、上传或发送给别人：

- `amap.webservice.local.json`：高德 Web 服务 Key，用于路线与候选地点实算。
- `amap.config.local.js`：高德 JS API Key 与安全密钥，用于交互地图。
- `data/trip-request.json`：当前用户的旅行请求；每趟旅行应使用新的 `request_id`。

若由安装包创建，模板已生成但仍是占位符。先填入自己的高德凭证，再运行生成器。基础链路不需要浏览器依赖；只有高德 JS API 降级和浏览器 QA 才需要在 Skill 源码目录执行 `npm install`，并接入共享 Chrome CDP。

当项目通过 `.agents/skills/self-drive-planner` 软链接引用本 Skill 时，必须从私人项目根目录运行命令。程序会把 `data/`、`.roadtrip/` 和 `trip.generated.js` 写入当前私人项目，不得写回 SkillSource。

## 支持的两种入口

### 指定目的地

接收起点、目的地、单程/往返、天数、必经城市、驾驶上限和偏好。最终默认输出一条完整往返环线；内部候选走廊可以比较，但不要把“去程二选一”误当成最终行程。

### 自由推荐

接收起点、天数、驾驶上限和偏好。先给出 2–3 个不同主题的方向，每个方向写清主题和适配理由；选定一个方向后再生成完整行程。

自由推荐请求必须包含：

- `selected_destination`
- 2–3 个 `destination_candidates`
- Agent 生成的 `driving_route_order`

## 第一步：整理请求

将用户自然语言写入 `data/trip-request.json`。至少确认：

- `request_id`：每趟旅行唯一。
- `origin`、`primary_destination` 或 `selected_destination`。
- `trip_mode`：`fixed_destination_oneway`、`fixed_destination_roundtrip` 或 `free_recommendation`。
- `duration_days`、出发日期和时间。
- 人数、实际驾驶员数量、车型或能源类型。
- 每日公里硬上限和舒适驾驶小时数。
- 必经/不去城市、最大绕路时间。
- 美食、自然、历史、地方文化、小众、避拥挤等偏好。

信息不全时采用保守值：单司机、每天最多 8 小时、跨城日不安排正式景点。不能凭空补车型、油耗、预约、营业或拥挤事实。

## 第二步：选择输入编制方式

### 自动蓝图

设置：

```json
{
  "planning_input_mode": "auto_blueprint",
  "driving_route_order": ["起点", "沿途落脚", "目的地", "返程落脚", "起点"]
}
```

执行器会自动生成：

- `data/route-blueprint.json`
- `data/candidate-query-plan.json`
- `data/community/query-plan.json`
- 空的路线级官方核验清单

Agent 应先设计尽量满足驾驶硬上限的 `driving_route_order`。高德实算后若仍有超限段，执行器会沿实际路线寻找行政区落脚点，释放同等数量的原停留日、自动拆段并重新核验。没有足够停留日可调整时必须停止，要求增加总天数或手工改线，不能静默延长行程。

使用 `stop_preferences` 分配停留日；未明确分配的剩余天数会放到主目的地。

### 人工精修蓝图

复杂环线、跨境公共交通衔接或已经研究过的走廊使用：

```json
{ "planning_input_mode": "manual_blueprint" }
```

此模式必须提供与 `request_id` 一致的路线蓝图、候选查询和社区查询计划。执行器会保留人工精修内容，不会覆盖。

## 路线通用规则

- 主路线必须连续，从 `origin` 开始。
- 指定目的地必须进入主行程。
- 往返模式必须回到 `return_to` 或起点。
- 驾驶段和停留日总数必须等于 `duration_days`。
- 完整环线默认只输出一个正式路线卡片。
- 路线比较必须包含至少两条不同的地点序列，不能只换文案。
- 除起点最终闭环外，不得无理由重复城市。
- 必须折返时，在 `allowed_revisits` 写明地点、原因和来源：

```json
{
  "place_name": "某城市",
  "reason": "用户明确要求再次停留探亲",
  "source": "user_required"
}
```

允许的来源只有 `user_required` 和 `route_constraint`。不得通过创建不同地点 ID 绕过重复检查。

自动蓝图模式默认开启自动拆段；仅在用户明确要求完全保留路线时设置 `auto_route_repair: false`。人工精修蓝图默认不改线，只有显式设置 `auto_route_repair: true` 才允许执行器调整。单段最多自动加入 3 个落脚点，可用 `max_auto_stopovers_per_segment` 在 1–5 之间调整。

## 可选任务

办事、探亲、购物、会议和体验预约统一使用 `optional_tasks`，不得为某一种任务写城市或任务 ID 特判。

```json
{
  "id": "unique-task-id",
  "title": "任务名称",
  "enabled": true,
  "city": "任务发生地",
  "host_city": "住宿或车辆所在城市",
  "transport_mode": "公共交通往返",
  "estimated_hours": 4,
  "appointment_confirmed": false,
  "time_window_reserved": true,
  "consume_dedicated_day": false,
  "failure_policy": "use_existing_free_time",
  "fallback_activity": "失败后恢复附近低强度游玩",
  "safety_note": "出发前复核官方要求"
}
```

只有已确认预约或明确预留时间窗的任务才能进入已有 `stay/rest` 日。找不到自由时段时必须标记为未排入，不能占用驾驶日或增加整天缓冲。

## 执行

软链接模式下，在私人项目根目录运行：

```bash
node .agents/skills/self-drive-planner/scripts/run-trip.mjs --skip-community
node .agents/skills/self-drive-planner/scripts/run-trip.mjs --community-only
node .agents/skills/self-drive-planner/scripts/run-trip.mjs --fresh
node .agents/skills/self-drive-planner/scripts/run-trip.mjs --status
```

如果使用安装器复制安装，且当前目录就是 Skill 目录，也可使用原有短命令：

```bash
# 先生成高德路线、天气、候选地点和基础地图路书
node scripts/run-trip.mjs --skip-community

# 复用本地登录态补充社区证据
node scripts/run-trip.mjs --community-only

# 或一次执行完整链路
node scripts/run-trip.mjs

# 出发日临近或距上次采集已久时，忽略断点强制重采天气与社区证据
node scripts/run-trip.mjs --fresh

# 查看断点与输入是否变化
node scripts/run-trip.mjs --status
```

生成路书后，需要用手机在同一局域网预览时，复制安装模式运行 `npm run preview:mobile`；源码池模式从私人项目根目录运行 `npm --prefix .agents/skills/self-drive-planner run preview:mobile`。把终端输出的网址和二维码交给用户，保持进程在前台；用户结束预览后按 `Control+C`，确认网址已经不可访问且没有遗留预览进程。不得使用公网隧道、云端静态托管或上传行程文件替代本地预览。

状态保存在私人工作区的 `.roadtrip/runs/<request-id>.json`。每个阶段同时指纹化数据输入和执行代码；需求或逻辑变化后必须自动重算，不得复用旧结果。

高德 Web 服务额度不可用时，允许复用共享 Chrome CDP 中的高德 JS API。只新建并关闭本次标签页，不得关闭共享浏览器。

## 社区证据

社区内容用于发现候选、停车、排队、拥挤和避坑信号，不能替代高德路线事实或官方规则。

1. B站使用只读公开搜索。
2. 小红书通过 OpenCLI Browser Bridge 复用用户已有登录态。
3. 不读取或导出 Cookie，不点赞、评论、收藏或发布。
4. 查询间隔至少 2.5 秒。
5. 验证码出现时立即暂停，等待用户处理，禁止绕过。
6. 每完成一个查询立即保存；网络错误有限重试。
7. 同一结论至少需要两个平台的独立来源，或同平台三个独立来源且包含评论证据。
8. 证据不足时只能标记“候选”或“单平台观察”，不能写成确定推荐。

美食优先级为中或高时，候选计划必须包含当地美食查询；具体店铺只有达到社区证据门槛后才能进入“吃什么”，否则只保留品类方向。纯电车需要同时查询落脚城市充电站，但地图候选不能替代沿途实时补能核验。

## 车辆与补能

读取 `vehicle.energy_type` 和 `vehicle.range_km`。已知续航时按保留 25% 安全余量估算每个驾驶日至少需要几次充电或加油，并写入逐日路书；未知时必须明确要求补充，不能假设车型或续航。补能次数只用于预留时间，具体服务区、接口、开放状态和备用站仍需出发前按实时导航确认。

## 事实分层

- 高德已核验：位置、距离、基础驾驶时间、收费估算。
- 天气预报：标明来源和更新时间，不能当长期气候事实。
- 社区交叉验证：只代表内容证据达到门槛，仍需 Agent 终审。
- 单平台观察：只能用于风险提示。
- 待补证：不得给具体店名或确定体验判断。
- 官方核验：营业、预约、口岸和事务要求必须保存官方来源与核验时间。

页面中的来源数量、候选数量和已交叉验证数量必须分别展示，不能合并成“全部真实”。

## 输出要求

最终交付：

- `index.html`：全屏可拖拽、缩放的真实地图。
- `trip.generated.js`：当前请求生成的数据层。
- 一条完整逐日行程，包含驾驶段、到达安排、停留、吃什么、玩什么和 Plan B。
- 地图时间轴和文字路书可点击、可滚动，移动端无横向溢出。
- 明确区分地图事实、社区证据、候选方向和未确认信息。

## 成品验收

验收分两级。

### 基础验收（任何环境必须通过）

```bash
node scripts/qa-all.mjs
```

`qa-all.mjs` 使用无密钥通用样例，依次运行请求校验、规划核心单测、韧性、断点状态、固定目的地/自由推荐冷启动和页面冒烟。除页面浏览器检查可以按条件跳过外，其余套件必须全部通过。生成真实行程后再运行 `node scripts/run-trip.mjs --status`，确认不存在 stale 或 failed 阶段。

发布真实路书前，复制安装模式运行 `npm run check:strict`；源码池模式从私人项目根目录运行 `ROADTRIP_WORKSPACE_DIR="$PWD" npm --prefix .agents/skills/self-drive-planner run check:strict`。严格模式下，缺少生成行程、Playwright 或共享 Chrome 都会失败，不得把 skipped 当成页面验收通过。

### 浏览器验收（覆盖条件 7、8）

qa-page-smoke 已包含在 qa-all 中：连接共享 Chrome，校验页面标题与时间轴同 `TRIP_DATA` 一致、375px 视口无横向滚动、无控制台错误。playwright-core 或共享 Chrome CDP 不可用、或行程尚未生成时，它会输出 skipped 并以 0 退出——此时条件 7、8 并未被真正验证，不能视为已通过。补齐条件 7、8 需在 Skill 根目录执行 `npm install`（提供 playwright-core）并接入共享 Chrome CDP（默认 `http://127.0.0.1:9222`）后重跑；逐站点点击与详情滚动仍需人工抽查。

只有同时满足以下条件才能宣布完成：

1. 请求和路线蓝图校验通过。
2. 所有驾驶段满足用户硬上限；若不满足，必须重新设计路线，不能只加警告。
3. 无理由重复城市检查通过。
4. 固定目的地和自由推荐两种模式通过。
5. 至少一条与当前示例完全无关的路线完成冷启动生成。
6. 通用生产生成器不包含示例城市或任务 ID 硬编码。
7. 桌面端所有站点可点击，详情可滚动到底；移动端无横向溢出。
8. 页面无控制台错误。
9. `--status` 不存在 stale 或 failed 阶段。
10. 登录、验证码、降级和待补证状态如实显示。

密钥只能保存在本地忽略文件中，禁止写进 HTML、日志、Git 或对话。
