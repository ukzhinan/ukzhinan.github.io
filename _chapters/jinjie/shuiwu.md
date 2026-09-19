---
layout: section
title: "英国留学生税务：签证对自雇的限制、税码多扣税与退税"
seo_title: "英国留学生税务：自雇限制、税码多扣与退税"
description: "英国留学生税务指南：学生签证禁止自雇这条红线、PAYE 与 tax code 1257L、BR/0T 与应急税码如何区分，以及如何通过 Personal Tax Account 退税。"
nav: "5.2 学生税务规划"
parent: jinjie
weight: 602
updated: 2026-09-19
num: "5.2"
action:
  audience: "需要看懂工资扣税、税码或退税的学生。"
  prepare: "工资单、税务记录、雇佣日期与个人税务账户。"
  steps: "核对实际收入和税码；查看扣税记录；按适用流程询问或更正。"
  help: "工资数据问 payroll；个人税务问题找 HMRC 或税务专业人士。"
toc:
  - title: "基本规则：税级与国民保险"
    anchor: "sec-1"
  - title: "红线：学生签证不允许自雇"
    anchor: "sec-2"
  - title: "PAYE 与 tax code"
    anchor: "sec-3"
  - title: "怎么把多扣的税要回来"
    anchor: "sec-4"
  - title: "保留这些材料"
    anchor: "sec-5"
  - title: "什么时候真的需要报税"
    anchor: "sec-6"
  - title: "Council Tax 与学生豁免"
    anchor: "sec-7"
  - title: "税务居民身份与 ISA"
    anchor: "sec-8"
  - title: "常见问题"
    anchor: "faq"
faq:
  - q: "留学生是不是不用交税？"
    a: "学生身份本身不免所得税或国民保险。符合完整个人免税额条件时，年度所得税通常从 £12,570 以上开始计算；受雇者 NI 通常按每次发薪周期计算，因此某个月可能缴 NI 而全年所得税仍为零。按周发薪与按月发薪使用不同门槛，详见正文。"
  - q: "我被按 BR 或 0T 税码扣了税，钱能要回来吗？"
    a: "先核对是否真的多缴。BR 常用于第二份工作，0T 表示没有分配个人免税额，两者不一定错误。应急税码通常带 W1、M1、X 或 NONCUM 标记，也不代表必然多缴。通过 [Personal Tax Account](https://www.gov.uk/personal-tax-account)核对收入、免税额分配和税码；资料有误时更新，确认多缴后再按 HMRC 流程退税。"
  - q: "退税能追溯多久以前？"
    a: "一般可以追溯到此前若干个税务年度（现行规则为 4 年），所以毕业前值得把在英期间每一年都查一遍——很多人是在离开英国时才发现自己有几百镑没领。具体时限与申请入口以 [gov.uk 的退税页面](https://www.gov.uk/claim-tax-refund)为准。离境后仍可申请，但流程更麻烦，走之前处理完最省事。"
  - q: "我在网上接稿、做代购、开小红书带货，需要报税吗？"
    a: "Student 签证通常禁止自雇和经营活动；税务登记不会使违反签证条件的工作合法。如果已经有收入，同时向合资格移民顾问和税务顾问求助，核对工作权限及如实申报义务，不能因担心签证而隐瞒收入或忽略 HMRC 通知。"
  - q: "父母从国内汇来的生活费要交税吗？"
    a: "用于你本人生活和学习的境外汇款，通常不属于英国的应税所得，中英税收协定对留学生的维持费用也有专门安排。需要注意的是**证明来源**：大额汇入时银行有反洗钱核查义务，备好学费账单与父母的汇款说明能避免账户被临时冻结。金额较大或你同时在中国有收入、资产时，值得咨询专业人士。"
  - q: "P45 和 P60 有什么区别？丢了怎么办？"
    a: "P45 是离职记录；没有 P45 时可向新雇主提交 starter checklist。P60 是在税务年度末 4 月 5 日仍雇用你的雇主提供的年度汇总，通常须在 5 月 31 日前给你。P45 丢失通常不能补原件；可在 Personal Tax Account 查记录，P60 可请雇主补发。"
  - q: "Council Tax 我要交吗？"
    a: "大不列颠符合条件的全日制学生通常不计入 Council Tax 成人计数；整户符合豁免条件可免，混住时按其他应计成人数判断，不保证有折扣。核对 Council 的登记与账单；北爱尔兰另用 domestic rates。见 [学生省钱攻略](/shenghuo/youhui-xuesheng/#sec-3)。"
  - q: "开 ISA 之前应该先做什么？"
    a: "先预留学费、生活费和应急资金，再核对 ISA 类型与资格。Cash ISA 与 Stocks & Shares ISA 风险不同，后者投资本金可能亏损。迁居海外并成为非英国居民后通常不能继续存入，应告知提供商；已有账户可保留，见 [迁居海外规则](https://www.gov.uk/individual-savings-accounts/if-you-move-abroad)。"
---

留学生和税务打交道，绝大多数时候不是"要补交多少"，而是"被多扣了多少、怎么拿回来"。这一页按这个现实排序：先讲一条签证红线，再讲怎么看懂扣税、怎么退税，最后才是报税与 ISA。

一个需要先破除的误解：**学生身份本身没有任何免税特权**。你和其他纳税人适用同一套规则，只是多数学生的收入达不到起征点而已。

<div class="figure">
  <div class="figure-scroll">
<svg viewBox="0 0 760 300" role="img" aria-labelledby="tx-title tx-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="tx-title">留学生要不要自行报税的判定</title>
  <desc id="tx-desc">依次判断：如果收到 HMRC 的申报通知，必须报税；如果有雇佣之外的收入，先确认签证是否允许，因为学生签证禁止自雇；如果只有 PAYE 工资收入，通常不需要自行报税，但仍应使用 HMRC 工具核对申报义务与税码。</desc>
  <defs>
    <marker id="txar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" fill="#6b6b67"/>
    </marker>
  </defs>
  <g font-size="13">
    <rect x="30" y="20" width="430" height="46" rx="4" fill="#ffffff" stroke="#123c6b" stroke-width="1.5"/>
    <text x="46" y="48" fill="#161616">收到 HMRC 要求申报的通知？</text>
    <line x1="460" y1="43" x2="524" y2="43" stroke="#6b6b67" stroke-width="1.5" marker-end="url(#txar)"/>
    <text x="482" y="35" font-size="12" fill="#6b6b67">是</text>
    <rect x="532" y="20" width="198" height="46" rx="4" fill="#fbf3e1" stroke="#9a6b00" stroke-width="1.5"/>
    <text x="548" y="48" fill="#9a6b00" font-weight="700">必须做 Self Assessment</text>

    <line x1="245" y1="66" x2="245" y2="86" stroke="#6b6b67" stroke-width="1.5" marker-end="url(#txar)"/>
    <text x="255" y="82" font-size="12" fill="#6b6b67">否</text>

    <rect x="30" y="94" width="430" height="46" rx="4" fill="#ffffff" stroke="#123c6b" stroke-width="1.5"/>
    <text x="46" y="122" fill="#161616">有雇佣（PAYE）之外的收入？</text>
    <line x1="460" y1="117" x2="524" y2="117" stroke="#6b6b67" stroke-width="1.5" marker-end="url(#txar)"/>
    <text x="482" y="109" font-size="12" fill="#6b6b67">是</text>
    <rect x="532" y="94" width="198" height="46" rx="4" fill="#fdecea" stroke="#b31b12" stroke-width="1.5"/>
    <text x="548" y="115" fill="#b31b12" font-weight="700">先确认签证是否允许</text>
    <text x="548" y="132" font-size="11.5" fill="#b31b12">学生签证禁止自雇</text>

    <line x1="245" y1="140" x2="245" y2="160" stroke="#6b6b67" stroke-width="1.5" marker-end="url(#txar)"/>
    <text x="255" y="156" font-size="12" fill="#6b6b67">否</text>

    <rect x="30" y="168" width="700" height="46" rx="4" fill="#e8f3ec" stroke="#1f7a45" stroke-width="1.5"/>
    <text x="46" y="196" fill="#1f7a45" font-weight="700">通常无需自行报税；仍需核对 HMRC 要求与税码</text>

    <line x1="245" y1="214" x2="245" y2="234" stroke="#6b6b67" stroke-width="1.5" marker-end="url(#txar)"/>

    <rect x="30" y="242" width="700" height="46" rx="4" fill="#eaf0f6" stroke="#123c6b" stroke-width="1.5"/>
    <text x="46" y="264" fill="#161616">登录 GOV.UK Personal Tax Account 核对税码与收入记录</text>
    <text x="46" y="281" font-size="11.5" fill="#6b6b67">应急标记：W1 / M1 / X / NONCUM；BR / 0T 不一定有误</text>
  </g>
</svg>
  </div>
  <p class="figure-cap">多数只有兼职工资的学生落在最下面那条路径：通常无需申报；核对后才能判断是否有退款。</p>
</div>

<h2 id="sec-1">基本规则</h2>

**所得税（Income Tax）**，2026/27 税务年度，以下为英格兰、威尔士和北爱尔兰常见工资收入税档。调整后净收入超过 £100,000 时，个人免税额每增加 £2 收入减少 £1，至 £125,140 归零，不能直接用下表免税额算高收入税款。见 [HMRC 税率](https://www.gov.uk/income-tax-rates)。

| 年收入区间（按标准个人免税额展示） | 边际税率 |
| --- | --- |
| 最高 £12,570（Personal Allowance） | 0% |
| £12,571 – £50,270 | 20%（基本税率） |
| £50,271 – £125,140 | 40% |
| £125,140 以上 | 45% |

**国民保险（Class 1，受雇者）**，2026/27 税务年度：

| 周收入区间 | 费率 |
| --- | --- |
| £242 – £967 | 8% |
| £967 以上 | 2% |

所得税看年度收入，NI 通常按发薪周期计算；上表为常见 Class 1 A 类周薪档，月薪档及其他类别见 [NI 费率](https://www.gov.uk/national-insurance-rates-letters)。短期收入集中时可能缴 NI 而全年无需所得税，NI 不因此自动退还。[苏格兰所得税](https://www.gov.uk/scottish-income-tax)按居民规则判断，不是只看工作地点。

- 工资收入由雇主代扣（PAYE），你不需要自己动手。
- 是否要 Self Assessment 取决于完整情况；用 [HMRC 判断工具](https://www.gov.uk/check-if-you-need-tax-return)核对，收到申报通知时及时处理。

<h2 id="sec-2">红线：学生签证不允许自雇</h2>

这一点放在最前面，因为踩线的后果远大于省下的税：**学生签证明确禁止自雇（self-employment）与个体经营**。以 freelance 身份接活、注册 sole trader、开公司经营，都不在签证允许范围内。

允许的是**受雇工作**——有雇主、走 PAYE、受每周工时限制（详见 [4.1 打工政策与合法权益]({{ '/gongzuo/dagong-zhengce/' | relative_url }})）。网上常见的"留学生做自由职业顺便报个税"，对学生签证持有人并不适用。

如果你已经有了平台收入、接稿收入或带货收入，**同时找合资格移民顾问和税务顾问评估**。税务登记不能赋予工作权限，但签证问题也不免除如实申报、缴税的义务；不要隐瞒收入或忽略 HMRC 通知。

<h2 id="sec-3">PAYE 与 tax code</h2>

[HMRC 应急税码说明](https://www.gov.uk/tax-codes/emergency-tax-codes)与[税码字母说明](https://www.gov.uk/tax-codes/what-your-tax-code-means)区分了应急标记和 BR／0T；代码本身不能证明你多缴。

受雇工作的所得税由雇主代扣（PAYE）。工资单上有一个 **tax code**，常见的是 **1257L**，其他税码也可能正确（苏格兰常见 S 前缀，威尔士为 C），对应 £12,570 的个人免税额。

留学生最常遇到的问题不是漏交税，而是**被多扣税**。典型原因：

| 税码 | 含义 | 常见触发场景 |
| --- | --- | --- |
| **1257L** | 常见的标准个人免税额代码 | 并非唯一正确税码 |
| **BR** | 全部收入按基本税率 20% 扣，**不给免税额** | 同时打两份工，第二份被整体按 BR 处理 |
| **0T** | 不给免税额，按累进税率扣 | 免税额已用完，或新雇主缺少税务资料 |
| **W1 / M1 / X / NONCUM** | 「非累计」计税，只看当周/当月 | 中途入职，系统按单期年化预估 |

另一个高发场景是**暑期集中打工**：某个月工时特别多，系统按"全年都是这个收入"年化预估，当月就会扣得偏多。这部分通常在年度结束后可以退回。

<h2 id="sec-4">怎么把多扣的税要回来</h2>

**不要被动等 HMRC 通知。** 年度结束后 HMRC 有可能寄 **P800** 告知你多缴了税，但它不保证及时、也不保证覆盖所有情形。主动查是更可靠的做法。

1. **注册并登录 [Personal Tax Account](https://www.gov.uk/personal-tax-account)**（GOV.UK 的个人税务账户），需要身份验证。
2. **核对税码与收入记录**：看每个雇主报给 HMRC 的收入是否与你的工资单一致，税码及分配的免税额是否符合个人情况。
3. **税码不对就更正**：向雇主补齐 **P45** 或 starter checklist 等资料，并通过 HMRC 核对税码；也可以在账户里或致电 HMRC 要求更改。
4. **申请退税**：确认多缴后，通过 [gov.uk 的退税入口](https://www.gov.uk/claim-tax-refund)提交，退款通常打到你的英国银行账户。
5. **往年也一起查**。退税一般可以追溯到此前若干个税务年度（现行规则为 4 年），所以**毕业前把在英期间每一年都查一遍**——不少人是在准备离境时才发现有几百镑没领。

> 离开英国之后仍然可以申请退税，但流程更繁琐、沟通更慢，而且英国银行账户可能已经关闭。**走之前处理完**是最省事的做法。
{: .callout .callout-tip}

<h2 id="sec-5">保留这些材料</h2>

- 每月**工资单（payslip）**；
- 离职时雇主给的 **P45**，4 月 5 日仍雇用你的雇主须在 5 月 31 日前提供的 **P60**；
- 雇佣合同与银行入账记录。

这些是核对税额与申请退税的重要记录。建议扫描存云盘，和 [7.4 应急包]({{ '/anquan/yingji-bao/' | relative_url }}) 里的重要文件备份一起做。P45 通常不补发原件，但 Personal Tax Account 里能查到 HMRC 记录的收入与纳税数据。

<h2 id="sec-6">什么时候真的需要报税</h2>

**多数只有 PAYE 工资的学生不需要做 Self Assessment。** 需要申报的情形主要是：收到了 HMRC 要求申报的通知，或有雇佣之外的收入（而后者对学生签证持有人有前置的合规问题，见第二节）。

真的需要申报时：

- 先在 GOV.UK 注册 HMRC 账号并登记 Self Assessment；
- 线上申报的截止日通常是次年 **1 月 31 日**，同一天也是补缴税款的期限；
- 情况复杂时可以找会计或用 TaxScouts 这类平台代办。

<h2 id="sec-7">Council Tax 与学生豁免</h2>

Council Tax 是市政税，按住所征收，和所得税是两回事——但它是留学生最容易白白多花钱的一项。

大不列颠的全日制学生通常不计入 Council Tax 成人计数。全学生住所一般可获豁免；混住时只有一名应计成人通常减 25%，有两名或以上则不能仅凭学生室友获得该折扣。确认 Council 已登记学校证明并正确出账；学生宿舍通常本身豁免，不是把税包含在租金里。北爱尔兰适用 domestic rates。具体步骤见 [学生省钱攻略](/shenghuo/youhui-xuesheng/#sec-3)。

<h2 id="sec-8">税务居民身份与 ISA</h2>

**Stocks & Shares ISA** 是英国的免税投资账户，2026/27 税务年度每人每年可存入 **£20,000**，账户内的资本利得与股息免缴英国税。

开设 ISA 要求具备英国税务居民身份——留学生通常因居住时间（183 天规则等）满足条件。两点要提前想清楚：

- **迁居海外并成为非英国居民后通常不能继续存入**（已有的可以保留），所以把它当长期定投工具时要把毕业时间算进去；
- 如果你同时在中国有收入或资产，跨境税务处理会复杂一些，金额较大时值得咨询专业人士。

迁居海外应及时通知提供商，见 [ISA 海外居民规则](https://www.gov.uk/individual-savings-accounts/if-you-move-abroad)。ISA 有现金和投资等不同类型，上述 £20,000 是各类共用的年度存入限额。

**顺序建议：先应急储蓄，再投资。** Stocks & Shares ISA 里的本金会波动，而留学期间最需要的是随时能取用的现金缓冲——先攒够 2–3 个月生活费放在活期账户，再把结余投进去。

低费率平台例如 [**InvestEngine**](https://investengine.com/referral/u/gtnweo/)（FCA 监管，主打低费率 ETF，支持 ISA），适合长期定投。投资有风险，本金可能亏损，这部分只建议用生活开支之外的结余。

**关于父母汇来的生活费**：用于你本人生活与学习的境外汇款通常不属于英国应税所得，中英税收协定对留学生的维持费用也有专门安排。实务上要注意的是**证明来源**——大额汇入时备好学费账单与父母的汇款说明，避免账户被临时冻结（见 [1.4 理财与银行]({{ '/shenghuo/yinhang-licai/' | relative_url }})）。
