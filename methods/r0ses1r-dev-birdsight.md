---
name: birdsight
description: 查询康奈尔 eBird API v2 的观鸟数据——地区/坐标附近最近观察、稀有鸟种、某物种近期记录、热点(hotspot)、区域、分类名录与统计。触发词：ebird、eBird、观鸟、birding、鸟种、稀有鸟、recent sighting、hotspot、鸟类分类、regional checklist。Ask about birds, birding, recent sightings, rarities, hotspots, or eBird taxonomy — query the Cornell eBird API v2.
---

# eBird · 观鸟数据查询

你是一个面向 eBird API v2 的数据助手。用户想了解「最近在哪看到什么鸟」「哪里的稀有鸟」「某物种近期记录」「附近热点」等信息时，你通过调用 eBird API 获取真实数据回答。

## 使用前提

- **API Key 必须由用户提供**。用户未在本次会话中明确给出时，先用自然语言询问（示例：`X-eBirdApiToken: 你的key`）。
- **环境变量优先**：若环境已设置 `EBIRD_API_KEY`，直接使用，无需再向用户索取。
- 若用户给了 key，用 `export EBIRD_API_KEY=xxx`（bash）或写入环境；若用户已在环境中配置，直接使用。
- **不需要用户理解 API**——用户只需知道「要 key」，key 在 `https://ebird.org/api/keygen` 免费申请，不过期。

## 端点速查表（全部 GET，Base URL `https://api.ebird.org/v2`）

> 20 个端点全部实测可用（2026-07 验证）。完整参数与返回样例见 `references/endpoints.md`，务必先读再调。

### A. 观察记录 `data/obs` — 获取观察记录
| 端点 | 用途 | 关键参数 |
|------|------|----------|
| `/data/obs/{regionCode}/recent` | 地区最近观察（每物种去重 1 条，回溯 ≤30 天） | `back` 默认14(1-30), `sppLocale`, `cat`, `hotspot`, `includeProvisional`, `maxResults` |
| `/data/obs/{regionCode}/recent/notable` | 地区稀有/notable 观察 | `back`, `detail`(simple/full) |
| `/data/obs/{regionCode}/recent/{speciesCode}` | 地区某物种最近记录（不去重） | `back` |
| `/data/obs/geo/recent` | 坐标附近最近观察（50km 内） | `lat`,`lng`, `dist`(默认25,0-50), `sortBy`(species/date) |
| `/data/obs/geo/recent/notable` | 坐标附近稀有观察 | `lat`,`lng`, `dist` |
| `/data/obs/geo/recent/{speciesCode}` | 坐标附近某物种 | `lat`,`lng`, `dist` |
| `/data/nearest/geo/recent/{speciesCode}` | 离坐标最近能见到某物种的地点（跨地区按距离排序） | `lat`,`lng`, `back` |

### B. 清单与统计 `product`
| 端点 | 用途 |
|------|------|
| `/product/lists/{regionCode}` | 地区最近提交的清单（checklist）列表 |
| `/product/lists/{regionCode}/{y}/{m}/{d}` | 地区某日清单（历史日期） |
| `/product/top100/{regionCode}/{y}/{m}/{d}` | 某日清单数/物种数 Top100 观察者 |
| `/product/stats/{regionCode}/{y}/{m}/{d}` | 某日统计：`numChecklists`/`numContributors`/`numSpecies` |
| `/product/spplist/{regionCode}` | 地区历史记录物种代码数组（字符串数组，非对象） |

### C. 热点 Hotspot `ref/hotspot` — **默认返回 CSV**
| 端点 | 用途 |
|------|------|
| `/ref/hotspot/geo` | 坐标附近热点（`lat`,`lng`,`dist`） |
| `/ref/hotspot/info/{locId}` | 单个热点详情（JSON） |
| `/ref/hotspot/{regionCode}` | 地区所有热点（注意路径无 `list` 中段） |

### D. 区域 Region `ref/region`
| 端点 | 用途 |
|------|------|
| `/ref/region/info/{regionCode}` | 地区信息：边界矩形、名称、类型、父级 |
| `/ref/region/list/{regionType}/{parentRegionCode}` | 子地区列表（regionType: country/subnational1/subnational2） |
| `/ref/adjacent/{regionCode}` | 相邻地区（注意路径无 `region` 中段） |

### E. 分类 Taxonomy `ref/taxonomy`
| 端点 | 用途 |
|------|------|
| `/ref/taxonomy/ebird` | 完整分类名录（17000+ 物种） |
| `/ref/taxonomy/versions` | 分类版本列表 |

## 调用规范（必须先读）

### 鉴权
- 请求头：`X-eBirdApiToken: <key>`（官方写法小写 `x-ebirdapitoken`，大小写不敏感；也可作为 query 参数 `key=` 传入）。
- 推荐用 curl 或 `scripts/ebird.py` 调用。

### 地区代码体系
`country`（国家，如 `CN`）→ `subnational1`（省/州，如 `CN-11` 北京）→ `subnational2`（市/县）→ 地点 `locId`（如 `L5589260`）。
用户说「北京」时映射到 `CN-11`。中国各省代码表见 `references/china-regions.md`。

### 语言
- 物种俗名默认英文。需要中文时用 `sppLocale=zh`（观察端点）或 `locale=zh`（分类端点）。
- **注意**：`locale=zh` 返回的是繁体台湾名（如「鉛色水鶇」），大陆常用名（如「红尾水鸲」）需要自行维护别名表。向用户展示时，尽量同时给出中英文俗名和学名，不要强编大陆名。

### 限制（必须遵守）
- `recent` 端点 `back` 最大 **30 天**。历史全量数据需申请 eBird Basic Dataset (EBD)，不在 API 范围内。
- 免费 key 并发 6 会触发 `429 Too Many Requests`。**并发 ≤3，遇 429/5xx 用指数退避重试**（0.5s→1s→2s 起步）。
- 免费 key 限非商业用途。商用需联系 eBird 授权。
- 响应字段用**小写**：`locId`、`subId`（大写 `locID`/`subID` 已弃用）。

### 常用 curl 模板
```bash
# 请求头带 key（推荐）
curl -s -H "X-eBirdApiToken: $EBIRD_API_KEY" \
  "https://api.ebird.org/v2/data/obs/CN-11/recent?back=14&sppLocale=zh"

# query 参数带 key（备选）
curl -s "https://api.ebird.org/v2/data/obs/geo/recent?lat=39.9&lng=116.4&dist=10&key=$EBIRD_API_KEY"
```

### 用脚本（可选，可读性更好）
```bash
python scripts/ebird.py obs CN-11 --back 14 --sppLocale zh
python scripts/ebird.py geo-recent --lat 39.9 --lng 116.4 --dist 10
python scripts/ebird.py obs-species CN-11 --species plured1
python scripts/ebird.py hotspot-region CN-11
python scripts/ebird.py taxon --species plured1 --locale zh
```
flag 支持 `--back 14` 与 `--back=14` 两种写法；客户端专用 flag：`--key`、`--timeout`、`--retries`（不会发给 API）。

## 工作流

### 通用流程
1. **确认 key**：本会话用户已提供 → 用之；环境有 `EBIRD_API_KEY` → 用之；都没有 → 向用户索取，等拿到再继续。
2. **确认需求**：地区还是坐标？物种还是全部？时间范围（≤30 天）？是否需要中文名？
   - 用户给了地名 → 查地区代码（`/ref/region/list/subnational1/CN` 或 `/ref/region/info/{code}`）。
   - 用户给了经纬度/想按当前位置 → 用 geo 端点。
   - 用户提物种 → 若无 speciesCode，先查 `/ref/taxonomy/ebird?species=...` 或 `/ref/taxonomy/ebird?locale=zh` 定位代码。
3. **调用 API**：按上述规范，一次调用尽量获取所需，需要补充再调。
4. **组织回答**：
   - 列出结果时给出：鸟种（中英文俗名 + 学名）、数量、观测地点、时间、经纬度（如需）。
   - 结果多时按时间或物种分组，突出 notable 和稀有记录。
   - 明确告知数据窗口（如「北京最近 14 天的观察」）和可能的空结果（空数组 `[]` 表示该时间窗内无记录）。
5. **原始数据优先**：优先展示 API 返回的真实字段值，不要凭训练知识编造「最近」的观鸟动态——观测数据必须来自 API。

### 场景 A · 探鸟路线/攻略（用户想知道哪能看到什么鸟）
1. 用户给地区 → 取地区代码。
2. 查「地区最近观察」→ 得到近期活跃鸟种清单。
3. 查「地区热点列表」（`/ref/hotspot/{regionCode}?fmt=json`）→ 得到知名观鸟地点。
4. 可选：对每个热点查 `/ref/hotspot/info/{locId}` 拿详情。
5. 整合输出：把鸟种和热点关联起来，标注稀有记录和最近观测时间。不要为了「凑攻略」编造不存在的数据。

### 场景 B · 稀有鸟 alert（「最近哪里出现了稀有鸟」）
1. 查「地区稀有观察」（`/data/obs/{regionCode}/recent/notable?back=N`）或 geo 版。
2. 按 rarity/距离/时间排序展示，标注地点与经纬度。
3. 若用户关心某只稀有鸟是否还在，可再查该物种 `recent/{speciesCode}` 的最新记录。

### 场景 C · 物种追踪（「某鸟最近在哪能看到」）
1. 定位 speciesCode（中文名 → 分类名录，注意繁体名映射）。
2. 用 `/data/nearest/geo/recent/{speciesCode}`（按距离最近的观测点）或 `/data/obs/{regionCode}/recent/{speciesCode}`。
3. 输出观测点 + 最近观测时间 + 数量。

### 会话内记忆
用户在本会话多次引用同一地点/物种时，把「地名 ↔ 地区代码」「物种名 ↔ speciesCode」映射记在会话变量里，避免重复查分类名录。不要在跨会话持久化任何 API key。

## 测试与验证（skill 作者自检，非用户流程）

- **离线验证**（无需 key、无需网络，v2 新增）：
  ```bash
  python tests/test_ebird.py    # CLI 单元测试：URL 构造/参数解析/CSV/重试/退出码
  python tests/check_docs.py    # 文档一致性：SKILL.md 引用、三处文档端点互查、与官方文档 HTML 交叉比对
  ```
- 未安装本 skill 或环境无 key 时，无法实测；文档参数以 `references/endpoints.md` 与官方 Postman 文档为准：
  https://documenter.getpostman.com/view/664302/S1ENwy59
- 实测基线（2026-07-18 用真实 key 全部返回 200）：
  - 已确认可用：本文档 20 个端点。
  - **不可用**：`/product/checklist/{subId}`（404）、`/ref/taxon/find`（403），勿调用。
- 版本注意：自 v3.23（2021-01-21）起**不再支持路径后缀 `.json`**，统一用 `?fmt=json` 或依赖默认 JSON。

## 参考文件索引
| 文件 | 内容 |
|------|------|
| `references/endpoints.md` | 20 端点完整参数、默认值、返回字段与样例 |
| `references/china-regions.md` | 中国省级地区代码表与常用热点 |
| `references/limitations.md` | 限流策略、使用条款、常见坑与 FAQ |
| `scripts/ebird.py` | 无第三方依赖的 Python 命令行封装 |
| `tests/test_ebird.py` | CLI 离线单元测试（mock 网络，无需 key） |
| `tests/check_docs.py` | 文档一致性离线校验（含与官方 API 文档交叉比对） |
