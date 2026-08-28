#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO/GEO build for 品味 (Pinwei). Run from the repo root: python seo/build_seo.py"""
import datetime
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scouts"))
import geo_kit as G
import prep_signals as prep

SITE = G.Site(
    # 线上是 https://ourword.ai/skill/ 。曾经写成 skill-store，那个地址现在 404，
    # 而 canonical / og:url / sitemap / llms.txt 全部从这一行派生 —— 改错一个字，
    # 全站 800 多个页面一起指向 404。改动前先确认线上路径。
    path="skill",
    name="Pinwei", name_zh="品味",
    tagline="discover agent skills with taste",
    tagline_zh="帮你发现有品位的 Skills",
    description=(
        "A daily-restocked shelf of agent skills for Claude Code, Codex and other coding "
        "agents — each one with what it actually does, who it is for, and the one-line "
        "install command. Skills are picked by hand from public repositories; the shelf "
        "favours the ones that are fun or genuinely useful over the ones that merely exist."),
    description_zh=(
        "品味是一手挑选的 Agent Skill 货架，给 Claude Code、Codex 和同类智能体用。"
        "每一件都写清做什么用、应用范围、如何使用和怎么安装。"),
    keywords=("品味, Pinwei, Agent Skill, Claude Code Skills, Codex Skills, "
              "SKILL.md, Claude 技能, 有品位的 Skills, 做图 skill, 写字 skill, 工作 skill"),
    item_type="SoftwareApplication", item_noun="skill", item_noun_zh="skill",
    changefreq="daily",
)

# 星数刻意不出现在任何面向读者的页面上：本店自己的选品标准写着星数会亏待新发布、
# 垂直、非英语的好项目，那就不能拿它当门面。替代的是「作者做到哪一步」——
# 从 skill 正文里读得出、能指出出处的备料证据。见 scouts/prep_signals.py。
HOW = ("Scouts crawl public GitHub repositories for skill definitions every day; each candidate "
       "is checked by hand before it goes on the shelf. Star counts are deliberately not shown: "
       "they lag, and they penalise newly published, narrowly vertical and non-English work. "
       "Where the shelf note says what prep work is visible, that is read off the skill's own "
       "text — reference files, runnable scripts, bundled assets, stated boundaries.")

CITE = ("Cite the individual skill page. The skill itself belongs to its author — the repository "
        "link on each page is the authoritative source. Attribute the shelf note to "
        "\"Pinwei 品味 (OurWord AI)\".")

CAT_EN = {"creative": "images", "writing": "writing", "life": "everyday",
          "work": "work", "fun": "play"}
CAT_ZH = {"creative": "做图", "writing": "写字", "life": "生活",
          "work": "工作", "fun": "玩乐"}


# skills/ 里这几个是聚合产物，不是货。它们没有 id，会被当成一件 slug 为空的商品
# 写出 i//index.html 这种垃圾页，并且混进 sitemap 和 llms.txt。
AGGREGATES = {"feed.json", "rejected-feed.json"}


# 备料证据：进程启动时从 methods/ 本地算一次，不发网络请求。
PREP_EVIDENCE = prep.load_all()


def load_items():
    feed = json.load(open("skills/feed.json", encoding="utf-8"))
    items = []
    for s in feed.get("skills") or []:
        if s.get("hide") or not (s.get("id") or s.get("name")):
            continue
        name = s.get("name") or s.get("id") or ""
        title = s.get("title_zh") or name
        cat = s.get("category") or ""
        repo = s.get("repo") or ""
        stars = s.get("stars")

        desc_en = s.get("desc_en") or s.get("tagline_en") or ""
        sum_en = G.plain(s.get("tagline_en") or desc_en, 240)
        sum_zh = G.plain(s.get("tagline_zh") or s.get("title_zh") or desc_en, 240)

        blocks, blocks_zh = [], []
        if desc_en:
            blocks.append(("What does this skill do?", desc_en))
            blocks_zh.append(("Q：这个 skill 做什么？", s.get("desc_zh") or desc_en))
        if s.get("why_en"):
            blocks.append(("Why is it worth installing?", s["why_en"]))
        if s.get("why_zh"):
            blocks_zh.append(("Q：为什么值得装？", s["why_zh"]))

        inst = s.get("install") or {}
        cmd = inst.get("clone") or inst.get("cmd") or inst.get("command") or ""
        if cmd:
            blocks.append(("How do you install it?",
                           "%s\n\nThen point your agent at the skill directory." % cmd))
            blocks_zh.append(("Q：怎么装？", "%s\n\n然后把智能体指向这个 skill 目录即可。" % cmd))

        prov = []
        if repo:
            prov.append("Repository: %s" % repo)
        # 星数不进页面（见 HOW 上方注释）。它仍在 skills/*.json 里供排序和门槛用。
        _badge, _ev = prep.badge_for(PREP_EVIDENCE.get(s.get("id") or ""))
        if _badge == "ready":
            prov.append("Prep work visible in the skill's own text: %s."
                        % ", ".join(prep.SIGNAL_LABELS[x][1] for x in _ev))
        if s.get("skill_count"):
            prov.append("The repository ships %s skills in total." % s["skill_count"])
        if s.get("homepage"):
            prov.append("Homepage: %s" % s["homepage"])
        if prov:
            blocks.append(("Where does it come from?", "\n".join(prov)))
            blocks_zh.append(("Q：它从哪来？", "\n".join(prov)))

        tags = [t for t in [CAT_EN.get(cat, cat), s.get("kind"), s.get("owner")] if t]
        items.append(G.Item(
            slug="%s" % (s.get("id") or name),
            title=name, summary=sum_en or ("Agent skill %s from %s." % (name, repo)),
            title_zh=title, summary_zh=sum_zh,
            blocks=blocks, blocks_zh=blocks_zh,
            source_url=s.get("url") or (("https://github.com/" + repo) if repo else ""),
            updated=(s.get("pushed_at") or s.get("added_at") or "")[:10],
            tags=tags,
        ))
    items.sort(key=lambda i: (i.updated or ""), reverse=True)
    return items


def main():
    items = load_items()
    today = datetime.date.today().isoformat()
    # 内容页归 write_shelf_pages。这里只写机器能读的入口：首页头、sitemap、llms、RSS。
    G.write_robots(SITE, ".", extra_sitemaps=["https://ourword.ai/sitemap.xml"])
    G.write_sitemap(SITE, items, ".", today, extra_urls=())
    # 不把已废弃的 /all/、/t/ 写进 sitemap
    sm = open("sitemap.xml", encoding="utf-8").read()
    sm = "\n".join(line for line in sm.splitlines()
                   if "/skill/all/" not in line and "/skill/t/" not in line
                   and "/skill/zh/" not in line) + "\n"
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    G.write_llms(SITE, items, ".", HOW, CITE, hubs=())
    G.write_rss(SITE, items, ".")
    G.patch_index("index.html", SITE, items, zh=True)
    rep = {"items": len(items), "sitemap": sm.count("<loc>"), "index": True}
    print("pinwei seo/geo:", json.dumps(rep, ensure_ascii=False))
    return rep


if __name__ == "__main__":
    main()
