---
name: video-quote-image-i18n
description: 把任意语言的视频（外挂字幕或无字幕）取帧，配上翻译后的字幕，拼成社交平台 3:4 金句长图。用户要求把外语访谈/播客做成中文金句图、翻译视频字幕做图、给没有烧录字幕的视频加字幕拼图、把 YouTube 内容做成小红书图文，或要把这套样式固定成模板时使用；也用于调整既有长图的时间点、译文、字体和画面数量。若视频字幕已经烧录在画面里且不需要翻译，改用 native-subtitle-quote-image。
---

# 跨语言金句拼图

处理**字幕不在画面里**或**需要换语言**的视频。字幕从字幕轨取出，译文由你（Agent）产出，再由脚本重绘到画面上。

与 `native-subtitle-quote-image` 的分工：那个保留原生烧录字幕、明确不翻译；这个负责它覆盖不到的场景。

## 路径与依赖

- 将 `<SKILL_DIR>` 解析为当前 `SKILL.md` 所在目录的绝对路径，不要假设工作目录就是 Skill 目录。
- Python 3.10+。运行前检查：

  ```bash
  python3 -c "from PIL import Image; print('ok')" && command -v ffmpeg && command -v yt-dlp
  ```

- 依赖缺失时先向用户说明并取得安装授权，再运行：

  ```bash
  python3 -m pip install -r "<SKILL_DIR>/requirements.txt"
  ```

## 固定样式

- 默认输出 3:4、1440×1920。
- 每张图默认 5 个时间点：第一帧是主画面，其余 4 帧各配一句译文。
- 译文绘制在每格底部，带渐变压暗和描边，保证任何画面上都可读。
- 字号自适应收缩；中文按字断行，拉丁语优先按空格断行。
- 不覆盖用户已有成品，使用新的输出目录。

## 工作流

1. **取素材**。有链接就用 `fetch`，本地已有视频和字幕就用 `segments`：

   ```bash
   python3 "<SKILL_DIR>/scripts/quote_frame.py" fetch "VIDEO_URL" --out-dir WORK_DIR
   python3 "<SKILL_DIR>/scripts/quote_frame.py" segments LOCAL.vtt --out WORK_DIR/segments.json
   ```

   `fetch` 默认只拉源语言字幕（`--sub-langs en,en-US`）。**不要去平台要翻译轨**——译文由你产出，多要一种语言只会增加 429 的概率。

2. **读 `segments.json`，挑金句**。这一步是判断，不是机械翻译：
   - 挑能独立成立的完整判断，不挑半句话和过渡句。
   - 一张图里的 4 句要能连成一段完整表达。
   - YouTube 自动字幕已在解析阶段做过去滚动处理，但仍可能断句奇怪，按语义重新组织成人话，不要逐条直译。

3. **翻译，并且加一句你自己的落地判断**。这是整套流程唯一不可替代的一步：
   - 前 3 句是译文，**最后一句留给"这在你的场景里怎么用"**。
   - 只翻译不落地，成品就是二道贩子内容，没有护城河。
   - 目标语言由用户指定，写进 manifest 的 `lang` 字段备查。

4. **先单帧试排**，确认字体和可读性：

   ```bash
   python3 "<SKILL_DIR>/scripts/quote_frame.py" probe VIDEO -t 60 --text "试排一句中文" --out probe.jpg
   ```

5. **写 manifest**：

   ```json
   {
     "lang": "zh-CN",
     "images": [
       {
         "title": "标题",
         "frames": [
           { "time": 15.0, "text": "主画面上的钩子" },
           { "time": 18.5, "text": "译文第一句" },
           { "time": 27.0, "text": "译文第二句" },
           { "time": 34.0, "text": "译文第三句" },
           { "time": 44.0, "text": "你自己的落地判断" }
         ]
       }
     ]
   }
   ```

   同一张图内 `time` 必须严格递增。也兼容 `"times": [15, 18.5, ...]` 的旧写法，此时不绘制文字（等同原生模式）。

6. **渲染整套**：

   ```bash
   python3 "<SKILL_DIR>/scripts/quote_frame.py" render VIDEO \
     --manifest manifest.json --out-dir OUTPUT_DIR \
     --aspect 3:4 --width 1440 --hero-fraction 0.42
   ```

7. **逐张检查**成品和 `final_contact_sheet.jpg`：文字完整不截断、没压到人脸、格与格之间无黑边、译文没有重复。有问题只调对应时间点 0.5–3 秒或改文案，重新渲染。

## 选帧与选句规则

- 优先选人物、动作或环境清楚的帧作主画面。
- 字幕格允许画面重复，但**文案不能重复**。
- 说话人视频画面变化小是正常的，靠文案推进，不靠画面推进。
- 源视频分辨率低时仍输出 1440×1920，但要明确这是放大尺寸，**不得宣称提升了真实清晰度**。
- 避开说话人闭眼、口型极端张开的帧。

## 字体

自动按 macOS / Linux / Windows 常见路径挑选，优先 PingFang、Hiragino Sans GB、Noto CJK。
非 CJK 目标语言或需要指定字重时，用 `--font /path/to/font.ttf` 覆盖。字体要支持目标语言的字符集，否则会出现方框。

## 权利边界

- 输入视频与生成画面的权利由使用者自行确认。
- 本 Skill 会在他人画面上叠加新文字并再发布，比单纯引用更进一步，使用前请自行判断合规性。
- 生成物中应保留可追溯的出处信息（作者、平台、链接）。

## 资源

- `scripts/quote_frame.py`：字幕解析、去滚动、取帧、绘字、拼图、总览图。
- `requirements.txt`：Python 依赖。

## 交付

向用户提供输出目录、总览图、manifest。直接展示总览图。**不得把未经逐张检查的图片报告为完成。**
