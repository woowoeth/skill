---
name: connect
description: 统一收件箱：一条命令汇总微信没回的消息、飞书待处理（IM 未回/任务/审批/未读邮件）、Obsidian 拖延任务，输出稳定 JSON 给 Today.app、cron 和任意 Agent；内置 doctor 本地体检与首次安装 onboarding（微信密钥提取与解密、lark-cli 安装与设备码授权、vault 配置）。当用户说 统一收件箱、收件箱、inbox、connect、今天有什么没处理、谁在等我回、我欠了谁、微信没回的消息、飞书待办、待审批、未读邮件、拖延任务、体检、doctor、配置 connect、安装 connect、setup connect 时使用；遇到退出码 1/2、sources 状态 error/stale/unauthenticated/unavailable、HMAC 验证失败、密钥过期、missing_scopes、device_code is invalid 时也用本 skill 排障。只读不写：不发不回消息（飞书发消息因 app 层未开通 im:message.send_as_user，明确不支持）、不改任务完成态；微信待办/日程/干货的 Discord 推送流水线归 wx-echo 老 skill，飞书文档/表格等操作归 lark 系列 skill。
metadata:
  version: 0.1.0
  requires:
    bins: ["python3"]
    optional-bins: ["lark-cli", "cc", "npm", "sqlite3"]
---

# connect — 统一收件箱

三个来源，一个出口：**微信没回的消息 + 飞书待处理（im/task/approval/mail）+ Obsidian
拖着没干的任务** → 一条命令 → 稳定 JSON。Layer 1（scripts/ 纯 Python）只出事实，
Layer 2（本文件）负责判断与引导——改分析口径改文档，不用动代码。

## 0. 路径规则（就一条）

**work_dir = config.yaml 所在目录**。skill 目录（本文件所在，下称 skill_dir）只读；
密钥、解密数据、venv 等运行时产物全住 work_dir（推荐 `~/.connect/`）。config 里的
相对路径都相对 work_dir 解析；想复用别处已有数据（比如旧的解密目录），写绝对路径。

config 寻址顺序：`--config` 参数 > 环境变量 `$CONNECT_CONFIG` > `~/.connect/config.yaml`。

标准命令形态（Today.app / cron 就用这个，cwd 无关）：

```bash
<work_dir>/venv/bin/python <skill_dir>/scripts/inbox.py --config <work_dir>/config.yaml --refresh
```

## 1. 主流程判定树（任何请求先走这里）

```
用户要收件箱/待办汇总/排障
        │
        ▼
python3 <skill_dir>/scripts/doctor.py --config <cfg> --quick     # 纯 stdlib，<1s
        │
   ├─ 退出码 0/1（无 fail）──────► 直接拉取：
   │      <venv_python> scripts/inbox.py --config <cfg> --refresh
   │      按用户意图呈现（口语总结/markdown/原始 JSON）
   │
   └─ 退出码 2（有 fail）────────► 进 onboarding（§4）：
          逐条看 checks[] 里 status=fail 的项，
          按它的 fix 执行 / 引导，按它的 ref 读对应 reference，
          修完复跑 doctor，全绿再拉取
```

两条铁律：

1. **inbox 退出码 1 ≠ 失败**。那是「部分降级」：看 `sources.<name>.status` 分块采信，
   好的照常用，坏的把它的 `error`/`fix` 转告用户。绝不因为一个源挂了丢掉整份结果。
2. **首次安装 / 用户说「配置 connect」→ 直接进 §4**，不用先跑 doctor 猜。

## 2. 命令速查

### inbox.py（取数唯一入口）

```bash
<venv_python> <skill_dir>/scripts/inbox.py --config <cfg> [选项]
```

| 选项 | 说明 |
|---|---|
| `--sources wechat,feishu,obsidian` | 默认全开 |
| `--format json\|markdown\|both` | 默认 json；both = JSON 里多个 markdown 字段 |
| `--refresh` | 取数前先增量解密微信（数百毫秒），要新数据就带上 |
| `--limit N` / `--out FILE` / `--include-muted` | 截断 / 落盘 / 放回被静音项 |

退出码：**0** 三源全好 · **1** 部分降级（数据仍有效）· **2** 全挂。

### doctor.py（体检，onboarding 的判定核心）

```bash
python3 <skill_dir>/scripts/doctor.py --config <cfg> [--quick] [--format markdown]
```

纯 stdlib，**venv 没建好也能跑**（它就是用来诊断这个的）。`--quick` 只做文件系统级
检查（<1s，不起子进程不调 lark-cli）；全量档追加依赖探测、lark-cli 身份/scope、
self_wxid 比对。每项检查输出 `{id, status, detail, fix, ref}`——**fix 是可直接执行的
命令，ref 是要读的 reference**。

退出码：**0** 全绿 · **1** 只有 warn · **2** 有 fail。

### refresh_decrypt.py（微信解密）

```bash
<venv_python> <skill_dir>/scripts/refresh_decrypt.py --config <cfg> [--full]
```

日常增量 ~百毫秒级；`--full` 只在**首次安装**和**密钥重提后**用。退出码 2 = 密钥
HMAC 失败 → 读 `references/wechat-keys.md`。

## 3. 输出一分钟版（完整契约 → references/contract.md）

`items[]` 已按 `waiting_hours`（拖了多久）倒序。每条：

```
id       全局唯一且跨次运行稳定 → 可去重、可记「已处理」
source   wechat | feishu | obsidian
kind     dm | group_mention | feishu_im | feishu_task | feishu_approval | feishu_mail | task
title    微信=联系人 / 飞书=标题 / Obsidian=任务正文
detail   预览或文件位置          link  能跳则给（如 obsidian://）
flags    closer(收尾应答) looks_done(疑似已完成) date_guessed(日期靠猜) unread …
raw      源原始条目，不丢字段
```

`closer`/`looks_done` 默认被静音（所以 `sources.<name>.count` ≥ `counts.<name>` 是
正常的，差额=静音数）；`--include-muted` 放回。`wechat.status == "stale"` = 解密数据
超 2 小时，用 `--refresh`。

## 4. Onboarding（doctor 有 fail，或用户要求安装/配置时）

### 总控

- 顺序：**env → 微信 → 飞书 → Obsidian**。三源独立，用户可以只要其中一两个：
  不要的源在 config 里 `enabled: false`（obsidian 留空 vault 亦可），doctor 会跳过。
- 每修一项就复跑 `doctor --quick` 看进度，全绿后跑一次 inbox 收尾验证。
- **话术铁律**：凡是要 **sudo**（提微信密钥）、要**浏览器**（lark-cli config init、
  扫码授权）、可能要**密码**（npm -g）的步骤——一律输出命令请用户在自己终端执行，
  说「跑完告诉我」。Agent 绝不代跑 sudo，绝不索要密码。

### 4.1 环境

```bash
mkdir -p ~/.connect
cp <skill_dir>/config.example.yaml ~/.connect/config.yaml
python3 -m venv ~/.connect/venv
~/.connect/venv/bin/pip install -r <skill_dir>/scripts/requirements.txt
```

系统 python 常见是 externally-managed 且三个依赖全无——**别往系统 pip 装**，venv 是
唯一正路。

### 4.2 微信（最重的一段，坑也最多）

1. **编译密钥工具**（无需 sudo）：
   `cc -O2 -o find_all_keys_macos <skill_dir>/scripts/decrypt/find_all_keys_macos.c`
2. **提取密钥**【用户终端】——微信必须正在运行：
   `cd <work_dir> && sudo ./find_all_keys_macos`
   必须先 cd：`all_keys.json` 输出到当前目录。详细话术与失败分支 → `references/wechat-keys.md`
3. **填 config**：
   - `db_dir`：`ls -d ~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/*/db_storage`
     取带 wxid 的那个（doctor 探测不到时会把候选写进 detail）
   - `self_wxid`：**必须查 contact.db，禁止抄目录名**（目录名带 `_xxxx` 后缀，DB 里
     不带；抄错不报错、只是静默全空）→ `references/wechat-pitfalls.md`。
     解密前填不了没关系，先留空，第 5 步之后 doctor full 会教你查
4. **首次全量解密**：
   `<venv_python> <skill_dir>/scripts/refresh_decrypt.py --config <cfg> --full`
   历史消息多的号可达 19GB 级、要几分钟，**提前告知用户别以为卡死**。
   已有旧解密数据的机器：config 写绝对路径指过去复用，不要重解。
5. **回填 self_wxid** 并跑 `doctor`（full）复检——它会比对 contact.db，抄了目录名会
   被当场抓住（warn 且给出应改值）。

### 4.3 飞书

1. **装 CLI**：`npm install -g @larksuite/cli@latest`
   ——**不要用 npx 方式**（会 checksums 校验失败回滚）。装之前先确认是不是真没装：
   沙箱 PATH 常缺 `/opt/homebrew/bin`，`which` 落空 ≠ 没装，doctor 会兜底探测并
   给出绝对路径；已装但读不到时用 `CONNECT_LARK_CLI=/绝对路径` 指定 → `references/feishu-setup.md`
2. **配应用凭证**【用户浏览器】：`lark-cli config init`
3. **用户登录授权**——设备码 **split-flow 两轮**，一步都不能并：
   - 轮 1：`lark-cli auth login --recommend --no-wait --json` → 提取 verification_url
     与 device_code → `lark-cli auth qrcode "<url>" --output <png>` → **URL 在前、
     二维码在后**发给用户 → 说「授权完回来告诉我，**授权页把权限全勾上**」→
     **本轮到此为止，别再跑任何东西**
   - 轮 2（用户确认后）：`lark-cli auth login --device-code "<code>"`
   - 码 600 秒过期、重新发起会作废旧码；连挂两次就换兜底（用户自己终端跑
     `lark-cli auth login --recommend`）→ 全部细节 `references/feishu-auth.md`
4. **验证**：`lark-cli auth status` 看 `identities.user.available == true`。
   doctor full 会顺带查各线 scope，缺的直接给出增量授权命令。

### 4.4 Obsidian

问用户 vault 路径 → 填 `obsidian.vault` → doctor 验证目录存在且有 .md。
不装 Obsidian 桌面版也完全能用（纯文件读取）。建议 onboarding 时跑一次
`inbox.py --sources obsidian` 看结果，把混进来的「自动生成任务清单」路径加进
`obsidian.exclude` → `references/obsidian-notes.md`

## 5. doctor 检查项 → 处置对照

| id | fail 时读 | 一句话 |
|---|---|---|
| env.config / env.work_dir / env.venv / env.deps | §4.1 | 复制模板 / 建 venv / 装依赖 |
| wechat.db_dir | wechat-keys.md | detail 里有探测到的候选路径 |
| wechat.process | wechat-keys.md | warn 而已；只有提密钥那一刻必须微信在跑 |
| wechat.keys_file / wechat.key_hmac | wechat-keys.md | 用户终端 sudo 提密钥 → --full 重解 |
| wechat.decrypted | wechat-keys.md | 没有→--full；stale→--refresh |
| wechat.self_wxid | wechat-pitfalls.md | warn=抄了目录名（给了应改值）；fail=彻底不对 |
| feishu.cli / feishu.app_config | feishu-setup.md | npm 直装 / config init |
| feishu.user_identity | feishu-auth.md | split-flow 登录 |
| feishu.scopes | feishu-auth.md | warn：对应线降级，fix 里是现成的增量授权命令 |
| obsidian.vault / obsidian.has_md | obsidian-notes.md | 路径填对即可 |

## 6. 已知限制（负向清单，用户问到照实说）

- **不发消息、不回消息**。飞书侧 `im:message.send_as_user` 在 app 层未开通（要去
  开发者后台加 + 可能要管理员审批）；微信侧本 skill 只读解密库，无发送通道。
- **不回写完成态**：不勾 Obsidian 的框、不完成飞书任务、不代审批。
- 微信待办/日程/干货 → Discord 的闭环流水线是 **wx-echo** skill 的事；飞书文档/
  表格/日历等操作找 **lark-cli 自带 skill**（`lark-cli skills list`）。
- Windows 未适配（密钥提取工具是 macOS 的）。

## 7. Reference 强触发索引

命中任一条件时，**先读对应 reference 再动手**。命中多条按表序读，同一文件只读一次。

| 强触发条件（具体到错误串/退出码/字段名） | Reference |
|---|---|
| `HMAC 验证失败` / refresh_decrypt 退出码 2 / doctor `wechat.key_hmac` fail / `Full Disk Access` / 准备引导提密钥 / 首次全量解密 | `references/wechat-keys.md` |
| doctor `wechat.self_wxid` warn 或 fail / warning 含 `在 contact.db 中不存在` / `counts.wechat` 恒 0 且无报错 / preview 出现 `[消息类型 21474836…]` / 公众号混进结果 | `references/wechat-pitfalls.md` |
| `本机没有 lark-cli` / `sources.feishu.status == "unavailable"` / `checksums.txt not found` / 悬空 symlink / `command not found: lark-cli` 但机器其实装过 / `config init` 相关 | `references/feishu-setup.md` |
| `unauthenticated` / `identities.user.available == false` / `bot 不支持此命令` / `missing_scopes` / `missing required scope` / `console_url` / `device_code is invalid` / 准备发起或完成 `auth login` | `references/feishu-auth.md` |
| 飞书条目 `waiting_hours` 全 null / 混入机器人会话（`sender_type: app`、`p2p_target_type: bot`）/ 名字显示成 id / stderr 出现 `{"ok":false` / preview 全是 msg_type 占位符 | `references/feishu-pitfalls.md` |
| `vault 不存在` / doctor `obsidian.*` fail / 要解释 `date_guessed`、`looks_done`、`truncated_files` / 结果里全是检查清单式条目 | `references/obsidian-notes.md` |
| 调用方要字段定义 / 退出码语义 / `raw` 里有什么 / 做去重或「已处理」标记 / `count` 与 `counts` 对不上 | `references/contract.md` |

## 8. 维护

- **微信重启后**：密钥必失效。固定三步——用户终端 sudo 重提 → `refresh_decrypt --full`
  → `doctor --quick` 复检。inbox 的 `refresh.ok == false` 或 doctor `wechat.key_hmac`
  fail 都是同一件事。
- **飞书 token**：user token 2 小时自续（refresh token 7 天滚动）。彻底掉了 =
  `user_identity` fail → 重走 §4.3 第 3 步。
- **加/减飞书线**：改 config `feishu.sources`；加线后跑 doctor full 看 scope 缺不缺。
- **Obsidian 噪音**：结果里混进机器清单 → 把路径加进 `obsidian.exclude`。
