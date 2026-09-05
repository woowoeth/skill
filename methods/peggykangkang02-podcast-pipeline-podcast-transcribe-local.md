---
name: podcast-transcribe-local
description: 把小宇宙、喜马拉雅播客单集（或任意音频文件/直链）在本地离线转成逐字稿，不联网、不烧 API 额度。本地 onnxruntime 跑 SenseVoiceSmall，Apple Silicon 实测 60-70 倍实时（一期 76 分钟播客约 70 秒转完，输出约 2.5 万字）。当用户给出小宇宙链接（xiaoyuzhoufm.com/episode/...）、喜马拉雅链接（ximalaya.com/sound/...）、音频文件或音频直链，想要逐字稿、转录、转文字、字幕时，使用本技能。也可作为 xiaoyuzhou-podcast-notes 的上游：先本地出逐字稿，再交给它生成结构化笔记落 Obsidian。
---

# 本地播客转录

给一条播客链接，本地跑出逐字稿。全程离线，不调任何云端 ASR，不消耗 API 额度。

## 为什么用它

- **免费无限**：跑在你自己机器上，没有额度、没有账单
- **中文更准**：SenseVoice 中文 CER 约 7.8%，Whisper large-v3 约 20%
- **快**：M 系列芯片 60-70 倍实时。76 分钟播客约 70 秒
- **双平台**：小宇宙 + 喜马拉雅都支持（这是云端那套做不到的）

## 环境准备（只需一次）

依赖已装在受管虚拟环境里，别用系统 Python：

```bash
VENV=~/.workbuddy/binaries/python/envs/default   # 你的 Python 环境；没装 WorkBuddy 就写 python3 所在路径
```

若 `funasr_onnx` 缺失，装一次（用国内源，约 80 秒）：

```bash
"$VENV/bin/python" -m pip install funasr-onnx onnxruntime av numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

模型已随技能自带（`models/`，231 MB），不需要联网下载。

> 不装 PyTorch。torch 体积大、下载慢，onnxruntime 版本效果一致且快得多。
> 不依赖系统 ffmpeg —— 用 PyAV 解码，ffmpeg 没装也能跑。

## 用法

```bash
VENV=~/.workbuddy/binaries/python/envs/default   # 你的 Python 环境；没装 WorkBuddy 就写 python3 所在路径
SK=~/.workbuddy/skills/podcast-transcribe-local

# 小宇宙
"$VENV/bin/python" "$SK/scripts/transcribe.py" "https://www.xiaoyuzhoufm.com/episode/<id>" --out ./_work

# 喜马拉雅
"$VENV/bin/python" "$SK/scripts/transcribe.py" "https://www.ximalaya.com/sound/<id>" --out ./_work

# 本地音频文件 / 音频直链
"$VENV/bin/python" "$SK/scripts/transcribe.py" ./audio.m4a --out ./_work

# 先试跑前 2 分钟确认效果
"$VENV/bin/python" "$SK/scripts/transcribe.py" "<链接>" --out ./_work --max-seconds 120
```

### 参数

| 参数 | 说明 |
|---|---|
| `--out DIR` | 输出目录，默认 `./_work` |
| `--max-seconds N` | 只转前 N 秒，试跑用 |
| `--window N` | 切分窗口秒数，默认 20（实测最优，别乱改） |
| `--json` | 只输出 JSON 摘要，不打印正文 |

### 产物

| 文件 | 内容 |
|---|---|
| `_work/transcript.txt` | 纯文本逐字稿，**无标点** |
| `_work/transcript.srt` | 带时间戳字幕 |
| `_work/meta.json` | 平台、节目、标题、主播、时长、播放量、链接 |

## 关键实现细节（踩过的坑，别改回去）

1. **不要用 VAD 切分。** `funasr-onnx` 的 `Fsmn_vad` 在长音频上有缺陷——600 秒音频只切出前 37 秒的段，会静默丢掉 90% 内容。改用**固定 20 秒窗口**切分，实测输出量是 VAD 方案的 17 倍，且准确率更高。

2. **不要整段喂长音频。** 整段喂 600 秒虽然覆盖完整，但 SenseVoice 注意力退化，尾部输出明显错乱，且慢（5.8x 实时 vs 窗口切分 68.9x）。

3. **20 秒窗口优于 30 秒。** 同样 600 秒音频，20s 窗口 68.9x 实时，30s 窗口 61.3x，且 20s 的中英混排识别更准（KOL 不会识别成 q l）。

4. **标点模型已装，免费离线加标点。** 早期判断 onnx 标点模型 270-965 MB 太大没装，后来实测 `iic/punc_ct-transformer_zh-cn-common-vocab272727-onnx`（282 MB）值得装，已放在 `models/punc/`。用 `punctuate.py` 加标点，不联网不花钱（见下节）。中英混排的英文部分标点可能略不准，不影响阅读。

5. **喜马拉雅用移动端接口**：`m.ximalaya.com/tracks/<id>.json` 一次拿全元数据 + 播放量 + 音频直链，网页版 sound 页反而抓不到。

6. **Range 分段下载会损坏 AAC 帧**，PyAV 报 `Input buffer exhausted`。必须整文件下载。

## 加标点（免费离线）

转录产物 `transcript.txt/srt` 是**不带标点**的连续文本。用自带标点模型离线加标点：

```bash
VENV=~/.workbuddy/binaries/python/envs/default   # 你的 Python 环境；没装 WorkBuddy 就写 python3 所在路径
SK=~/.workbuddy/skills/podcast-transcribe-local
"$VENV/bin/python" "$SK/scripts/punctuate.py" --work-dir ./_work
```

产出：
| 文件 | 内容 |
|---|---|
| `_work/punctuated.txt` | 带标点的逐字稿，按块分段、段首有时间戳 |
| `_work/punctuated.srt` | 合并块级字幕，带标点 |
| `_work/chapters.txt` | 每 5 分钟一个时间标记 + 该段首句，写章节纪要用 |

参数：`--skip-head 30`（丢弃开头片头秒数）、`--block-chars 180`（每块约多少字）、`--chapter-min 5`（章节间隔分钟）。脚本自动跳过片头音乐段、合并字幕块、按时间戳切章节。

## 后续：接笔记流程

逐字稿出来后，交给 `xiaoyuzhou-podcast-notes` 生成结构化笔记落 Obsidian。它支持"已有转录文本"的入口——跳过它的转录步骤，直接：

```bash
"$VENV/bin/python" ~/.workbuddy/skills/xiaoyuzhou-podcast-notes/scripts/publish_to_vault.py \
    --meta ./_work --note ./note.md --transcript ./_work/transcript.txt --slug "四到六字简称"
```

喜马拉雅的元数据字段与小宇宙略有差异（`pub_date` 为空），落库前补一下日期。

## 已知限制

- **只识别不总结**：本技能只出逐字稿，总结和笔记由下游完成
- **无标点**：输出是不带标点的连续文本，需要 LLM 后处理
- **片头音乐段会识别成乱码**：SenseVoice 对音乐片段输出 `🎼` 标签和噪声文字，可丢弃开头 30 秒
- **付费内容拿不到音频直链**
