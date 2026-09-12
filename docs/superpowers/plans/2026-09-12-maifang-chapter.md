# 买房篇（第八章）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 新增独立的第八章「买房篇」，6 个专题页，覆盖从「该不该买」到「拿钥匙」的完整链路，并把全部税率与额度按核实过的数字与生效时点写进去。

**Architecture:** 纯内容 + frontmatter 改动的 Jekyll 站点。新增一个 `chapter-hub` 章目录页与 6 个 `layout: section` 专题页，weight 810–816 落在安全篇（800）与结语（850）之间的空档里。**现有页面的 `weight`、`num`、`permalink` 一律不动**，所以正文里几十处 5.x / 6.x / 7.x 交叉引用一处都不用改——这是本章与旅游篇那次改动最大的不同，不要照抄那次的「顺延」思路。

**Tech Stack:** Jekyll 4（`bundle exec jekyll build`）、kramdown（`auto_ids: false`，标题锚点手写 `<h2 id="...">`）、纯 SCSS，无 JS 框架。没有单元测试；本计划的「测试」是 `jekyll build`、CI 的 frontmatter 校验脚本，以及 grep 断言。

**Spec:** `docs/superpowers/specs/2026-09-12-maifang-chapter-design.md`

## Global Constraints

- **YAML 陷阱（最重要）：** frontmatter 的双引号标量里**不能出现 ASCII 双引号**。YAML 出错时 Jekyll 会**静默丢掉整块 frontmatter**（`faq`、`toc` 一起消失），页面照常构建、看不出问题。要引号就写中文引号「」，或整段换单引号包裹。每个任务的断言里都要 grep 一次渲染结果，确认 FAQ 真的出现了。
- **每页必须有** `title`、`description`、`nav`（CI 会校验），外加 `updated`（显示与 `dateModified` 用）。本次所有新页与被改页的 `updated` 一律写 `2026-09-12`。
- **`weight` 约定：** 章 = 序号 × 100，专题 = 章 weight + 小节号。本章例外：章 weight 用 **810**（不是 800，那是安全篇），专题 **811–816**。
- **数字只能抄「已核实的事实速查」这一节。** 不要凭记忆写税率，不要去搜二手中文攻略——本章最常见的错误来源就是把 2022–2025 年的临时印花税门槛当成现行标准。速查表里没有的具体金额，一律写量级 + 「以实际报价为准」。
- **每张税率表必须带独立的生效时点标注**，与 frontmatter 的 `updated` 分开。改错别字时不要顺手刷新这些日期。
- **不新增联盟链接**（CI 会校验 `rel="sponsored nofollow"`，本次应保持零变化）。不要在本章推荐具体的按揭 broker、conveyancer 或银行产品。
- **不写投资建议。** 不预测房价、不比较「买房 vs 投资股市」的收益率、不给按揭利率的具体数字。本章只讲流程、成本与规则。
- **中途不要 `git push`。** 推送即部署（`.github/workflows/pages.yml` 监听 main）。Task 1 之后到 Task 7 之前，章目录页会指向尚未写完的专题页；全部任务做完、Task 10 验证通过后再一次推送。
- **风格：** 跟随现有页面——中文正文、`.callout .callout-info/-tip/-warning/-success` 提示块、`<h2 id="sec-N">` 手写锚点、frontmatter 里 `toc:` 与 `faq:` 列表驱动目录和常见问题。不要引入新的 CSS 类。
- **章节交叉引用写现有编号**：租房是 1.1、税务是 5.2、学生优惠是 5.3、回国发展是 5.5、突发情况是 7.2。链接一律用 `{{ '/path/' | relative_url }}` 形式。

## 全局验证命令

每个任务末尾都要跑。下面记作 **`VERIFY`**：

```bash
cd /home/yfrl/projects/uk-handbook

# 1. 构建通过
bundle exec jekyll build --trace 2>&1 | tail -3

# 2. frontmatter 能解析且字段齐全（与 CI 同一段脚本）
ruby -ryaml -rdate -e '
  bad = []; missing = []
  Dir.glob("_chapters/**/*.md").push("index.md").each do |f|
    text = File.read(f)
    next unless text.start_with?("---")
    fm = text.split("---", 3)[1]
    begin
      data = YAML.safe_load(fm, permitted_classes: [Date, Time])
    rescue => e
      bad << "#{f}: #{e.message.lines.first.strip}"; next
    end
    %w[title description nav].each { |k| missing << "#{f}: 缺 #{k}" unless data && data[k] }
  end
  abort("front matter 解析失败:\n" + bad.join("\n")) unless bad.empty?
  abort("front matter 字段缺失:\n" + missing.join("\n")) unless missing.empty?
  puts "front matter OK"
'

# 3. 页数不少于 40
test "$(find _site -name index.html | wc -l)" -ge 40 && echo "page count OK"
```

**基线：** 改动前 `bundle exec jekyll build` 通过，`find _site -name index.html | wc -l` = **67**。做完全部任务后应为 **74**（新增 1 个 hub + 6 个专题，不删除任何页面）。

---

## File Structure

| 文件 | 职责 |
| --- | --- |
| `_chapters/maifang.md` | 第八章章目录页（`chapter-hub`）。章首语 + 自动列出 6 个专题。`key: maifang`、`/maifang/`、weight 810、num `"08"` |
| `_chapters/maifang/mai-vs-zu.md` | 8.1 买还是继续租。谁能买、买房不带来身份、真实总成本、回本测算、什么情况下不该买 |
| `_chapters/maifang/daikuan.md` | 8.2 预算与贷款。LTV 与首付、Freedom to Buy、收入倍数、签证持有人贷款、信用记录、Lifetime ISA、AIP、broker |
| `_chapters/maifang/kanfang-chujia.md` | 8.3 找房、看房与出价。挂牌平台、freehold vs leasehold、自查信息、看房清单、出价与 chain、gazumping |
| `_chapters/maifang/shuifei.md` | 8.4 税费总账。SDLT / LTT 表、海外买家与第二套房附加、其余一次性成本、总账表 |
| `_chapters/maifang/liucheng.md` | 8.5 从 offer 到交房。conveyancing 时间轴、三级测量、交换合同的法律分界、持有成本 |
| `_chapters/maifang/sugelan.md` | 8.6 苏格兰买房的不同之处。Home Report、offers over、missives、LBTT 与 ADS |
| `_chapters/fulu.md` | **修改**：关键数字表加一组「买房」 |
| `_chapters/shenghuo/zufang.md` | **修改**：页尾加一条指向第八章的出口链接 |
| `_chapters/jinjie/shuiwu.md` | **修改**：若正文提到房产相关税务则加交叉链接 |
| `index.md` | **修改**：「从这里开始」加第八章条目 |
| `README.md` | **修改**：目录表加行、章节概述表述、年度复核表加四行 |
| `_chapters/jieyu.md` 等 6 个 | **修改**：仅 `order:` 字段顺延（无渲染作用） |

---

## 已核实的事实速查（2026-09-12）

**写页面时直接抄这里，不要凭记忆改，也不要再去搜二手中文攻略。** 每组后面是来源。

### SDLT（英格兰与北爱尔兰）—— 现行分档自 **2025 年 4 月 1 日**起

| 房价区间 | 税率 |
| --- | --- |
| 至 £125,000 | 0% |
| £125,001–£250,000 | 2% |
| £250,001–£925,000 | 5% |
| £925,001–£1,500,000 | 10% |
| £1,500,000 以上 | 12% |

- **首次购房减免：** 0% 至 **£300,000**；5% 于 £300,001–£500,000；**房价超过 £500,000 则完全不适用**（不是超出部分不减免，是整笔按标准分档算——这是本章最值得单独强调的一条）。
- **追加房产附加：** 在上述税率之上 **+5%**（买下之后名下不止一套住宅即适用，海外已有房产也算）。
- **非英国居民附加：** **+2%**，判定标准是购房前 12 个月内在英停留**不足 183 天**。与追加房产附加**可叠加**。
- **2025 年秋季预算没有改动 SDLT。** 网上大量「印花税即将改革」的文章是预测，不是已生效的政策，不要写进正文。
- 来源：<https://www.gov.uk/stamp-duty-land-tax/residential-property-rates>

### LBTT（苏格兰）—— 分档自 **2021 年 4 月 1 日**起

| 房价区间 | 税率 |
| --- | --- |
| 至 £145,000 | 0% |
| £145,001–£250,000 | 2% |
| £250,001–£325,000 | 5% |
| £325,001–£750,000 | 10% |
| £750,000 以上 | 12% |

- **首次购房减免：** nil band 提高到 **£175,000**，最多省 **£600**。
- **ADS（Additional Dwelling Supplement）：** **8%**，自 **2024 年 12 月 5 日**起，**按全额房价计算**（不是分档），对价 £40,000 及以上适用。
- 对价 £40,000 及以上即使不产生税款也要申报。
- 来源：<https://revenue.scot/taxes/land-buildings-transaction-tax/residential-property> 与同站 ADS 页

### LTT（威尔士）

主表自 **2022 年 10 月 10 日**起：0% 至 £225,000；6% £225,001–£400,000；7.5% £400,001–£750,000；10% £750,001–£1,500,000；12% £1,500,000 以上。

高档（追加房产）表自 **2024 年 12 月 11 日**起：5% 至 £180,000；8.5% £180,001–£250,000；10% £250,001–£400,000；12.5% £400,001–£750,000；15% £750,001–£1,500,000；17% £1,500,000 以上。

- **威尔士没有首次购房减免。** 这条与英格兰、苏格兰都不同，是中文攻略照搬英格兰写法最常出错的地方，必须写明。
- 来源：<https://www.gov.wales/land-transaction-tax-rates-and-bands>

### Lifetime ISA

- 每年最多存入 **£4,000**；政府奖励 **25%**、每年封顶 **£1,000**。
- **18–39 岁**开户、**40 岁前**完成首次存入、可存到 **50 岁**。
- 首套房价格上限 **£450,000**；需在**首次存入满 12 个月**后购房。
- 不合规提取扣 **25%**（注意：25% 的罚扣高于 25% 的奖励，本金会亏损，这点要写清楚）。
- 来源：<https://www.gov.uk/lifetime-isa>

### HM Land Registry 登记费

Land Registration Fee Order 2024，**2024 年 12 月 9 日**生效。Scale 1「有偿整体转让」，电子申请较纸质减 **55%**：

| 房价 | 电子申请 | 纸质申请 |
| --- | --- | --- |
| £0–80,000 | £20 | £45 |
| £80,001–100,000 | £40 | £95 |
| £100,001–200,000 | £100 | £230 |
| £200,001–500,000 | £150 | £330 |
| £500,001–1,000,000 | £295 | £655 |
| £1,000,000 以上 | £500 | £1,105 |

来源：<https://www.gov.uk/guidance/hm-land-registry-registration-services-fees>

### 按揭担保计划（Freedom to Buy）

- **2025 年 7 月起转为常设**（此前是临时计划）。
- 支持 **91–95% LTV**，即首付 **5%** 起；房价上限 **£600,000**。
- **不限于首次购房者。** 主要贷款方都有参与。
- 机制是政府为贷款方兜底部分损失，**不是给买家的补贴**——这点要写清楚，读者常误以为能拿到钱。

### 收入倍数与贷款监管

- FPC 的「单家贷款方 4.5 倍以上放贷不超过 15%」流量限制已于 **2025 年**放宽，监管仍在就取消单家机构限额征询意见。
- **4.5 倍是市场基准，不是法定上限**；放宽后部分贷款方对个案给到 5–6 倍。
- 正文写法：写判断维度与「以贷款方当下政策为准」，**不要写死倍数，也不要点名银行**。

### High Value Council Tax Surcharge（仅英格兰）

- 2025 年秋季预算宣布，自 **2028 年 4 月**起对 **£2,000,000 及以上**住宅按档加收：£2m–2.5m 每年 £2,500；£2.5m–3.5m £3,500；£3.5m–5m £5,000；£5m 以上 £7,500。
- 向**业主**而非居住者征收，与现行 council tax 并行，由地方政府按同一账期收取。
- **目前处于征询阶段**，写作时标注「以最终立法为准」。与绝大多数读者无关，**只写一句**，用途是让读者被中介拿这条吓唬时知道门槛在哪。

### 出租房相关（本章只带一句，不展开）

- 房产收入所得税三档自 **2027 年 4 月**起各加 2 个百分点，变为 **22% / 42% / 47%**。
- 用途仅限于在 8.4 说明「买来出租是另一套税务体系，本手册不展开」。

### 核不到就不编

以下没有权威统一价，**只写量级并注明「以实际报价为准」，不写具体金额**：
律师费与 searches、三级测量费、按揭手续费与估值费、broker 费、搬家费、
各贷款方对签证持有人的具体政策、按揭利率。

### 两条需要在写作时现场核实的事实

- **Help to Buy 股权贷款已停止新申请**（2023 年 3 月结束）。写进 8.2 前用 gov.uk 核一次当前状态与是否有继任计划。
- **购房不带来任何英国移民身份**，Tier 1 (Investor) 签证已于 **2022 年 2 月**关闭。写进 8.1 前用 gov.uk 核一次。

---

## Task 1: 新建第八章章目录页，并整理 `order` 字段

**Files:**
- Create: `_chapters/maifang.md`
- Modify: `_chapters/jieyu.md`、`_chapters/fulu.md`、`_chapters/youhui.md`、`_chapters/yingyu.md`、`_chapters/about.md`、`_chapters/privacy.md`（各只改 `order:` 一行）

**Interfaces:**
- Produces: `key: maifang`、`/maifang/`、weight 810。Task 2–7 的专题页都写 `parent: maifang`，由 `_layouts/chapter-hub.html` 自动列出，**章目录页不需要手写专题链接列表**（但章首语里可以手写引导链接，照 `_chapters/lvxing.md` 的写法）。

- [ ] **Step 1: 写断言**

```bash
cd /home/yfrl/projects/uk-handbook
test -f _site/maifang/index.html && echo "hub built"
```

- [ ] **Step 2: 跑断言，确认还不存在**

预期：`test` 失败、无输出。

- [ ] **Step 3: 建 `_chapters/maifang.md`**

```yaml
---
layout: chapter-hub
title: "在英国买房：流程、贷款资格与全部税费"
description: "在英国买房的完整指南：什么身份能买、非永居能不能贷款、首付与收入倍数怎么算、印花税与海外买家附加税各是多少、从接受 offer 到交换合同的全流程，以及苏格兰完全不同的一套规则。"
nav: "第八章 买房篇"
key: maifang
permalink: /maifang/
order: 9
weight: 810
updated: 2026-09-12
num: "08"
---
```

- [ ] **Step 4: 写章首语**

照 `_chapters/lvxing.md` 的结构写三到四段，覆盖：

1. **开篇纠正两个误解**（这是全章最重要的两句）：买房本身**不限制国籍与签证身份**，受限的是贷款，不是产权；**买房不会带来任何英国移民身份**。
2. **这一章适合谁读**：打算毕业留英工作、考虑结束长期租房的人；帮孩子买房的家长；已定居准备换房的家庭。不适合谁：两三年内可能离开英国的人——原因在 8.1 讲。
3. **一个 `.callout .callout-warning` 时效性提示块**：本章所有税率与额度都标了生效时点，其中印花税分档自 2025 年 4 月 1 日起已回调（此前 2022–2025 年的临时门槛已失效），网上多数中文攻略仍在用旧数字；决策前务必以 gov.uk 为准。
4. **一段导航**：不确定该不该买从 8.1 开始；只想知道能不能贷款看 8.2；已经在看房看 8.3；想算清一共要花多少钱看 8.4；已经接受 offer 看 8.5；买在苏格兰**先看 8.6**。链接用 `{{ '/maifang/mai-vs-zu/' | relative_url }}` 形式。

- [ ] **Step 5: 改 6 个文件的 `order:`**

逐个文件改，**只改 `order:` 这一行，不要动 `weight`**：

| 文件 | `order:` 现在 | 改为 |
| --- | --- | --- |
| `_chapters/jieyu.md` | 9 | 10 |
| `_chapters/fulu.md` | 9 | 11 |
| `_chapters/youhui.md` | 10 | 12 |
| `_chapters/yingyu.md` | 11 | 13 |
| `_chapters/about.md` | 11 | 14 |
| `_chapters/privacy.md` | 12 | 15 |

改完确认没有文件的 `weight` 被动到：

```bash
cd /home/yfrl/projects/uk-handbook
git diff -U0 -- _chapters/jieyu.md _chapters/fulu.md _chapters/youhui.md \
  _chapters/yingyu.md _chapters/about.md _chapters/privacy.md | grep '^[-+]' | grep -v '^[-+][-+]'
```

预期：只看到 `order:` 的增删行，**不应出现任何 `weight:` 行**。

- [ ] **Step 6: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/projects/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
test -f _site/maifang/index.html && echo "hub built"
# 侧边栏里第八章应排在安全篇与结语之间
grep -o '/anquan/\|/maifang/\|/jieyu/' _site/index.html | uniq
# 页数应为 68
find _site -name index.html | wc -l
```

预期：`grep` 输出的顺序是 `/anquan/` → `/maifang/` → `/jieyu/`；页数 68。再跑完整 `VERIFY`。

- [ ] **Step 7: 提交**

```bash
cd /home/yfrl/projects/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add the home-buying chapter hub

Weight 810 drops the new chapter into the gap between the safety chapter
(800) and the closing note (850), so no existing weight, num, or section
cross-reference changes. Also clears up two duplicate order values that
predate this chapter; order has no rendering effect, only weight sorts.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: 8.1 买还是继续租

全章入口页，也是唯一一页允许谈「要不要买」这个决策本身的。

**Files:**
- Create: `_chapters/maifang/mai-vs-zu.md`

**Interfaces:**
- Consumes: Task 1 建的 `key: maifang`。
- Produces: `/maifang/mai-vs-zu/`，供章目录页与 1.1 租房页反向链接。

- [ ] **Step 1: 现场核实两条事实**

在写正文前，用 gov.uk 核实并记下结论：

1. Tier 1 (Investor) 签证的关闭状态与日期（预期：2022 年 2 月 17 日关闭新申请）。
2. 是否存在任何「买房可获居留」的英国签证路径（预期：没有）。

核不到就写保守表述，**不要写成绝对承诺之外的任何形式**——这条只能是「买房不带来身份」，不能写成「买房有助于签证」。

- [ ] **Step 2: 写断言并确认还不存在**

```bash
cd /home/yfrl/projects/uk-handbook
test -f _site/maifang/mai-vs-zu/index.html && echo "8.1 built"
```

- [ ] **Step 3: 写 frontmatter**

```yaml
---
layout: section
title: "在英国该买房还是继续租：谁能买、要花多少、几年回本"
description: "在英国买房前先算清楚的几笔账：什么签证身份能买房（买房不限身份，受限的是贷款）、买房不会带来任何英国移民身份、首付之外还要准备多少一次性成本、简单的回本测算方法，以及哪些情况下继续租房才是对的。"
nav: "8.1 买还是继续租"
parent: maifang
weight: 811
updated: 2026-09-12
num: "8.1"
toc:
  - title: "什么身份能买：买房与签证的关系"
    anchor: "sec-1"
  - title: "买房不会带来英国身份"
    anchor: "sec-2"
  - title: "首付之外还要准备多少钱"
    anchor: "sec-3"
  - title: "几年才回本：一个能自己套的算法"
    anchor: "sec-4"
  - title: "这几种情况建议继续租"
    anchor: "sec-5"
  - title: "常见问题"
    anchor: "faq"
---
```

- [ ] **Step 4: 写正文五节**

**sec-1 什么身份能买** —— 英国对**购房者的国籍与签证身份没有限制**，学生签、工签、旅游签、甚至不在英国居住的人都可以持有英国房产；真正卡人的是**贷款**（见 8.2）与**税**（非居民要多交 2%，见 8.4）。用 `.callout .callout-info` 把这句单独提出来，因为中文社区普遍反过来理解。

**sec-2 买房不会带来英国身份** —— 写实：没有任何英国签证路径以购房为条件，Tier 1 (Investor) 已于 2022 年关闭。用 `.callout .callout-warning`。点明这是中介话术的高发点：「买房送身份」「买房方便续签」都不成立。买房与签证唯一的真实关联方向是相反的——**签证剩余时长会影响你能不能贷到款**。

**sec-3 首付之外还要准备多少钱** —— 列出一次性成本清单并指向 8.4 的总账表：印花税（**完全拿不回来的沉没成本**，这个定性要写死）、律师费与 searches、测量费、按揭手续费与估值费、土地登记费、搬家费。金额一律写量级 + 「以实际报价为准」，**只有印花税与土地登记费可以给具体数字，且要链到 8.4**。

**sec-4 几年才回本** —— 给一个读者能自己套的算法，不给任何房价假设：
「一次性成本合计 ÷（每月租金 − 每月房贷利息与持有成本）＝ 粗略回本月数」。
写清楚三点：分母用的是**利息**而不是月供全额（还本金那部分是转成了你的资产，不是支出）；持有成本要含 service charge、ground rent、房屋保险与维修预留；这个算法**不包含房价涨跌**，因为本手册不预测房价。

**sec-5 这几种情况建议继续租** —— 签证剩余时长短或毕业后去向未定；两三年内可能离开英国（一次性成本摊不平）；首付会掏空应急金；还在试工作、城市可能换；leasehold 剩余年限短而预算只够买这类房（指向 8.3）。

- [ ] **Step 5: 写 `faq`（4–5 条）**

至少覆盖：持学生签证能买房吗（能，买房不限身份，但贷款很难，见 8.2）；买房能帮我留在英国吗（不能，没有这类签证路径）；父母在国内全款给我买，算我的还是他们的（涉及产权登记与谁是买方，指向 8.4 的海外买家附加税与 8.5 的产权登记）；买房到底比租房便宜吗（看持有年限，给 sec-4 的算法，不给结论）；印花税能退吗（一般不能，仅在特定情形如卖掉原有住宅后申请退还追加房产附加税，指向 8.4）。

**写 faq 时注意 Global Constraints 里的 YAML 陷阱**：`a:` 的值用双引号包裹时，里面要引号只能用「」。

- [ ] **Step 6: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/projects/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
test -f _site/maifang/mai-vs-zu/index.html && echo "8.1 built"
# frontmatter 没被静默丢掉：faq 与 toc 应该渲染出来了
grep -c 'id="faq"' _site/maifang/mai-vs-zu/index.html
grep -c 'sec-5' _site/maifang/mai-vs-zu/index.html
```

预期：两个 `grep -c` 都 ≥ 1。再跑完整 `VERIFY`。

- [ ] **Step 7: 提交**

```bash
cd /home/yfrl/projects/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add 8.1 on whether to buy or keep renting

Opens the chapter by correcting the two misconceptions that cost readers
the most: buying is not restricted by visa status (lending is), and no UK
visa route is granted by owning property. Gives a break-even method the
reader can apply to their own numbers rather than a worked example that
would date.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: 8.2 预算与贷款

**Files:**
- Create: `_chapters/maifang/daikuan.md`

**Interfaces:**
- Consumes: Task 1 的 `key: maifang`；8.1 的「贷款才是真正的限制」这一论点在此展开。
- Produces: `/maifang/daikuan/`。

- [ ] **Step 1: 现场核实一条事实**

用 gov.uk 核实 Help to Buy 股权贷款的当前状态（预期：2023 年 3 月结束新申请，无继任的股权贷款计划），以及 Shared Ownership 是否仍在运行。核到什么写什么，核不到就不提这个计划。

- [ ] **Step 2: 写断言并确认还不存在**

```bash
cd /home/yfrl/projects/uk-handbook
test -f _site/maifang/daikuan/index.html && echo "8.2 built"
```

- [ ] **Step 3: 写 frontmatter**

```yaml
---
layout: section
title: "英国按揭贷款：首付比例、收入倍数与签证持有人能否贷款"
description: "在英国申请按揭的实操：LTV 与首付比例怎么定、2025 年 7 月转为常设的按揭担保计划（5% 首付、房价上限 60 万镑）、收入倍数 4.5 倍的真实含义、签证持有人被贷款方看哪几项、从零建立英国信用记录的方法、Lifetime ISA 的 4000 镑年额度与 45 万镑房价上限，以及 AIP 什么时候办。"
nav: "8.2 预算与贷款"
parent: maifang
weight: 812
updated: 2026-09-12
num: "8.2"
toc:
  - title: "首付、LTV 与按揭担保计划"
    anchor: "sec-1"
  - title: "能贷多少：收入倍数与负担能力测试"
    anchor: "sec-2"
  - title: "签证持有人贷款：贷款方在看什么"
    anchor: "sec-3"
  - title: "英国信用记录怎么从零建起"
    anchor: "sec-4"
  - title: "Lifetime ISA：省钱的同时别踩上限"
    anchor: "sec-5"
  - title: "AIP、正式申请与 broker"
    anchor: "sec-6"
  - title: "常见问题"
    anchor: "faq"
---
```

- [ ] **Step 4: 写正文六节**

**sec-1 首付、LTV 与按揭担保计划** —— LTV 的定义与「首付越高利率档越好」的阶梯效应（写机制，不写具体利率）。**按揭担保计划（Freedom to Buy）**按速查表写：2025 年 7 月起常设、91–95% LTV、房价上限 £600,000、不限首次购房者，并写明**它是政府给贷款方的兜底、不是给买家的补贴**。Help to Buy 按 Step 1 的核实结果写。

**sec-2 能贷多少** —— 收入倍数按速查表写：**4.5 倍是市场基准而非法定上限**，2025 年监管放宽后个案可到 5–6 倍，以贷款方当下政策为准，**不点名银行、不写死倍数**。负担能力测试看的是什么：收入构成（基本工资 vs 奖金 vs 自雇）、现有债务与信用卡额度、受抚养人数、压力利率测试。

**sec-3 签证持有人贷款** —— 各行政策不公开且差异大，所以写**判断维度**：签证剩余时长（普遍是关键门槛）、在英连续居住时长、收入是否英国来源与币种、首付比例要求（非永居常被要求更高首付）、是否有英国信用记录。明确写「有贷款方做这类业务，条件按个案定，去问 broker 比逐家银行问快」——但**不推荐具体 broker**。

**sec-4 英国信用记录怎么从零建起** —— 电子名册（选民登记，注意留学生的资格限制）、把水电宽带账单放到自己名下、信用卡按时全额还款且控制使用率、避免短期内密集申请留下大量硬查询、三家征信机构可自查。链到 5.2 税务页与 1.4 银行开户页。

**sec-5 Lifetime ISA** —— 按速查表写全部数字：£4,000/年、25% 奖励封顶 £1,000、18–39 岁开户、40 岁前首次存入、可存到 50 岁、首套房价上限 **£450,000**、需开户满 12 个月、不合规提取扣 25%。用 `.callout .callout-warning` 写两个陷阱：**£450,000 上限在伦敦极易触顶，且超一镑就整笔不能用于购房**；**25% 的罚扣高于 25% 的奖励，中途取出会亏本金**。再写一句资格前提：需为英国税务居民，离开英国后的处理要另查。

**sec-6 AIP、正式申请与 broker** —— AIP/DIP 是什么、为什么中介会先要这个、软查询与硬查询的区别、AIP 有效期、AIP 不等于批贷。broker 的两种收费模式与「whole of market」的含义，写成判断标准而非推荐。

- [ ] **Step 5: 写 `faq`（5–6 条）**

至少覆盖：学生签证能贷款吗（极难，写清门槛在哪）；签证只剩两年还能贷吗（取决于贷款方，写判断维度）；父母在国内的收入能算进来吗（一般不能，境外收入与担保的常见障碍）；没有英国信用记录怎么办（sec-4 的路径 + 时间预期）；Lifetime ISA 买到 £450,000 以上的房子会怎样（不能用于购房，取出扣 25%，本金亏损）；5% 首付真的能买吗（能，但要说清高 LTV 的代价）。

- [ ] **Step 6: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/projects/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
test -f _site/maifang/daikuan/index.html && echo "8.2 built"
grep -c 'id="faq"' _site/maifang/daikuan/index.html
grep -c '450,000\|£450' _site/maifang/daikuan/index.html
```

预期：两个 `grep -c` 都 ≥ 1。再跑完整 `VERIFY`。

- [ ] **Step 7: 提交**

```bash
cd /home/yfrl/projects/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add 8.2 on budgets and mortgages

Covers the part that actually gates non-permanent residents: what lenders
look at, how to build a UK credit file from nothing, and the Lifetime ISA
limits. Income multiples are written as a market baseline with the 2025
relaxation noted, not as a fixed rule, and no lender is named.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: 8.3 找房、看房与出价

**Files:**
- Create: `_chapters/maifang/kanfang-chujia.md`

**Interfaces:**
- Consumes: Task 1 的 `key: maifang`。
- Produces: `/maifang/kanfang-chujia/`，leasehold 一节供 8.1 与 8.5 反向链接。

- [ ] **Step 1: 写断言并确认还不存在**

```bash
cd /home/yfrl/projects/uk-handbook
test -f _site/maifang/kanfang-chujia/index.html && echo "8.3 built"
```

- [ ] **Step 2: 写 frontmatter**

```yaml
---
layout: section
title: "英国看房与出价：产权类型、看房清单与 chain 怎么回事"
description: "在英国找房看房出价的实操：挂牌平台怎么用、freehold 与 leasehold 的区别以及剩余年限、ground rent、service charge 各意味着什么、看房时要逐项确认的清单、出价与还价的常见做法、chain 是什么，以及交换合同前双方都可以无责退出这一点对买家的实际影响。"
nav: "8.3 找房、看房与出价"
parent: maifang
weight: 813
updated: 2026-09-12
num: "8.3"
toc:
  - title: "在哪找房，挂牌价怎么看"
    anchor: "sec-1"
  - title: "Freehold 与 Leasehold"
    anchor: "sec-2"
  - title: "看房前能自己查到的信息"
    anchor: "sec-3"
  - title: "看房清单"
    anchor: "sec-4"
  - title: "出价、还价与 chain"
    anchor: "sec-5"
  - title: "交换合同前，一切都可能反悔"
    anchor: "sec-6"
  - title: "常见问题"
    anchor: "faq"
---
```

- [ ] **Step 3: 写正文六节**

**sec-1 在哪找房** —— Rightmove / Zoopla / OnTheMarket 的覆盖差异、直接联系中介的作用、挂牌价（asking price）在英国是**起点而非定价**，以及 guide price、offers over、offers in excess of 的含义差别。

**sec-2 Freehold 与 Leasehold**（本页最重要的一节，给足篇幅）—— 两种产权的本质区别；leasehold 要逐项确认的四件事：**剩余年限**（年限越短越难贷款、延期成本随年限下降急升）、**ground rent**（条款里的递增机制）、**service charge**（历年金额与是否有大修摊派 major works）、**管理方与 lease 条款限制**（能否出租、能否养宠物、能否改动）。再写 share of freehold 与新建公寓的常见坑。用 `.callout .callout-warning` 写一句：leasehold 的问题**在交换合同之后几乎无法补救**，要在出价前就让律师看 lease。

**sec-3 看房前能自己查到的信息** —— EPC 等级（可在线查）、council tax band、成交历史、洪水风险、规划申请记录、周边治安统计。写成「看房前先查这几项，不合适就不用去」。

**sec-4 看房清单** —— 潮湿与霉斑（英国老房最常见问题）、窗户与隔热、供暖系统与锅炉年份、电气与燃气证书、屋顶与外墙、朝向与采光、噪音（不同时段各看一次）、手机信号与宽带可用速率、停车。写成可勾选的列表。

**sec-5 出价、还价与 chain** —— 出价通过中介进行、可附条件（如要求撤下挂牌）、卖方接受后仍不具约束力。**chain** 的定义与风险：链条上任一环节断裂会整体停摆；**无链条买家（首次购房者、现金买家）在同等价格下有实质优势**，出价时要主动说明。

**sec-6 交换合同前，一切都可能反悔** —— **gazumping**（卖方接受更高报价而毁约）与 gazundering（买方临交换前压价）在英格兰与威尔士**合法**，因为约束力从交换合同才开始（见 8.5）。这与中国的购房习惯差别最大，单独成节。写三条实际对策：尽量缩短从接受 offer 到交换的时间、要求卖方撤下挂牌、了解 home buyer protection 类保险的存在但不推荐具体产品。

- [ ] **Step 4: 写 `faq`（5 条左右）**

至少覆盖：leasehold 剩余多少年就该警惕（写清「年限越短越难贷款且延期越贵」的机制与咨询律师的时点，不给绝对数字门槛）；service charge 会涨吗（会，要看历年记录与 major works）；挂牌价能砍多少（没有通用比例，写判断依据）；卖方接受我的 offer 后又卖给别人，我能告他吗（在英格兰与威尔士不能，交换合同前无约束力）；新建房（new build）要注意什么（交付延期条款、管理费、开发商推荐的律师与按揭是否独立）。

- [ ] **Step 5: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/projects/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
test -f _site/maifang/kanfang-chujia/index.html && echo "8.3 built"
grep -c 'id="faq"' _site/maifang/kanfang-chujia/index.html
grep -c 'sec-6' _site/maifang/kanfang-chujia/index.html
```

再跑完整 `VERIFY`。

- [ ] **Step 6: 提交**

```bash
cd /home/yfrl/projects/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add 8.3 on viewing and making an offer

Gives leasehold its own long section because it is where a Chinese buyer
loses the most money and the damage is unfixable after exchange. Also
states plainly that gazumping is legal in England and Wales, which is the
sharpest break from how buyers expect an accepted offer to work.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: 8.4 税费总账

全章数字密度最高的一页。**所有税率只能抄「已核实的事实速查」。**

**Files:**
- Create: `_chapters/maifang/shuifei.md`

**Interfaces:**
- Consumes: Task 1 的 `key: maifang`。
- Produces: `/maifang/shuifei/`，供 8.1、8.5、附录速查表反向链接。

- [ ] **Step 1: 写断言并确认还不存在**

```bash
cd /home/yfrl/projects/uk-handbook
test -f _site/maifang/shuifei/index.html && echo "8.4 built"
```

- [ ] **Step 2: 写 frontmatter**

```yaml
---
layout: section
title: "英国买房要交多少税费：印花税分档、海外买家附加与全部一次性成本"
description: "在英国买房的全部一次性支出：2025 年 4 月起生效的 SDLT 分档与首次购房减免、非英国居民 2% 附加税与第二套房 5% 附加税怎么叠加、威尔士 LTT 的两张表与它没有首次购房减免这件事、土地登记费档，以及律师费、测量费、按揭手续费等要另外预留多少。"
nav: "8.4 税费总账"
parent: maifang
weight: 814
updated: 2026-09-12
num: "8.4"
toc:
  - title: "印花税 SDLT：英格兰与北爱尔兰"
    anchor: "sec-1"
  - title: "首次购房减免与 50 万镑悬崖"
    anchor: "sec-2"
  - title: "两种附加税：海外买家与第二套房"
    anchor: "sec-3"
  - title: "威尔士：LTT 与没有首次购房减免"
    anchor: "sec-4"
  - title: "税之外的一次性成本"
    anchor: "sec-5"
  - title: "一张总账表"
    anchor: "sec-6"
  - title: "常见问题"
    anchor: "faq"
---
```

- [ ] **Step 3: 写正文六节**

**sec-1 印花税 SDLT** —— 抄速查表的五档表格，**表头或表下单独标注「现行分档自 2025 年 4 月 1 日起」**。写清楚是**分段累进**（每一档只对落在该档的部分计税），中文攻略常写成全额单一税率。用 `.callout .callout-warning` 提醒：2022–2025 年的临时门槛（nil band £250,000、首次购房 £425,000）**已经失效**，网上大量攻略仍在用，别照着算预算。

**sec-2 首次购房减免与 50 万镑悬崖** —— 0% 至 £300,000、5% 于 £300,001–£500,000；**房价超过 £500,000 整笔减免作废，按标准分档计算**。这是本页最该被单独搜到的一条，用 `.callout .callout-warning` 强调「£500,000 是悬崖不是斜坡」，并说明这在伦敦与东南部意味着什么。再写「首次购房者」的认定口径：**在全球范围内从未拥有过住宅**——在国内有房的人不符合条件，这条中国读者极易误判。

**sec-3 两种附加税** —— **非英国居民 +2%**，判定是购房前 12 个月内在英停留**不足 183 天**（写清是按停留天数而非签证类型判定，且可在满足条件后申请退还）；**追加房产 +5%**，名下不止一套住宅即适用，**海外已有房产也计入**——这两条对中国买家的实际影响远大于本地买家。明确写两者**可以叠加**，并给出叠加后的量级感受。再一句：买来出租是另一套税务体系（房产收入所得税三档自 2027 年 4 月起升至 22%/42%/47%），本手册不展开。

**sec-4 威尔士** —— 抄速查表的主表（自 2022 年 10 月 10 日起）与高档表（自 2024 年 12 月 11 日起），各自标生效时点。**用 `.callout .callout-warning` 写明威尔士没有首次购房减免**，并说明这是中文攻略照搬英格兰写法最常出错的地方。苏格兰指向 8.6。北爱尔兰在 FAQ 里说明。

**sec-5 税之外的一次性成本** —— 逐项列出：律师费与 searches、测量费（三级，详见 8.5）、按揭手续费与估值费、**土地登记费**（抄速查表的六档表，标明 Land Registration Fee Order 2024 自 2024 年 12 月 9 日生效，电子申请减 55%）、搬家费。除土地登记费外**一律写量级 + 以实际报价为准**。

**sec-6 一张总账表** —— 一张表把上述项目列成「项目 / 金额或量级 / 出现时点 / 能否退」三到四列，让读者知道首付之外还要另留多少现金、以及哪些钱是在交换合同前就要付掉的（律师费与测量费即使交易失败也照付，这点要写明）。**不要给假想房价的完整算例**——会过期，且容易被当成报价。

- [ ] **Step 4: 写 `faq`（5–6 条）**

至少覆盖：我在国内有房，还算首次购房者吗（不算，全球口径）；印花税什么时候交、怎么交（由律师在完成交割后代为申报与缴纳，有法定期限）；2% 海外买家附加税能退吗（满足居住天数条件后可申请退还，写清是按天数判定）；北爱尔兰适用哪一套（与英格兰同用 SDLT）；夫妻一方有房、以另一方名义买能否避开 5% 附加（不能，写清认定是按家庭单位而非个人，且要提醒这类安排另有法律后果）；房价刚好在 £500,000 附近怎么办（说明悬崖效应下多付一镑的代价）。

- [ ] **Step 5: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/projects/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
test -f _site/maifang/shuifei/index.html && echo "8.4 built"
grep -c 'id="faq"' _site/maifang/shuifei/index.html
# 现行数字在、失效的旧门槛只应出现在「已失效」的提醒语境里
grep -o '125,000\|300,000\|500,000\|425,000\|225,000' _site/maifang/shuifei/index.html | sort | uniq -c
# 生效时点必须出现
grep -c '2025 年 4 月 1 日' _site/maifang/shuifei/index.html
```

预期：`125,000`、`300,000`、`500,000`、`225,000` 都出现；`425,000` 若出现，**必须**在「已失效」的段落里——逐条肉眼确认上下文。生效时点 ≥ 1。再跑完整 `VERIFY`。

- [ ] **Step 6: 提交**

```bash
cd /home/yfrl/projects/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add 8.4 on stamp duty and the full cost of buying

Every rate table carries its own effective date, separate from the page's
updated field, because these are the figures most likely to be read from a
stale Chinese-language guide. Two points get their own callouts: first-time
relief is a cliff at £500,000, not a taper, and first-time status is judged
worldwide, so a flat back home disqualifies you.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: 8.5 从 offer 到交房

**Files:**
- Create: `_chapters/maifang/liucheng.md`

**Interfaces:**
- Consumes: Task 1 的 `key: maifang`；8.3 的 sec-6（交换合同前无约束力）在此给出完整的法律分界说明。
- Produces: `/maifang/liucheng/`。

- [ ] **Step 1: 写断言并确认还不存在**

```bash
cd /home/yfrl/projects/uk-handbook
test -f _site/maifang/liucheng/index.html && echo "8.5 built"
```

- [ ] **Step 2: 写 frontmatter**

```yaml
---
layout: section
title: "英国买房流程：律师、测量、交换合同与交割"
description: "从卖方接受 offer 到拿到钥匙的完整流程：conveyancing 各阶段在做什么、searches 查的是什么、三级 RICS 测量怎么选以及为什么按揭估值不能替代它、交换合同这条法律分界线意味着什么（此前可无责退出，此后毁约赔定金），以及交房后每月还要付哪些持有成本。"
nav: "8.5 从 offer 到交房"
parent: maifang
weight: 815
updated: 2026-09-12
num: "8.5"
toc:
  - title: "全流程时间轴"
    anchor: "sec-1"
  - title: "律师在做什么：conveyancing 与 searches"
    anchor: "sec-2"
  - title: "测量：三级怎么选"
    anchor: "sec-3"
  - title: "交换合同：法律分界线"
    anchor: "sec-4"
  - title: "完成交割与拿钥匙"
    anchor: "sec-5"
  - title: "交房之后的持有成本"
    anchor: "sec-6"
  - title: "常见问题"
    anchor: "faq"
---
```

- [ ] **Step 3: 写正文六节**

**sec-1 全流程时间轴** —— 按顺序：卖方接受 offer → 委托律师（conveyancer）→ 正式按揭申请与估值 → searches → 测量 → 律师查询与回复 → 交换合同 → 完成交割。写清**这个过程通常以月计而不是以周计**，以及最常见的三个拖慢点（searches 的地方政府响应、按揭正式批复、chain 上其他环节）。不给具体周数承诺。

**sec-2 律师在做什么** —— conveyancing 包含什么；searches 查的是什么（地方政府规划与道路、环境、排水与供水、矿区等按地区追加）；产权与 lease 条款审查；**律师费与 searches 即使交易失败也通常照付**（no completion no fee 的条款要看清适用范围）。再写一句独立性：开发商或中介「推荐」的律师要确认是否独立。

**sec-3 测量：三级怎么选** —— RICS 三个级别的适用场景（新一些的标准房 / 多数二手房 / 老房、有改动或明显问题的房）。用 `.callout .callout-warning` 写死一条：**按揭估值（valuation）是贷款方为自己做的风险评估，不是给你的房屋检查，不能替代测量**。这是读者最常省错的一笔钱。费用写量级。

**sec-4 交换合同：法律分界线**（本页最重要的一节，独立成节）—— 交换之前：任一方可以无责退出，gazumping 合法（见 8.3）。交换之时：付定金（通常为房价的 10%）、确定完成日期。交换之后：毁约方承担违约责任，买方毁约通常损失定金。用 `.callout .callout-warning`。再写一句实务：**房屋保险通常从交换合同起就要生效**，因为风险自交换起转移，这一条很多买家漏办。

**sec-5 完成交割与拿钥匙** —— 尾款划转、钥匙交接的实际时点、律师代为申报与缴纳印花税（有法定期限，见 8.4）、土地登记（费用见 8.4）。提醒**完成日当天资金到账时间会影响能否当天拿钥匙**。

**sec-6 交房之后的持有成本** —— council tax（band 怎么查，学生豁免的适用边界指向 5.3）、leasehold 的 service charge 与 ground rent（见 8.3）、房屋保险（建筑险与财产险的区别，按揭方通常要求建筑险）、维修预留。最后一句带过 **High Value Council Tax Surcharge**：2028 年 4 月起针对 £2,000,000 及以上住宅、向业主征收、目前处于征询阶段以最终立法为准，与绝大多数读者无关。

- [ ] **Step 4: 写 `faq`（5 条左右）**

至少覆盖：整个流程要多久（写影响因素与拖慢点，不给承诺周数）；交换合同后我能反悔吗（能，但通常损失 10% 定金）；测量报告查出问题怎么办（可据此重新议价或要求修复，写时点在交换之前）；律师能不能自己选（能，写独立性判断）；房屋保险什么时候开始买（交换合同起生效）。

- [ ] **Step 5: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/projects/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
test -f _site/maifang/liucheng/index.html && echo "8.5 built"
grep -c 'id="faq"' _site/maifang/liucheng/index.html
grep -c 'sec-6' _site/maifang/liucheng/index.html
```

再跑完整 `VERIFY`。

- [ ] **Step 6: 提交**

```bash
cd /home/yfrl/projects/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add 8.5 on conveyancing through to completion

Exchange of contracts gets its own section: it is the line where nothing
becomes binding, and readers coming from a Chinese purchase expect that
line much earlier. Also states that a mortgage valuation is not a survey,
which is the cost readers most often cut by mistake.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: 8.6 苏格兰买房的不同之处

**Files:**
- Create: `_chapters/maifang/sugelan.md`

**Interfaces:**
- Consumes: Task 1 的 `key: maifang`；前五页建立的英格兰流程作为对照基准。
- Produces: `/maifang/sugelan/`。

- [ ] **Step 1: 写断言并确认还不存在**

```bash
cd /home/yfrl/projects/uk-handbook
test -f _site/maifang/sugelan/index.html && echo "8.6 built"
```

- [ ] **Step 2: 写 frontmatter**

```yaml
---
layout: section
title: "在苏格兰买房：Home Report、offers over 与 LBTT"
description: "苏格兰买房与英格兰完全不同的一套规则：卖方提供的 Home Report 让买家看房前就能拿到估价与状况报告、offers over 与 closing date 的竞价机制、missives 取代交换合同因而约束力产生的时点不同、LBTT 分档与首次购房减免，以及按全额房价计征的 8% 附加住宅税 ADS。"
nav: "8.6 苏格兰买房的不同之处"
parent: maifang
weight: 816
updated: 2026-09-12
num: "8.6"
toc:
  - title: "为什么苏格兰要单独讲"
    anchor: "sec-1"
  - title: "Home Report：卖方先把底牌摊开"
    anchor: "sec-2"
  - title: "Offers over 与 closing date"
    anchor: "sec-3"
  - title: "Missives：约束力从哪一刻开始"
    anchor: "sec-4"
  - title: "LBTT 与 ADS"
    anchor: "sec-5"
  - title: "常见问题"
    anchor: "faq"
---
```

- [ ] **Step 3: 写正文五节**

**sec-1 为什么苏格兰要单独讲** —— 开篇用 `.callout .callout-warning` 写明：苏格兰是独立法域，买房流程、报告制度、约束力时点与税种**四项全都不同**，前面五页的内容**不能直接套用**；能沿用的只有贷款相关（8.2，贷款方多为全英业务）。

**sec-2 Home Report** —— 由**卖方**提供、买家看房前即可索取，通常含单一调查报告（状况与估价）、能源报告与物业问卷。对买家的实际意义：**估价与状况信息前置**，不必像英格兰那样自费测量后才发现问题；但也要写清它是卖方委托的，重大关切仍可自行追加检查。

**sec-3 Offers over 与 closing date** —— 挂牌常写 offers over，实际成交价普遍高于该数字；有意者向卖方律师**注记兴趣（note interest）**，竞争者多时卖方设 **closing date**，各方在截止时点提交**一次性密封报价**。写清这与英格兰逐轮加价的还价方式完全不同，以及它对买家出价策略的影响。

**sec-4 Missives** —— 双方律师往来的正式函件构成合同，**missives concluded（结定）即产生约束力**，取代英格兰的「交换合同」。写清约束力产生的时点与英格兰不同，因此**gazumping 的窗口期与风险分布也不同**。

**sec-5 LBTT 与 ADS** —— 抄速查表的 LBTT 五档表并标注「分档自 2021 年 4 月 1 日起」；首次购房减免 nil band 提高到 **£175,000**、最多省 **£600**。**ADS 8%**，自 **2024 年 12 月 5 日**起，**按全额房价计算而非分档**，对价 £40,000 及以上适用——用 `.callout .callout-warning` 强调「按全额计」这一点，因为它与英格兰的 +5% 分档叠加方式不同，金额差别很大。

- [ ] **Step 4: 写 `faq`（4 条左右）**

至少覆盖：苏格兰买房还需要自己做测量吗（Home Report 已含状况与估价，但重大关切可自行追加）；offers over 上面要加多少（没有通用比例，写判断依据与 closing date 的密封报价机制）；苏格兰也有 gazumping 吗（missives 结定后即有约束力，窗口期与英格兰不同）；前面几页哪些内容在苏格兰仍然适用（贷款相关基本适用，流程、报告、税种都不适用）。

- [ ] **Step 5: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/projects/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
test -f _site/maifang/sugelan/index.html && echo "8.6 built"
grep -c 'id="faq"' _site/maifang/sugelan/index.html
grep -c '145,000\|175,000' _site/maifang/sugelan/index.html
grep -c '2024 年 12 月 5 日' _site/maifang/sugelan/index.html
```

预期：三个 `grep -c` 都 ≥ 1。再跑完整 `VERIFY`。

- [ ] **Step 6: 提交**

```bash
cd /home/yfrl/projects/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add 8.6 on buying in Scotland

Scotland differs on all four axes that matter — the seller-supplied Home
Report, sealed bids at a closing date, binding missives instead of
exchange, and LBTT with an 8% supplement charged on the full price rather
than in bands — so it gets its own section rather than scattered caveats.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: 速查表与相邻章节的出口链接

**Files:**
- Modify: `_chapters/fulu.md`（关键数字表加一组「买房」）
- Modify: `_chapters/shenghuo/zufang.md`（页尾加出口链接）
- Modify: `_chapters/jinjie/shuiwu.md`（仅在正文已提及房产相关税务时加交叉链接）

**Interfaces:**
- Consumes: Task 5 的 `/maifang/shuifei/` 与 Task 3 的 `/maifang/daikuan/`。

- [ ] **Step 1: 在 `_chapters/fulu.md` 的「关键数字」一节加一组「买房」**

插在 `<h2 id="sec-2">关键数字（2026/27）</h2>` 之下现有的「住与行」组之后，照现有三列格式（项目 / 数字 / 展开）：

| 项目 | 数字 | 展开 |
| --- | --- | --- |
| 印花税起征（英格兰、北爱） | **£125,000** | 自 2025 年 4 月 1 日起，[8.4] |
| 首次购房免税额度 | **£300,000** | 房价超 £500,000 则完全不适用 |
| 非英国居民附加税 | **+2%** | 购房前 12 个月在英不足 183 天 |
| 追加房产附加税 | **+5%** | 海外已有房产也计入 |
| 苏格兰 ADS | **8%**，按全额房价计 | 自 2024 年 12 月 5 日起，[8.6] |
| Lifetime ISA 年额度 | **£4,000**，奖励 25% | 首套房价上限 **£450,000**，[8.2] |

「展开」列的章节号照现有写法做成链接：`[8.4]({{ '/maifang/shuifei/' | relative_url }})`。

同时更新 `fulu.md` 的 `description`，把买房关键数字纳入（现有 description 列举了各组内容）。

- [ ] **Step 2: 在 `_chapters/shenghuo/zufang.md` 页尾加出口链接**

在文件末尾「实用 App」列表之后，加一个 `.callout .callout-info` 块，一句话指向第八章：从长期租房转向考虑买房的读者，该看哪一页（给 8.1 与 8.2 两个链接）。**不要改动该页其余任何内容。**

- [ ] **Step 3: 检查 `_chapters/jinjie/shuiwu.md` 是否需要交叉链接**

```bash
cd /home/yfrl/projects/uk-handbook
grep -n '房产\|印花税\|Stamp Duty\|租金收入' _chapters/jinjie/shuiwu.md
```

有命中就在相应位置加一句指向 8.4 的链接；**没有命中就不动这个文件**，并在提交信息里说明未改动。

- [ ] **Step 4: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/projects/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
# 速查表里出现买房数字且链接可达
grep -c 'maifang/shuifei' _site/fulu/index.html
grep -c 'maifang' _site/shenghuo/zufang/index.html
```

预期：两个 `grep -c` 都 ≥ 1。再跑完整 `VERIFY`。

- [ ] **Step 5: 提交**

```bash
cd /home/yfrl/projects/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Wire the home-buying chapter into the quick-reference and rental pages

Adds the six buying figures readers most often need at a glance, and gives
the rental page an exit toward chapter 8 for readers moving on from
long-term renting.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: 首页与 README

**Files:**
- Modify: `index.md`（「从这里开始」列表）
- Modify: `README.md`（概述、目录表、年度复核表）

- [ ] **Step 1: 在 `index.md` 的「从这里开始」加第八章条目**

加在第七章安全篇条目之后，照现有格式（章名加粗链接 + 破折号 + 专题链接列举）：

```markdown
- **[第八章 买房篇]({{ '/maifang/' | relative_url }})** —— [买还是继续租]({{ '/maifang/mai-vs-zu/' | relative_url }})、[预算与贷款]({{ '/maifang/daikuan/' | relative_url }})、[找房看房与出价]({{ '/maifang/kanfang-chujia/' | relative_url }})、[税费总账]({{ '/maifang/shuifei/' | relative_url }})、[从 offer 到交房]({{ '/maifang/liucheng/' | relative_url }})、[苏格兰买房]({{ '/maifang/sugelan/' | relative_url }})
```

先确认第七章条目的实际写法并与之对齐（有的条目带一句说明，有的直接列专题）。

- [ ] **Step 2: 改 `README.md` 的概述与目录表**

- 开头的「覆盖**生活、学业、社交文化、工作实习、生活进阶、旅游、安全应急**七大方面……共 7 章 + 行前准备 + 三个附录」改为八大方面、8 章，把「买房」加进列举。
- 目录表在「第七章 安全与应急篇」之后加一行：

```markdown
| 第八章 买房篇 | `/maifang/` | 6（买还是继续租、预算与贷款、找房看房与出价、税费总账、从 offer 到交房、苏格兰买房） |
```

- [ ] **Step 3: 在 `README.md` 的「金额与政策的年度复核」表加四行**

```markdown
| 每年 4 月 | SDLT 分档、首次购房减免门槛、追加房产附加税 | `maifang/shuifei` | [gov.uk](https://www.gov.uk/stamp-duty-land-tax/residential-property-rates) |
| 每年 4 月 | LBTT 分档与 ADS、LTT 主表与高档表 | `maifang/shuifei`、`maifang/sugelan` | [revenue.scot](https://revenue.scot/taxes/land-buildings-transaction-tax)、[gov.wales](https://www.gov.wales/land-transaction-tax-rates-and-bands) |
| 每年 4 月 | Lifetime ISA 年额度与 £450k 房价上限 | `maifang/daikuan`、`fulu` | [gov.uk](https://www.gov.uk/lifetime-isa) |
| 不定期 | 海外买家 2% 附加税、Freedom to Buy 条件、Land Registry 费档 | `maifang/shuifei`、`maifang/daikuan` | gov.uk |
```

再在该表下方现有的免签提醒段落之后，加一句同类的强调：**买房篇的每张税率表各自带生效时点，与 frontmatter 的 `updated` 分开；印花税分档自 2025 年 4 月 1 日起已回调，改错别字时不要顺手刷新这些日期。**

- [ ] **Step 4: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/projects/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
grep -c 'maifang' _site/index.html
grep -c 'maifang' README.md
```

预期：两个 `grep -c` 都 ≥ 1（README 不参与构建，直接 grep 源文件）。再跑完整 `VERIFY`。

- [ ] **Step 5: 提交**

```bash
cd /home/yfrl/projects/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
List the home-buying chapter on the home page and in the README

Adds the four annual review rows this chapter needs; its rate tables carry
their own effective dates, and the README now says so alongside the
existing visa-snapshot warning.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 10: 全站收尾验证

**Files:** 无改动（除非发现问题）

- [ ] **Step 1: 完整构建与页数核对**

```bash
cd /home/yfrl/projects/uk-handbook
rm -rf _site
bundle exec jekyll build --trace 2>&1 | tail -3
find _site -name index.html | wc -l
```

预期：**74**（基线 67 + 7 个新页）。对不上就逐个 `test -f` 找出缺哪一页。

- [ ] **Step 2: frontmatter 逐页确认没被静默丢弃**

```bash
cd /home/yfrl/projects/uk-handbook
for p in mai-vs-zu daikuan kanfang-chujia shuifei liucheng sugelan; do
  n=$(grep -c 'id="faq"' "_site/maifang/$p/index.html")
  t=$(grep -c 'class="toc"' "_site/maifang/$p/index.html")
  echo "$p faq=$n toc=$t"
done
```

预期：六页的 `faq` 与 `toc` **全部 ≥ 1**。任何一项为 0，就是该页 frontmatter 的 YAML 被静默丢掉了——回去查双引号标量里是不是混进了 ASCII 双引号。

- [ ] **Step 3: 阅读顺序与导航**

```bash
cd /home/yfrl/projects/uk-handbook
# 侧边栏顺序：安全篇 → 买房篇六页 → 结语
grep -o 'href="/[a-z-]*/\?[a-z-]*/"' _site/maifang/mai-vs-zu/index.html | head -30
# 上一页/下一页链条：8.1 的上一页应是安全篇最后一节，8.6 的下一页应是结语
grep -A2 'chapter-nav' _site/maifang/sugelan/index.html | head -20
```

肉眼确认第八章整体落在安全篇与结语之间，且六个专题内部顺序为 8.1→8.6。

- [ ] **Step 4: 联盟链接与 sitemap**

```bash
cd /home/yfrl/projects/uk-handbook
# 本章不应引入任何联盟链接：下面应无输出
ruby -ryaml -e '
  matches = (YAML.load_file("_data/affiliates.yml")["domains"] || []).map { |d| d["match"] }.compact
  Dir.glob("_site/maifang/**/*.html").each do |f|
    File.read(f).scan(/<a\s([^>]*)>/) do |attrs,|
      href = attrs[/href="([^"]*)"/, 1]
      puts "#{f}: #{href}" if href && matches.any? { |m| href.include?(m) }
    end
  end
'
# sitemap 收录了七个新页
grep -c 'maifang' _site/sitemap.xml
```

预期：第一段无输出；`grep -c` 为 **7**。

- [ ] **Step 5: 数字与来源的最后一遍人工核对**

对照本计划「已核实的事实速查」，逐条确认正文里出现的每个具体金额都能在速查表里找到对应条目：

```bash
cd /home/yfrl/projects/uk-handbook
grep -oh '£[0-9][0-9,]*' _chapters/maifang/*.md | sort | uniq -c | sort -rn
```

把输出里的每个金额与速查表比对。**出现在速查表之外的金额一律删掉或改成量级表述**，唯一的例外是明确标注为「已失效」的旧门槛。

- [ ] **Step 6: 推送**

前面所有断言通过后，一次性推送（推送即部署）：

```bash
cd /home/yfrl/projects/uk-handbook
git status --short
git log --oneline -10
git push
```

- [ ] **Step 7: 确认线上构建**

```bash
gh run list --limit 3
```

等最近一次 `Build and deploy site` 变为 success。失败就看日志，最可能的失败点是 frontmatter 校验（YAML 双引号）与页数下限。

---

## Self-Review 记录

**1. Spec 覆盖检查**

| Spec 要求 | 对应任务 |
| --- | --- |
| 新建第八章 hub，weight 810、num 08 | Task 1 |
| 6 个专题页 811–816 | Task 2–7 |
| 现有页面 weight/num/permalink 不动 | Task 1 Step 5 的 `git diff` 断言 |
| `order` 字段顺延并修重复值 | Task 1 Step 5 |
| 8.1–8.6 各页内容大纲 | Task 2–7 的 Step「写正文」 |
| 已核实事实清单 + 生效时点标注 | 计划的「已核实的事实速查」+ Task 5/7 的断言 |
| 核不到就写量级 | Global Constraints + Task 10 Step 5 的金额核对 |
| README 年度复核表加四行 | Task 9 Step 3 |
| `index.md`、README 目录 | Task 9 Step 1–2 |
| `fulu.md` 买房关键数字 | Task 8 Step 1 |
| `zufang.md` 出口链接 | Task 8 Step 2 |
| `jinjie/shuiwu.md` 视情况加链接 | Task 8 Step 3（带条件判断命令） |
| 不新增联盟链接 | Task 10 Step 4 的断言 |
| 不写 buy-to-let 专页 | Task 5 sec-3 一句话带过 |
| 验收 1–5 | Task 10 Step 1–5 |

无遗漏。

**2. 占位符扫描**

计划内无 TBD / TODO / 「参照 Task N」。两处「现场核实」（Task 2 Step 1 的投资签证、Task 3 Step 1 的 Help to Buy）是**有明确预期结论与失败时写法**的核实动作，不是占位符。Task 8 Step 3 是带 grep 判据的条件动作，不是模糊指示。

**3. 命名一致性**

`key: maifang`、`parent: maifang` 在 Task 1 与 Task 2–7 中一致；六个文件名 `mai-vs-zu`、`daikuan`、`kanfang-chujia`、`shuifei`、`liucheng`、`sugelan` 在 File Structure、各任务的 frontmatter、Task 8/9 的链接、Task 10 的循环断言中拼写一致；weight 811–816 与 `num` 8.1–8.6 一一对应。
