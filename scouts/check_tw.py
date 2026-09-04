#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""繁体站门禁。

    python3 scouts/check_tw.py

七条判据，各防一类**在另外两个站真的发生过**的事故：

① 结构一一对应 —— 简体站每页 /tw/ 都要有，反过来不能多。
   少一页是死链，多一页是没人维护的孤儿。
② 独立断言：几个关键位置必须存在，且 i/ 的条目数两边一致。
   这一条不依赖 SKIP 表 —— ① 拿同一份表算两边，跳错了会两边一起漏，
   它自己看不见。原声那边就是这么把 sources/ 整个漏掉而 ① 全绿。
③ 链接集合一致 —— 两版页面的 href/src 取出来必须逐个相同
   （这个站用相对链接，繁体版不该有任何改写）。
   主站正是这条抓到一个隐蔽 bug：占位符用了 \\x00，而 OpenCC 底层是
   C 字符串遇 \\x00 就截断，URL 被正文填满，页面照样渲染、构建照样通过。
④ 没有漏转 —— 正文里不该再出现只存在于简体的字。
⑤ 没有切错组合 —— 「绝不该出现」的那张表。逐字审只能看见你想到要看的字；
   这个站的「7 天曆史」就是这张表扫出来的。
⑥ 歧义字都登记过 —— 一简多繁里两边都讲得通的那些字，每处的三字上下文
   必须在 scouts/tw_allow.txt 里。新条目每天上架，这条会持续报几条要审。
⑦ 语言标记自报繁体 —— og:locale / inLanguage 是标记不是正文，转换转不到，
   漏了就被搜索引擎和分享卡片按简体归类。
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import tw as TW  # noqa: E402

TWDIR = os.path.join(ROOT, "tw")
TAG = re.compile(r"<script.*?</script>|<style.*?</style>", re.S)
LINK = re.compile(r'\b(?:href|src)="([^"]*)"')
ALT = re.compile(r'<link rel="alternate" hreflang[^>]*>')
SIMP_ONLY = "们这时说过还没个来对开关问题实现样种应认识电话书长门闻见丽乐乡习买卖头条声词语读观"


def pages(root, skip):
    out = {}
    for dp, dn, fn in os.walk(root):
        rel = os.path.relpath(dp, root)
        if set(rel.split(os.sep)) & skip:
            dn[:] = []
            continue
        for f in fn:
            if f in ("index.html", "404.html"):
                p = os.path.join(dp, f)
                out[os.path.relpath(p, root).replace(os.sep, "/")] = p
    return out


def body(s):
    return " ".join(re.findall(r">([^<>]+)<", TAG.sub("", s)))


def main():
    if not os.path.isdir(TWDIR):
        print("✗ 没有 tw/ —— 先跑 python3 scouts/tw.py")
        return 1
    sc = pages(ROOT, TW.SKIP_DIRS)
    tw = pages(TWDIR, TW.SKIP_DIRS - {"tw"})
    bad = []

    # ① 结构
    for m in sorted(set(sc) - set(tw))[:5]:
        bad.append("繁体站缺页：%s" % m)
    for e in sorted(set(tw) - set(sc))[:5]:
        bad.append("繁体站多出孤儿页：%s" % e)

    # ② 不依赖 SKIP 表的独立断言
    for rel in ("index.html", "sitemap.xml", "feed.xml"):
        if not os.path.exists(os.path.join(TWDIR, rel)):
            bad.append("繁体站缺 %s" % rel)
    for d in ("i", "zh"):
        a = os.path.join(ROOT, d)
        b = os.path.join(TWDIR, d)
        if os.path.isdir(a):
            na = len([x for x in os.listdir(a) if os.path.isdir(os.path.join(a, x))])
            nb = len([x for x in os.listdir(b) if os.path.isdir(os.path.join(b, x))]) \
                if os.path.isdir(b) else 0
            if na != nb:
                bad.append("%s/ 两版条目数不一致：简体 %d，繁体 %d" % (d, na, nb))

    # ③ 链接集合
    n_link = 0
    for k in sorted(set(sc) & set(tw)):
        sa = open(sc[k], encoding="utf-8", errors="ignore").read()
        sb = open(tw[k], encoding="utf-8", errors="ignore").read()
        if ALT.findall(sa) != ALT.findall(sb):
            bad.append("hreflang 两版不一致：%s" % k)
        a = LINK.findall(ALT.sub("", sa))
        b = [x.replace("/skill/tw/", "/skill/") for x in LINK.findall(ALT.sub("", sb))]
        if a != b:
            d = [(x, y) for x, y in zip(a, b) if x != y][:2]
            bad.append("链接对不上：%s  %s" % (k, d or "(数量 %d vs %d)" % (len(a), len(b))))
            if len([x for x in bad if x.startswith("链接对不上")]) >= 5:
                break
        n_link += len(a)

    # ④⑤⑥ 逐页扫
    allow = TW.load_allow()
    unseen = {}
    for k in sorted(tw):
        t = body(open(tw[k], encoding="utf-8", errors="ignore").read())
        hit = sorted({c for c in t if c in SIMP_ONLY})
        if hit and len([x for x in bad if x.startswith("疑似漏转")]) < 5:
            bad.append("疑似漏转：%s 出现简体字 %s" % (k, "".join(hit[:6])))
        for w in TW.NEVER:
            if w in t:
                i = t.index(w)
                if len([x for x in bad if x.startswith("切错")]) < 5:
                    bad.append("切错：%s 里出现「%s」 …%s…"
                               % (k, w, t[max(0, i - 10):i + 11]))
                break
        for c in TW.contexts(t):
            if c not in allow:
                unseen.setdefault(c, k)
        # ⑦ 语言标记：繁体页里**任何地方**都不该出现 zh-CN / zh_CN。
        #    只查 og:locale 是不够的 —— 首页那段 I18N 脚本在运行时把
        #    documentElement.lang 覆盖回 zh-CN，看页面看不出来，
        #    只有在浏览器里读 lang 才发现。所以整篇扫。
        #    （hreflang 用的是 zh-Hans，不是 zh-CN，不会误报。）
        raw = open(tw[k], encoding="utf-8", errors="ignore").read()
        m = re.search(r"zh[-_]CN", raw)
        if m and len([x for x in bad if "zh-CN" in x or "zh_CN" in x]) < 3:
            i = m.start()
            bad.append("%s 里还有 %s …%s…"
                       % (k, m.group(0), raw[max(0, i - 40):i + 12].replace("\n", " ")))

    # ⑧ 英文排版那一块不许丢。
    #    主站上这类「html[lang=en] 的字体覆盖」丢过两次 —— 写在样式表末尾
    #    的东西，谁改一下、哪次回滚一下就没了，而页面照样渲染、构建照样
    #    通过，只是整页英文换回了中文字体的西文字形（窄、低对比、字宽不匀，
    #    「哪里不对但说不出」）。这里只查它在不在：静态一条，够拦住丢失。
    idx = os.path.join(ROOT, "index.html")
    if os.path.exists(idx):
        raw = open(idx, encoding="utf-8", errors="ignore").read()
        for what, needle in (("英文排版块", 'id="hwx-en-type"'),
                             ("标题字体", "Playfair+Display"),
                             ("正文字体", "Source+Serif+4"),
                             ("英文变量覆盖", 'html[lang="en"]{')):
            if needle not in raw:
                bad.append("index.html 里没有%s（%s）—— 英文页会退回中文字体"
                           % (what, needle))

    # ⑨ 运行时 fetch 的数据必须在繁体站里存在。
    #    这一类静态检查全绿也照样坏：首页 fetch("skills/feed.json") 取货架，
    #    而 skills/ 被跳过了 —— 繁体首页显示「feed.json 讀取失敗，貨架這次沒裝上」，
    #    结构、链接、语言标记全对。只有真的打开页面才看得见。
    FETCH = re.compile(r"""fetch\(\s*["']([^"']+)""")
    for k, p_ in sorted(tw.items()):
        raw = open(p_, encoding="utf-8", errors="ignore").read()
        for u in FETCH.findall(raw):
            if u.startswith(("http", "//", "data:")):
                continue
            tgt = os.path.normpath(os.path.join(os.path.dirname(p_), u))
            if not os.path.exists(tgt):
                bad.append("%s 要 fetch 的 %s 在繁体站里不存在" % (k, u))
                break
        if len([x for x in bad if "fetch" in x]) >= 3:
            break

    if unseen:
        bad.append("歧义字上下文没登记过 %d 处（看一眼对不对，对就跑 "
                   "python3 scouts/gen_tw_allow.py）：" % len(unseen))
        for c, k in sorted(unseen.items())[:30]:
            bad.append("    %s      ← %s" % (c, k))

    print("繁体站 %d 页 · 校对链接 %d 条 · 歧义字白名单 %d 条"
          % (len(tw), n_link, len(allow)))
    if bad:
        print("\n不合格：")
        for b in bad:
            print(("  ✗ " + b) if not b.startswith("    ") else b)
        return 1
    print("✓ 结构一一对应、链接一致、无漏转、无切错组合、歧义字全部登记、语言标记自报繁体")
    return 0


if __name__ == "__main__":
    sys.exit(main())
