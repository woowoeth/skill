---
name: video-render-skill
description: |
  把符合 storyboard/v1 契约的分镜稿渲染成带配音和字幕的 MP4 成片（edge-tts + Remotion）。
  当用户要「把日报/分镜稿渲染成视频」「出成片」「生成视频」「给这份 storyboard.json 配音并渲染」，
  或 ai-weekly-skill 的日报视频流程走到渲染一步时，必须使用本 skill；即使用户没说 Remotion 或 TTS 也要用。
  不用于：写分镜稿、选新闻、改文案、找配图——那是调用方（ai-weekly-skill）的事。
compatibility: 需要 node ≥ 20、ffmpeg/ffprobe、python3、uv（uvx）、系统字体 Noto Sans CJK SC
---

# Video Render Skill

输入一份分镜稿，输出一部成片。本 skill 里没有内容判断：分镜稿说什么就念什么、显示什么。发现内容问题（句子太长、选题不对、图不合适），**修分镜稿，不改这里**。

## 三步流程

每次渲染都是同样三步，按顺序跑，不跳步。`<sb>` 是分镜稿**文件**的绝对路径，`<out>` 是它所在**目录**的绝对路径（产物写回同目录）。必须用绝对路径：第 2 步会先 `cd` 进 remotion 目录，相对路径会被解析到错误位置。

```bash
SKILL=~/.claude/skills/video-render-skill

# 1. 逐句配音，产出 <out>/audio/*.mp3 和 <out>/timeline.json
python3 $SKILL/scripts/tts.py <sb>

# 2. 渲染（首次会自动 npm install 并下载 Chrome Headless Shell，约 3-5 分钟；之后 30 秒视频约 30-60 秒）
cd $SKILL/remotion && npm run render -- <out>

# 3. 校验并写摘要 <out>/summary.tsv
$SKILL/scripts/verify.sh <out>
```

三步任何一步非零退出就停，把 stderr 原样报给用户，不要自己绕。常见退出原因和含义见「失败怎么读」。

`verify.sh` 通过只说明**结构**对了（帧数等于时间线、有音轨、配音文件齐全、音视频时长差在 0.2 秒内）；它不看画面内容。交付前抽两三帧看一眼（`ffmpeg -i <mp4> -vf "select=eq(n\,200)" -vframes 1 f.png`）。

## 契约

分镜稿格式在 `references/routes/storyboard.md`，机器校验用 `references/routes/storyboard.schema.json`。第 1 步开始前 `tts.py` 会先跑 schema 校验，格式不对当场指出哪一段哪个字段。契约怎么演进、效果不满意先查哪一层，也都在那份文件里——**遇到「要不要改契约」的念头先读它**。

## 改 Remotion 代码之前

`remotion/` 是标准 Remotion 项目。动它之前先读 Remotion 官方 Agent Skills（没装就装）：

```bash
npx skills add remotion-dev/skills   # 装到当前环境
```

然后按需读 `/remotion-markup`（排版、字体、音频）、`/remotion-render`（渲染参数）、`/remotion-captions`（字幕）、`/remotion-docs`（查文档）。这些是参考书，不接管流程：它们不知道分镜稿、契约和 TTS。

`remotion-dev/template-prompt-to-video` 只当范本看它的 `calculateMetadata` 怎么按音频定帧数，不 fork。`remotion-superpowers` 不用——它自己写脚本找素材，和本 skill 的边界冲突。

## 项目结构

```
video-render-skill/
├── SKILL.md
├── CONTEXT.md                        # 渲染侧术语
├── references/routes/
│   ├── storyboard.md                 # 契约 v1（人读）
│   └── storyboard.schema.json        # 契约 v1（机读）
├── scripts/
│   ├── tts.py                        # 逐句 edge-tts → audio/ + timeline.json（含词级时间戳）
│   ├── edge_synth.py                 # tts.py 的合成后端，WordBoundary 走 Python API
│   ├── bridge_talkcraft.py           # timeline.json → video-talkcraft 三件输入（实验，见下）
│   └── verify.sh                     # ffprobe 校验成片，写 summary.tsv
├── remotion/
│   ├── package.json                  # render 脚本；依赖装在这里
│   └── src/
│       ├── Root.tsx                  # Composition、zod schema、calculateMetadata
│       ├── Daily.tsx                 # 按时间线串场景 + 音频 + 字幕
│       ├── fit.ts                    # 缩字号到下限、仍放不下则抛错
│       ├── fonts.ts                  # 显式加载 Noto Sans CJK SC
│       └── scenes/                   # Opening/Headline/Roundup/Closing，各含有图/无图
└── evals/fixtures/                   # 测试用分镜稿
```

## 几个刻意的设计，别顺手「优化」掉

- **每句单独合成配音**，不整段合成再切。字幕与声音的边界因此精确；句间语调略生硬是接受的代价。
- **时长由配音实测决定**，`calculateMetadata` 把每段各句时长求和向上取整到帧。任何按字数估时长的做法都会让画面和声音错位。
- **画面文字放不下时先缩字号，缩到下限抛错，绝不截断**。截断是静默丢内容，抛错让内容层去删字。
- **字体显式加载并等就绪**（`fonts.ts`）。不这么做首帧可能落回默认字体，且只在部分帧上出现，很难查。
- **`voice` 来自分镜稿**，不在这里改。声音是人格的一部分，归内容层。

## 失败怎么读

| 现象 | 含义 | 去哪修 |
|---|---|---|
| `tts.py` 报 schema 错，指出 `scenes[2].kind` | 分镜稿格式不合契约 | 调用方重新产出分镜稿 |
| `tts.py` 报某句合成失败（已自动重试 8 次） | edge-tts 服务端间歇故障 | 等几分钟重跑同一命令，已合成的句子会跳过；目前只有 edge 一个后端 |
| 渲染报 `overflow: s02.screen.title` | 该段标题缩到下限仍放不下 | 改分镜稿，缩短那段文字 |
| 渲染报字体加载超时 | 系统没有 Noto Sans CJK SC | `fc-list :lang=zh` 检查，装字体 |
| `verify.sh` 报帧数不符 | 时间线与成片不一致，属渲染 bug | 报给用户，附 timeline.json 和 ffprobe 输出 |
| `verify.sh` 报无音轨或 audio 缺文件 | 音频没进成片 / 配音不齐 | 重跑 tts.py 补齐后再渲染；仍无音轨属渲染 bug |

## 后置（不在本 skill 现阶段范围）

背景音乐、片头动画、封面图、逐字显影字幕、条目高亮、竖版版式、Doubao 后端。清单在 ai-weekly-skill 的 `docs/video-backlog.md`。

## 实验：把画面交给 video-talkcraft（2026-09-04 起，未定稿）

本 skill 自带的 `remotion/` 是 MVP 版式。正在验证 [video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft)（装在 `~/.claude/skills/video-talkcraft`）能否明显做得更好。它要的输入是「完整口播稿 + 一条整段配音 + 字级时间戳」，我们逐句合成的产物用桥转过去，**不跑它的 ASR**——句边界已知、词边界 edge-tts 顺手给了：

```bash
python3 $SKILL/scripts/tts.py <sb>                          # 同上，多出 audio/*.words.json
python3 $SKILL/scripts/bridge_talkcraft.py <dir>/timeline.json   # → <dir>/talkcraft/{script.json, audio/full.wav, audio/timestamps.json, brief.md}
```

之后从 talkcraft 流程的 ③ 素材开始走，②（配音+时间戳）跳过。`brief.md` 是分镜稿 `screen`/`image` 的摘要，喂给它的 SHOTBOOK 当事实红线与画面提示。结论出来前 `remotion/` 保留；许可证 PolyForm Noncommercial，商用前须作者授权（记在 backlog）。
