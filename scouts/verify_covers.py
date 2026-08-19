#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
封面原图校验 —— 拉封面的头几个字节，量真实宽高，和 feed 里的 `cover_w`/`cover_h` 对账。

# 为什么是这条不变量，而不是「会不会被裁」

「会不会被裁」是**渲染事实**：谁裁的、裁掉多少，读者点一下就看到原图，
而且画幅数值属于卡片版式，跟着版式走，不该固化成跨模块契约 ——
守卫拿前端的常量去量前端的常量，**定义上不可能失败**，那不是守卫。

真正的不变量是 `docs/PROTOCOL.md`「流里给短的，详情给全的」那条的后半句：

  **流里可以裁；全的那份必须真的在一次点击之外，且一刀不动。**

图片这边它天然成立 —— 因为 `cover` 就是原图 URL，裁剪只发生在渲染 ——
**除非有人把预裁过的图塞进 `cover`**。那一刻规矩就破了，而且**从数据上看不出来**：
`cover_w`/`cover_h` 还是当初量的那对数，URL 还是那个 URL，只有字节变了。

所以这个脚本只回答一个问题：**那个 URL 现在指着的，还是当初量过的那张图吗？**

# 为什么单独一个脚本，不塞进 check_curation

它要联网。`check_curation.py` 是本地体检，跑得快、任何时候都能跑、结果确定；
把网络请求塞进去会让它变慢又变脆，CI 里一次超时就红一次，
最后的结果是大家开始忽略它 —— 那比没有守卫更糟。

用法:
  python3 scouts/verify_covers.py            # 全部上站封面
  python3 scouts/verify_covers.py --limit 10 # 只查前 10 张
  python3 scouts/verify_covers.py --json     # 机器可读
退出码: 0 = 没有不一致；1 = 有（可以进 CI 的定时任务，不进每次提交）
"""
from __future__ import annotations
import os, sys, json, struct, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scout_lib as lib  # noqa: E402

HEAD_BYTES = 65536      # 够所有格式的尺寸头；GitHub raw 支持 Range，不用整张拉
UA = "pinwei-cover-verify/1.0 (+https://github.com/woowoeth/skill)"


def fetch_head(url: str) -> tuple[bytes | None, str, str]:
    """返回 (字节, content_type, 错误)。拉不到就返回错误 —— 不猜。"""
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Range": f"bytes=0-{HEAD_BYTES - 1}"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read(HEAD_BYTES), (r.headers.get("Content-Type") or ""), ""
    except urllib.error.HTTPError as e:
        return None, "", f"http {e.code}"
    except Exception as e:
        return None, "", type(e).__name__


_SVG_WH = None      # 延迟编译，见 svg_dims


def svg_dims(b: bytes) -> tuple[int, int] | None:
    """SVG 没有像素，但有 `width`/`height` 或 `viewBox` —— 那正是 cover_w/cover_h 的来源。

    这 4 张 SVG 原本被跳过了，但**它们在数据里是有 cover_w/cover_h 的**，
    而手写的数字正是最需要对账的那种。所以这里把 viewBox 也量出来。
    """
    global _SVG_WH
    if _SVG_WH is None:
        import re as _re
        _SVG_WH = (_re.compile(rb'<svg\b[^>]*', _re.I | _re.S),
                   _re.compile(rb'\bwidth\s*=\s*["\']?\s*([\d.]+)', _re.I),
                   _re.compile(rb'\bheight\s*=\s*["\']?\s*([\d.]+)', _re.I),
                   _re.compile(rb'\bviewBox\s*=\s*["\']\s*[-\d.]+[ ,]+[-\d.]+[ ,]+([\d.]+)[ ,]+([\d.]+)', _re.I))
    tag_re, w_re, h_re, vb_re = _SVG_WH
    m = tag_re.search(b)
    if not m:
        return None
    tag = m.group(0)
    mw, mh = w_re.search(tag), h_re.search(tag)
    if mw and mh:
        return round(float(mw.group(1))), round(float(mh.group(1)))
    mv = vb_re.search(tag)
    if mv:
        return round(float(mv.group(1))), round(float(mv.group(2)))
    return None


def dims(b: bytes) -> tuple[int | int, int | int] | None:
    """从头字节解出像素尺寸。认不出返回 None —— **认不出就说认不出，不估算。**"""
    # **先认魔数，再认 SVG。** 顺序反过来我踩过一次：用 `b"<svg" in b[:2000]` 当判据，
    # 结果 4 张真 PNG 被劫持 —— 它们带 C2PA 溯源元数据，里头嵌了一个
    # `image/svg+xml` 图标，于是四张不相关的图一起报出同一个 716×716。
    # 四个不同的图量出同一个尺寸，那不是数据坏了，是量的方法坏了。
    # 教训和我们一直在防的那个病同源：**判据得核过，不能想当然。**
    if b[:8] == b"\x89PNG\r\n\x1a\n" and b[12:16] == b"IHDR":
        return struct.unpack(">II", b[16:24])
    if b[:3] == b"GIF":
        w, h = struct.unpack("<HH", b[6:10])
        return w, h
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        c = b[12:16]
        if c == b"VP8X":
            w = int.from_bytes(b[24:27], "little") + 1
            h = int.from_bytes(b[27:30], "little") + 1
            return w, h
        if c == b"VP8 ":
            return struct.unpack("<HH", b[26:30])[0] & 0x3FFF, struct.unpack("<HH", b[26:30])[1] & 0x3FFF
    if b[:2] == b"\xff\xd8":                       # JPEG：走段，找 SOF
        i = 2
        while i < len(b) - 9:
            if b[i] != 0xFF:
                i += 1
                continue
            m = b[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                     0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", b[i + 5:i + 9])
                return w, h
            if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
                i += 2
                continue
            try:
                i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
            except Exception:
                return None
    # 到这儿说明不是任何栅格格式 —— 只有这时才当 SVG 看，而且必须是**开头**就是
    lead = b[:400].lstrip().lstrip(b"\xef\xbb\xbf")
    if lead[:5] == b"<?xml" or lead[:4] == b"<svg":
        return svg_dims(b)
    return None


def main() -> None:
    argv = sys.argv[1:]
    items = lib.apply_editorial(lib.load_items())
    for it in items.values():
        lib.normalize_item(it)
    live = sorted((it for it in items.values()
                   if not it.get("hide") and (it.get("cover") or "").strip()),
                  key=lambda x: x["id"])
    if "--limit" in argv:
        live = live[:int(argv[argv.index("--limit") + 1])]

    bad, unmeasurable, broken, ok = [], [], [], 0
    for it in live:
        url = it["cover"].strip()
        b, ctype, e = fetch_head(url)
        if b is None:
            broken.append((it, e))
            print(f"  [拉不到 {e}] {it['id']}\n      {url}")
            continue
        d = dims(b)
        if d is None:
            # SVG 之类没有像素尺寸的：说认不出，不当成通过也不当成失败
            unmeasurable.append((it, ctype))
            print(f"  [量不出 {ctype or '?'}] {it['id']}")
            continue
        w, h = d
        rw, rh = it.get("cover_w"), it.get("cover_h")
        if not (isinstance(rw, int) and isinstance(rh, int)):
            unmeasurable.append((it, "feed 里没有 cover_w/cover_h"))
            print(f"  [无记录尺寸] {it['id']}  实际 {w}×{h}")
            continue
        if (w, h) != (rw, rh):
            bad.append((it, (rw, rh), (w, h)))
            print(f"  [不一致] {it['id']}\n      记录 {rw}×{rh} → 实际 {w}×{h}"
                  f"{'  ←可能被换成了预裁版' if w * h < rw * rh else '  ←图换了'}")
        else:
            ok += 1

    print(f"\n上站封面 {len(live)} 张：一致 {ok} · 不一致 {len(bad)} · "
          f"量不出 {len(unmeasurable)} · 拉不到 {len(broken)}")
    if bad:
        print("**不一致就是那条不变量被破了**：`cover` 该指着原图，"
              "尺寸变小尤其要查是不是被换成了预裁版 —— 那样「详情页给原比例」就成了空话。")
    if broken:
        print("拉不到的那些是坏封面，卡片上会开天窗，归内容和 editorial 层。")
    if "--json" in argv:
        print(json.dumps({
            "live": len(live), "ok": ok,
            "mismatch": [{"id": i["id"], "recorded": list(r), "actual": list(a)}
                         for i, r, a in bad],
            "unmeasurable": [i["id"] for i, _ in unmeasurable],
            "broken": [{"id": i["id"], "error": e} for i, e in broken],
        }, ensure_ascii=False, indent=1))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
