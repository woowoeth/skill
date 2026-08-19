#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
年龄两个字段：`repo_created_at` 和 `skill_first_seen`，外加口径标记 `age_source`。

# 为什么要两个字段而不是一个

店主想知道的是「**这件 skill** 什么时候出现的」。仓库创建时间只在一种情况下等于它：
**这件 skill 就是仓库本体**（`path` 为空）。skill 长在子目录里时，仓库可能是三年前建的
后端服务，skill 是上周加的 —— 拿仓库年龄当 skill 年龄，误差可以是几年。

在架 152 件里 **78 件（51%）是子目录里的 skill**。所以「先只填 repo_created_at，
标 age_source=repo」这个做法，对一半的货是在印一个答非所问的数字 ——
和「skill_count 含测试夹具」是同一个形状的错：数字来源真实，但回答的不是标签说的那个问题。

# age_source 的三个取值（这一层零网络，本地就能算准）

| 值 | 含义 | 前端 |
|---|---|---|
| `"file"` | 拿到了 `skill_first_seen` —— 这件 skill 自己的首次出现时间 | **显示**，最准 |
| `"repo"` | `path` 为空，这件就是仓库本体，仓库创建时间就是它的年龄 | **显示** |
| `""` | 只有 `repo_created_at`，但这件长在子目录里 —— 那是**仓库**的年龄不是**它**的 | **不显示** |

关键性质：**口径算得出来的时候，数字还没到手。** `age_source` 只依赖 `path`，
本地零网络就能定；日期要等 API。所以口径先落地、数字后补 ——
正好是「印在货架上的数字没核过来源」那个病的反面。

# 取数怎么取

- `repo_created_at` ← `GET /repos/{repo}` 的 `created_at`。每个仓库一次。
- `skill_first_seen` ← 该 `path` 下**最早**的一次提交。GitHub 的 commits 接口按时间倒序，
  所以要先用 `per_page=1` 拿 `Link: rel="last"` 问出总页数，再取最后一页 —— **每件两次调用**。

**没有 token 时未认证配额是 60 次/小时**，填不满全店（在架 152 件、去重仓库上百个）。
所以这个脚本：配额用完就停下、如实报告填到哪一步、**没取到的一律留空，绝不估算**。

用法:
  python3 scouts/fetch_ages.py --probe owner/repo:path   # 只探一件，不写盘（看口径差多少）
  python3 scouts/fetch_ages.py --dry-run                 # 报告要打多少次调用、配额够不够
  python3 scouts/fetch_ages.py --write                   # 真的取并写回 skills/*.json
  python3 scouts/fetch_ages.py --write --limit 40        # 只处理前 40 件（配额有限时分批）
"""
from __future__ import annotations
import os, sys, json, urllib.request, urllib.error, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scout_lib as lib  # noqa: E402

API = "https://api.github.com"
UA = "pinwei-skill-scout/1.0 (+https://github.com/woowoeth/skill)"


_REMAINING: int | None = None      # 从上一次响应头回收的配额，None = 还不知道


def _req(url: str):
    """返回 (json, headers)。失败返回 (None, None) —— 读不到就空着，不猜。

    顺手把 `X-RateLimit-Remaining` 记进 _REMAINING：配额本来就随每个响应回来，
    再单独去问一次 /rate_limit 是白跑一趟网络。
    """
    h = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if lib.GH_TOKEN:
        h["Authorization"] = f"Bearer {lib.GH_TOKEN}"
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=20)
        hd = dict(r.headers)
        global _REMAINING
        try:
            _REMAINING = int(hd["X-RateLimit-Remaining"])
        except Exception:
            pass
        return json.load(r), hd
    except urllib.error.HTTPError as e:
        print(f"    [http {e.code}] {url}")
        return None, None
    except Exception as e:
        print(f"    [{type(e).__name__}] {url}")
        return None, None


def rate_left(force: bool = False) -> int | None:
    """剩余配额。**None = 问不出来**，和「0 = 真的用完了」严格分开。

    混在一起会造出一句假话：网络抖一下就报「配额用尽，停在第 N 件」，
    而实际上配额还满着。宁可说不知道。/rate_limit 本身不计入配额。
    """
    if not force and _REMAINING is not None:
        return _REMAINING
    d, _ = _req(f"{API}/rate_limit")
    if not d:
        return None
    return d.get("resources", {}).get("core", {}).get("remaining")


def repo_created(repo: str) -> str:
    d, _ = _req(f"{API}/repos/{repo}")
    return (d or {}).get("created_at", "")[:10]


def path_first_commit(repo: str, path: str) -> str:
    """该 path 下最早一次提交的日期。两次调用：先问总页数，再取最后一页。"""
    url = f"{API}/repos/{repo}/commits?path={urllib.parse.quote(path)}&per_page=1"
    d, h = _req(url)
    if not d:
        return ""
    last = 1
    link = (h or {}).get("Link", "")
    for part in link.split(","):
        if 'rel="last"' in part and "page=" in part:
            try:
                last = int(part.split("page=")[-1].split(">")[0].split("&")[0])
            except Exception:
                last = 1
    if last > 1:
        d, _ = _req(url + f"&page={last}")
        if not d:
            return ""
    try:
        return d[-1]["commit"]["committer"]["date"][:10]
    except Exception:
        return ""


# 口径判定只有一份实现，在 scout_lib.age_source() —— 这里只是转个手。
age_source = lib.age_source


def _probe(spec: str) -> None:
    repo, _, path = spec.partition(":")
    print(f"探测 {repo}" + (f"  path={path}" if path else "  （仓库本体）"))
    rc = repo_created(repo)
    print(f"  repo_created_at  = {rc or '（取不到）'}")
    if path:
        sf = path_first_commit(repo, path)
        print(f"  skill_first_seen = {sf or '（取不到）'}")
        if rc and sf:
            import datetime
            d = (datetime.date.fromisoformat(sf) - datetime.date.fromisoformat(rc)).days
            print(f"  **口径差 {d} 天**（{d/365:.1f} 年）—— 拿仓库年龄当这件 skill 的年龄就差这么多")


def main() -> None:
    argv = sys.argv[1:]
    if "--probe" in argv:
        for spec in argv[argv.index("--probe") + 1:]:
            if spec.startswith("--"):
                break
            _probe(spec)
        return

    # **读合并视图，写原始文件。** 这两件必须分开：
    #   合并视图（apply_editorial）用来判断在架、拿到店长可能改过的 path；
    #   写盘只能写 skills/*.json 里那份原件 —— 否则店长文案会被烤进商品文件，
    #   变成第二份真相，而且以后从 editorial 撤改也撤不掉（实测 712 件里 334 件受影响）。
    raw = lib.load_items()
    merged = lib.apply_editorial(lib.load_items())
    shelved = [it for it in merged.values() if not it.get("hide")]
    todo = [it for it in shelved if not (it.get("repo_created_at") or "").strip()]
    todo.sort(key=lambda x: x.get("id", ""))          # 确定性，分批跑不会漏也不会重
    if "--limit" in argv:
        todo = todo[:int(argv[argv.index("--limit") + 1])]
    repos = sorted({it["repo"] for it in todo})
    subdir = [it for it in todo if (it.get("path") or "").strip()]
    need = len(repos) + 2 * len(subdir)
    left = rate_left(force=True)
    print(f"待填 {len(todo)} 件 · 去重仓库 {len(repos)} 个 · 子目录件 {len(subdir)} 个")
    print(f"需要约 {need} 次调用（仓库各 1 次 + 子目录件各 2 次）")
    print(f"当前配额剩 " + (f"{left} 次" if left is not None else "**问不出来**")
          + ("（带 token）" if lib.GH_TOKEN else "（未认证，上限 60/小时）"))
    if left is not None and need > left:
        print(f"**配额不够，差 {need - left} 次。** 分批跑（--limit N）或换带 token 的环境；"
              f"这一轮取不到的一律留空，不估算。")
    if "--write" not in argv:
        print("（预演：没有写盘）")
        return

    cache: dict[str, str] = {}
    done = skipped = 0
    for it in todo:
        left = rate_left()
        if left is not None and left <= 3:
            print(f"配额只剩 {left}，停在第 {done} 件 —— 剩下 {len(todo) - done} 件留空，下轮再来")
            skipped = len(todo) - done
            break
        sid, r, path = it["id"], it["repo"], (it.get("path") or "").strip()
        created = cache[r] if r in cache else cache.setdefault(r, repo_created(r))
        first = path_first_commit(r, path) if path else ""
        target = raw.get(sid)
        if target is None:                            # 只在 editorial 里存在，没有原件可写
            print(f"  [跳过] {sid} 在 skills/ 里没有对应文件")
            continue
        target["repo_created_at"] = created
        if path:
            target["skill_first_seen"] = first
        target["age_source"] = lib.age_source(target)
        lib.save_item(target)
        done += 1
        print(f"  [{done}] {sid}  repo={created or '-'} file={first or '-'} "
              f"source={target['age_source'] or '（空=不显示）'}")
    print(f"写回 {done} 件"
          + (f"，还有 {skipped} 件没填（留空，不是「没有」）" if skipped else "")
          + "。跑 python3 scouts/scout_lib.py 重建 feed。")


if __name__ == "__main__":
    main()
