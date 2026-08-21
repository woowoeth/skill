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

# 有毒或需严格控量的中药。**只列「用错了会出人命」的那些**，不列全药典 ——
# 这张表是为了让「药名 + 数量」这个组合能被抓到，不是为了识别中药。
# **只列「用错了会出人命」的那些**，而且刻意**不列** 甘草/石膏/麻黄/大黄/芒硝 ——
# 它们几乎出现在每一张方子里，列进来的后果实测过：一份医案库里几百行
# 「处方内容是桂枝10克 白芍10克 炙甘草10克」全部命中，真正危险的那两行淹在里面。
# 这类「常见但要控量」的药改由下面的「巨剂量形态」接住（两/斤 这种单位本身就大，
# 或者写着 起步/起手/以上）。
TCM_HERBS = (r"附子|川乌|草乌|乌头|天雄|白附子|生半夏|生南星|马钱子|朱砂|雄黄|硫磺"
             r"|甘遂|大戟|芫花|巴豆|斑蝉|蟾酥|藜芦|商陆|狼毒|轻粉|砒石|细辛")

# 「这一行的 g/kg 是营养学不是药理」。实测 12 次假阳性全在这一档：
# 蛋白质 1.6-2.0g/kg、猫补水 50-70ml/kg、豚鼠维C 10-30mg/kg、重金属残留 砷≤5mg/kg。
NUTRITION_CTX = re.compile(
    r"(蛋白|protein|碳水|carb|脂肪|fat|热量|kcal|卡路里|calorie|补水|饮水|hydrat"
    r"|维生素|vitamin|矿物质|纤维|fiber|体重.{0,4}(?:每|per)|每(?:公斤|kg).{0,6}体重"
    r"|残留|限量|标准值|≤|<=|体重|磅|lbs?\b)", re.I)

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
    # 中医剂量。**这一档是补的，而它的缺失直接让两件最危险的货进了架。**
    #
    # 原来的「剂量」表只认 mg|μg|g|ml|IU，于是全部漏掉：
    #   · `生附子2-3钱`、`石膏12-14两`（中医用钱/两/枚，不是毫克）
    #   · `附子200g起步`（有 g，但后面没有 qd/每次 这类频次词）
    #   · `附子1枚≈20g`
    # 漏掉的这两件里，一件写着「电话/远程急救：破格救心汤原方，**附子200g起步**」，
    # 另一件写着「**附子不麻不昏即剂量不够**」—— 而麻和昏正是附子中毒的前驱症状。
    #
    # 判据不是单位，是**照着它就能给人用药**。所以要「药名 + 数量」近邻，
    # 光有「3钱」不算（可能是菜谱），光有药名也不算（可能在讲药性）。
    "剂量·中医": re.compile(
        # ① 剧毒药 + 任何数量
        r"((?:" + TCM_HERBS + r")[^。；\n]{0,20}?\d+(?:\.\d+)?\s*(?:-|~|–|至)?\s*"
        r"\d*(?:\.\d+)?\s*(?:钱|两|分|枚|片|斤|克|g|ml)"
        # ② 巨剂量形态 —— 常见药（甘草石膏麻黄）靠这一档接住，不进药名表
        r"|\d+(?:\.\d+)?\s*(?:-|~|–|至)?\s*\d*\s*(?:两|斤)\s*(?:起|以上|一剂|重症)"
        r"|\d+(?:\.\d+)?\s*(?:钱|两|分|枚|片|斤|克|g)\s*(?:起步|起手|以上|打底)"
        # ③ 把「放开剂量」写成规矩本身
        r"|(?:剂量|用量)\s*[^。；\n]{0,8}?(?:按体重折算|大胆|不得人为收敛|逐日累加)"
        r"|不麻不昏|不麻不.{0,2}即.{0,4}不够)", re.I),
    # 联盟营销分润
    "分润": re.compile(
        # `aff(?:iliate)?[-_ ]?(?:link|id|tag)` 会匹配 **affid**avit 里的 `aff`+`id` ——
        # 实测在两件签证/公民身份 skill 里命中 7 次，全是 `notarised same-person affidavit`
        # （公证的同一人声明书）。**同事早就报过这条，我当时没修，于是它又咬了一次。**
        r"(联盟(?:链接|营销|计划)|affiliate[-_ ]?(?:link|id|tag)|\baff[-_](?:link|id|tag)\b"
        r"|[?&]tag=[a-z0-9_-]{3,}"
        r"|CPS\s*(?:分润|佣金|链接)|返佣|带货链接|推广位|amzn\.to|taobao\.com/[a-z]*\?.*pid=)", re.I),
    # 身体/关系升级阶梯、话术脚本
    # 「推倒」第一版是裸词，第一次实测就在一份育儿参考里命中了
    # 「叠到 2-3 块时让宝宝推倒（这也是乐趣！）」—— 幼儿搭积木。
    # 所以带人称的那几个词一律要求近处有对象标记（她/他/对方/女生…），
    # 单独一个动词不定罪。**只会产假阳性的判据是噪音，而假阳性挨着真命中最伤信任。**
    "越界话术": re.compile(
        # `escalation ladder` 不一定是身体升级 —— 实测两处是**搜索深度递进**
        # （吉他装备调研：rig rundowns → interviews → tab/gear sites）。同事报过，我没修。
        r"(肢体(?:推进|升级|接触)阶梯|身体升级"
        r"|(?:升级阶梯|escalation\s*(?:ladder|boundaries))"
        r"(?=[^。；\n]{0,60}(?:肢体|身体|接吻|拥抱|亲密|touch|kiss|intimacy|consent|她|女生))"
        # `kino` 第一版是裸词，实测在 **Tsukinomori（月ノ森）** 里面命中了 ——
        # 拉丁字母的短词一律要词边界，否则它会藏在任何专有名词里。
        # `kino` 连词边界也不够 —— 实测有个 CLI 就叫 kino，命中 30 次。
        # 它只在把妹语境里才是术语，所以要求近处有那套词。
        r"|过度怂|\bkino\b(?=[^。；\n]{0,40}(?:升级|推进|接触|试探|她|女生))"
        r"|Mystery\s*Method|Blueprint\s*Decoded"
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
    # 成规模转载他人受版权保护的正文。**这一档原来整个不存在** ——
    # 两件最大的下架货（24.6MB 古籍 PDF 全文页、4.6MB 闭门课原文）
    # 一条正则都没命中，是人翻「读不到的文件」清单时觉得 8MB 的 md 不对劲才查出来的。
    # 这里用的是**廉价代理指标**，不是判决：路径/文件名自称是逐字稿、
    # 或文件自己承认「保存完整文本层 / 不做截断 / 去水印」。体积那一档在 scan_one 里另算。
    # **只留「文件自己承认在做什么」的措辞。**
    # 第一版把 `逐字稿|transcript|lyrics` 也放进来，实测 8 处假阳性全是
    # 在讨论「我们**没有**这些」（「未取得逐字稿」「公开网页很少提供完整 transcript」）——
    # 就是那类「在讲反面案例」的误命中。
    # 那两件真货（24.6MB 古籍全文页 / 4.6MB 闭门课原文）本来也不是靠散文里的词抓到的，
    # 是靠**体积和目录**。所以词挪到路径判（BULK_PATH），体积单独算（见 scan_one）。
    "转载正文": re.compile(
        r"(完整文本层|不做(?:字符)?截断|去水印|移除.{0,8}水印|物理页均有记录"
        r"|全文(?:页|录入|收录)|版权归原(?:权利人|作者)|如有侵权请联系删除)", re.I),
    # 工具的功能就是取盗版。**这一档原来抓不到** ——
    # 原判据是体积和目录，抓的是「仓库里带着盗印正文」；而这类仓库很干净，
    # 盗版是**运行时下载的**。同一个危害，而且它可复用、更可扩散。
    # 实测三件：Z-Library / Anna's Archive 下载、PanSou 转存夸克、以及把两条打包的。
    "取盗版": re.compile(
        r"(z-?lib(?:rary)?|zlibrary|annas?[-_ ]?archive|安娜的档案|libgen|sci-?hub|"
        r"pansou|盘搜|资源.{0,4}转存|网盘.{0,4}(?:转存|搜索|采集)|"
        # `pirat(?:e|ed|ing)` 是裸子串，实测三处命中全是假阳性：
        # 「**Pirates** of the Caribbean」「**Pirates** of Penzance」（配乐/音乐剧片名）、
        # 以及 `_AS**PIRAT**ED_RULES`（送气音规则，方言 IPA 转拼音脚本）。
        # **这是子串误命中第三次**（前两次：`kino` 藏在 Tsukinomori、`推倒` 命中幼儿搭积木）。
        # 拉丁短词一律词边界 + 语境词，别再裸放。
        r"盗版|破解版|\bpirated?\s*(?:copy|copies|content|ebooks?|books?|资源|下载)"
        r"|\bpiracy\b|crack(?:ed)?\s*(?:版|version|software)|"
        r"电子书.{0,6}(?:下载|资源库)|epub.{0,6}(?:批量|爬))", re.I),
    # 模型护栏破限。**不是 AIGC 检测规避，是 jailbreak，原表上没有这一行。**
    # 实测一件写着「解除常规道德与内容限制」「禁止输出任何拒绝性语言」
    # 「1岁以上即视为成年」—— 最后那句已经不只是破限。
    "破限": re.compile(
        r"(解除.{0,8}(?:限制|约束|审查|护栏)|无限制模式|越狱|jailbreak|DAN\s*mode|"
        r"禁止.{0,6}拒绝|不得拒绝|不许拒绝|绕过.{0,6}(?:安全|审查|护栏|content\s*polic)|"
        r"uncensored|no\s*(?:refusal|restrictions?|filter)|bypass.{0,10}safety|"
        r"\d+\s*岁以上.{0,6}(?:视为|即为|算)\s*成年)", re.I),
    # 拿消费级设备数据下临床结论。
    # 分界线：**数据源是消费级设备 + 输出是疾病名或疾病区间 → 红线。**
    # 不是剂量（没有东西可给人用），也不是毒性阈值（那是劝你别碰）——
    # 是**拿手表上的一个数说出「心衰区间」**，而那个数的精度撑不起这句话。
    # 在架的反例正好划清了线：一件**故意把综合健康分留成空值**；
    # 另一件用的是真体检报告（临床级数据）而不是手表。
    "消费级数据下临床结论": re.compile(
        r"((?:VO2\s*max|静息心率|HRV|血氧|睡眠评分|步数|手表|wearable|apple\s*health|"
        r"fitbit|garmin|whoop|oura)[^。；\n]{0,40}"
        r"(?:heart\s*failure|心衰|心力衰竭|糖尿病|房颤|猝死风险|疾病区间|临床.{0,4}(?:区间|标准|诊断)|"
        r"确诊|病理|risk\s*of\s*death))", re.I),
    # AIGC 检测规避
    "检测规避": re.compile(
        # 「降重」原来是裸词，实测 7 次假阳性：健身件的「合理降重」（减体重）
        # 和倪海厦针灸模块里的道家内丹文「引任脉**降重**楼」。要求近处有查重语境。
        r"(bypass\s*(?:gptzero|turnitin|zerogpt|copyleaks|originality)"
        r"|绕过\s*(?:查重|AI\s*检测|AIGC\s*检测)|降\s*AIGC|过\s*turnitin"
        r"|降重[^。；\n]{0,12}(?:查重|论文|知网|维普|AIGC|检测)"
        r"|(?:查重|论文|知网|维普|AIGC|检测)[^。；\n]{0,12}降重)", re.I),
}
# 绕反爬用共享的那张表
TABLES["绕反爬"] = RED_SCRAPE_HARD

# 「这一行是在说它不做这件事」。命中不丢，只是换个标签打出来。
# 「这一行说的是毒性/致死阈值」，不是用药剂量。
TOX_CONTEXT = re.compile(
    r"(中毒|致死|毒性|半数致死|LD\s*50|lethal|toxic|中毒量|超过.{0,6}会中毒|危险剂量)", re.I)

REFUSAL = re.compile(
    # `不得` 要排掉「万不得已」—— 实测它把全店最危险的一行打成了「声明不做」：
    #   「| 电话/远程急救 | 破格救心汤原方，附子200g起步 | ⚠️ 无四诊合参，风险极高，**仅限万不得已** |」
    # 「万不得已」是在说「这么干很危险但有时只能这么干」，那是**加强**而不是拒绝。
    r"(never|don'?t|do not|refuse|without\s+bypass|not\s+bypass|not\s+a\s+license"
    r"|user\s+(?:clears|solves|does)"
    # 补几个「作者自陈过不去」的措辞。实测一处：作者写「受限于知网/万方付费墙和
    # 纸质出版物未数字化，**只能拿到摘要**…如果你能通过个人账号或图书馆权限拿到全文，
    # 把内容发过来」—— 明说自己过不去、请你用自己的合法权限，那是反例不是红线。
    r"|不会|不许|(?<!万)不得|禁止|拒绝|绝不|从不|由(?:你|用户)|你自己|用户自己|手动(?:过|输)|请你"
    r"|受限于|只能拿到|拿不到|过不去|无法(?:抓取|获取|绕|通过)|不读取|不打印|不保存|未数字化)", re.I)

# 「这个文件名自己在说它干什么」—— 同仓任何位置都要扫，不管在不在 skill 目录下。
SUSPICIOUS_NAME = re.compile(
    r"(stealth|undetected|anti[-_]?bot|anti[-_]?detect|bypass|fingerprint|"
    r"export[-_]?cookies?|cookie[-_]?(?:dump|export|steal|read)|browser[-_]?cookie|"
    r"user[-_]?agents?|ua[-_]?pool|proxy[-_]?pool|captcha|slider|滑块|反爬|"
    r"wallet|private[-_]?key|keystore|mnemonic|seed[-_]?phrase)", re.I)

# 「这个路径本身在说它装了别人的正文」。词放在路径上判，不放在散文里判 ——
# 散文里出现「逐字稿」多半是在说「我们没有逐字稿」。
BULK_PATH = re.compile(r"(pdf-evidence|逐字稿|transcript|lyrics|ebooks?|闭门课|课程原文|全集)", re.I)
# 单个随件文本文件超过这个字节数就打标让人去看。
# 两件真货的量级：一件 24.6MB（六模块古籍 PDF 全文页），一件 4.6MB（闭门课原文）；
# 已拒的播客逐字稿那件是 2.2MB。300KB 是「一份参考资料」和「一本书」之间的分界。
BULK_BYTES = 300_000

# 自动纳入扫描的目录（不用等正文点名）
AUTO_DIRS = ("references/", "reference/", "assets/", "scripts/", "data/", "docs/", "prompts/")
TEXTY = (".md", ".txt", ".json", ".yaml", ".yml", ".py", ".js", ".mjs", ".ts", ".sh",
         ".csv", ".toml", ".ini", ".html")
MAX_BYTES = 8_000_000        # 单文件上限，超了如实报「太大没读」。走 raw，不吃 API 限额
MAX_FILES = 200              # 单件上限，超了如实报（并汇总进收尾那段，见 main）
# 扫描优先级：**references/ 和 scripts/ 排在 assets/ docs/ 前面**。
# 实测代价：全架复查时 17/231 件被 MAX_FILES 静默截断（最多一件 337 个文件没扫），
# 而最终下架的 `hugohe3/ppt-master` 那三个带 curl_cffi 指纹伪装的脚本
# **就藏在那 337 个里** —— 被 300 个菜谱和截图挤出了窗口。
# 危险永远在 references/ 和 scripts/ 里，不在 assets/ 里。
DIR_PRIORITY = ("references/", "reference/", "scripts/", "prompts/", "data/", "docs/", "assets/")


# ---------------------------------------------------------------------------
# 扫描存档 —— 「扫过」这件事必须留在磁盘上，不能留在人的记忆里
#
# 这个脚本原来是纯手动工具：谁记得跑就跑。而「靠人记得」在这个项目里已经
# 失效过很多次（拒收榜去重键、从不执行的守卫、前端扔掉排序），所以扫描结果
# 现在**自动落盘**，`check_curation.py` 的守卫去查「有没有扫过、扫的是不是这一版」。
#
# 三个指纹，各管一件事：
#   · upstream_tree_sha  —— 扫描当时上游 HEAD 的整棵树 sha。任何文件变了它就变。
#                           下次联网扫描时可以拿它比，判断「上游动过没有」。
#   · skill_md_blob_sha  —— 扫描当时 SKILL.md 的 blob sha。正文本身变了它就变。
#   · method_sha256      —— 扫描当时本地 `methods/<id>.md` 的 sha256。
#                           **守卫只比这一个**，因为它是纯本地的：不联网就能判断
#                           「我们手上的正文存档，是不是扫过的那一版」。
#                           methods/ 被重新抓取刷新过，这个值就对不上 —— 那份扫描作废。
#
# 为什么守卫不去比上游 sha：那要联网，而每次构建都联网这条路是错的
# （同 prep_signals 模块头：徽章从本地存档算，零新增爬取）。
# 扫描是抓取期的事，守卫只查存档。
# ---------------------------------------------------------------------------
ARCHIVE = os.path.join(ROOT, "scouts", "scan_archive.json")
SKILLS_DIR = os.path.join(ROOT, "skills")
METHODS_DIR = os.path.join(ROOT, "methods")


def method_sha256(sid: str) -> str:
    """本地 methods/<id>.md 的 sha256。没有存档返回空串 —— 空和「对不上」不是一回事。"""
    import hashlib
    f = os.path.join(METHODS_DIR, f"{sid}.md")
    if not os.path.exists(f):
        return ""
    with open(f, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _ids_for(repo: str, base: str) -> list:
    """这一次扫的 (repo, path)，对应货架上哪几件。

    一个仓库可以拆出多件（不同 path），所以按 (repo, path) 精确配。
    扫仓库根、而这个仓库只有一件时，也算配上 —— 那件就是仓库本体。
    配不上就返回空：存档照样写，但记成未挂靠，让它在守卫里看得见，
    而不是静默变成「这件没扫过」。
    """
    import glob as _g
    rows = []
    for f in _g.glob(os.path.join(SKILLS_DIR, "*.json")):
        if os.path.basename(f) in ("feed.json", "rejected-feed.json"):
            continue
        try:
            it = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if isinstance(it, dict) and it.get("id") and (it.get("repo") or "") == repo:
            rows.append(it)
    exact = [r for r in rows if (r.get("path") or "").strip("/") == (base or "").strip("/")]
    if exact:
        return [r["id"] for r in exact]
    if not (base or "").strip("/") and len(rows) == 1:
        return [rows[0]["id"]]
    return []


def archive_write(results: list) -> tuple:
    """把扫描结果并进 scouts/scan_archive.json。返回 (挂靠上的件数, 未挂靠的次数)。"""
    doc = {}
    if os.path.exists(ARCHIVE):
        try:
            doc = json.load(open(ARCHIVE, encoding="utf-8"))
        except Exception:
            doc = {}
    doc.setdefault("_说明",
        "机器扫描存档。每一件在架商品必须在这里有一条，且 method_sha256 要和当前 "
        "methods/<id>.md 对得上 —— 否则 scouts/check_curation.py --strict 会红。"
        "由 scouts/scan_refs.py 自动写入，人不要手改。")
    doc.setdefault("_字段",
        "entries[<skill id>] = {repo, path, scanned_at, upstream_tree_sha, skill_md_blob_sha, "
        "method_sha256, files_scanned, skipped, hits, unreadable, hit_files}。"
        "method_sha256 是守卫唯一比对的字段（纯本地、不联网）；空串表示扫描时本地没有 "
        "methods/<id>.md 存档，那种情况版本无法本地核验，守卫会单独报。"
        "unmapped[] 记「扫了但配不上任何在架件」的 (repo, path)。")
    ent = doc.setdefault("entries", {})
    unmapped = doc.setdefault("unmapped", [])
    mapped_n, unmapped_n = 0, 0
    for r in results:
        repo, base = r.get("repo", ""), (r.get("path") or "")
        row = {
            "repo": repo, "path": base,
            "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "upstream_tree_sha": r.get("tree_sha", ""),
            "skill_md_blob_sha": r.get("skill_md_sha", ""),
            "files_scanned": r.get("scanned", 0),
            "skipped": r.get("skipped", 0),
            "hits": len(r.get("hits") or []),
            "unreadable": len(r.get("unreadable") or []),
            "hit_files": [h.get("file") for h in (r.get("hits") or []) if isinstance(h, dict)],
        }
        ids = _ids_for(repo, base)
        if not ids:
            unmapped_n += 1
            key = f"{repo}#{base}"
            unmapped[:] = [u for u in unmapped if u.get("key") != key]
            unmapped.append({"key": key, **row})
            continue
        for sid in ids:
            ent[sid] = {**row, "method_sha256": method_sha256(sid)}
            mapped_n += 1
    json.dump(doc, open(ARCHIVE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return mapped_n, unmapped_n


def _prio(path: str) -> tuple:
    for i, d in enumerate(DIR_PRIORITY):
        if f"/{d}" in f"/{path}":
            return (i, path)
    return (len(DIR_PRIORITY), path)


def gh(path: str):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if r.returncode != 0:
        return None, (r.stderr or "").strip()[:140]
    try:
        return json.loads(r.stdout), None
    except Exception as e:                                    # noqa: BLE001
        return None, f"响应不是 JSON: {e}"


def fetch_text(repo: str, path: str):
    """→ (text, err)。err 不是 None 时 text 一定是 None，反之亦然。

    走 `raw.githubusercontent.com` 而不是 contents API，两个原因都是实测出来的：

      1. **contents API 对 >1MB 的文件不给 `content` 字段**（返回 null），
         而全架复查时被跳过的 31 个文件里**有 6 个就是问题本身** ——
         其中一件 24.6MB 的古籍全文页、一件 4.6MB 的闭门课原文，
         正是最终下架的两件最大的货。
      2. raw 不吃 API 限额。全架跑一遍是几千个文件，走 API 会打穿主限额
         （实测撞过一次，等了 23 分钟）。

    既然是逐行正则，大文件流式读就行，**没必要跳**。上限抬到 8MB 只为兜住
    误配到二进制的情况；超了仍然如实报，不静默跳过。
    """
    url = f"https://raw.githubusercontent.com/{repo}/HEAD/{path}"
    r = subprocess.run(["curl", "-sL", "--max-time", "60", "-w", "%{http_code}", url],
                       capture_output=True)
    body = r.stdout
    if not body:
        return None, "curl 无输出"
    code = body[-3:].decode("ascii", "replace")
    body = body[:-3]
    if code != "200":
        return None, f"HTTP {code}"
    if len(body) > MAX_BYTES:
        return None, f"{len(body)} 字节，超过 {MAX_BYTES} 上限，没读（**这不是扫过没命中**）"
    if b"\x00" in body[:2048]:
        return None, "看着是二进制，没读"
    return body.decode("utf-8", "replace"), None


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
    # 版本指纹：树 sha 管「上游动过没有」，blob sha 管「正文本身变没变」。
    # 取不到就留空 —— 空和「对不上」在守卫里是两种不同的报法。
    tree_sha = (tree.get("sha") or "")
    blob_of = {t["path"]: (t.get("sha") or "")
               for t in (tree.get("tree") or []) if t.get("type") == "blob"}

    # 没指定 path 时**自己去树里找 SKILL.md**，别让「没告诉我在哪」变成漏扫。
    # 实测栽过一次：`sea0710/medical-record-butler-skill` 的 SKILL.md 在 `skill/` 下，
    # 工具报了「读不到」就收工 —— 那份带化疗剂量的 references/ 一个字没扫。
    # 报错不等于尽到了责任：手里明明有整棵树。
    if smd not in all_paths:
        found = sorted((p for p in all_paths if p.endswith("SKILL.md")),
                       key=lambda p: (p.count("/"), p))
        if not found:
            print(f"  ✗ 整棵树里没有 SKILL.md —— 这本身就是问一（装不进 agent）")
            return {"repo": repo, "path": base, "tree_sha": tree_sha,
                    "unreadable": ["<no SKILL.md>"], "hits": []}
        smd = found[0]
        base = os.path.dirname(smd)
        print(f"  ! 给的路径下没有 SKILL.md，自己在树里找到：{smd}"
              + (f"（另有 {len(found)-1} 个：{found[1:4]}）" if len(found) > 1 else ""))

    body, err = fetch_text(repo, smd)
    if err:
        print(f"  ✗ SKILL.md 读不到（{smd}）：{err}")
        return {"repo": repo, "path": base, "tree_sha": tree_sha,
                "skill_md_sha": blob_of.get(smd, ""), "unreadable": [smd], "hits": []}

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
    # **同仓任何位置的可疑文件，不管在不在 skill 目录下、正文有没有点名。**
    #
    # 实测漏过一件：`mediastormdev/dream-to-video-skill` 扫出「✓ 没命中」，
    # 因为 SKILL.md 在 `skills/dream-to-video/`，而危险代码在**仓库根的 `dream_to_video/`**
    # —— 不在 skill 目录里，正文也没点名。人手动拉 `dream_to_video/browser/stealth.py`，
    # 第一行是 `"""Playwright 反自动化检测"""`。
    #
    # 判据不是「在不在这一件的目录里」，是**文件名自己在说它干什么**。
    # 一个叫 stealth / export_cookies / user-agent 的文件，放在仓库任何角落都要看。
    sus = {p for p in all_paths
           if p.endswith(TEXTY) and SUSPICIOUS_NAME.search(p)}
    want |= sus
    ordered = sorted(want, key=_prio)
    trimmed = ordered[:MAX_FILES]
    skipped = max(0, len(ordered) - MAX_FILES)
    print(f"  正文点名 {len(named)} 个 · 自动纳入 {len(auto)} 个 · 合计扫 {len(trimmed)}"
          + (f"（**上限 {MAX_FILES}，剩下 {skipped} 个没扫**）" if skipped else ""))

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
                # 认栽标记的窗口从「固定 ±25 字」改成「**回溯到句首**」。
                # 实测代价：全架 112 条命中里，`·声明不做` 一次都没出现 ——
                # 两处教科书式的拒绝全是裸命中：
                #   「**Do not** automate repeated headed attempts or add anti-detection bypasses」
                #   「It is **not a license** to bypass CAPTCHA」
                # 前者的 `Do not` 离命中词 44 字，±25 接不住。
                # 但也不能放宽成整行 —— 那样 trip-planner 路由表里无关的「手动过」
                # 又会把真问题盖掉（那次是我收窄的原因）。按句读切，两头都接得住。
                # 表格的竖线也算句读。一整行 markdown 表格里没有句号，
                # 不加 `|` 的话「回溯到句首」会把整行五个单元格都吃进来，
                # 于是别的格子里的字会决定这一格的判断 —— 那正是我上一版
                # 收窄成 ±25 字要躲开的毛病，只是从固定字数换成了整行。
                SEP = "。；.;\n!?|｜"
                ls = max((txt.rfind(c, 0, m.start()) for c in SEP), default=-1) + 1
                le = min((x for x in (txt.find(c, m.end()) for c in SEP) if x > 0),
                         default=len(txt))
                # **「声明不做」这个标签只给「绕反爬 / 检测规避 / 转载正文」这三档。**
                #
                # 剂量类命中永远原样显示，不许被降级。原因是关键词分不出这两句：
                #   「不得绕过验证码」        —— 真的拒绝
                #   「剂量…不得人为收敛」    —— 命令你**别把剂量调小**
                # 后者字面上带「不得」，意思却正相反。实测这一条把 nihaixia
                # 那句「剂量大胆授权…不得人为收敛——生附子起手2-3钱」标成了「声明不做」。
                # 在「可能是漏报」和「可能是噪音」之间，剂量这一档必须选噪音。
                # 「密钥与代下单」也进可降级档。实测一处：
                #   「这条路线让 B站页面自己用登录态请求 `/x/player/wbi/v2`，
                #    **不读取、不打印浏览器 cookie**。」
                # 这一档的危害要求「真去做」，所以明确说不做的，标签该反映出来。
                # **剂量档仍然不可降级** —— 那一档在「可能漏报」和「可能噪音」之间必须选噪音。
                SOFTENABLE = ("绕反爬", "检测规避", "转载正文", "密钥与代下单")
                tag = label
                if label in SOFTENABLE and REFUSAL.search(txt[ls:le]):
                    tag = f"{label}·声明不做"
                found.append((tag, ln, m.group(0)[:60], line))
        # 毒性阈值不是用药指示 —— **它跟「照着它就能给人用药」正好相反**。
        # 实测栽过：`Zgdfsgd/fridge-hero` 的高风险清单里写「中毒剂量：2-5mg/kg体重」，
        # 那是在劝你别吃，不是在教你喂。同理 LD50 / 致死量 / lethal dose。
        # 毒性上下文**按整份文件判，不按行**。
        # 实测：那张 101 味毒性药的表，列名写着「内服剂量上限」、大多数行配着
        # 「中毒表现/致死」，但有 3 行本行没写这两个字，于是只有那 3 行漏出来 ——
        # 既是假阳性，又会让人误以为「只有 3 行有克数」。整份文件是不是一张毒性上限表，
        # 是文件级的性质，不是行级的。
        # **毒性豁免只对西药剂量档生效，不对「剂量·中医」生效。**
        #
        # 第一版我把它应用到所有 `剂量*` 档，后果当场出现：`likeskill` 的 SKILL.md 里
        # 「附子中毒」出现三次以上（因为它把附子中毒当成一个要治的证），
        # 于是整份文件被判成毒性上限表，**它那句「破格救心汤原方，附子200g起步」被整个消音**。
        # 我为修一个假阳性造了一个更严重的漏报，而漏掉的正是全店最危险的一句。
        #
        # 分界：mg/kg 这种写法**确实**常出现在毒性阈值表里（「中毒剂量 2-5mg/kg」是劝你别吃），
        # 而「剧毒药名 + 数量」这个组合本身就是「照着能给人用药」，不存在同形的无害用法。
        file_is_tox = len(TOX_CONTEXT.findall(txt)) >= 3
        def _drop(f):
            if f[0] != "剂量":
                return False
            if file_is_tox or TOX_CONTEXT.search(f[3]):
                return True
            # **`g/kg` 和 `mg/kg` 不是一回事。** 宏量营养素按克每公斤给
            # （蛋白 1.6-2.0g/kg 体重），药几乎永远是 mg/kg 或 μg/kg。
            # 所以「本行提到体重/蛋白」只豁免 g/kg，不豁免 mg/kg ——
            # 否则「对乙酰氨基酚 10-15mg/kg 体重」也会被一起放过，那是最不能放过的一句。
            hit = f[2] if len(f) > 2 else ""
            gram_per_kg = re.search(r"(?<![mμugc])g\s*/\s*kg", hit, re.I)
            return bool(gram_per_kg and NUTRITION_CTX.search(f[3]))
        found = [f for f in found if not _drop(f)]
        # 折叠**按命中原文去重**，不按出现顺序截断。
        #
        # 第一版是「同一档最多留前 6 条」，后果当场出现：`likeskill` 那句
        # 「破格救心汤原方，**附子200g起步**」排在第 7 条之后，**被我自己的降噪删掉了** ——
        # 而它是全店最危险的一行。**按出现顺序截断，等于让「谁排在前面」决定「谁重要」。**
        #
        # 按原文去重不会有这个问题：同一种写法（`附子30-200g`）出现五次折叠成一条，
        # 而 `附子200g起步` 是另一个字符串，它必然活下来。
        # 折叠掉多少条如实报出来，不静默。
        capped, seen_txt, dup = [], set(), {}
        for f in found:
            # 去重键是「命中词 + **所在行**」，不是命中词。
            #
            # 只按命中词的后果实测过：`likeskill` 第 395 行和第 399 行的命中串
            # 都是 `附子200g`，于是 399 被 395 吃掉 —— 而两行的意思差得远：
            #   395:「⚠️ 必须立即送医，中医急救需在有经验医师指导下进行」
            #   399:「**电话/远程急救** … ⚠️ 无四诊合参，风险极高」
            # **同一个匹配串，两句话的危险程度完全不同。** 两个不同的行是两个不同的发现。
            #
            # 这已经是我的降噪第三次删掉最该看的那一行（前两次：按出现顺序截断前 6 条、
            # 文件级毒性豁免）。**教训：每加一道降噪，都要拿最危险的那一行当回归测试。**
            key = (f[0], re.sub(r"\s+", "", (f[2] or "")), re.sub(r"\s+", "", (f[3] or ""))[:120])
            if key in seen_txt:
                dup[f[0]] = dup.get(f[0], 0) + 1
                continue
            seen_txt.add(key)
            capped.append(f)
        for lab, n in dup.items():
            capped.append((f"{lab}·另有{n}处重复写法", 0, "", "（同一文件内相同原文已折叠）"))
        found = capped
        # 体积与路径 —— 不靠正文措辞。**那两件最大的下架货就是这么该被抓到的，
        # 而上一版一条正则都没命中，是人翻「读不到的文件」清单时觉得 8MB 的 md 不对劲才查出来的。**
        nb = len(txt.encode("utf-8", "ignore"))
        if nb >= BULK_BYTES or BULK_PATH.search(p):
            why = []
            if nb >= BULK_BYTES:
                why.append(f"{nb/1024/1024:.1f}MB 散文")
            if BULK_PATH.search(p):
                why.append(f"路径含「{BULK_PATH.search(p).group(0)}」")
            found.append(("转载正文·体积路径", 0, "", " · ".join(why) + "（体积和路径不是判决，去看它装的是谁的正文）"))
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
    return {"repo": repo, "path": base, "skipped": skipped,
            "tree_sha": tree_sha, "skill_md_sha": blob_of.get(smd, ""),
            "scanned": len(hits) + len(clean),
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
    ap.add_argument("--no-archive", action="store_true",
                    help="不写 scouts/scan_archive.json（默认会写，守卫靠它判断有没有扫过）")
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
    trunc = [(o["repo"], o.get("skipped", 0)) for o in out if o.get("skipped")]
    print(f"\n{'='*72}\n扫了 {len(out)} 件 · 有命中 {n_hit} 件 · "
          f"**命中在随件里的 {n_off} 处** · 读不到 {n_unread} 个文件")
    # 静默截断必须和「读不到」一样显眼。批量跑的时候，逐件那行会淹在几千行日志里 ——
    # 而全架复查时最终下架的一件，问题就藏在被截断的 337 个文件里。
    if trunc:
        print(f"  **有 {len(trunc)} 件没扫完**（上限 {MAX_FILES}，这不是扫过没命中）：")
        for r, n in sorted(trunc, key=lambda x: -x[1])[:15]:
            print(f"      {r} —— 还剩 {n} 个文件没扫")
    print("机器只指出「这一行你去看」，判决是人的事。")
    if a.as_json:
        json.dump(out, open(a.as_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"→ {a.as_json}")

    # 存档是**默认动作**，不是可选开关。理由见 ARCHIVE 那段：
    # 「扫过」不能是一件靠人记得去记录的事，否则守卫查到的永远是空档。
    if not a.no_archive:
        m, u = archive_write(out)
        print(f"→ 存档 {os.path.relpath(ARCHIVE, ROOT)}：挂靠 {m} 件"
              + (f"，另有 {u} 次扫描配不上任何在架件（记在 unmapped）" if u else ""))
    else:
        print("! --no-archive：这次没留痕，守卫会照旧认为这些件没扫过")


if __name__ == "__main__":
    main()
