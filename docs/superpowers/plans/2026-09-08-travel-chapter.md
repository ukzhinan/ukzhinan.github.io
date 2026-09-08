# 旅游篇（第六章）Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `_chapters/jinjie/lvxing.md` 单页升格为独立的第六章「旅游篇」，拆成 5 个专题页，补足中国护照免签清单与从英国申请申根签证的完整流程。

**Architecture:** 纯内容 + frontmatter 改动的 Jekyll 站点。新增一个 `chapter-hub` 章目录页与 5 个 `layout: section` 专题页；安全与应急篇整体顺延为第七章；进阶篇余下五页编号上移一位。排序完全由 frontmatter 的 `weight` 决定，URL 由 `permalink` 决定，两者独立——所以编号改动不影响任何 URL，只影响侧边栏顺序与正文里的链接文字。

**Tech Stack:** Jekyll 4（`bundle exec jekyll build`）、kramdown（`auto_ids: false`，标题锚点手写 `<h2 id="...">`）、纯 SCSS，无 JS 框架。没有单元测试；本计划的「测试」是 `jekyll build`、CI 的 frontmatter 校验脚本，以及 grep 断言。

**Spec:** `docs/superpowers/specs/2026-09-08-travel-chapter-design.md`

## Global Constraints

- **YAML 陷阱（最重要）：** frontmatter 的双引号标量里**不能出现 ASCII 双引号**。YAML 出错时 Jekyll 会**静默丢掉整块 frontmatter**（`faq`、`toc` 一起消失），页面照常构建、看不出问题。要引号就写中文引号「」，或整段换单引号包裹。
- **每页必须有** `title`、`description`、`nav`（CI 会校验），外加 `updated`（显示与 `dateModified` 用）。本次所有新页与被改页的 `updated` 一律写 `2026-09-08`。
- **`weight` 约定：** 章 = 序号 × 100，专题 = 章 weight + 小节号。
- **BRP 已停用：** 全站做过 BRP 清理，涉及英国居留证明时只写 eVisa / UKVI 账户 / share code，**不要写回 BRP**。
- **不新增联盟链接**（CI 会校验 `rel="sponsored nofollow"`，本次应保持零变化）。
- **中途不要 `git push`。** 推送即部署（`.github/workflows/pages.yml` 监听 main）。Task 3–8 之间会短暂存在旧旅行页与新旅游篇内容重复的状态，全部任务做完、Task 9 验证通过后再一次推送。
- **风格：** 跟随现有页面——中文正文、`.callout .callout-info/-tip/-warning` 提示块、`<h2 id="sec-N">` 手写锚点、frontmatter 里 `toc:` 与 `faq:` 列表驱动目录和常见问题。不要引入新的 CSS 类。

## 全局验证命令

每个任务末尾都要跑。下面记作 **`VERIFY`**：

```bash
cd /home/yfrl/uk-handbook

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

**基线：** 改动前 `bundle exec jekyll build` 通过，`find _site -name index.html | wc -l` = 60。做完全部任务后应为 66（新增 1 个 hub + 5 个专题，减 1 个旧旅行页，加 1 个 redirect = 60 − 1 + 6 + 1 = 66）。

---

## File Structure

| 文件 | 职责 |
| --- | --- |
| `_chapters/lvxing.md` | 第六章章目录页（`chapter-hub`）。章首语 + 自动列出 5 个专题 |
| `_chapters/lvxing/guihua.md` | 6.1 出行规划与签证总览。入口页：目的地 → 要办什么；护照有效期；90/180；EES/ETIAS；保险；学业日历 |
| `_chapters/lvxing/shengen.md` | 6.2 申根签证全流程。递交国规则、材料、费用、预约、退件原因 |
| `_chapters/lvxing/mianqian.md` | 6.3 免签与易签国家清单。三张表 + 自助复核方法 |
| `_chapters/lvxing/dingpiao.md` | 6.4 廉航与订票实操。行李、机场、值机、比价、铁路大巴、住宿 |
| `_chapters/lvxing/jingnei.md` | 6.5 英国境内旅行。Advance/Railcard/split ticketing + 目的地 |
| `redirects/jinjie-lvxing.html` | `/jinjie/lvxing/` → `/lvxing/` |
| `_chapters/jinjie/lvxing.md` | **删除**（Task 8） |

---

## 已核实的事实速查（2026-09-08）

**写页面时直接抄这里，不要凭记忆改，也不要再去搜二手清单。** 每条后面括号里是来源。

**申根 / 欧盟边境**

- 申根短期签证费 **€90**（成人）、**€45**（6–11 岁）、6 岁以下免，**自 2024-06-11 起**。Visa Code 规定每三年复核，下次在 2027 年。（欧盟委员会 Migration and Home Affairs）
- 网上大量「2026 年 6 月起涨到 €90」的说法是二手错误，**不要采信**。
- 申根区 **29 个成员国**。保加利亚、罗马尼亚已于 **2025-01-01** 全面加入；**塞浦路斯不在申根区**。
- **EES 自 2026-04-10 起在所有申根区外部边界全面运行**，取代护照盖章，登记姓名、证件信息与生物识别数据（指纹 + 面部图像），自动记录出入境时间并自动计算停留天数。首次入境耗时明显变长。
- **ETIAS 仍未启动且已延期**：欧盟在 2026 年 7 月从官网撤下 Q4 2026 的目标，现在指向 2027 年，具体日期未定。ETIAS 面向**免签国**公民，中国护照持有人赴申根区仍需申根签证，两者不重叠。**旧页写的「预计 2026 年第四季度启动」必须更正。**
- 申根签证要求旅行医疗保险保额 **不低于 €30,000** 且覆盖全程；护照在离开申根区时仍有 **3 个月以上**有效期，且签发不超过 10 年。
- 递交国规则：向**停留时间最长**的国家申请；几国时间相同则向**首个入境**国申请。
- 90/180：任意连续 180 天内累计停留不超过 90 天，滚动计算，入境与离境当天各算一整天。

**中国护照本身免签（互免协定，普通护照，均为不超过 30 日）**

亚洲：泰国（2024-03-01）、新加坡（2024-02-09）、马来西亚（2025-07-17）、阿联酋（2018-01-16）、卡塔尔（2018-12-21）、马尔代夫（2022-05-20）、哈萨克斯坦（2023-11-10）、乌兹别克斯坦（2025-06-01）、阿塞拜疆（2025-07-16）、亚美尼亚（2020-01-19）、格鲁吉亚（2024-05-28）。
欧洲：塞尔维亚（2017-01-15）、阿尔巴尼亚（2023-03-18）、波黑（2018-05-29）、白俄罗斯（2018-08-10）。
美洲：巴巴多斯（2017-06-01）、巴哈马（2014-02-12）、多米尼克（2022-09-19）、格林纳达（2015-06-10）、安提瓜和巴布达（2024-05-11）、苏里南（2021-05-01）。
非洲：塞舌尔（2013-06-26）、毛里求斯（2013-10-31）。
大洋洲：斐济（2015-03-14）、汤加（2016-08-19）、萨摩亚（2025-04-02）、所罗门群岛（2024-12-28）。
（外交部《中外互免签证协定一览表》。**只收录「适用护照种类」明确含「普通护照」的条目**——仅覆盖外交/公务护照的协定不进表，这是二手清单最常见的错误来源。厄瓜多尔在表内但标注「目前暂停执行」，**不要收录**。）

**这份清单是核实过的摘录，不保证穷尽原表。** 页面上必须写明这一点并给出原表链接，让读者能自己去查本表没收的国家——不要把它写成「全部免签国家」。同理，本次核查中拿不到可靠来源的条目（例如圣马力诺）一律不写，宁缺勿错。

**单方面对中国普通护照免签（本页只写下面这几条，都是核实过的）**

- **土耳其**：**自 2026-01-02 起**对以**旅游、过境**为目的的持普通护照中国公民免签，任意 180 天内累计停留不超过 **90 天**。中国驻土耳其使馆提示：护照有效期不少于 6 个月且有空白签证页，备好**纸质**往返机票、酒店订单、行程单、实体信用卡或资金证明。**来土工作、学习不适用**，须另办相应签证。逾期停留会被罚款并可能被禁止入境。（中国驻土耳其大使馆 2026-01-12 温馨提示、新华网）
- **俄罗斯**：中国公民持普通护照免签赴俄，单次停留不超过 **30 天**——但这是**试行**政策，**有效期至 2026-09-14**。是否延长以官方通知为准，**页面必须写明这个到期日**。（中国驻俄使领馆通知、新华网）
- **摩洛哥、突尼斯**：单方面对中国公民免签。
- **韩国济州岛、越南富国岛**：属于「特定地区免签」，不等于全国免签，要写清限定范围。

**凭英国签证 / 居留或申根签证可简化入境（本页只写下面三条）**

- **黑山（Montenegro）**：持申根成员国、澳大利亚、加拿大、爱尔兰、日本、新西兰、英国或美国签发的**有效签证或居留许可**者，可免签停留 **30 天**（不限国籍，签证需在停留期内有效）。对持英国学生签证的中国留学生适用。
- **墨西哥**：持**有效且已使用过的多次入境**英国签证或英国永居，可免办墨西哥签证、停留至 **180 天**，但仍须办 **FMM 入境卡**（2026 年约 983 MXN，商业航班通常已含在票价里）。同样适用于美国、加拿大、日本、智利与申根国签证。**必须如实标注的不确定性**：这条规则是按实体贴纸签证写的，而英国已转 eVisa（无实体卡），实际能否顺利适用有风险——写成「出发前向航空公司与墨西哥使馆各确认一次」，**不要许诺**。
- **北马其顿**：认的是**申根成员国、塞浦路斯或爱尔兰**签发的居留许可，可免签入境、单次不超过 15 天、任意 6 个月内累计不超过 90 天——**不含英国**。把它当成反例写进「常见错误」，提醒读者别照抄网上把英国算进去的清单。

**爱尔兰（要写实，旧页说得太软）**

- BIVS（英爱签证体系）与短期签证豁免计划（Short Stay Visa Waiver Programme）**都只覆盖英国短期访问签证**，**英国学生签证与工作签证不在覆盖范围内**。
- 所以持英国学生签证的中国留学生去爱尔兰，**通常需要单独申请爱尔兰签证**。
- 英国 ETA **不能**用于短期签证豁免计划。
- 共同旅行区（Common Travel Area）主要适用于英爱公民，不是给第三国国民的免签通道。

**核不实的一律不进表。** 直布罗陀、阿鲁巴、秘鲁这几条在本次核查中拿不到可靠来源，**不要写进页面**。

**自助复核的三个来源**（写进 6.3 的复核一节）

1. **IATA Travel Centre** —— 航空公司值机时实际执行的口径，最贴近登机口的现实。
2. **中国领事服务网**（`cs.mfa.gov.cn`）的国别信息与《中外互免签证协定一览表》—— 互免协定的权威来源。注意站上那份《持普通护照中国公民前往有关国家和地区入境便利待遇一览表》**最近一次更新是 2023 年 12 月，已经过期**（比如它还把泰国、马来西亚列为临时性单方面免签，而这两国后来都签了互免协定），**不要拿它当现行清单**。
3. **目的国驻华使馆官网** —— 三者不一致时以目的国官方为准。

---

## Task 1: 安全与应急篇顺延为第七章

把安全篇的章号、`weight`、`order` 与四个专题的编号整体上移，为第六章腾出 weight 700。**必须先做这一步**，否则新增 `lvxing.md`（weight 700）时会有两章抢同一个 weight，排序不确定。

**Files:**
- Modify: `_chapters/anquan.md`（frontmatter `nav`/`order`/`weight`/`num`，正文第 21 行的 6.2 引用）
- Modify: `_chapters/anquan/jinji-dianhua.md`、`tufa-qingkuang.md`、`geren-fangfan.md`、`yingji-bao.md`（frontmatter `nav`/`weight`/`num`，`yingji-bao.md` 正文第 74 行的 6.2 引用）
- Modify: `_chapters/jieyu.md`（`order` 8→9，`weight` 800→850，避免与安全篇新的 800 撞车）
- Modify: `_chapters/chufaqian.md`（第 45 行「第六章」，第 58/125/129 行的 6.4/6.2/6.3）
- Modify: `_chapters/fulu.md`（第 47 行 6.1）
- Modify: `_chapters/gongzuo/zhichang-liyi.md`（第 85 行 6.2）
- Modify: `_chapters/shenghuo/shouji-wangluo.md`（第 41 行 6.1）
- Modify: `_chapters/shenghuo/yinshi-jiankang.md`（第 157 行 6.1）
- Modify: `_chapters/jinjie/shuiwu.md`（第 163 行 6.4）
- Modify: `_chapters/jinjie/lvxing.md`（第 39 行 6.2 —— 这页 Task 8 才删，先一并改掉，免得中间状态里留错编号）
- Modify: `index.md`（第 61 行「第六章 安全与应急篇」→「第七章」）

**Interfaces:**
- Produces: 安全篇占用 `weight` 800–804、`num` "07" 与 7.1–7.4；`weight` 700 空出来给 Task 3 的旅游篇；结语移到 `weight` 850。

- [ ] **Step 1: 写断言——先确认旧编号确实还在**

```bash
cd /home/yfrl/uk-handbook
# 这些命令现在应该有输出（说明旧编号存在），任务做完后应该没有输出
grep -rn '第六章 安全' --include=*.md _chapters index.md README.md
grep -rnE 'num: "6\.[1-4]"' _chapters/anquan
grep -rn 'weight: 70[0-4]' _chapters/anquan
```

- [ ] **Step 2: 跑一遍确认断言此刻「失败」（即旧编号还在）**

预期：三条命令都有输出。`_chapters/anquan.md` 有 `第六章 安全与应急篇`，四个专题页有 `num: "6.1"`–`"6.4"` 与 `weight: 701`–`704`。

- [ ] **Step 3: 改安全篇自身的 frontmatter**

`_chapters/anquan.md`：

```yaml
nav: "第七章 安全与应急篇"
order: 8
weight: 800
num: "07"
```

四个专题页，逐个改 `nav`（编号部分）、`weight`、`num`：

| 文件 | `nav` | `weight` | `num` |
| --- | --- | --- | --- |
| `anquan/jinji-dianhua.md` | `"7.1 紧急联系电话与资源"` | `801` | `"7.1"` |
| `anquan/tufa-qingkuang.md` | `"7.2 常见突发情况与处理步骤"` | `802` | `"7.2"` |
| `anquan/geren-fangfan.md` | `"7.3 个人防范与日常安全"` | `803` | `"7.3"` |
| `anquan/yingji-bao.md` | `"7.4 建立个人应急包"` | `804` | `"7.4"` |

`_chapters/jieyu.md`：`order: 9`、`weight: 850`。

- [ ] **Step 4: 改正文里的编号引用**

**不要用无条件的 `sed -i 's/6\.1/7.1/g'`** —— `6.1`、`6.2` 这类串也可能出现在金额、日期或版本号里。先看上下文再逐处改：

```bash
cd /home/yfrl/uk-handbook
grep -rnE '\b6\.[1-4]\b' --include=*.md _chapters index.md README.md
```

按上面 Files 一节列出的行逐个确认是「指向安全篇专题的链接文字」之后再替换（`6.1 紧急电话` → `7.1 紧急电话`，依此类推）。`index.md` 第 61 行同时把「第六章」改成「第七章」。

`_chapters/anquan.md` 正文里若有「本章四个专题」之类的表述，保持不变（专题数没变）。

- [ ] **Step 5: 跑断言确认通过**

```bash
cd /home/yfrl/uk-handbook
# 全部应该没有输出
grep -rn '第六章 安全' --include=*.md _chapters index.md README.md
grep -rnE 'num: "6\.[1-4]"' _chapters/anquan
grep -rn 'weight: 70[0-4]' _chapters/anquan
grep -rnE '\b6\.[1-4]\b' --include=*.md _chapters index.md README.md
# 应该有输出：新编号已就位
grep -rnE 'num: "7\.[1-4]"' _chapters/anquan
```

最后一条 `grep -rnE '\b6\.[1-4]\b'` 若仍有输出，逐条看是不是误报（例如无关的数字）；确认是无关数字就跳过，是漏改就补。

- [ ] **Step 6: 跑 `VERIFY`**

预期：构建通过、`front matter OK`、`page count OK`。另外肉眼确认排序：

```bash
cd /home/yfrl/uk-handbook
ruby -ryaml -rdate -e '
  Dir.glob("_chapters/**/*.md").map { |f|
    d = YAML.safe_load(File.read(f).split("---",3)[1], permitted_classes: [Date, Time]) rescue nil
    [d && d["weight"] || 9999, d && d["nav"]]
  }.sort.each { |w, n| puts "#{w}\t#{n}" }
'
```

预期顺序：… 600 第五章 / 601–606 进阶篇六个专题 / **800 第七章** / 801–804 安全篇四个专题 / 850 结语 / 900 附录1 / 950 附录2 / 960 关于 / 970 隐私。weight 700 应为空缺。

- [ ] **Step 7: 提交**

```bash
cd /home/yfrl/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Renumber the safety chapter to make room for a travel chapter

Moves 安全与应急篇 from 第六章 to 第七章 (weight 700 to 800, sections 6.x
to 7.x) and shifts 结语 to weight 850, freeing weight 700 for the new
travel chapter. Updates every cross-reference that names a section number.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: 进阶篇余下五个专题编号上移一位

旅行页要从进阶篇搬走，5.1 腾空，所以 5.2–5.6 上移成 5.1–5.5。

**Files:**
- Modify: `_chapters/jinjie/jiazhao.md`、`shuiwu.md`、`youhui-xuesheng.md`、`zhiye-fazhan.md`、`huiguo.md`（frontmatter `nav`/`weight`/`num`，以及各自正文里的自引用与互引用）
- Modify: `_chapters/jinjie.md`（第 21 行 5.6 引用）
- Modify: `_chapters/fulu.md`（第 62/69/84/96 行：5.6/5.3/5.2/5.5）
- Modify: `_chapters/gongzuo.md`（第 16/18/22 行：5.3/5.6/5.5）
- Modify: `_chapters/gongzuo/dagong-zhengce.md`（第 41/169 行 5.6、第 192 行 5.3）
- Modify: `_chapters/gongzuo/jianzhi-leixing.md`（第 29 行 5.3）
- Modify: `_chapters/gongzuo/shixi.md`（第 33/41/123 行 5.5）
- Modify: `_chapters/gongzuo/zhichang-liyi.md`（第 100 行 5.3）
- Modify: `_chapters/shejiao/fang-zhapian.md`（第 156 行 5.4）
- Modify: `_chapters/shenghuo.md`（第 20 行 5.4）
- Modify: `_chapters/shenghuo/jiaotong.md`（第 66 行 5.2）
- Modify: `_chapters/shenghuo/yinhang-licai.md`（第 219 行 5.3）
- Modify: `_chapters/shenghuo/zufang.md`（第 207 行 5.4）
- Modify: `_chapters/xueye/gaodeng-jiaoyu.md`（第 35 行 5.5）

**Interfaces:**
- Consumes: Task 1 已腾空 weight 700 并把安全篇挪到 800。
- Produces: 进阶篇占用 `weight` 601–605、`num` 5.1–5.5；`weight` 606 与 `num` 5.6 不再存在。

- [ ] **Step 1: 写断言**

```bash
cd /home/yfrl/uk-handbook
# 现在应有输出，做完后应无输出
grep -rn 'num: "5.6"' _chapters
grep -rn 'weight: 606' _chapters
```

- [ ] **Step 2: 跑断言，确认旧编号还在**

预期：`_chapters/jinjie/huiguo.md` 命中 `num: "5.6"` 与 `weight: 606`。

- [ ] **Step 3: 改五个专题页的 frontmatter**

**按升序逐个改**（目标编号都已腾空，不会撞车）：

| 文件 | `nav` | `weight` | `num` |
| --- | --- | --- | --- |
| `jinjie/jiazhao.md` | `"5.1 在英国申请驾照"` | `601` | `"5.1"` |
| `jinjie/shuiwu.md` | `"5.2 学生税务规划"` | `602` | `"5.2"` |
| `jinjie/youhui-xuesheng.md` | `"5.3 最大化利用学生身份优惠"` | `603` | `"5.3"` |
| `jinjie/zhiye-fazhan.md` | `"5.4 提前布局职业发展"` | `604` | `"5.4"` |
| `jinjie/huiguo.md` | `"5.5 回国发展与离境准备"` | `605` | `"5.5"` |

- [ ] **Step 4: 改全库的 5.x 引用**

同样**不要盲 sed**。先列出全部命中：

```bash
cd /home/yfrl/uk-handbook
grep -rnE '\b5\.[1-6]\b' --include=*.md _chapters index.md README.md
```

映射关系（**从 5.2 开始按升序替换**，这样不会把刚改好的又改一遍）：

```
5.2 驾照        → 5.1
5.3 税务        → 5.2
5.4 学生优惠    → 5.3
5.5 职业发展    → 5.4
5.6 回国发展    → 5.5
```

逐处确认上下文是「指向进阶篇专题的链接文字」再改。注意 `_chapters/jinjie/huiguo.md` 与 `shuiwu.md` 正文里有指向同章其他专题的互引用，也要一起改。**原来的 5.1（旅行）引用只在 `index.md:60`，那一处留给 Task 3 处理，本任务不动。**

- [ ] **Step 5: 跑断言确认通过**

```bash
cd /home/yfrl/uk-handbook
# 应无输出
grep -rn 'num: "5.6"' _chapters
grep -rn 'weight: 606' _chapters
grep -rnE '\b5\.6\b' --include=*.md _chapters index.md README.md
# 应有输出
grep -rn 'num: "5.5"' _chapters/jinjie/huiguo.md
```

- [ ] **Step 6: 跑 `VERIFY`，并再跑一次 Step 6 的 weight 排序脚本**

预期：600 第五章 / 601–605 五个专题 / 700 空缺 / 800 第七章 / …

- [ ] **Step 7: 提交**

```bash
cd /home/yfrl/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Shift the remaining 生活进阶篇 sections up one number

The travel page moves out of 生活进阶篇 into its own chapter, so 5.2-5.6
become 5.1-5.5. Updates every cross-reference that names one of them.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: 新建第六章章目录页、重定向与站点导航

建 hub 页、旧 URL 重定向，并把首页目录、进阶篇章首语、README 都改到新结构。此时 hub 还没有子页，`chapter-hub` 布局会跳过「本章包含 N 个专题」那一块，构建正常。

**Files:**
- Create: `_chapters/lvxing.md`
- Create: `redirects/jinjie-lvxing.html`
- Modify: `index.md`（第 60 行：进阶篇的旅行链接移出；新增第六章一行）
- Modify: `_chapters/jinjie.md`（章首语删掉讲旅行的部分，专题数 6→5，`description` 去掉旅行）
- Modify: `README.md`（顶部方面列表与章数、目录表）

**Interfaces:**
- Consumes: Task 1 腾空的 weight 700。
- Produces: `key: lvxing` 供 5 个专题页的 `parent:` 引用；`/lvxing/` URL；`weight` 701–705 留给 Task 4–8。

- [ ] **Step 1: 写断言**

```bash
cd /home/yfrl/uk-handbook
# 现在应无输出，做完后应有输出
test -f _chapters/lvxing.md && echo "hub exists"
test -f _site/lvxing/index.html && echo "hub built"
test -f _site/jinjie/lvxing/index.html && echo "redirect built"
```

- [ ] **Step 2: 跑断言，确认三个都还不存在**

`_site/jinjie/lvxing/index.html` 此刻**是存在的**（旧页还在），这一条要到 Task 8 删掉旧页、重定向接管之后才有意义——本步骤只确认 `_chapters/lvxing.md` 与 `_site/lvxing/index.html` 不存在。

- [ ] **Step 3: 建 `_chapters/lvxing.md`**

```markdown
---
layout: chapter-hub
title: "从英国出发的旅行：申根签证、免签国家与省钱订票"
description: "从英国出发的旅行完整指南：目的地要办什么签证的判断路径、从英国申请申根签证的全流程与费用、中国护照免签与凭英国签证可简化入境的国家清单、廉航行李与机场的隐性成本，以及英国境内的省钱订票方法。"
nav: "第六章 旅游篇"
key: lvxing
permalink: /lvxing/
order: 7
weight: 700
updated: 2026-09-08
num: "06"
---
```

正文（约 300–400 字）要点，按现有章首语的写法组织：

- 英国的地理位置确实适合探索欧洲，但「便宜」是有条件的——签证、行李、机场往返这三项最容易把省下的钱赔回去。
- 先看学业日历再看机票：英国的假期常紧跟 deadline，圣诞假之后往往就是考试或论文提交。
- 两条时效性提醒，用 `.callout .callout-warning` 包一个：**EES 自 2026-04-10 起全面运行**，首次入境要多留时间；**ETIAS 已延期到 2027 年、日期未定**，但中国护照持有人本来就需要申根签证，与 ETIAS 不重叠。
- 一句话指路：不确定目的地要办什么，先看 [6.1 出行规划与签证总览]；只想搞清申根，直接去 [6.2]；想找不用办申根的地方，看 [6.3]。链接用 `{{ '/lvxing/guihua/' | relative_url }}` 的写法。

- [ ] **Step 4: 建 `redirects/jinjie-lvxing.html`**

照抄 `redirects/06-anquan.html` 的结构，只换 permalink 与目标：

```html
---
permalink: /jinjie/lvxing/
sitemap: false
---
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>已移动到 {{ '/lvxing/' | absolute_url }}</title>
  <link rel="canonical" href="{{ '/lvxing/' | absolute_url }}">
  <meta name="robots" content="noindex, follow">
  <meta http-equiv="refresh" content="0; url={{ '/lvxing/' | relative_url }}">
</head>
<body>
  <p>本页已移至 <a href="{{ '/lvxing/' | relative_url }}">{{ '/lvxing/' | absolute_url }}</a>，正在跳转……</p>
</body>
</html>
```

> **注意：** 此刻 `_chapters/jinjie/lvxing.md` 还在，它的 `permalink` 由 collection 的 `/:path/` 规则生成同一个 `/jinjie/lvxing/`，会和这个 redirect 撞车。Jekyll 遇到重复 URL 会告警但仍会构建，产物里保留其中一个。**这是预期的中间状态**，Task 8 删掉旧页后即解除。若构建直接报错而非告警，就把本步骤挪到 Task 8 一起做。

- [ ] **Step 5: 改 `index.md` 的目录列表**

第 60 行现在是：

```markdown
- **[第五章 生活进阶篇]({{ '/jinjie/' | relative_url }})** —— [假期欧洲旅行]({{ '/jinjie/lvxing/' | relative_url }})、[考驾照]({{ '/jinjie/jiazhao/' | relative_url }})、[税务与退税]({{ '/jinjie/shuiwu/' | relative_url }})、[学生优惠]({{ '/jinjie/youhui-xuesheng/' | relative_url }})、[毕业后职业规划]({{ '/jinjie/zhiye-fazhan/' | relative_url }})、[回国发展]({{ '/jinjie/huiguo/' | relative_url }})
```

改成两行（进阶篇去掉旅行，新增旅游篇）：

```markdown
- **[第五章 生活进阶篇]({{ '/jinjie/' | relative_url }})** —— [考驾照]({{ '/jinjie/jiazhao/' | relative_url }})、[税务与退税]({{ '/jinjie/shuiwu/' | relative_url }})、[学生优惠]({{ '/jinjie/youhui-xuesheng/' | relative_url }})、[毕业后职业规划]({{ '/jinjie/zhiye-fazhan/' | relative_url }})、[回国发展]({{ '/jinjie/huiguo/' | relative_url }})
- **[第六章 旅游篇]({{ '/lvxing/' | relative_url }})** —— [出行规划与签证总览]({{ '/lvxing/guihua/' | relative_url }})、[申根签证全流程]({{ '/lvxing/shengen/' | relative_url }})、[免签与易签国家清单]({{ '/lvxing/mianqian/' | relative_url }})、[廉航与订票]({{ '/lvxing/dingpiao/' | relative_url }})、[英国境内旅行]({{ '/lvxing/jingnei/' | relative_url }})
```

（第 61 行的第七章安全篇在 Task 1 已改好。）

- [ ] **Step 6: 改 `_chapters/jinjie.md`**

- `description`：删掉「假期欧洲旅行与申根签证、」，其余不动。
- 正文「六个专题里有两项建议**尽早办**」→「五个专题」。
- 正文倒数第二段里讲旅行的那句（「至于旅行，英国的位置确实适合探索欧洲，但订票前记得先看一遍课程的评估时间表——英国的假期常紧跟 deadline」）删掉，改成一句指路：旅行相关的内容已独立成 [第六章 旅游篇]({{ '/lvxing/' | relative_url }})。

- [ ] **Step 7: 改 `README.md`**

- 第 3 行：方面列表加「旅游」，`共 6 章` → `共 7 章`。
- 目录表：进阶篇专题数 `6（国际旅行、驾照、…）` → `5（驾照、税务、学生优惠、职业发展、回国发展）`；在它下面插入一行 `| 第六章 旅游篇 | /lvxing/ | 5（出行规划与签证总览、申根签证、免签与易签国家、廉航与订票、英国境内旅行） |`；安全篇那行 `第六章` → `第七章`。

- [ ] **Step 8: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -5   # 注意有没有 URL 冲突告警
test -f _site/lvxing/index.html && echo "hub built"
grep -rn "jinjie/lvxing" --include=*.md index.md _chapters   # 应无输出
```

再跑完整 `VERIFY`。

- [ ] **Step 9: 提交**

```bash
cd /home/yfrl/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add the travel chapter hub and point navigation at it

Creates 第六章 旅游篇 at /lvxing/ with a redirect from the old
/jinjie/lvxing/ URL, and updates the home page index, the 生活进阶篇
opener and the README table of contents.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: 6.1 出行规划与签证总览

本章的入口页，回答「我想去 X，要办什么」。

**Files:**
- Create: `_chapters/lvxing/guihua.md`

**Interfaces:**
- Consumes: Task 3 建的 `key: lvxing`。
- Produces: `/lvxing/guihua/`，供其余四页与首页反向链接。

- [ ] **Step 1: 写断言**

```bash
cd /home/yfrl/uk-handbook
test -f _site/lvxing/guihua/index.html && echo "6.1 built"
```

- [ ] **Step 2: 跑断言，确认还不存在**

- [ ] **Step 3: 写 frontmatter**

```yaml
---
layout: section
title: "从英国出发怎么规划旅行：签证判断路径、护照有效期与 90/180 规则"
description: "从英国出发旅行的第一页：按目的地判断要办申根签证、单办目的国签证还是免签直接走，护照有效期的两套标准，90/180 规则的滚动算法，2026 年 4 月起全面运行的 EES 对过关的影响，ETIAS 的最新时间表，以及别和 deadline 撞车的行程安排。"
nav: "6.1 出行规划与签证总览"
parent: lvxing
weight: 701
updated: 2026-09-08
num: "6.1"
toc:
  - title: "先判断：目的地要办什么"
    anchor: "sec-1"
  - title: "护照有效期的两套标准"
    anchor: "sec-2"
  - title: "90/180 规则怎么算"
    anchor: "sec-3"
  - title: "过关会遇到什么：EES 与 ETIAS"
    anchor: "sec-4"
  - title: "旅行保险"
    anchor: "sec-5"
  - title: "订票前先看学业日历"
    anchor: "sec-6"
  - title: "常见问题"
    anchor: "faq"
---
```

- [ ] **Step 4: 写正文六节**

**sec-1 先判断：目的地要办什么** —— 一张内联 SVG 判断路径图，包在 `.figure > .figure-scroll` 里，带 `<title>`/`<desc>`。四条分支：申根区 29 国 → 办申根签证（去 6.2）；欧盟内非申根的塞浦路斯与英国以外的其他国家 → 单办目的国签证；中国护照本身免签 → 直接走（去 6.3）；凭英国签证或居留可简化入境 → 条件核实后走（去 6.3）。图下面用一段文字复述同样的判断顺序，供读屏与不看图的读者。

**sec-2 护照有效期的两套标准** —— 申根：离开申根区时仍有 3 个月以上有效期，且签发不超过 10 年。多数其他目的地：离境时仍有 6 个月以上。结论按 6 个月准备。护照快到期时优先处理续签，补办周期可能打乱整个假期，链到 [7.2 常见突发情况与处理步骤]。

**sec-3 90/180 规则怎么算** —— 任意连续 180 天内累计不超过 90 天；滚动计算，不按自然年也不按次数重置；每次入境往前回看 180 天累加；入境与离境当天各算一整天。频繁短途往返的人要自己记账，欧盟官网有官方计算器。

**sec-4 过关会遇到什么：EES 与 ETIAS** —— 从旧页迁移，**ETIAS 那段按「已核实的事实速查」更正**。EES 自 2026-04-10 全面运行的三点实际影响（首次入境明显变长、之后主要是核验、停留天数由系统自动精确计算）；ETIAS 面向免签国公民、已延期至 2027 年且日期未定、与中国护照持有人不重叠。

**sec-5 旅行保险** —— 申根要求保额不低于 €30,000 且覆盖全程；比价渠道 Compare the Market、MoneySuperMarket；提醒学校或银行账户可能已附带旅行险，先查再买。

**sec-6 订票前先看学业日历** —— 用 `.callout .callout-warning`：英国的假期常紧跟 deadline，圣诞假之后往往就是考试或论文提交，复活节同理；订票前把课程评估时间表过一遍。链到 [2.6 毕业论文] 与 [2.5 考试与 Presentation] 的实际编号（学业篇编号本次未改动，照现有的写）。

- [ ] **Step 5: 写 `faq`（4–5 条）**

从旧页迁移并改写，至少覆盖：90/180 到底怎么算；EES 换新系统对我有什么影响；ETIAS 我要不要办（答：中国护照持有人不需要，且它已延期到 2027 年）；护照有效期要留多久；什么时候订票最合适。

**写 faq 时注意 Global Constraints 里的 YAML 陷阱**：`a:` 的值用双引号包裹时，里面要引号只能用「」。

- [ ] **Step 6: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
test -f _site/lvxing/guihua/index.html && echo "6.1 built"
# frontmatter 没被静默丢掉：faq 与 toc 应该渲染出来了
grep -c 'faq' _site/lvxing/guihua/index.html
grep -c 'sec-4' _site/lvxing/guihua/index.html
```

再跑完整 `VERIFY`。

- [ ] **Step 7: 提交**

```bash
cd /home/yfrl/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add 6.1 trip planning and visa overview

Opens the travel chapter with a decision path from destination to what you
have to apply for, the two passport-validity standards, how the rolling
90/180 rule is counted, and the current EES and ETIAS position.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: 6.2 申根签证全流程

**Files:**
- Create: `_chapters/lvxing/shengen.md`

**Interfaces:**
- Produces: `/lvxing/shengen/`。

- [ ] **Step 1: 写断言**

```bash
cd /home/yfrl/uk-handbook
test -f _site/lvxing/shengen/index.html && echo "6.2 built"
```

- [ ] **Step 2: 跑断言，确认还不存在**

- [ ] **Step 3: 写 frontmatter**

```yaml
---
layout: section
title: "从英国申请申根签证：向哪国递交、材料清单与常见退件原因"
description: "在英国读书期间申请申根签证的完整流程：向哪个国家递交的规则、用 eVisa share code 作英国居留证明、完整材料清单、€90 签证费与 VFS 服务费、旺季预约提前量、审理时长，以及最常见的退件与拒签原因。"
nav: "6.2 申根签证全流程"
parent: lvxing
weight: 702
updated: 2026-09-08
num: "6.2"
toc:
  - title: "申根区包括哪些国家"
    anchor: "sec-1"
  - title: "第一步：确定向哪个国家递交"
    anchor: "sec-2"
  - title: "材料清单"
    anchor: "sec-3"
  - title: "费用与预约"
    anchor: "sec-4"
  - title: "常见退件与拒签原因"
    anchor: "sec-5"
  - title: "争取多次入境签"
    anchor: "sec-6"
  - title: "常见问题"
    anchor: "faq"
---
```

- [ ] **Step 4: 写正文六节**

**sec-1 申根区包括哪些国家** —— 29 个成员国；保加利亚与罗马尼亚已于 2025-01-01 全面加入；**塞浦路斯不在申根区**，去塞浦路斯要单独办（并说明持双次/多次入境有效申根签证或申根国居留许可可免签入境塞浦路斯，但**英国签证不算**）。英国已不在申根区，所以要单独办。

**sec-2 第一步：确定向哪个国家递交** —— 向停留时间最长的国家申请；几国时间相同则向首个入境国申请。用 `.callout .callout-warning` 强调：递交错国家是常见退件原因，而且这一步错了后面材料再全也没用。

**sec-3 材料清单** —— 用列表逐项写，每项后面加一句「为什么会卡在这」：有效护照（离开申根区时仍有 3 个月以上、签发不超过 10 年）；**英国合法居留证明 = eVisa，用 UKVI 账户生成 share code**（明确写 2024 年底前发放的 BRP 卡已停用）；在读证明（学校开的 Student Status Letter）；近 3–6 个月银行流水（要能覆盖行程开销）；往返机票与住宿预订（先订可免费取消的）；旅行医疗保险，保额不低于 €30,000 且覆盖整个行程。

**sec-4 费用与预约** —— 签证费 €90（成人）/ €45（6–11 岁）/ 6 岁以下免，**自 2024-06-11 起**，另加 VFS Global 等外包机构的服务费与可选的加急、快递、代填费。提醒：Visa Code 每三年复核费用，下次在 2027 年，以官方为准。预约：圣诞与复活节前名额极紧，行程建议提前一到两个月开始办。

**sec-5 常见退件与拒签原因** —— 递交国选错；流水覆盖不了行程开销；保险保额不足或覆盖期短于行程；行程单与机票住宿预订不一致；居留证明用了已停用的 BRP；护照有效期不满足 3 个月余量。

**sec-6 争取多次入境签** —— 多次入境签（multi-entry / LTV）对一年里要去几次欧洲的人价值很大；良好的申根出入境记录会提高获批概率；申请时把后续行程计划说清楚。

- [ ] **Step 5: 写 `faq`（4–5 条）**

覆盖：申根签证要向哪个国家申请；英国居留证明现在要交什么（eVisa share code，不是 BRP）；一共要花多少钱；什么时候开始约；被拒签了怎么办（看拒签信的理由代码、可申诉或补齐材料重递，不要立刻换国家重复递交）。

- [ ] **Step 6: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
test -f _site/lvxing/shengen/index.html && echo "6.2 built"
grep -c 'faq' _site/lvxing/shengen/index.html
# 不应写回 BRP 作为现行证明
grep -n 'BRP' _site/lvxing/shengen/index.html
```

最后一条应只在「BRP 已停用」这样的否定语境里出现。再跑完整 `VERIFY`。

- [ ] **Step 7: 提交**

```bash
cd /home/yfrl/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add 6.2 the full Schengen visa process

Covers which country to apply to, the eVisa share code that replaced the
BRP as proof of UK residence, the full document list, the EUR 90 fee and
VFS service charges, and the reasons applications actually come back.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: 6.3 免签与易签国家清单

本章最核心的新内容，也是全站最容易过期的一页。**三张表的内容一律从本计划「已核实的事实速查」抄，不要另找二手清单补充。**

**Files:**
- Create: `_chapters/lvxing/mianqian.md`

**Interfaces:**
- Produces: `/lvxing/mianqian/`。

- [ ] **Step 1: 写断言**

```bash
cd /home/yfrl/uk-handbook
test -f _site/lvxing/mianqian/index.html && echo "6.3 built"
```

- [ ] **Step 2: 跑断言，确认还不存在**

- [ ] **Step 3: 写 frontmatter**

```yaml
---
layout: section
title: "中国护照免签国家与凭英国签证可简化入境的地方"
description: "从英国出发不用办申根签证也能去的地方：与中国互免签证协定的国家清单（普通护照，30 日）、单方面对中国免签的土耳其与俄罗斯的最新条件、持英国签证或居留可免签入境的黑山与墨西哥，以及爱尔兰为什么对留学生并不免签、出发前怎么自己复核。"
nav: "6.3 免签与易签国家清单"
parent: lvxing
weight: 703
updated: 2026-09-08
num: "6.3"
toc:
  - title: "先说清楚：这页怎么用"
    anchor: "sec-1"
  - title: "一、中国护照本身免签（互免协定）"
    anchor: "sec-2"
  - title: "二、单方面对中国免签"
    anchor: "sec-3"
  - title: "三、凭英国签证或居留可简化入境"
    anchor: "sec-4"
  - title: "爱尔兰：留学生最常搞错的一个"
    anchor: "sec-5"
  - title: "出发前怎么自己复核"
    anchor: "sec-6"
  - title: "常见问题"
    anchor: "faq"
---
```

- [ ] **Step 4: 写 sec-1，页首的时效性声明**

页面开头先放一条 `.callout .callout-warning`，写明：本页三张表是 **2026 年 9 月 8 日**的快照；签证政策随时变，且**变更往往不预告**；出发前必须按 sec-6 的方法自己复核一遍，尤其是已经买了不可退机票之前。

再用一段话说清三类的区别：第一类看的是**你的护照**，第二类看的是**目的国单方面给的政策**（最不稳定），第三类看的是**你手上的英国签证或居留**。三类的适用条件完全不同，别混着用。

- [ ] **Step 5: 写 sec-2，互免协定表**

按洲分组的表格，三列：**国家 / 停留期限 / 协定生效日期**。停留期限一栏统一写「不超过 30 日」。条目照抄「已核实的事实速查」里的互免协定清单（亚洲 11 国、欧洲 4 国、美洲 6 国、非洲 2 国、大洋洲 4 国）。

表头上方一行小字：抄录自外交部《中外互免签证协定一览表》，抄录日期 2026-09-08，只收录「适用护照种类」明确含「普通护照」的条目。

表下面三条提醒：

- 免签入境**不等于**可长期停留或居住，协定一般限 30 日以内；
- 表里不含只覆盖外交、公务护照的协定——网上很多清单把这些也算进去，这是最常见的错误来源；
- 厄瓜多尔虽在原表内但标注「目前暂停执行」，本表未收录。

- [ ] **Step 6: 写 sec-3，单方面免签**

不做大表，逐条写，每条把条件写全：

- **土耳其**（重点，最值得写细）：自 2026-01-02 起对以**旅游、过境**为目的的持普通护照中国公民免签，任意 180 天内累计不超过 90 天。中国驻土耳其使馆提示：护照有效期不少于 6 个月且有空白签证页，备好**纸质**往返机票、酒店订单、行程单、实体信用卡或资金证明。**来土工作或学习不适用**，须另办签证。逾期停留会被罚款并可能被禁止入境。
- **俄罗斯**：持普通护照免签、单次不超过 30 天，但这是**试行**政策，**有效期至 2026-09-14**——用 `.callout .callout-warning` 单独框出来，写明是否延长以中国驻俄使领馆通知为准，订票前务必先查。
- **摩洛哥、突尼斯**：单方面对中国公民免签。
- **韩国济州岛、越南富国岛**：只对**特定地区**免签，不等于全国免签；离开该地区仍需签证。

- [ ] **Step 7: 写 sec-4，凭英国签证或居留简化入境**

表格三列：**国家 / 条件 / 停留期限**，只三行，条件写足：

- **黑山**：持申根成员国、澳、加、爱尔兰、日、新西兰、英国或美国签发的有效签证或居留许可（须在停留期内有效）→ 免签 30 天。规则不限国籍，持英国学生签证的中国留学生适用。
- **墨西哥**：持有效且**已使用过的多次入境**英国签证或英国永居 → 免签停留至 180 天，但仍须办 **FMM 入境卡**（2026 年约 983 MXN，商业航班通常已含在票价里）。同样适用于美、加、日、智利与申根国签证。
- **北马其顿**：**反例**。它认的是申根成员国、塞浦路斯或爱尔兰签发的居留许可（单次不超过 15 天、任意 6 个月内累计不超过 90 天），**不含英国**。

表后面必须写的两段：

1. `.callout .callout-warning`：**墨西哥这条有实务风险。** 规则是按实体贴纸签证写的，而英国已全面转向 eVisa（没有实体卡可出示）。出发前向**航空公司**（值机时按 IATA 口径拦人的是他们）与**墨西哥驻英使馆**各确认一次，不要只凭本页或网上帖子就买不可退机票。
2. 一段关于「网上清单为什么经常错」的提醒，用北马其顿当例子：很多中文清单把「申根/爱尔兰居留许可」笼统写成「欧洲居留」并把英国算进去，照抄会在登机口被拦。

- [ ] **Step 8: 写 sec-5，爱尔兰**

单开一节，因为这是留学生问得最多、也最容易被误导的一个。

- BIVS（英爱签证体系）与短期签证豁免计划**都只覆盖英国短期访问签证**，**英国学生签证与工作签证不在覆盖范围内**。
- 结论：持英国学生签证的中国留学生去爱尔兰，**通常需要单独申请爱尔兰签证**，要留出办理时间。
- 共同旅行区（Common Travel Area）主要适用于英爱公民，不是给第三国国民的免签通道。
- 英国 ETA 不能用于短期签证豁免计划。
- 好消息：有良好签证记录（持有过英国、申根、美、加、澳、新西兰签证并守规）的申请人，可能符合爱尔兰五年多次入境短期签证的条件，值得一问。

- [ ] **Step 9: 写 sec-6，自助复核方法**

按「已核实的事实速查」末尾那三个来源写，讲清各自的用途与顺序：IATA Travel Centre（航空公司实际执行的口径，最贴近登机口现实）→ 中国领事服务网的国别信息与《中外互免签证协定一览表》（互免协定的权威来源）→ 目的国驻华使馆官网（三者不一致时以它为准）。

**必须写进去的一条**：中国领事服务网上那份《持普通护照中国公民前往有关国家和地区入境便利待遇一览表》最近一次更新是 **2023 年 12 月，已经过期**——它还把泰国、马来西亚列为临时性单方面免签，而这两国后来都签了互免协定。**别拿它当现行清单**，要用同站的《中外互免签证协定一览表》。

- [ ] **Step 10: 写 `faq`（5 条）**

覆盖：免签是不是就可以随便待多久（不是，协定一般限 30 日，且免签入境不等于可居住/打工）；持英国学生签证去爱尔兰要不要签证（要，BIVS 与豁免计划都不覆盖学生签证）；土耳其免签能不能用来短期上语言课（不能，免签只限旅游过境）；墨西哥那条到底靠不靠谱（写清 eVisa 的不确定性与双重确认的做法）；网上的免签清单为什么互相矛盾（三类政策混写、把外交公务护照协定算进普通护照、把英国算进申根居留）。

- [ ] **Step 11: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
test -f _site/lvxing/mianqian/index.html && echo "6.3 built"
grep -c 'faq' _site/lvxing/mianqian/index.html
# 快照日期与俄罗斯到期日必须在页面上
grep -c '2026-09-08\|2026 年 9 月 8 日' _site/lvxing/mianqian/index.html
grep -c '2026-09-14\|2026 年 9 月 14 日' _site/lvxing/mianqian/index.html
# 没有把核不实的条目写进去
grep -n '直布罗陀\|阿鲁巴\|秘鲁' _site/lvxing/mianqian/index.html
```

最后一条应无输出。再跑完整 `VERIFY`。

- [ ] **Step 12: 提交**

```bash
cd /home/yfrl/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add 6.3 visa-free and simplified-entry destinations

Three separate lists — mutual visa-exemption agreements, unilateral
visa-free policies, and entry on the strength of a UK visa — each with its
conditions spelled out, plus why Ireland is not visa-free for students and
how to re-check any of it before booking.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: 6.4 廉航与订票实操

**Files:**
- Create: `_chapters/lvxing/dingpiao.md`

**Interfaces:**
- Produces: `/lvxing/dingpiao/`。

- [ ] **Step 1: 写断言**

```bash
cd /home/yfrl/uk-handbook
test -f _site/lvxing/dingpiao/index.html && echo "6.4 built"
```

- [ ] **Step 2: 跑断言，确认还不存在**

- [ ] **Step 3: 写 frontmatter**

```yaml
---
layout: section
title: "廉航与订票实操：行李、机场位置与住宿怎么不把省下的钱赔回去"
description: "从英国飞欧洲的订票实操：廉航行李尺寸与提前买额度、Stansted 与 Luton 这类机场往返市区的隐性成本、强制在线值机、比价工具怎么用、欧洲境内铁路与长途大巴的替代方案，以及可免费取消的住宿预订。"
nav: "6.4 廉航与订票实操"
parent: lvxing
weight: 704
updated: 2026-09-08
num: "6.4"
toc:
  - title: "行李是主要成本"
    anchor: "sec-1"
  - title: "机场位置的隐性成本"
    anchor: "sec-2"
  - title: "在线值机与其他容易被收费的环节"
    anchor: "sec-3"
  - title: "比价工具怎么用"
    anchor: "sec-4"
  - title: "欧洲境内的铁路与大巴"
    anchor: "sec-5"
  - title: "住宿"
    anchor: "sec-6"
  - title: "常见问题"
    anchor: "faq"
---
```

- [ ] **Step 4: 写正文六节**

从旧页迁移并扩写。

**sec-1 行李是主要成本** —— Ryanair、Wizz Air 的随身尺寸限制严格且执行到位；机场补票远贵于线上提前买额度；出发前用尺子量一遍，别信「我上次就这么过了」。

**sec-2 机场位置的隐性成本** —— Stansted、Luton、Gatwick 到伦敦市区要额外一到两小时和一笔车费；比价时把这部分算进总价再和别的航班比，结论常常和票面价不一样。同样适用于目的地一侧的「城市名 + 远郊机场」。

**sec-3 在线值机与其他容易被收费的环节** —— 部分廉航强制线上值机、机场补办收费；选座、优先登机、改名、纸质登机牌各有收费项；付款方式与货币转换也可能加价。

**sec-4 比价工具怎么用** —— Skyscanner、Google Flights、Kayak；用「整月」视图找便宜日期；比完价回航司官网订，出问题时改退更好办。

**sec-5 欧洲境内的铁路与大巴** —— 短途（两三小时以内）算上安检与机场往返，火车常常更快也不贵；长途大巴最便宜但耗时；夜车适合预算优先的行程。

**sec-6 住宿** —— Booking.com（可免费取消，适合签证材料还没下来时先占位）、Airbnb（多人拼住）、Hostelworld（背包客）。提醒：申根签证要交住宿预订，先订可免费取消的。

链到 [6.5 英国境内旅行] 讲英国国内那一段，链到 [6.2 申根签证全流程] 讲预订与签证的先后顺序。

- [ ] **Step 5: 写 `faq`（3–4 条）**

覆盖：廉航怎么才能真的省到钱（行李、机场位置、在线值机三项加进总价再比）；行李超了在机场补要多少（写量级并注明以官网为准）；机票和签证哪个先办（订可免费取消的住宿与机票用于递签，签证下来再确认）；从伦敦哪个机场出发划算。

- [ ] **Step 6: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -3
test -f _site/lvxing/dingpiao/index.html && echo "6.4 built"
grep -c 'faq' _site/lvxing/dingpiao/index.html
```

再跑完整 `VERIFY`。

- [ ] **Step 7: 提交**

```bash
cd /home/yfrl/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add 6.4 budget airline and booking practicalities

The three places a cheap fare stops being cheap — baggage, airport
location and forced online check-in — plus how to use the comparison
sites, when rail or coach beats flying, and freely cancellable bookings.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: 6.5 英国境内旅行，并删除旧的旅行页

最后一个内容任务。写完 6.5 就把 `_chapters/jinjie/lvxing.md` 删掉，让 Task 3 建的重定向接管旧 URL。

**Files:**
- Create: `_chapters/lvxing/jingnei.md`
- Delete: `_chapters/jinjie/lvxing.md`

**Interfaces:**
- Consumes: Task 3 建的 `redirects/jinjie-lvxing.html`。
- Produces: `/lvxing/jingnei/`；`/jinjie/lvxing/` 由重定向页独占。

- [ ] **Step 1: 写断言**

```bash
cd /home/yfrl/uk-handbook
test -f _site/lvxing/jingnei/index.html && echo "6.5 built"
# 旧页删掉后，这个 URL 应该是重定向页（含 http-equiv refresh），而不是原来的旅行正文
grep -q 'http-equiv="refresh"' _site/jinjie/lvxing/index.html && echo "redirect took over"
```

- [ ] **Step 2: 跑断言，确认两条都还不成立**

此刻 `_site/jinjie/lvxing/index.html` 里应该还是旧旅行页的正文（或与重定向页撞车后的其中一个）。

- [ ] **Step 3: 写 frontmatter**

```yaml
---
layout: section
title: "英国境内旅行：Advance 票、Railcard 叠加与 split ticketing"
description: "英国境内假期出行怎么省：Advance 票的提前量、16-25 与 26-30 Railcard 与 Advance 叠加、split ticketing 拆票、长途大巴的取舍，以及苏格兰高地、湖区、北威尔士与康沃尔的季节、交通和成本量级。"
nav: "6.5 英国境内旅行"
parent: lvxing
weight: 705
updated: 2026-09-08
num: "6.5"
toc:
  - title: "火车票怎么买便宜"
    anchor: "sec-1"
  - title: "长途大巴的取舍"
    anchor: "sec-2"
  - title: "几个值得去的地方"
    anchor: "sec-3"
  - title: "常见问题"
    anchor: "faq"
---
```

- [ ] **Step 4: 写正文三节**

**sec-1 火车票怎么买便宜** —— Advance 票提前订通常比当天买便宜一半以上，但绑定车次、改退受限；16-25 / 26-30 Railcard 可与 Advance 叠加（Railcard 怎么办、划不划算见 [1.3 日常出行与交通]，不在这里重复）；split ticketing 把一段行程拆成几张票，部分线路能显著便宜，有专门的比价网站；团体票与往返票的适用场景。

**sec-2 长途大巴的取舍** —— National Express、Megabus 比火车慢但便宜很多；夜班车适合预算优先的行程，但要算上到站时间太早无处可去的成本。

**sec-3 几个值得去的地方** —— 苏格兰高地、湖区、北威尔士、康沃尔各一小段：适合的季节、怎么到、大致成本量级、以及为什么算上机场往返时间之后性价比常常高于飞欧洲。价格只写量级并注明以官网为准（README 的年度复核表约定）。

用 `.callout .callout-tip` 收一句：假期头尾两天的票价最贵，错开一两天常常能省一半。

- [ ] **Step 5: 写 `faq`（3 条）**

覆盖：Railcard 值不值得买；split ticketing 合法吗（合法，铁路条款允许，只要途中各站列车都停靠）；英国国内玩还是飞欧洲划算。

- [ ] **Step 6: 删掉旧的旅行页**

```bash
cd /home/yfrl/uk-handbook
git rm _chapters/jinjie/lvxing.md
```

删之前先确认它的内容都已经落到 6.1–6.5：出行步骤 → 6.1 与 6.4；申根材料 → 6.2；不需要申根签证的地方 → 6.3；廉航实操 → 6.4；EES/ETIAS → 6.1；英国境内出行省钱 → 6.5；八条 FAQ → 分散到五页的 `faq`。

- [ ] **Step 7: 跑断言与 `VERIFY`**

```bash
cd /home/yfrl/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -5   # 不应再有 URL 冲突告警
test -f _site/lvxing/jingnei/index.html && echo "6.5 built"
grep -q 'http-equiv="refresh"' _site/jinjie/lvxing/index.html && echo "redirect took over"
grep -q 'lvxing' _site/jinjie/lvxing/index.html && echo "redirect points at new chapter"
# hub 页应列出 5 个专题
grep -c 'hub-link' _site/lvxing/index.html
```

最后一条预期 5。再跑完整 `VERIFY`。

- [ ] **Step 8: 提交**

```bash
cd /home/yfrl/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add 6.5 travelling inside the UK and retire the old travel page

Completes the travel chapter with UK rail and coach savings and a few
destinations, then deletes _chapters/jinjie/lvxing.md now that all of its
content lives in 6.1-6.5 and the redirect covers its URL.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: README 复核约定与全站收尾验证

**Files:**
- Modify: `README.md`（年度复核表新增一行）

**Interfaces:**
- Consumes: Task 1–8 的全部改动。

- [ ] **Step 1: 写断言**

```bash
cd /home/yfrl/uk-handbook
grep -q 'lvxing/mianqian' README.md && echo "review row added"
```

- [ ] **Step 2: 跑断言，确认还没加**

- [ ] **Step 3: 在 README 的「金额与政策的年度复核」表里加一行**

加在表格末尾：

```markdown
| 每年一次 | 免签与易签国家清单、快照日期 | `lvxing/mianqian` | [外交部《中外互免签证协定一览表》](https://cs.mfa.gov.cn/gyls/lsgz/fwxx/)、IATA Travel Centre |
```

表格下面那段「手机套餐、Prime Student、返现金额这类商业价格变动太频繁……」之后，补一句：**签证政策变动不预告，且过期信息会让读者在登机口被拦——所以 `lvxing/mianqian` 的三张表各自带快照日期，与 frontmatter 的 `updated` 分开，改错别字时不要顺手刷新快照日期。**

- [ ] **Step 4: 全站收尾验证**

```bash
cd /home/yfrl/uk-handbook
bundle exec jekyll build --trace 2>&1 | tail -5

# 页数应为 66（基线 60 − 旧旅行页 1 + 新页 6 + 重定向 1）
find _site -name index.html | wc -l

# 侧边栏与上下页的顺序
ruby -ryaml -rdate -e '
  Dir.glob("_chapters/**/*.md").map { |f|
    d = YAML.safe_load(File.read(f).split("---",3)[1], permitted_classes: [Date, Time]) rescue nil
    [d && d["weight"] || 9999, d && d["nav"]]
  }.sort.each { |w, n| puts "#{w}\t#{n}" }
'

# 没有残留的旧链接与旧编号
grep -rn 'jinjie/lvxing' --include=*.md _chapters index.md README.md   # 应无输出
grep -rn '第六章 安全' --include=*.md _chapters index.md README.md      # 应无输出
grep -rnE 'num: "5\.6"|num: "6\.[1-4]"' _chapters                       # 应无输出

# 章数与专题数
grep -c 'hub-link' _site/lvxing/index.html    # 5
grep -c 'hub-link' _site/jinjie/index.html    # 5
grep -c 'hub-link' _site/anquan/index.html    # 4
```

再跑一遍完整 `VERIFY`（含 frontmatter 校验）。

- [ ] **Step 5: 起本地服务肉眼过一遍**

```bash
cd /home/yfrl/uk-handbook
bundle exec jekyll serve --port 4000
```

访问确认：

- `http://localhost:4000/` 首页目录里第六章旅游篇、第七章安全篇都在，链接可点；
- 侧边栏七章顺序正确，徽章数字 01–07 连续；
- `http://localhost:4000/lvxing/` 列出 5 个专题，描述文字正常；
- 五个专题页的目录（`toc`）与常见问题（`faq`）都渲染出来了——**这两块消失就说明 frontmatter 的 YAML 出错被静默丢掉了**；
- `http://localhost:4000/jinjie/lvxing/` 跳到 `/lvxing/`；
- 任一专题页底部的上下页导航能串起前后章。

- [ ] **Step 6: 提交并推送**

```bash
cd /home/yfrl/uk-handbook
git add -A
git commit -m "$(cat <<'EOF'
Add the visa list to the annual fact-review schedule

Visa policy changes without notice and stale entries get readers stopped at
the gate, so the three lists in lvxing/mianqian carry their own snapshot
dates, tracked separately from each page's updated field.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"

# 全部任务完成、验证通过后一次推送（推送即部署）
git push origin main
```

---

## Self-Review 记录

**Spec coverage** —— spec 各节对应的任务：结构改动 → Task 1–3；五个专题的内容规划 → Task 4–8；跨页引用与 README → Task 1–3、Task 9；准确性策略（清单只写条件、每表带快照日期、README 复核行）→ Task 6 Step 4/5、Task 9 Step 3；已核实的事实 → 本计划「已核实的事实速查」，Task 4–6 逐条引用；验证 → 每个任务的 `VERIFY` 加 Task 9 的收尾。旧页内容的去向在 Task 8 Step 6 有逐项对照。

**已知的取舍** —— 这是内容仓库，没有单元测试，所以 TDD 的循环改成「先写会失败的 grep/构建断言 → 确认它现在失败 → 改 → 确认通过」。断言主要防两类真实故障：frontmatter YAML 静默丢块，和编号迁移漏改。

**Type consistency** —— 全计划统一使用的标识：`key: lvxing`、`parent: lvxing`、`permalink: /lvxing/`、五页文件名 `guihua`/`shengen`/`mianqian`/`dingpiao`/`jingnei`、`weight` 700–705、`num` "06" 与 6.1–6.5；安全篇 800–804 与 "07"、7.1–7.4；进阶篇 601–605 与 5.1–5.5；结语 850。Task 3 的 `index.md` 链接与 Task 4–8 的 `permalink` 用同一组文件名。
