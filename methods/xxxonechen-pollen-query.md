---
name: pollen-query
description: 查询花粉浓度及过敏指数。通过中国天气网(graph.weatherdt.com API)获取花粉浓度等级、过敏风险提示和7天历史+预报数据，uapis.cn API 作为备用数据源。适用于用户询问花粉浓度、花粉过敏风险、过敏指数、花粉预报等场景。触发词：花粉浓度、花粉指数、过敏指数、花粉预报、pollen、过敏风险。
agent_created: true
---

# Pollen Query - 花粉浓度查询

## Overview

查询指定城市的花粉浓度等级、过敏风险提示和历史7天+明日预报数据。主数据源为中国天气网花粉 API（graph.weatherdt.com），备用数据源为 uapis.cn 免费 API。仅依赖 Python 标准库，无需安装第三方包。

## 使用场景

- 用户询问某城市花粉浓度/花粉指数
- 用户询问过敏风险/过敏指数
- 用户计划出行，想了解目的地花粉情况
- 花粉过敏人群需要每日防护参考

## 支持的城市

花粉监测站覆盖53个城市，完整列表见 `references/city_codes.md`。主要包括：
北京、上海、广州、深圳、杭州、成都、武汉、西安、重庆、天津、南京、哈尔滨、沈阳、长春、济南、郑州、长沙、南昌、福州、昆明、贵阳、南宁、海口、拉萨、乌鲁木齐、呼和浩特、银川、西宁、兰州等。

不在列表中的城市无法查询花粉浓度数据。

## 查询流程

### Step 1: 执行查询

通过城市名查询（推荐）：

```bash
python scripts/pollen_query.py --city 北京
```

也支持英文城市名或9位城市代码：

```bash
python scripts/pollen_query.py --city-code beijing
python scripts/pollen_query.py --city-code 101010100
```

指定数据源：

```bash
python scripts/pollen_query.py --city 北京 --source weather_cn
python scripts/pollen_query.py --city 北京 --source uapis
```

脚本会优先使用天气网 API，失败时自动切换到 uapis.cn。

### Step 2: 解读结果

脚本输出 JSON 格式数据。

**主数据源（graph.weatherdt.com）返回示例：**
```json
{
  "source": "weather.com.cn",
  "city": "北京",
  "season": "夏秋",
  "pollen_levels": [
    {"date": "2026-08-15", "display_date": "08/15(星期六)", "level": "中", "level_code": 3, "advice": "易引发过敏，加强防护，对症用药。", "label": "明天预报"},
    {"date": "2026-08-14", "display_date": "08/14(星期五)", "level": "中", "level_code": 3, "advice": "易引发过敏，加强防护，对症用药。", "label": "今日实况"},
    {"date": "2026-08-13", "display_date": "08/13(星期四)", "level": "中", "level_code": 3, "advice": "易引发过敏，加强防护，对症用药。"}
  ],
  "legend": [
    {"level": "未检测到花粉", "minNum": 0, "maxNum": 0},
    {"level": "很低", "minNum": 1, "maxNum": 20},
    {"level": "低", "minNum": 21, "maxNum": 60},
    {"level": "中", "minNum": 61, "maxNum": 170},
    {"level": "高", "minNum": 171, "maxNum": 390},
    {"level": "很高", "minNum": 391, "maxNum": ""}
  ]
}
```

关键字段说明：
- `pollen_levels[0]`：明天预报（有 `label: "明天预报"`）
- `pollen_levels[1]`：今日实况（有 `label: "今日实况"`）
- `pollen_levels[2+]`：过去7天历史数据
- `level_code`：-1 表示暂无数据，0=未检测到，1=很低，2=低，3=中，4=高，5=很高
- `legend`：花粉等级图例，含数值范围（粒/千平方毫米）

**备用数据源（uapis.cn）返回示例：**
```json
{
  "source": "uapis.cn",
  "city": "北京",
  "pollen": {"level": "较低", "brief": "不易发", "advice": "花粉浓度较低"},
  "allergy": {"level": "较低", "brief": "不易发", "advice": "过敏风险较低"}
}
```

### Step 3: 向用户呈现结果

将 JSON 结果转换为易读的文本格式，包含：
1. 当前花粉浓度等级及数值范围（从 legend 中查找对应范围）
2. 过敏风险提示（advice 字段）
3. 明日预报趋势
4. 过去7天历史趋势（可选）
5. 防护建议

## 注意事项

- 天气网花粉数据仅覆盖53个有监测站的城市，小城市无数据
- 花粉浓度数据有季节性，非花粉季可能显示"暂无"或"未检测到花粉"
- 部分城市某些日期可能无数据（level_code 为 -1），属正常现象
- uapis.cn 备用数据源提供的是花粉扩散指数，非具体浓度值
- API 需要设置 `Referer: https://www.weather.com.cn` 请求头，脚本已处理
