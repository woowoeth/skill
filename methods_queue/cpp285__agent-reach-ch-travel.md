---
name: agent-reach-ch-travel
description: >
  MUST USE when the user wants to research 国内旅居/去某地住一段时间/租房/房租/
  天气/周边设施/生活成本 in China — e.g. 我想去大理旅居 / 帮我查一下成都的房租 /
  那个城市冬天冷不冷 / 附近有没有菜市场和医院 / 一个月要花多少钱。

  只读公开入口、无需登录，全程无封号风险。用 ch-travel 命令或
  agent_reach_ch_travel Python 包获取内容。

  NOT for: 小红书/推特/Reddit/Facebook/Instagram 等需登录态的平台（有封号风险，
  用主项目 agent-reach 并配专用小号）；发帖/评论等写操作；海外城市调研。
metadata:
  homepage: https://github.com/Panniantong/agent-reach
---

# 中文旅居检索（ch-travel）

针对「去国内某地旅居/短住」的只读调研，**无登录、无封号风险**。

## 常驻规则

1. **只走公开入口**：Jina Reader、bili-cli / B站公开 API、feedparser、中国天气网。不碰 Cookie、不登录。
2. **声明你在用什么**：开工前说一句「使用 ch-travel 的 XX 检索」。
3. **先 B站圈片区，再定向读页面**：B站实地视频最真实，先搜视频锁定片区，再用 rent/weather/facilities 定向读该片区。

## 命令速查

```bash
# 房租（豆瓣小组最易读；贝壳/安居客被反爬拦时降级到豆瓣/知乎/政府官网）
ch-travel rent 大理 -k 月租

# 天气（城市名或代码）
ch-travel weather 大理

# 周边设施（best-effort；体感信息优先用 bili）
ch-travel facilities 大理 菜市场

# B站实地体验（无需登录，信息密度最高）
ch-travel bili "大理旅居 房租"

# 通用网页 / RSS
ch-travel read "URL"
ch-travel feeds "RSS_URL"
```

## 降级链（失败时按序执行，拿到非空内容即停）

- **房租**：豆瓣租房小组 → 安居客 → 贝壳/链家；再不行读知乎/公众号/政府官网 URL。
- **天气**：中国天气网城市名 → 直接城市代码；长期气候叠加 B站「XX 冬天」视频。
- **设施**：大众点评被拦 → `ch-travel bili "城市 菜市场/医院/交通"`。
- **B站**：`bili` 未装 → `bilibili_search_api`（CLI 已自动降级）。

## 详细参考

- 全部命令与城市代码表见 `README.md`。
- Python API：`from agent_reach_ch_travel import rent, weather, facilities, experience, web, feeds`。
