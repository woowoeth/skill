#!/usr/bin/env bash
# 提交并推送，撞冲突不白跑。
#
# 2026-09-03：sweep 判了 800 个候选、上架 8 件，最后「提交」一步 rebase 撞上
# i/*/index.html 和 feed.json 的冲突 → 整轮结果一件没推上去。那些文件全是**生成物**
# （scout_lib.refresh() 从 skills/*.json + editorial/*.json 重建），手合它们毫无意义。
#
# 规矩：先提交**源**，rebase 时生成物冲突随便取一侧，rebase 完从合并后的源重生成一次，再提交推送。
# 这个脚本给所有工作流的提交步骤共用 —— 以前每个工作流各写一遍，各有各的坑。
set -euo pipefail
MSG="${1:-bot: update}"
GEN='^(skills/feed\.json|skills/rejected-feed\.json|i/.*|sitemap\.xml|llms.*\.txt|feed\.xml|robots\.txt|index\.html)$'

git config user.name  "skill-store-bot"
git config user.email "skill-store-bot@users.noreply.github.com"

git add -A
if git diff --cached --quiet; then echo "[sync] 没有变化"; exit 0; fi
git commit -q -m "$MSG"

for attempt in 1 2 3 4 5 6; do
  git fetch -q origin main
  if git rebase origin/main >/dev/null 2>&1; then :; else
    # 冲突：生成物取我们这边（之后重生成），其余取正在 rebase 的提交（我们的改动）
    while [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; do
      git diff --name-only --diff-filter=U | while IFS= read -r f; do
        [ -z "$f" ] && continue
        if echo "$f" | grep -Eq "$GEN"; then git checkout --ours -- "$f" 2>/dev/null || git rm -q --cached -- "$f" 2>/dev/null || true
        else git checkout --theirs -- "$f" 2>/dev/null || true; fi
        [ -e "$f" ] && git add -- "$f" || true
      done
      GIT_EDITOR=true git rebase --continue >/dev/null 2>&1 || { git rebase --skip >/dev/null 2>&1 || true; }
    done
  fi
  # 合并后的源 → 重生成一次生成物
  python3 scouts/scout_lib.py >/dev/null 2>&1 || python3 -c "import sys;sys.path.insert(0,'scouts');import scout_lib as L;L.refresh()" >/dev/null 2>&1 || true
  git add -A
  git diff --cached --quiet || git commit -q -m "$MSG（rebase 后重生成生成物）"
  if git push -q origin HEAD:main; then echo "[sync] 已推 $(git rev-parse --short HEAD)"; exit 0; fi
  echo "[sync] 推被拒（第 $attempt 次），重来"; sleep $(( (RANDOM % 5) + 2 ))
done
echo "[sync] 六次都没推上去"; exit 1
