---
name: cantonese-transcribe
description: |
  把粤语播客/音频转成带粤拼注音的文稿。触发词:"粤语转文稿"、"转粤语文稿"、
  "粤语转文字"、或用户给一个粤语音频文件/文件夹/播客链接(小宇宙、YouTube 等)
  并要求转成文稿、字幕、逐字稿时使用。
  全程本地运行(FunASR SenseVoice 识别 + ct-punc 断句加标点 + ToJyutping 粤拼注音),
  不上传音频、不依赖任何外部大模型 API。输出一句一行的 md 文稿(配粤拼)
  和一份手机能直接打开的排版 PDF。
allowed-tools:
  - Bash
  - Read
metadata:
  trigger: 粤语音频/播客链接转文稿
  home: ~/.claude/skills/cantonese-transcribe
---

# 粤语转文稿

给一个音频文件、装满音频的文件夹,或播客/视频链接(小宇宙、YouTube 等),
输出:

- `xxx.md`  一句一行的文稿,每句下面配一行粤拼注音
- `xxx.pdf` 同样内容排好版,手机直接打开就能看

引擎全部跑在用户自己电脑上:SenseVoiceSmall(粤语专门识别)+ FSMN-VAD(切句)
+ ct-punc(标点恢复,统一重新加标点比 ASR 自带的准)+ ToJyutping(粤拼注音,
基于 rime-cantonese 词库)。**不要**另外调用任何在线大模型 API 来做断句或翻译——
断句这一步已经由本地的 ct-punc 模型完成,足够准,也是这个 skill 能跨模型复用、
不依赖 Claude 本身语言能力的关键设计。

具体断句/排版规则已经写死在 `transcribe_cantonese.py` 里,不要另起炉灶用别的方式
重新分句:

- 先去掉 ASR 自带的粗糙标点,交给 ct-punc 统一重新加
- 严格按句末标点(。！？!?)切句,逗号不算句末
- 超过 30 字的整句,排版时才在逗号处折行(不算独立句子,折行间不空行,句间才空行)
- 每句配一行斜体粤拼
- 自动去掉 SenseVoice 输出里夹带的表情符号(😊🎼等)
- 只产出 md + pdf,不产出 txt/srt
- 转写时会自动套用 `corrections.txt`(错字词纠正)和 `jyutping_overrides.txt`
  (多音字粤拼覆盖),这两个表用户可能会持续手动编辑积累,不要清空或覆盖它们

## 用户反馈"这个字听错了/粤拼不对"时怎么办

不要凭空替用户猜改哪个词。引导用户把正确写法加进 `corrections.txt`
(`错字词 => 正确字词`)或 `jyutping_overrides.txt`(`词 :: 音节 音节 ...`),
然后用下面这条重新生成,不用重跑识别(省几分钟):
```
cd ~/.claude/skills/cantonese-transcribe
source .venv/bin/activate
python transcribe_cantonese.py --resync "<对应的 .md 路径>"
```
第一次 resync 会自动存一份 `.md.bak` 备份。

## 执行步骤

1. **确认环境**(第一次用才需要,已经装过就跳过):
   ```
   cd ~/.claude/skills/cantonese-transcribe
   which ffmpeg || brew install ffmpeg
   test -d .venv || python3 -m venv .venv
   source .venv/bin/activate
   pip show funasr >/dev/null 2>&1 || pip install -r requirements.txt
   ```
   `pip install -r requirements.txt` 第一次会装 torch/funasr 等,包比较大,要等几分钟。

2. **运行转写**(把用户给的音频路径/文件夹/链接原样传进去):
   ```
   cd ~/.claude/skills/cantonese-transcribe
   source .venv/bin/activate
   python transcribe_cantonese.py "<用户提供的音频路径、文件夹或播客/视频链接>"
   ```
   - 如果是链接,默认会下载到当前目录的 `下载音频/` 文件夹,再转写。
   - 首次运行还会自动从 ModelScope 下载三个模型(SenseVoice + VAD + ct-punc,
     加起来约 2G 多),之后离线可用。这一步和依赖安装都可能跑几分钟到十几分钟,
     用 `run_in_background` 跑,别让用户干等。
   - 长音频(比如一小时播客)转写本身也要几分钟,同样建议后台跑,完成后再汇报结果。

3. **汇报结果**:把生成的 `.md` 和 `.pdf` 完整路径告诉用户,可以贴一小段
   md 内容的预览(前几句)方便用户确认效果。

## 常见问题

- 报错找不到 ffmpeg → `brew install ffmpeg`
- 没独显也能跑,默认用 CPU,SenseVoice 是小模型,速度可接受
- 支持 mp3/m4a/wav/aac/flac/ogg/mp4/opus 等,ffmpeg 能读的基本都行
- 极少数播客平台有防盗链,`yt-dlp` 可能下不了,这种情况请用户手动下载音频后
  再把本地路径传给这个 skill
