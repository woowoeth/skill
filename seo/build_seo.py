#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO/GEO build for Skill 商店. Run from the repo root: python seo/build_seo.py"""
import datetime
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo_kit as G

SITE = G.Site(
    path="skill-store",
    name="Skill Store", name_zh="Skill 商店",
    tagline="agent skills worth installing, restocked daily",
    tagline_zh="每天上新的好玩 Agent Skill 精选店",
    description=(
        "A daily-restocked shelf of agent skills for Claude Code, Codex and other coding "
        "agents — each one with what it actually does, who it is for, and the one-line "
        "install command. Skills are picked by hand from public repositories; the shelf "
        "favours the ones that are fun or genuinely useful over the ones that merely exist."),
    description_zh=(
        "每天上新的 Agent Skill 精选店：给 Claude Code、Codex 这类编程智能体用的 skill，"
        "每一条都写清楚它到底做什么、适合谁、以及一行安装命令。所有 skill 从公开仓库人工挑选，"
        "偏好「好玩」或者「真有用」的，而不是「存在」的。"),
    keywords=("claude code skills, agent skills, claude skills, codex skills, MCP skills, "
              "AI agent plugins, skill 商店, agent skill 推荐, claude code 技能, 智能体插件"),
    item_type="SoftwareApplication", item_noun="skill", item_noun_zh="skill",
    changefreq="daily",
)

HOW = ("Scouts crawl public GitHub repositories for skill definitions every day; each candidate "
       "is checked by hand before it goes on the shelf. Star counts and last-push dates come "
       "straight from the GitHub API.")

CITE = ("Cite the individual skill page. The skill itself belongs to its author — the repository "
        "link on each page is the authoritative source. Attribute the shelf note to "
        "\"Skill Store (OurWord AI)\".")

CAT_EN = {"dev": "development", "creative": "creative", "writing": "writing", "work": "work",
          "docs": "documentation", "meta": "meta", "fun": "fun", "life": "life"}
CAT_ZH = {"dev": "写代码", "creative": "创作", "writing": "写字", "work": "办公",
          "docs": "文档", "meta": "元技能", "fun": "好玩", "life": "生活"}


def load_items():
    items = []
    for p in sorted(glob.glob("skills/*.json")):
        try:
            s = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if s.get("hide"):
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
        if stars:
            prov.append("%s stars on GitHub at the time of listing." % stars)
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
    rep = G.build(SITE, items, root=".", today=datetime.date.today().isoformat(),
                  how_built=HOW, cite_as=CITE,
                  extra_sitemaps=["https://ourword.ai/sitemap.xml"])
    print("skill-store seo/geo:", json.dumps(rep, ensure_ascii=False))
    return rep


if __name__ == "__main__":
    main()
