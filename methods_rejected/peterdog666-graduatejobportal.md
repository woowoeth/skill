---
name: graduate-job-portal
description: >
  一键生成「校园应届生求职服务全栈官网」完整工程化项目。
  包含首页落地页、登录注册、岗位列表/详情、Offer智能对比、入职材料清单等全功能模块。
  UI为现代科技风（渐变+卡片+动效），全响应式，工程级代码规范，支持二次开发。
  author: WorkBuddy User
  agent_created: true
  version: "1.0.0"
  tags: [website-generator, campus-recruitment, job-portal, frontend]
---

# Graduate Job Portal - 应届生求职服务官网生成器

## 触发条件

当用户提到以下意图时，触发此 Skill：
- "生成应届生求职网站" / "创建校园招聘平台"
- "一键生成求职服务官网" / "帮我做一个求职网站"
- "graduation job portal" / "campus recruitment website"
- 任何涉及「应届生 / 校招 / 求职平台 / 招聘网站」的生成请求

---

## 执行指令

触发后，**立即**将 `<skill_dir>/template/` 目录下的所有文件
复制到用户指定的输出目录（默认 `./graduate-job-portal/`）。

如果用户没有指定输出目录，询问后使用默认路径。

复制完成后告知用户：
1. 项目文件位置
2. 用浏览器直接打开 `index.html` 即可预览
3. CSS 变量集中在 `style.css:root` 中，修改即可换主题色
4. 可上传至 GitHub Pages / Vercel 免费托管

---

## 模板文件目录结构

```
<template>/
├── index.html
├── login.html
├── register.html
├── jobs.html
├── job-detail.html
├── offer-compare.html
├── onboarding.html
├── css/
│   ├── style.css
│   ├── index.css
│   ├── auth.css
│   ├── jobs.css
│   ├── job-detail.css
│   ├── offer-compare.css
│   └── onboarding.css
└── js/
    ├── main.js
    ├── index.js
    ├── jobs.js
    ├── offer-compare.js
    └── onboarding.js
```

---

## 设计规范（供二次开发参考）

| 变量 | 色值 | 用途 |
|------|------|------|
| `--primary` | `#4f6ef7` | 主色调（科技蓝） |
| `--accent` | `#00d4ff` | 强调色（青蓝） |
| `--accent-secondary` | `#a855f7` | 辅助色（紫色） |
| `--bg-primary` | `#0a0e27` | 主背景（深蓝黑） |
| `--bg-card` | `rgba(20,30,80,0.65)` | 卡片背景（玻璃态） |

### 圆角规范
- `--radius-sm: 8px` — 按钮、输入框
- `--radius-md: 16px` — 卡片
- `--radius-lg: 24px` — Hero 区
- `--radius-full: 9999px` — 标签、徽章

### 响应式断点
- `768px` — 移动端（单列、汉堡菜单）
- `1024px` — 平板（卡片 2 列）

---

## 各页面功能说明

| 文件 | 功能 |
|------|------|
| `index.html` | 首页：Hero、轮播公告、6大服务卡片、求职时间线、CTA |
| `login.html` | 登录：表单验证、密码显示切换、社交登录入口 |
| `register.html` | 注册：密码强度检测、确认密码、用户协议勾选 |
| `jobs.html` | 岗位列表：城市/类型筛选、标签筛选、薪资/日期排序、分页加载 |
| `job-detail.html` | 岗位详情：描述、要求、福利、公司介绍、侧边栏 |
| `offer-compare.html` | Offer对比：多维打分、对比表格、智能推荐 |
| `onboarding.html` | 入职清单：按公司类型分类、勾选进度、打印 |
