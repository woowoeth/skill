# 原料库 / Materials

**这里的东西不是 skill，不上货架。** 但它们是做 skill 的好原料 —— 数据集、模型、素材库。
收在这里是为了不丢掉，也为了将来做自制 skill 时有底座可用。

判断标准：**clone 下来放进 `~/.claude/skills` 什么都不会发生的东西，就不该上货架** —— 但可以进这里。

| 名字 | 是什么 | 能拿来做什么 | 注意 |
|---|---|---|---|
| [hasaneyldrm/exercises-dataset](https://github.com/hasaneyldrm/exercises-dataset) ★20k | 1324 个健身动作数据集：动画 GIF、180×180 缩略图、肌群与器械数据、六语言分步说明，128MB | 做健身类 skill 的现成动作库（「排一周训练计划并配演示图」）。自己攒这套要很久 | **License 是 NOASSERTION**，带 NOTICE.md，商用前要先弄清授权 |
| [unstonio/pixelgpt-24x24](https://github.com/unstonio/pixelgpt-24x24) ★65 | 68M 参数的本地 24×24 像素图生成模型，RTX 5090 上 30 分钟训练完，逐像素预测调色板索引 | 我们的 pixelpad 就是学它的内核机制（不降采样、直接落索引）另走一条路实现的 | 是模型+网页 demo，无 SKILL.md |
| [unstonio/pixelGPT-autoresearch](https://github.com/unstonio/pixelGPT-autoresearch) | 用 VLM 反馈做自主训练调优 | pixelpad 的「渲染→看→改」回环设计参考了它 | 训练脚本，非 skill |

## 用法

看到有价值但不是 skill 的东西 → 记这里，不要塞进货架。
将来要做自制 skill（像 pixelpad 那样）时，先翻这份表看有没有现成底座。
