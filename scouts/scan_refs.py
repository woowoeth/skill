#!/usr/bin/env python3
"""正文自己指向的参考文件，也要过一遍红线 —— 别靠每轮选货的人自己想起来翻。

## 为什么有这个脚本

「门面干净、危险藏在 `references/` 里」这个形状，到 2026-08-20 已经出现**四次**，
而且两次是「门面越讲究，随件越危险」：

  · `SquirtleHankes/super-daddy` —— SKILL.md 写着「绝对禁止剧烈摇晃」「5S 摇幅 2–3 厘米」，
    婴儿对乙酰氨基酚 10-15mg/kg 在 `references/health_guide.md` 第 39 行
  · `nanny-interview-tools/nanny-interview-prep` —— 同一组剂量，同样在 references/
  · `sea0710/medical-record-butler-skill` —— SKILL.md 是干净的病历台账、还写着危急值就医提示；
    被它自己指定为「唯一权威依据」的 `references/blood_test_reference.json` 里是
    `①立即注射G-CSF 150μg qd`、`皮下注射TPO 1万单位 或 IL-11 1.5mg`
  · `WayPanda/dating-skill` —— SKILL.md 是读到过最讲究的 consent 契约（拒绝醉酒、
    拒绝突破拒绝、拒绝权力关系）；`references/interest-escalation-boundaries.md` 是一条身体升级阶梯
  · `ErikaAlk/trip-planner` —— 门面是全店最硬的「不许编造」受控词表；
    随件 `references/scraping-method.md` 是携程飞猪小红书的登录态取数手册

四件都过了「读完 SKILL.md」这一关。**这不再是偶发，是这个生态的一种常见结构。**

## 它做什么、不做什么

**做**：把一件 skill 的 SKILL.md 和它随件的参考/脚本/数据文件全抓下来，逐行扫红线，
把命中的**原文和行号**打出来，让人看见那句话本身。

**不做**：不下判决，不自动拒收。机器给的是「这一行你去看」，判决是人的事
（同 wide_funnel 里 SOFT 的原则：别让机器替人下红线判决）。

**读不到就说读不到。** 超限、404、二进制，一律如实列出 —— 一个静默跳过的文件
和一个扫过没命中的文件，在输出里必须长得不一样。

## 用法

    python3 scouts/scan_refs.py owner/repo                    # SKILL.md 在仓库根
    python3 scouts/scan_refs.py owner/repo:some/path          # SKILL.md 在子目录
    python3 scouts/scan_refs.py --file picks.json             # 批量：读 [{"repo":..,"path":..}]
    python3 scouts/scan_refs.py owner/repo --all              # 连没命中的文件也列出来

认证走 `gh` CLI 现有凭据。不读也不用任何 PAT。
"""
from __future__ import annotations
import argparse, base64, json, os, re, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scouts"))

# 绕反爬那张表**不复制**，从 wide_funnel 导 —— 两份真相迟早会分叉。
from wide_funnel import RED_SCRAPE_HARD  # noqa: E402

# --- 红线表。每一条后面都站着一件真读到过的东西 ---------------------------------
TABLES = {
    # 具体医疗剂量。判据是「**有没有一个数，照着它就能给人用药**」——
    # 「遵医嘱」「按说明书」不算，`10-15mg/kg`、`150μg qd`、`0.1g tid` 算。
    "剂量": re.compile(
        r"(\d+(?:\.\d+)?\s*(?:-|~|–|至)?\s*\d*(?:\.\d+)?\s*"
        r"(?:mg|μg|ug|mcg|g|ml|IU|万单位|单位)\s*/\s*kg"          # 每公斤
        r"|\d+(?:\.\d+)?\s*(?:mg|μg|ug|mcg|g|ml|IU|万单位)\s*"
        r"(?:qd|bid|tid|qid|q\d+h|每日|每天|每次|一日|一次)"        # 剂量+频次
        r"|(?:每次|每日|每天|一次)\s*\d+(?:\.\d+)?\s*(?:mg|μg|ug|g|ml|IU|万单位)"
        r"|皮下注射\s*\S{0,12}\s*\d"
        r"|立即注射|静脉推注|肌注\s*\d)", re.I),
    # 联盟营销分润
    "分润": re.compile(
        r"(联盟(?:链接|营销|计划)|aff(?:iliate)?[-_ ]?(?:link|id|tag)|[?&]tag=[a-z0-9_-]{3,}"
        r"|CPS\s*(?:分润|佣金|链接)|返佣|带货链接|推广位|amzn\.to|taobao\.com/[a-z]*\?.*pid=)", re.I),
    # 身体/关系升级阶梯、话术脚本
    # 「推倒」第一版是裸词，第一次实测就在一份育儿参考里命中了
    # 「叠到 2-3 块时让宝宝推倒（这也是乐趣！）」—— 幼儿搭积木。
    # 所以带人称的那几个词一律要求近处有对象标记（她/他/对方/女生…），
    # 单独一个动词不定罪。**只会产假阳性的判据是噪音，而假阳性挨着真命中最伤信任。**
    "越界话术": re.compile(
        r"(肢体(?:推进|升级|接触)阶梯|身体升级|升级阶梯|escalation\s*(?:ladder|boundaries)"
        # `kino` 第一版是裸词，实测在 **Tsukinomori（月ノ森）** 里面命中了 ——
        # 拉丁字母的短词一律要词边界，否则它会藏在任何专有名词里。
        r"|过度怂|\bkino\b|Mystery\s*Method|Blueprint\s*Decoded"
        r"|(?:推倒|拿下|搞定|攻略)\s*(?:她|他|对方|女生|男生|妹子|目标)"
        r"|(?:她|他|对方|女生|妹子).{0,8}(?:就(?:能|会)上钩|会心动|愿意到你家)"
        r"|话术(?:库|脚本|模板).{0,20}(?:她|他|对方|目标))", re.I),
    # 明文私钥 / 浏览器 cookie / 代执行金融交易
    "密钥与代下单": re.compile(
        r"(-----BEGIN\s+(?:RSA\s+|EC\s+|OPENSSH\s+)?PRIVATE\s+KEY"
        r"|private[-_ ]?key\s*[:=]\s*[\"']?(?:0x)?[0-9a-fA-F]{32,}"
        r"|助记词|mnemonic\s*[:=]|seed\s*phrase"
        r"|browser[-_ ]?cookie3|chrome.*Login\s*Data|读取.{0,6}浏览器.{0,4}cookie"
        r"|create_order|place_order|下单买入|市价买入|一键下单|发起转账|withdraw\()", re.I),
    # AIGC 检测规避
    "检测规避": re.compile(
        r"(bypass\s*(?:gptzero|turnitin|zerogpt|copyleaks|originality)"
        r"|绕过\s*(?:查重|AI\s*检测|AIGC\s*检测)|降\s*AIGC|过\s*turnitin|降重)", re.I),
}
# 绕反爬用共享的那张表
TABLES["绕反爬"] = RED_SCRAPE_HARD

# 「这一行是在说它不做这件事」。命中不丢，只是换个标签打出来。
# 「这一行说的是毒性/致死阈值」，不是用药剂量。
TOX_CONTEXT = re.compile(
    r"(中毒|致死|毒性|半数致死|LD\s*50|lethal|toxic|中毒量|超过.{0,6}会中毒|危险剂量)", re.I)

REFUSAL = re.compile(
    r"(never|don'?t|do not|refuse|without\s+bypass|not\s+bypass|user\s+(?:clears|solves|does)"
    r"|不会|不许|不得|禁止|拒绝|绝不|从不|由(?:你|用户)|你自己|用户自己|手动(?:过|输)|请你)", re.I)

# 自动纳入扫描的目录（不用等正文点名）
AUTO_DIRS = ("references/", "reference/", "assets/", "scripts/", "data/", "docs/", "prompts/")
TEXTY = (".md", ".txt", ".json", ".yaml", ".yml", ".py", ".js", ".mjs", ".ts", ".sh",
         ".csv", ".toml", ".ini", ".html")
MAX_BYTES = 400_000          # 单文件上限，超了如实报「太大没读」
MAX_FILES = 60               # 单件上限，超了如实报「只读了前 N 个」


def gh(path: str):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode != 0:
        return None, (r.stderr or "").strip()[:140]
    try:
        return json.loads(r.stdout), None
    except Exception as e:                                    # noqa: BLE001
        return None, f"响应不是 JSON: {e}"


def fetch_text(repo: str, path: str):
    """→ (text, err)。err 不是 None 时 text 一定是 None，反之亦然。"""
    d, err = gh(f"repos/{repo}/contents/{path}")
    if err:
        return None, err
    if isinstance(d, list):
        return None, "是目录不是文件"
    if (d.get("size") or 0) > MAX_BYTES:
        return None, f"{d['size']} 字节，超过 {MAX_BYTES} 上限，没读"
    if not d.get("content"):
        return None, "没有 content 字段（可能是 LFS 或过大）"
    try:
        return base64.b64decode(d["content"]).decode("utf-8", "replace"), None
    except Exception as e:                                    # noqa: BLE001
        return None, f"解码失败: {e}"


def referenced_paths(text: str, base: str) -> set[str]:
    """正文里点名的本地路径。只收看起来像仓库内相对路径的。"""
    out = set()
    pats = (r"\[[^\]]*\]\(([^)\s#]+)\)",          # markdown 链接
            r"`([^`\n]+?\.(?:md|json|txt|ya?ml|py|js|csv|html))`",
            r"(?:^|\s)((?:\.{0,2}/)?(?:references?|assets|scripts|data|prompts)/[^\s`)\"']+)")
    for p in pats:
        for m in re.finditer(p, text, re.M):
            u = m.group(1).strip()
            if u.startswith(("http://", "https://", "mailto:", "#")):
                continue
            u = u.lstrip("./")
            if not u or ".." in u:
                continue
            out.add(f"{base}/{u}" if base else u)
    return out


def scan_one(repo: str, path: str = "", show_all: bool = False) -> dict:
    base = path.strip("/")
    smd = f"{base}/SKILL.md" if base else "SKILL.md"
    print(f"\n{'='*72}\n{repo}" + (f"  ({base})" if base else "") + f"\n{'='*72}")

    tree, err = gh(f"repos/{repo}/git/trees/HEAD?recursive=1")
    if err:
        print(f"  ✗ 取不到文件树：{err}")
        return {"repo": repo, "path": base, "unreadable": ["<tree>"], "hits": []}
    all_paths = [t["path"] for t in (tree.get("tree") or []) if t.get("type") == "blob"]

    # 没指定 path 时**自己去树里找 SKILL.md**，别让「没告诉我在哪」变成漏扫。
    # 实测栽过一次：`sea0710/medical-record-butler-skill` 的 SKILL.md 在 `skill/` 下，
    # 工具报了「读不到」就收工 —— 那份带化疗剂量的 references/ 一个字没扫。
    # 报错不等于尽到了责任：手里明明有整棵树。
    if smd not in all_paths:
        found = sorted((p for p in all_paths if p.endswith("SKILL.md")),
                       key=lambda p: (p.count("/"), p))
        if not found:
            print(f"  ✗ 整棵树里没有 SKILL.md —— 这本身就是问一（装不进 agent）")
            return {"repo": repo, "path": base, "unreadable": ["<no SKILL.md>"], "hits": []}
        smd = found[0]
        base = os.path.dirname(smd)
        print(f"  ! 给的路径下没有 SKILL.md，自己在树里找到：{smd}"
              + (f"（另有 {len(found)-1} 个：{found[1:4]}）" if len(found) > 1 else ""))

    body, err = fetch_text(repo, smd)
    if err:
        print(f"  ✗ SKILL.md 读不到（{smd}）：{err}")
        return {"repo": repo, "path": base, "unreadable": [smd], "hits": []}

    # 要扫的文件 = SKILL.md + 正文点名的 + 自动纳入目录下的
    want = {smd}
    named = {p for p in referenced_paths(body, base) if p in all_paths}
    want |= named
    prefix = f"{base}/" if base else ""
    auto = {p for p in all_paths
            if p.startswith(prefix) and p.endswith(TEXTY)
            and any(f"/{d}" in f"/{p[len(prefix):]}" or p[len(prefix):].startswith(d)
                    for d in AUTO_DIRS)}
    want |= auto
    ordered = sorted(want)
    trimmed = ordered[:MAX_FILES]
    print(f"  正文点名 {len(named)} 个 · 自动纳入 {len(auto)} 个 · 合计扫 {len(trimmed)}"
          + (f"（**上限 {MAX_FILES}，剩下 {len(ordered)-MAX_FILES} 个没扫**）"
             if len(ordered) > MAX_FILES else ""))

    hits, unread, clean = [], [], []
    for p in trimmed:
        txt, err = fetch_text(repo, p)
        time.sleep(0.25)
        if err:
            unread.append((p, err))
            continue
        found = []
        for label, pat in TABLES.items():
            for m in pat.finditer(txt):
                ln = txt.count("\n", 0, m.start()) + 1
                lines = txt.splitlines()
                line = lines[ln - 1].strip() if ln - 1 < len(lines) else ""
                # 长行（压缩 JSON、一整行 CSV）要显示**命中点周围的窗口**，不是行首。
                # 实测栽过：`blood_test_reference.json` 是单行 JSON，
                # 打出来的「第 1 行」是文件开头的字段说明，真正命中的剂量在几千字符之后 ——
                # 一条指错地方的线索，比没有线索更浪费人的时间。
                if len(line) > 150:
                    ls = txt.rfind("\n", 0, m.start()) + 1
                    a, b = max(ls, m.start() - 70), m.end() + 70
                    line = ("…" if a > ls else "") + txt[a:b].replace("\n", " ") + "…"
                line = line[:200]
                # 「声明不做」的行**不丢，单独标**。
                # `ErikaAlk/trip-planner` 的 SKILL.md 里三处命中都是诚实的拒绝
                # （"You never read, solve, or bypass CAPTCHAs"），而真问题在
                # `references/research-playbook.md` 的「按反爬强度分流」路由表里。
                # **两边都摆出来才是完整的故事** —— 丢掉拒绝那半，读的人会以为它在吹自己会绕；
                # 丢掉路由表那半，就是这个脚本存在的理由没了。
                # 「声明不做」的标记必须**紧挨着命中词**（前后 25 字内），不能是整行里有就算。
                # 实测栽过：trip-planner 的路由表里有一行
                # 「反爬/登录/验证码重 → 真实 Chrome；真人指纹最不易被风控；撞验证码能让用户手动过」——
                # 整行里有「手动过」，于是这一行被标成了「声明不做」，
                # **而它恰恰是这一件的真问题。差点被我自己的降噪盖掉。**
                near = txt[max(0, m.start() - 25):m.end() + 25]
                tag = f"{label}·声明不做" if REFUSAL.search(near) else label
                found.append((tag, ln, m.group(0)[:60], line))
        # 毒性阈值不是用药指示 —— **它跟「照着它就能给人用药」正好相反**。
        # 实测栽过：`Zgdfsgd/fridge-hero` 的高风险清单里写「中毒剂量：2-5mg/kg体重」，
        # 那是在劝你别吃，不是在教你喂。同理 LD50 / 致死量 / lethal dose。
        found = [f for f in found
                 if not (f[0].startswith("剂量") and TOX_CONTEXT.search(f[3]))]
        if found:
            hits.append((p, found))
        else:
            clean.append(p)

    for p, found in hits:
        star = " ⚠ **不是 SKILL.md**" if p != smd else ""
        print(f"\n  ▸ {p}{star}")
        seen = set()
        for label, ln, hit, line in found:
            k = (label, ln)
            if k in seen:
                continue
            seen.add(k)
            print(f"      [{label}] 第 {ln} 行: {line or hit}")
    if unread:
        print(f"\n  读不到 {len(unread)} 个（**不是扫过没命中**）：")
        for p, e in unread:
            print(f"      {p} —— {e}")
    if show_all and clean:
        print(f"\n  扫过没命中 {len(clean)} 个：")
        for p in clean:
            print(f"      {p}")
    if not hits:
        print(f"\n  ✓ 扫了 {len(clean)} 个文件，没命中"
              + (f"；另有 {len(unread)} 个读不到" if unread else ""))
    else:
        real = [(p, [f for f in fs if "·声明不做" not in f[0]]) for p, fs in hits]
        real = [(p, fs) for p, fs in real if fs]
        n_say = sum(1 for _, fs in hits for f in fs if "·声明不做" in f[0])
        if n_say:
            print(f"\n  （其中 {n_say} 处是「声明不做」，不是它会做 —— 但两边都摆出来才是完整的故事）")
        off = [p for p, _ in real if p != smd]
        if off:
            print(f"\n  ‼ **命中里有 {len(off)} 个不在 SKILL.md 里** —— "
                  f"就是「门面干净、问题在随件里」那个形状")
    return {"repo": repo, "path": base,
            "hits": [{"file": p, "found": [{"label": a, "line": b, "text": d}
                                           for a, b, _, d in f]} for p, f in hits],
            "unreadable": [{"file": p, "why": e} for p, e in unread],
            "clean": clean}


def main() -> None:
    ap = argparse.ArgumentParser(description="扫一件 skill 的正文与随件文件里的红线")
    ap.add_argument("target", nargs="?", help="owner/repo 或 owner/repo:path")
    ap.add_argument("--file", help="批量：一个 JSON，[{repo, path}] 或 {keep:[…]}")
    ap.add_argument("--all", action="store_true", help="连扫过没命中的文件也列出来")
    ap.add_argument("--json", dest="as_json", help="把结果写到这个路径")
    a = ap.parse_args()

    jobs = []
    if a.file:
        d = json.load(open(a.file, encoding="utf-8"))
        rows = d.get("keep") if isinstance(d, dict) else d
        jobs = [(r["repo"], (r.get("path") or "")) for r in rows]
    elif a.target:
        repo, _, path = a.target.partition(":")
        jobs = [(repo, path)]
    else:
        ap.error("给一个 owner/repo，或者 --file")

    out = [scan_one(r, p, a.all) for r, p in jobs]
    n_hit = sum(1 for o in out if o["hits"])
    n_off = sum(1 for o in out for h in o["hits"]
                if h["file"] != (f"{o['path']}/SKILL.md" if o["path"] else "SKILL.md"))
    n_unread = sum(len(o["unreadable"]) for o in out)
    print(f"\n{'='*72}\n扫了 {len(out)} 件 · 有命中 {n_hit} 件 · "
          f"**命中在随件里的 {n_off} 处** · 读不到 {n_unread} 个文件")
    print("机器只指出「这一行你去看」，判决是人的事。")
    if a.as_json:
        json.dump(out, open(a.as_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"→ {a.as_json}")


if __name__ == "__main__":
    main()
