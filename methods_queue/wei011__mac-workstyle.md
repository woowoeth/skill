---
name: mac-workstyle
description: 读 macOS 自带的 pmset 电源日志，算出用户真实的开合盖作息——首次开盖/末次合盖时刻、下班后工作占比、深夜与周末工作率，并对照《劳动法》36/41 条折算月加班倍数。当用户问"我到底每天工作多久""帮我看看我的作息""我是不是在隐形加班""分析我的电脑使用时间"时使用。
---

# mac-workstyle

用 `pmset -g log`（macOS 自带，无需权限、不联网）还原用户真实作息。

## 怎么跑

```bash
python3 workstyle.py --scan          # 扫本机
python3 workstyle.py --demo          # 样本数据（非 macOS 也能跑）
python3 workstyle.py --scan --json   # JSON，便于二次加工
python3 workstyle.py --scan --ai     # 追加大模型解读，需 ANTHROPIC_API_KEY
```

## 解读要点

- **`workday.avg_span_hours` 减 `avg_active_hours`** 是"在岗但没在用"的空隙，午休 + 会议多半藏在这。
- **`totals.off_hours_share`** 超过 30% 是关键信号：问题不是干得久，是**什么时候都在干**。
- **`legal.cap_multiple`** 是月加班对法定 36 小时上限的倍数，≥2 要直接点出"这是超载不是勤奋"。
- **`range.days_covered < 7`** 时必须提醒样本太小，只看结构别看绝对值。

## 三条一定要跟用户说清楚的口径

1. 统计的是**电脑醒着**，不是**在工作**——追剧和写代码它分不清。
2. pmset 日志只留最近一两周，长期不合盖的机器事件天然稀少。
3. 数据全程本地计算；只有 `--ai` 时才会把**汇总数字**（非逐条流水）发给模型。

不要拿这份报告替用户下"你被剥削了"的结论，把数字给他，让他自己判断。
