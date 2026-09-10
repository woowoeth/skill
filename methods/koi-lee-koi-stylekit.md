---
name: koi-stylekit
description: 按 Koi StyleKit 的风格目录选择画风并生成可复用的中文插画提示词，适用于用户希望统一配图画风或导出风格配方时。
---

# Koi StyleKit

在本技能目录运行 `python3 scripts/koi.py list` 查看风格。用户没选风格时展示目录与对应样图位置；保留用户明确选择。

生成示例：
```sh
python3 scripts/koi.py render --style duotone-print --subject '女孩给猫撑伞' --format text
```

用途通过 `--purpose single|explain|cover` 指定；只有用户指定比例时才传 `--aspect`。默认 JSON 含配方版本与验证状态，方便记录。主题作为数据安全传入命令，不能直接拼接未经转义的 shell 字符串。

配方唯一来源是 `wireframes/styles.json`，不要凭记忆替换它。配方保留实测文本；淡彩强调物由雨伞泛化为关键物体，跨主题稳定性尚未验证；不要保证输出与样图相同。默认输出提示词，不调用生图服务、不发布内容。用户明确要求生图时使用当前可用图像工具并保留实际请求和验证状态。

此技能需要完整仓库目录；不要只安装 SKILL.md。英文翻译、参考图输入和 MCP 尚未实现。

## 配色与统一导出

JSON schema 为 koi-stylekit.v0.2。颜色词可能冲突时默认不生成提示词，退出码 2，status 为 needs_color_choice。向用户说明固定配色与主题颜色的取舍；已有明确选择时直接使用 `--color-policy style` 或 `--color-policy subject`。保留主题颜色是未验证变体。检测仅匹配部分颜色词，不能保证发现所有冲突。标题通过 `--caption` 独立导出，不加入绘图文字要求。

网页可使用普通静态服务器运行，浏览器与 CLI 共用配方目录和 render-rules.json，跨运行时对照测试以 Python 渲染器为基准。Agent 继续使用本地 Python CLI；无需构建网页版。
