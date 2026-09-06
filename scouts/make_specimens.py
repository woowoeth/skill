# -*- coding: utf-8 -*-
"""给取不到作者真图的在架货，做一张**只有图形、没有文字**的站方样张（cover_kind: specimen）。

    python3 scouts/make_specimens.py                 # 所有在架且没图的
    python3 scouts/make_specimens.py --replace       # 连判成 replace 的一起做
    python3 scouts/make_specimens.py --ci            # 进货工作流用：图形是猜的，cover_verdict 留空待人过目
    python3 scouts/make_specimens.py <id> [<id>…]    # 指定几件
    python3 scouts/make_specimens.py --tally         # 只看每件会分到哪个图形，不渲染

## 为什么要有这一步

店主 2026-09-06 定的底线：**每一件在架的都必须有图**（docs/COVERS.md）。
在架 319 件里 162 件没图，且全在 2–3 天前跑过 repo_covers（含翻文件树）—— 作者仓里
就没有图。再跑一百遍也是零。剩下的路只有一条：我们自己做。

## 为什么图上一个字都没有

第一版把 title_zh 和 tagline 排成大字放在图里。店主一眼看穿：「你生成的这些图也不好，
明显和下面的标题描述重复了」—— 卡片底下本来就印着标题和描述，图里再写一遍等于同一句话
说两遍；而且它违反 COVERS.md 自己那句「字只能当标签，不能当解释」。作废。

现在的做法：**按它干的事配一个图形**。视频剪成帧、书拆成块、照片变贴纸、字幕落到时间轴、
音频变波形 —— 三十来个能力图形，按 title/tagline/name 里的词分派。图形是 icon 级的
示意，不是假截图；同一类能力共用同一个图形，像一套设计过的图标系统，扫几张就认得。
遮住标题，它至少能回答「这东西处理的是什么、变成了什么」。

三条硬规则照 assets/ours/op7418-guizang-social-card-skill.png：不要圆角、不要阴影、
不要渐变；一个 accent（#8b3d2f）加一个墨色、一个纸色，没有第四种颜色。

## 落盘

assets/covers/<id>.png（1200×800）；editorial/curation.json 写 cover / cover_kind=specimen /
cover_w / cover_h / cover_real=false / cover_verdict=ok / cover_motif（分到的图形名，方便复查）。
之后跑 scouts/make_thumbs.py 出 w800 派生图。图注由 index.html capSpecimen 负责说明
「站方样张，不是产出物截图」。
"""
from __future__ import annotations
import datetime
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CUR = os.path.join(ROOT, "editorial", "curation.json")
FEED = os.path.join(ROOT, "skills", "feed.json")
OUT = os.path.join(ROOT, "assets", "covers")

W, H = 1200, 800
A, INK, INK2, PAPER = "#8b3d2f", "#14120e", "#8a857a", "#f5f2ea"


def _frames(n=5, x0=-330, y=-70, w=110, h=140, gap=22):
    return "".join('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="7"/>'
                   % (x0 + i * (w + gap), y, w, h, INK) for i in range(n))


def _wave(x0=-330, x1=330, y=0, n=44, amp=90, seed=3):
    import math
    bars = []
    for i in range(n):
        t = i / (n - 1)
        a = amp * (0.35 + 0.65 * abs(math.sin(t * 9.7 + seed) * math.cos(t * 3.1)))
        x = x0 + t * (x1 - x0)
        bars.append('<rect x="%.0f" y="%.0f" width="8" height="%.0f" fill="%s"/>' % (x, y - a, 2 * a, INK))
    return "".join(bars)


def _grid(cols=4, rows=3, x0=-330, y0=-200, w=140, h=110, gap=20, fill_fn=None):
    out = []
    for r in range(rows):
        for c in range(cols):
            f = fill_fn(r, c) if fill_fn else "none"
            out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="6"/>'
                       % (x0 + c * (w + gap), y0 + r * (h + gap), w, h, f, INK))
    return "".join(out)


def _arrow(x0=-40, x1=40, y=0):
    return ('<path d="M%d,%d L%d,%d" stroke="%s" stroke-width="8"/>'
            '<path d="M%d,%d l-26,-26 M%d,%d l-26,26" stroke="%s" stroke-width="8" stroke-linecap="square"/>'
            % (x0, y, x1, y, A, x1, y, x1, y, A))


def _page(x, y, w=200, h=260, lines=6, fold=True):
    s = '<path d="M%d,%d L%d,%d L%d,%d L%d,%d L%d,%d Z" fill="none" stroke="%s" stroke-width="7"/>' % (
        x, y, x + w - 40, y, x + w, y + 40, x + w, y + h, x, y + h, INK)
    if fold:
        s += '<path d="M%d,%d L%d,%d L%d,%d" fill="none" stroke="%s" stroke-width="7"/>' % (
            x + w - 40, y, x + w - 40, y + 40, x + w, y + 40, INK)
    for i in range(lines):
        lw = w - 60 - (30 if i % 3 == 2 else 0)
        s += '<rect x="%d" y="%d" width="%d" height="10" fill="%s"/>' % (x + 30, y + 70 + i * 28, lw, INK2)
    return s


# ── 能力图形 ─────────────────────────────────────────────────────────
# 每个图形回答一句：它处理的是什么，变成了什么。坐标系原点在画面中心，视野约 ±560×±340。
MOTIFS = {
    # 视频 → 帧
    "video_cut": _frames(5) + '<rect x="-330" y="110" width="660" height="6" fill="%s"/>' % A
                 + "".join('<rect x="%d" y="96" width="6" height="34" fill="%s"/>' % (x, A) for x in (-200, -70, 60, 190)),
    # 字幕 → 时间轴
    "subtitle": '<rect x="-330" y="-40" width="660" height="80" fill="none" stroke="%s" stroke-width="7"/>' % INK
                + "".join('<rect x="%d" y="-16" width="%d" height="32" fill="%s"/>' % (x, w, A) for x, w in ((-300, 130), (-140, 90), (-20, 170), (180, 110)))
                + '<rect x="-330" y="90" width="660" height="6" fill="%s"/>' % INK2,
    # 音频 → 波形
    "audio": _wave(),
    # 音频 → 游戏/节奏
    "audio_game": _wave(x0=-330, x1=60, amp=70) + _arrow(100, 170) + '<rect x="200" y="-110" width="130" height="220" fill="none" stroke="%s" stroke-width="7"/>' % INK
                  + "".join('<circle cx="265" cy="%d" r="14" fill="%s"/>' % (y, A) for y in (-60, 0, 60)),
    # 照片 → 插画/贴纸
    "photo_to_art": '<rect x="-330" y="-150" width="260" height="300" fill="none" stroke="%s" stroke-width="7"/>' % INK
                    + '<circle cx="-250" cy="-80" r="28" fill="%s"/>' % INK2
                    + '<path d="M-330,110 L-250,20 L-190,80 L-140,30 L-70,120" fill="none" stroke="%s" stroke-width="7"/>' % INK2
                    + _arrow(-30, 50)
                    + '<path d="M120,-120 L300,-140 L330,110 L90,130 Z" fill="none" stroke="%s" stroke-width="7"/>' % A
                    + '<path d="M150,60 Q200,-60 260,50" fill="none" stroke="%s" stroke-width="9"/>' % A
                    + '<circle cx="240" cy="-60" r="26" fill="%s"/>' % A,
    # 海报 / 印刷
    "poster": '<rect x="-190" y="-260" width="380" height="520" fill="none" stroke="%s" stroke-width="7"/>' % INK
              + '<rect x="-140" y="-200" width="280" height="240" fill="%s"/>' % A
              + '<rect x="-140" y="80" width="200" height="16" fill="%s"/>' % INK
              + '<rect x="-140" y="120" width="120" height="16" fill="%s"/>' % INK2,
    # 贴纸 / 拼贴
    "sticker": "".join('<path d="M%d,%d l%d,%d l%d,%d l%d,%d Z" fill="%s" stroke="%s" stroke-width="6"/>'
                       % (x, y, 150, -20, 20, 120, -150, 20, PAPER, INK) for x, y in ((-320, -120), (-90, -40), (140, -140)))
               + '<rect x="-260" y="-100" width="80" height="60" fill="%s"/>' % A
               + '<circle cx="0" cy="20" r="34" fill="%s"/>' % A
               + '<path d="M180,-120 L260,-60 L200,-30 Z" fill="%s"/>' % A
               + "".join('<rect x="%d" y="%d" width="90" height="26" fill="%s" fill-opacity=".35"/>' % (x, y, A) for x, y in ((-200, -140), (30, -60), (230, -160))),
    # 字体 / 排版
    "font": '<path d="M-300,120 L-190,-160 L-80,120 M-262,30 L-118,30" fill="none" stroke="%s" stroke-width="16" stroke-linecap="square"/>' % INK
            + '<path d="M40,-160 L40,120 M40,-160 L200,-160 M40,-20 L170,-20 M40,120 L200,120" fill="none" stroke="%s" stroke-width="16" stroke-linecap="square"/>' % A
            + '<rect x="-330" y="160" width="660" height="6" fill="%s"/>' % INK2,
    # 手绘 / 白板动画
    "whiteboard": '<rect x="-330" y="-200" width="660" height="400" fill="none" stroke="%s" stroke-width="7"/>' % INK
                  + '<path d="M-260,120 C-180,-140 -60,-140 20,60 S180,-100 260,40" fill="none" stroke="%s" stroke-width="9"/>' % A
                  + '<circle cx="260" cy="40" r="18" fill="%s"/>' % A,
    # 分镜 / 故事板
    "storyboard": _grid(3, 2, x0=-330, y0=-170, w=200, h=150, gap=30)
                  + "".join('<path d="M%d,%d l60,-50 l40,30 l60,-60" fill="none" stroke="%s" stroke-width="7"/>' % (x + 20, y + 110, A)
                            for x in (-330, -100, 130) for y in (-170, 10)),
    # 书/文档 → 结构块
    "book_to_blocks": _page(-330, -150, 220, 300, lines=6) + _arrow(-70, 10)
                      + _grid(3, 3, x0=60, y0=-150, w=80, h=80, gap=20, fill_fn=lambda r, c: A if (r + c) % 2 == 0 else "none"),
    # 文档 / 公文 / 格式
    "document": _page(-110, -170, 260, 340, lines=8),
    # 简历
    "resume": _page(-140, -190, 280, 380, lines=8) + '<rect x="-100" y="-140" width="70" height="90" fill="%s"/>' % A,
    # 幻灯片
    "slides": '<rect x="-330" y="-170" width="500" height="300" fill="none" stroke="%s" stroke-width="7"/>' % INK
              + '<rect x="-280" y="-110" width="220" height="24" fill="%s"/>' % A
              + '<rect x="-280" y="-40" width="300" height="12" fill="%s"/>' % INK2
              + '<rect x="-280" y="0" width="240" height="12" fill="%s"/>' % INK2
              + '<rect x="-230" y="-70" width="500" height="300" fill="%s" stroke="%s" stroke-width="7"/>' % (PAPER, INK)
              + '<rect x="-180" y="-10" width="220" height="24" fill="%s"/>' % A
              + '<rect x="-180" y="60" width="320" height="12" fill="%s"/>' % INK2,
    # 图表 / 数据
    "chart": "".join('<rect x="%d" y="%d" width="70" height="%d" fill="%s"/>' % (x, 170 - h, h, A if i == 3 else INK)
                     for i, (x, h) in enumerate(((-300, 120), (-190, 200), (-80, 160), (30, 300), (140, 220), (250, 80))))
             + '<rect x="-330" y="176" width="660" height="6" fill="%s"/>' % INK2,
    # 流程图 / 架构图
    "diagram": "".join('<rect x="%d" y="%d" width="160" height="90" fill="none" stroke="%s" stroke-width="7"/>' % (x, y, INK)
                       for x, y in ((-330, -200), (-80, -200), (170, -200), (-80, 60)))
               + '<path d="M-170,-155 L-80,-155 M80,-155 L170,-155 M0,-110 L0,60" fill="none" stroke="%s" stroke-width="7"/>' % A
               + '<rect x="-40" y="-80" width="80" height="16" fill="%s"/>' % A,
    # 代码 / 开发
    "code": '<path d="M-150,-130 L-300,0 L-150,130" fill="none" stroke="%s" stroke-width="16" stroke-linecap="square"/>' % INK
            + '<path d="M150,-130 L300,0 L150,130" fill="none" stroke="%s" stroke-width="16" stroke-linecap="square"/>' % INK
            + '<path d="M50,-170 L-50,170" stroke="%s" stroke-width="14"/>' % A,
    # 搜索 / 研究
    "research": '<circle cx="-60" cy="-40" r="150" fill="none" stroke="%s" stroke-width="14"/>' % INK
                + '<path d="M50,70 L220,240" stroke="%s" stroke-width="22" stroke-linecap="square"/>' % INK
                + "".join('<rect x="%d" y="%d" width="%d" height="12" fill="%s"/>' % (-150, y, w, A) for y, w in ((-90, 180), (-50, 130), (-10, 160))),
    # 翻译 / 语言
    "translate": '<text x="-200" y="60" font-family="Songti SC,STSong,serif" font-size="230" font-weight="700" fill="%s" text-anchor="middle">文</text>' % INK
                 + _arrow(-40, 40, 0)
                 + '<text x="200" y="60" font-family="Georgia,serif" font-size="230" font-weight="700" fill="%s" text-anchor="middle">A</text>' % A,
    # 聊天 / 消息
    "chat": '<path d="M-330,-160 L60,-160 L60,40 L-180,40 L-250,110 L-250,40 L-330,40 Z" fill="none" stroke="%s" stroke-width="7"/>' % INK
            + '<path d="M-40,-40 L330,-40 L330,160 L250,160 L250,230 L180,160 L-40,160 Z" fill="%s" stroke="%s" stroke-width="7"/>' % (PAPER, A)
            + "".join('<rect x="%d" y="%d" width="%d" height="10" fill="%s"/>' % (x, y, w, c) for x, y, w, c in ((-290, -110, 260, INK2), (-290, -80, 180, INK2), (0, 10, 260, A), (0, 40, 200, A))),
    # 日历 / 习惯
    "calendar": _grid(7, 4, x0=-330, y0=-140, w=80, h=70, gap=14, fill_fn=lambda r, c: A if (r * 7 + c) in (3, 8, 9, 15, 16, 17, 23) else "none"),
    # 身体 / 健身
    "fitness": '<circle cx="0" cy="-120" r="50" fill="%s"/>' % INK
               + '<path d="M0,-60 L0,80 M-140,-20 L140,-20 M0,80 L-90,230 M0,80 L90,230" fill="none" stroke="%s" stroke-width="16" stroke-linecap="square"/>' % INK
               + '<rect x="-220" y="-40" width="60" height="40" fill="%s"/>' % A + '<rect x="160" y="-40" width="60" height="40" fill="%s"/>' % A,
    # 食物 / 菜谱
    "food": '<path d="M-220,-20 A220,220 0 0 0 220,-20 L220,10 L-220,10 Z" fill="%s"/>' % INK
            + '<rect x="-90" y="10" width="180" height="24" fill="%s"/>' % INK
            + '<path d="M-60,-140 C-60,-200 -20,-200 -20,-260 M20,-140 C20,-200 60,-200 60,-260" fill="none" stroke="%s" stroke-width="10"/>' % A,
    # 旅行 / 地图
    "travel": '<path d="M-330,120 L-120,-40 L60,60 L330,-140" fill="none" stroke="%s" stroke-width="9" stroke-dasharray="22 16"/>' % INK2
              + "".join('<path d="M%d,%d l-34,-70 a34,34 0 1 1 68,0 Z" fill="%s"/>' % (x, y, A) for x, y in ((-120, -40), (60, 60), (330, -140))),
    # 游戏 / 跑团 / 塔罗
    "game": '<rect x="-300" y="-150" width="300" height="300" fill="none" stroke="%s" stroke-width="9"/>' % INK
            + "".join('<circle cx="%d" cy="%d" r="26" fill="%s"/>' % (x, y, INK) for x, y in ((-230, -80), (-80, -80), (-150, 0), (-230, 80), (-80, 80)))
            + '<path d="M60,-190 L330,-160 L300,190 L30,160 Z" fill="none" stroke="%s" stroke-width="9"/>' % A
            + '<path d="M180,-80 L230,0 L180,80 L130,0 Z" fill="%s"/>' % A,
    # 手机壁纸 / 卡片
    "phone": '<rect x="-150" y="-300" width="300" height="600" fill="none" stroke="%s" stroke-width="9"/>' % INK
             + '<rect x="-110" y="-240" width="220" height="330" fill="%s"/>' % A
             + '<rect x="-110" y="120" width="160" height="14" fill="%s"/>' % INK + '<rect x="-110" y="160" width="100" height="14" fill="%s"/>' % INK2,
    # 印章 / 法律 / 合同
    "seal": _page(-330, -170, 300, 340, lines=7) + '<circle cx="180" cy="60" r="130" fill="none" stroke="%s" stroke-width="12"/>' % A
            + '<circle cx="180" cy="60" r="90" fill="none" stroke="%s" stroke-width="6"/>' % A
            + '<path d="M180,-10 L200,40 L250,45 L212,80 L222,130 L180,105 L138,130 L148,80 L110,45 L160,40 Z" fill="%s"/>' % A,
    # 网页 / 落地页
    "web": '<rect x="-330" y="-200" width="660" height="400" fill="none" stroke="%s" stroke-width="7"/>' % INK
           + '<rect x="-330" y="-200" width="660" height="50" fill="%s"/>' % INK
           + '<rect x="-280" y="-90" width="300" height="30" fill="%s"/>' % A
           + '<rect x="-280" y="-20" width="360" height="12" fill="%s"/>' % INK2 + '<rect x="-280" y="20" width="280" height="12" fill="%s"/>' % INK2
           + '<rect x="120" y="-100" width="160" height="200" fill="none" stroke="%s" stroke-width="7"/>' % A,
    # 兜底：一个圆和一个方相切（做/造）
    "make": '<circle cx="-80" cy="0" r="170" fill="none" stroke="%s" stroke-width="9"/>' % INK
            + '<rect x="-40" y="-130" width="300" height="300" fill="none" stroke="%s" stroke-width="9"/>' % A,
}

# 词 → 图形。先匹配的先赢，所以越具体的放越前。
RULES = [
    ("audio_game", r"音游|节奏游戏|rhythm"),
    ("subtitle", r"字幕|srt\b|transcri|听写|whisper|subtitle"),
    ("video_cut", r"剪(片|辑|映)|视频|video|ffmpeg|镜头|分镜|film|footage|clip"),
    ("audio", r"音频|音乐|播客|podcast|audio|music|配音|tts|语音"),
    ("whiteboard", r"白板|手绘动画|whiteboard|简笔"),
    ("storyboard", r"故事板|storyboard|漫画|comic|连环"),
    ("photo_to_art", r"照片|photo|插画|illustrat|水墨|手帐|素描|画成|变成.*画|风格化|滤镜"),
    ("sticker", r"贴纸|sticker|拼贴|collage|剪影|抠图|cutout"),
    ("poster", r"海报|poster|封面|banner|横幅|小红书|xhs|卡片|card|zine|杂志|印刷|排版"),
    ("font", r"字体|font|书法|calligraph|字形|typograph"),
    ("slides", r"ppt|幻灯|slides?|演示|keynote|deck"),
    ("resume", r"简历|resume|cv\b|求职"),
    ("seal", r"法(条|规|律)|合同|contract|专利|patent|公文|政务|law\b|legal|合规"),
    ("translate", r"翻译|translat|双语|bilingual|英文|中英"),
    ("book_to_blocks", r"拆(书|成)|一本书|book|epub|pdf|长文|知识库|笔记|obsidian|second.brain|摘要|总结"),
    ("document", r"文档|document|docx|word|格式|format|报告|report|论文|写作|writing|文案|copy|润色|改写|公文"),
    ("chart", r"图表|chart|数据|data|excel|表格|统计|dashboard|指标|分析"),
    ("diagram", r"流程图|架构|diagram|excalidraw|mermaid|示意|流程|workflow|pipeline"),
    ("code", r"代码|code|编程|开发|debug|测试|test|api|sdk|前端|frontend|backend|评审|review|git|deploy|部署"),
    ("research", r"搜索|search|研究|research|调研|检索|seo|geo|情报|osint|溯源"),
    ("chat", r"聊天|chat|微信|飞书|钉钉|slack|discord|telegram|im\b|消息|对话|客服|聊"),
    ("calendar", r"习惯|habit|日程|calendar|打卡|计划|planner|待办|todo|复盘|日记|journal"),
    ("fitness", r"健身|fitness|运动|锻炼|跑步|身体|睡眠|sleep|冥想|呼吸|健康|health"),
    ("food", r"菜谱|recipe|做饭|烹饪|食|cook|meal|咖啡|茶"),
    ("travel", r"旅行|travel|旅游|地图|map|路书|行程|itinerar|出行|导航"),
    ("game", r"游戏|game|跑团|dnd|d&d|rpg|塔罗|tarot|骰|卡牌|棋|谜"),
    ("phone", r"壁纸|wallpaper|锁屏|手机|phone|app\b|界面|ui\b"),
    ("web", r"网页|web|网站|landing|落地页|html|页面|站"),
]


OVERRIDE: dict = {}      # id → motif，由 --motifs <json> 装入；人（或判官）定的分派永远赢过正则


def motif_for(it: dict) -> str:
    if it["id"] in OVERRIDE and OVERRIDE[it["id"]] in MOTIFS:
        return OVERRIDE[it["id"]]
    # 正则只是兜底。实测它会被 desc_en 里的英文碎词带跑（"app" 落成 phone、
    # "search" 落成 research、"食" 落成 food 给龙猫护理配了一只碗）——
    # 一个错的图形比中性图形更糟，它在误导。所以正则只看中文标题和一句话，
    # 且判不出就 make。真正的分派走 --motifs（判官按中文意思逐件选的）。
    text = " ".join(str(it.get(k) or "") for k in ("title_zh", "tagline_zh")).lower()
    for name, pat in RULES:
        if re.search(pat, text, re.I):
            return name
    return "make"


TPL = """<!doctype html><meta charset="utf-8">
<style>html,body{margin:0;width:%(w)dpx;height:%(h)dpx;background:%(paper)s;overflow:hidden}
svg{position:absolute;left:0;top:0;width:%(w)dpx;height:%(h)dpx}</style>
<svg viewBox="-600 -400 1200 800" xmlns="http://www.w3.org/2000/svg">
  <rect x="-600" y="-400" width="1200" height="800" fill="%(paper)s"/>
  <g transform="translate(0,0) scale(1.15)">%(motif)s</g>
</svg>"""


def render_all(targets: list[dict]) -> list[tuple[str, str, str]]:
    from playwright.sync_api import sync_playwright
    done = []
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for it in targets:
            m = motif_for(it)
            pg.set_content(TPL % dict(w=W, h=H, paper=PAPER, motif=MOTIFS[m]))
            pg.wait_for_timeout(60)
            out = os.path.join(OUT, "%s.png" % it["id"])
            pg.screenshot(path=out, full_page=False)
            done.append((it["id"], out, m))
        b.close()
    return done


def main(argv):
    feed = json.load(io.open(FEED, encoding="utf-8"))["skills"]
    cur = json.load(io.open(CUR, encoding="utf-8"))
    items = cur.setdefault("items", {})
    # --motifs <json>：判官逐件选好的 id → 图形名。它赢过正则。
    if "--motifs" in argv:
        mp = argv[argv.index("--motifs") + 1]
        OVERRIDE.update(json.load(io.open(mp, encoding="utf-8")))
        argv = [a for a in argv if a != mp]
    ci = "--ci" in argv
    ids = [a for a in argv if not a.startswith("--")]
    if ids:
        targets = [x for x in feed if x["id"] in set(ids)]
    else:
        targets = [x for x in feed if not (x.get("cover") or "").strip()
                   or (items.get(x["id"]) or {}).get("cover_kind") == "specimen"]
        if "--replace" in argv:
            targets += [x for x in feed if (items.get(x["id"]) or {}).get("cover_verdict") == "replace"]
    seen, uniq = set(), []
    for x in targets:
        if x["id"] not in seen:
            seen.add(x["id"]); uniq.append(x)
    targets = uniq
    if "--tally" in argv:
        import collections
        c = collections.Counter(motif_for(x) for x in targets)
        for k, v in c.most_common():
            print("%-16s %3d  例：%s" % (k, v, "、".join((x.get("title_zh") or x["id"])[:14] for x in targets if motif_for(x) == k)[:80]))
        return 0
    if not targets:
        print("没有要做的"); return 0
    done = render_all(targets)
    today = datetime.date.today().isoformat()
    for sid, out, m in done:
        e = items.setdefault(sid, {})
        e.update({
            "cover": "/skill/" + os.path.relpath(out, ROOT),
            "cover_kind": "specimen", "cover_real": False,
            "cover_w": W, "cover_h": H, "cover_src": "", "cover_motif": m,
            # --ci：进货工作流自动跑的，图形是按标题正则猜的、没人打开看过。
            # 不写 ok —— 「有人看过」是底线（CLAUDE.md 第 2 条），机器不能替人签字。
            # 留空让货架体检在 48 小时内记「糙」，巡货的 agent 看图后再写 ok 或换图形。
            **({"cover_verdict": "",
                "cover_verdict_why": "CI 自动出的中性样张（图形 %s 按标题正则猜的），待判官过目" % m}
               if ci else
               {"cover_verdict": "ok",
                "cover_verdict_why": "站方样张（%s）：作者仓里没有可用的图；图上只有能力图形，没有文字" % m,
                "cover_judged_at": today}),
        })
    io.open(CUR, "w", encoding="utf-8").write(json.dumps(cur, ensure_ascii=False, indent=1))
    print("样张 %d 张 → assets/covers/，curation.json 已记；接着跑 scouts/covers_publish.py（refresh → 派生图，顺序不能反）" % len(done))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
