#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给靠预览卡/无图兜底的在架货，去作者仓里取真图。

店主 2026-09-03：「封面图同样的都是 github url 预览图还有大有小，另外很多有图的也没有
只有 github url 预览图，毫无吸引力」。

两步：
① 读该件 SKILL.md 所在目录和仓根的 README.md，抽出图片链接（markdown / <img>）；
② README 里没有的，再看仓的文件树：SKILL.md 目录下（没有则全仓）的 png/jpg/webp，
   文件名带 example/demo/screenshot/preview/output/sample/showcase 的排前面。
只要**作者自己仓里**的图（相对路径或指向同仓的 raw 链接）。外站图（imgur、CDN、别人的仓）一律不取
—— 版权和二维码的风险都在那儿。
候选按顺序试下载，第一张满足「宽 ≥600、不是 logo/avatar/qr/badge/pay 文件名、体积 ≥20KB、
宽高比 0.5–2.4」的当封面，写进 curation：cover / cover_kind=hero / cover_w / cover_h / cover_src。
取不到的**留空**（cover_kind=none），前端走 plate，不再铺预览卡。

09-03 教训：这个文件第一版写完跑完就丢了（多半是 rebase 冲突循环里被 checkout 掉了），
跑出来的 28 张图也差点没进仓 —— 脚本先 commit 再跑。
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scouts"))
BAD = re.compile(r"(logo|icon|favicon|avatar|头像|personal|selfie|portrait|badge|shield|qr|wechat|weixin|donate|sponsor|alipay|pay|banner-?small)", re.I)
GOOD = re.compile(r"(example|demo|screenshot|preview|output|sample|showcase|result|cover|hero|poster)", re.I)
IMG = re.compile(r"!\[[^\]]*\]\(([^)\s]+)|<img[^>]+src=[\"']([^\"']+)", re.I)
EXTS = ("png", "jpg", "jpeg", "webp")


def dims(path):
    try:
        import skill_scout as S
        return S.cover_dims(path)
    except Exception:
        return None


def _get(url: str, timeout: int = 20) -> str:
    r = subprocess.run(["curl", "-sL", "--max-time", str(timeout), url], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def readme_images(repo: str, path: str) -> list[str]:
    urls: list[str] = []
    cands = []
    if path:
        cands += [f"{path.rstrip('/')}/README.md", f"{path.rstrip('/')}/readme.md"]
    cands += ["README.md", "readme.md", "README.zh-CN.md", "README_zh.md"]
    for rp in cands:
        t = _get(f"https://raw.githubusercontent.com/{repo}/HEAD/{rp}")
        if len(t) < 50 or t.startswith("404"):
            continue
        base = os.path.dirname(rp)
        for m in IMG.finditer(t):
            u = (m.group(1) or m.group(2) or "").strip().split("#")[0]
            if not u or u.startswith("data:"):
                continue
            if u.startswith("http"):
                if re.search(rf"github(?:usercontent)?\.com/{re.escape(repo)}/", u, re.I):
                    u = re.sub(r"github\.com/([^/]+/[^/]+)/(?:blob|raw)/([^/]+)/", r"raw.githubusercontent.com/\1/\2/", u)
                    urls.append(u)
                continue
            rel = os.path.normpath(os.path.join(base, u.lstrip("./"))) if not u.startswith("/") else u.lstrip("/")
            urls.append(f"https://raw.githubusercontent.com/{repo}/HEAD/{rel}")
        if urls:
            break
    seen, out = set(), []
    for u in urls:
        if u not in seen and not BAD.search(u.split("/")[-1]):
            seen.add(u); out.append(u)
    return out[:6]


def tree_images(repo: str, path: str) -> list[str]:
    """README 没图时看文件树。走 gh api（用的是本机 gh 登录，不碰任何 PAT）。"""
    r = subprocess.run(["gh", "api", f"repos/{repo}/git/trees/HEAD?recursive=1", "--jq", ".tree[]|select(.type==\"blob\")|.path"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return []
    files = [p for p in r.stdout.split("\n") if p.rsplit(".", 1)[-1].lower() in EXTS]
    pre = path.rstrip("/") + "/" if path else ""
    files = [p for p in files if not BAD.search(p) and "node_modules" not in p and "/." not in "/" + p]   # 09-03：看整条路径，personal-brand/ 目录漏了两次
    # 只看 SKILL.md 目录之内。09-03 第一轮翻全仓兜底，捞回来 cli/cli 的 docs/primer 组件截图当
    # dependabot-triager 的封面 —— 图是真的，但不是这件 skill 的。仓根的 skill 才允许看全仓。
    inside = [p for p in files if pre and p.startswith(pre)]
    pool = inside if pre else files
    pool = [p for p in pool if not re.search(r"(^|/)(docs?|node_modules|\.github|test|tests|__pycache__)/", p)]
    pool.sort(key=lambda p: (0 if GOOD.search(p) else 1, len(p)))
    return [f"https://raw.githubusercontent.com/{repo}/HEAD/{p}" for p in pool[:6]]


def try_download(sid: str, urls: list[str]):
    for u in urls:
        name = u.rsplit("/", 1)[-1]
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else "png"
        if ext not in EXTS + ("gif",):
            ext = "png"
        out = os.path.join(ROOT, "assets", "covers", f"{sid}.{ext}")
        subprocess.run(["curl", "-sL", "--max-time", "30", "-o", out, u], capture_output=True)
        if not os.path.exists(out) or os.path.getsize(out) < 20000:
            if os.path.exists(out):
                os.remove(out)
            continue
        wh = dims(out)
        if not wh or wh[0] < 600 or not (0.5 <= wh[0] / wh[1] <= 2.4):
            os.remove(out); continue
        return u, out, wh
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=400)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--tree", action="store_true", help="README 没图时再翻文件树")
    ap.add_argument("--only-none", action="store_true", help="只跑现在 cover_kind=none/og 的")
    a = ap.parse_args()
    feed = json.load(open(os.path.join(ROOT, "skills", "feed.json"), encoding="utf-8"))["skills"]
    cur = json.load(open(os.path.join(ROOT, "editorial", "curation.json"), encoding="utf-8"))
    todo = [x for x in feed if (x.get("cover_kind") in ("og", "none", None, "")) or not x.get("cover")]
    # 09-03：CI 每班只跑 --max 40，若每次都从头扫同一批「确实没图」的，新货永远排不到。
    # 试过没取到的记 cover_tried_at，7 天内不再试；没试过的排最前。
    import datetime as _dt
    _today = _dt.date.today()
    def _tried_recently(x):
        t = (cur["items"].get(x["id"], {}) or {}).get("cover_tried_at")
        try:
            return t and (_today - _dt.date.fromisoformat(t)).days < 7
        except Exception:
            return False
    todo = [x for x in todo if not _tried_recently(x)]
    todo.sort(key=lambda x: (1 if (cur["items"].get(x["id"], {}) or {}).get("cover_tried_at") else 0, x.get("added_at") or ""), reverse=False)
    todo.sort(key=lambda x: 0 if not (cur["items"].get(x["id"], {}) or {}).get("cover_tried_at") else 1)
    print(f"在架 {len(feed)} · 靠预览卡或无图的 {len(todo)} 件 · 本轮试 {min(len(todo), a.max)} 件 · 翻树={a.tree}\n", flush=True)
    got = 0
    for x in todo[:a.max]:
        sid, repo, path = x["id"], x.get("repo", ""), x.get("path", "") or ""
        if not repo:
            continue
        imgs = readme_images(repo, path)
        ok = try_download(sid, imgs)
        src = "README"
        if not ok and a.tree:
            t = tree_images(repo, path)
            ok = try_download(sid, t); src = "文件树"
            imgs = imgs + t
        e = cur["items"].setdefault(sid, {})
        if ok:
            u, out, (w, h) = ok
            rel = os.path.relpath(out, ROOT)
            e.update({"cover": f"/skill/{rel}", "cover_kind": "hero", "cover_real": False, "cover_w": w, "cover_h": h, "cover_src": u})
            got += 1
            print(f"  ✓ {sid[:46]:46s} {w}x{h}  [{src}] {u[-50:]}", flush=True)
        else:
            e["cover_tried_at"] = _today.isoformat()
            if e.get("cover_kind") in ("og", None) or not e.get("cover"):
                e["cover"] = ""
                e["cover_kind"] = "none"
            print(f"  · {sid[:46]:46s} 自家仓里没有可用的图（试了 {len(imgs)} 张）", flush=True)
        time.sleep(0.3)
    if not a.dry:
        json.dump(cur, open(os.path.join(ROOT, "editorial", "curation.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n取到真图 {got}/{min(len(todo), a.max)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
