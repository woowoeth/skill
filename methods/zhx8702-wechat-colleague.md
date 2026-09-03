---
name: wechat-colleague
description: "微信同事蒸馏器 — 从微信聊天记录中解密数据、查看消息、蒸馏人物 AI Skill。全流程文档驱动，按需生成代码。"
argument-hint: "[command] [args]"
version: "3.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Agent, Glob, Grep
---

# 微信同事蒸馏器 v3

从本地微信聊天记录中：**解密数据库 → 查看消息 → 蒸馏人物 Skill**。

本 Skill 不预置代码，而是基于技术文档**按需生成**。所有加密规格、数据库结构、分析模板都在 `docs/` 和 `prompts/` 中。

---

## 命令

| 命令 | 说明 |
|------|------|
| `/wechat-colleague setup` | 首次设置：检测环境、生成提取脚本、解密数据库 |
| `/wechat-colleague sync` | 同步最新消息（增量解密） |
| `/wechat-colleague viewer` | 生成并启动 Web 聊天记录查看器 |
| `/wechat-colleague [人名]` | 蒸馏指定人（自动搜索所有会话） |
| `/wechat-colleague [人名] [群名]` | 从指定群蒸馏指定人 |
| `/wechat-colleague list` | 列出已蒸馏的同事 |
| `/wechat-colleague update [slug]` | 更新已有同事 |
| `/wechat-colleague delete [slug]` | 删除同事 |

无参数时自动检测状态并引导。

---

## 技术文档

在执行任何阶段前，先 Read 对应文档：

| 文档 | 内容 | 何时读取 |
|------|------|---------|
| `docs/encryption.md` | 数据库加密方案、密钥提取算法、解密伪代码 | setup / sync 时 |
| `docs/database_schema.md` | 数据库表结构、字段含义、SQL 查询参考 | 查看/蒸馏时 |
| `prompts/work_analyzer.md` | 工作能力提取维度和规则 | 蒸馏时 |
| `prompts/persona_analyzer.md` | 性格画像提取维度和标签翻译表 | 蒸馏时 |
| `prompts/work_builder.md` | work.md 生成模板 | 蒸馏时 |
| `prompts/persona_builder.md` | persona.md 五层结构模板 | 蒸馏时 |

文档路径用 `${CLAUDE_SKILL_DIR}/docs/` 和 `${CLAUDE_SKILL_DIR}/prompts/` 引用。

---

## Phase 1: Setup

### 自动状态检测

每次调用先检查：
```bash
# 1. 能否找到微信数据目录
find /mnt/c/Users/*/Documents/xwechat_files/ -name "db_storage" -type d 2>/dev/null  # WSL
# 或 ~/Documents/xwechat_files/ (Windows) 或 ~/Library/Containers/com.tencent.xinWeChat/ (macOS)

# 2. 是否已有 keys.json
# 3. 是否已有解密后的数据库
# 4. 数据库能否正常查询
```

### 密钥提取

Read `${CLAUDE_SKILL_DIR}/docs/encryption.md` 获取完整加密规格，然后：

1. **检测平台**（WSL/Windows/macOS）
2. **生成密钥提取 Python 脚本**，写到工作目录
   - 技术要点全在 `docs/encryption.md` 的「密钥提取」章节
   - Windows: 用 `pymem` + `psutil` 读 `Weixin.exe` 进程内存
   - 搜索正则: `x'([0-9a-fA-F]{96})'`
   - 通过 salt (数据库前16字节) 匹配密钥到数据库
   - 多账号时列出让用户选择
3. **引导用户运行**（需管理员权限）
   - WSL 环境可用 `powershell.exe python <脚本>` 直接调用
   - Windows 原生直接运行
4. **输出 keys.json**: `{ "数据库相对路径": "密钥hex" }`

### 数据库解密

Read `docs/encryption.md` 的解密算法，生成解密脚本：
- 逐页 AES-256-CBC 解密
- 第 1 页替换为 SQLite 头
- 每页保留区填零
- header[20] 设为 0x50
- 依赖: `pycryptodome`

### 验证

```bash
sqlite3 <db> "SELECT COUNT(*) FROM sqlite_master;"
```

---

## Phase 2: Sync

1. 读 keys.json
2. 对比每个加密 db 的 mtime 与解密版本
3. 只重新解密有变化的
4. 同步逻辑可以复用 Phase 1 的解密代码

---

## Phase 3: Viewer

Read `${CLAUDE_SKILL_DIR}/docs/database_schema.md` 获取数据库结构，生成 Flask Web 查看器：

**核心功能**：
- 会话列表（SessionTable, 按 sort_timestamp 排序）
- 聊天消息（Msg_<md5> 表, 按 create_time 排序）
- 头像（head_image.image_buffer, 明文 JPEG）
- 引用消息解析（XML 中 refermsg 节点）
- zstd 解压（WCDB_CT=4 时）
- 群聊发送者解析（`wxid:\n内容` 格式）
- 消息搜索
- 手动/自动同步刷新

**技术栈**：Flask + 单文件 HTML (内联 CSS/JS)
**端口**：5050

---

## Phase 4: 蒸馏人物

### Step 1: 搜索目标

Read `docs/database_schema.md` 了解表结构，然后直接用 Python+sqlite3 查询：

```python
# 搜索联系人
SELECT username, nick_name, remark FROM contact WHERE nick_name LIKE ? OR remark LIKE ?

# 搜索群
SELECT username, last_timestamp FROM SessionTable WHERE username LIKE '%@chatroom'

# 确认消息量：扫描 Msg_<md5> 表中以目标 wxid 开头的消息
```

### Step 2: 提取消息

```python
# 提取指定人在指定群的消息
table = "Msg_" + md5(chat_username)
# 解析 message_content (群聊去掉 wxid:\n 前缀)
# zstd 解压 (WCDB_CT=4)
# 引用消息解析 XML
# 格式化为: [YYYY-MM-DD HH:MM] 内容
# 统计: 消息量、活跃时段、高频词、类型分布
```

### Step 3: 双线分析

Read 以下 prompt 模板：
- `${CLAUDE_SKILL_DIR}/prompts/work_analyzer.md` — 工作能力提取维度
- `${CLAUDE_SKILL_DIR}/prompts/persona_analyzer.md` — 性格画像提取维度

基于提取的消息内容进行分析。

### Step 4: 生成 Skill

Read 以下模板：
- `${CLAUDE_SKILL_DIR}/prompts/work_builder.md` — work.md 格式
- `${CLAUDE_SKILL_DIR}/prompts/persona_builder.md` — persona.md 五层结构

生成并写入：

```
${CLAUDE_SKILL_DIR}/colleagues/<slug>/
├── SKILL.md          # frontmatter + PART A + PART B + 运行规则
├── work.md
├── persona.md
├── meta.json
└── knowledge/
    └── messages.txt
```

**同时安装到 `~/.claude/skills/colleague-<slug>/`** 使其可直接调用。

SKILL.md 格式：
```yaml
---
name: colleague-<slug>
description: "<名字> — <一句话描述>"
user-invocable: true
---
```

末尾运行规则：
```
1. PART B 判断态度
2. PART A 执行任务
3. 保持 PART B 表达风格
4. Layer 0 最高优先级
```

---

## Phase 5: 进化

### 纠正
用户说 "不对" / "TA不会这样" → 识别属于 Work 还是 Persona → Edit 对应文件 Corrections 节 → 重新生成 SKILL.md

### 更新
sync → 重新提取 → 增量合并

---

## 管理

### list
```bash
ls ${CLAUDE_SKILL_DIR}/colleagues/*/meta.json
```

### delete
确认后 `rm -rf colleagues/<slug>/` 和 `~/.claude/skills/colleague-<slug>/`

---

## 环境适配

| 平台 | 数据目录 | 密钥提取 | 解密/查看/蒸馏 |
|------|---------|---------|--------------|
| Windows | `Documents\xwechat_files\` | 本地 Python | 本地 Python |
| WSL | `/mnt/c/Users/.../xwechat_files/` | 调 `powershell.exe python` | 本地 Python |
| macOS | `~/Library/Containers/com.tencent.xinWeChat/` | 需 macOS 适配 | 本地 Python |
| Linux | N/A（无微信客户端） | N/A | 拿到 keys.json 后可解密 |

**关键原则**：密钥提取绑定平台，其余全部跨平台。
