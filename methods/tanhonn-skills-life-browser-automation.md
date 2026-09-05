---
name: life-browser-automation
description: 用于在用户授权并已准备的浏览器页面中，为需要循环等待、低频重试或持续监控的页面任务编写、执行并调整 Playwright 自动化脚本。适用于等待名额、余量、开放入口、可点击状态或其他页面状态变化的场景。
---

# 浏览器循环任务自动化

## 核心流程

1. 判断任务适用性: 按 [任务契约规则](references/task-contract.md) 判断本轮是否进入脚本流程；一次性填表、简单点击或普通页面操作直接使用浏览器操作能力处理。
2. 建立任务契约: 按 [任务契约规则](references/task-contract.md) 确认通用页面接管边界、目标任务、状态信号、重试策略、允许动作、暂停条件和人工接管点。
3. 编写 Playwright 脚本: 按 [Playwright 循环规则](references/playwright-loop.md) 生成任务专用脚本，只通过页面级交互完成低频观察和重试。
4. 执行、监控与修复: 按 [监控修正规则](references/monitoring-and-repair.md) 运行脚本、读取日志和截图；遇到异常时暂停脚本，分析原因并调整脚本。
