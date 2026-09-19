# 英国生存指南

一份面向中国留学生的英国适应指南，覆盖**生活、学业、社交文化、工作实习、生活进阶、旅游、安全应急、买房**八大方面，外加**行前准备**，共 8 章 + 行前准备 + 三个附录。

- **作者**：Steven在英国（合作邮箱 [xdaiuk@gmail.com](mailto:xdaiuk@gmail.com)）
- **版本**：2026年9月 / v1.3

## 目录

每章拆分为独立的专题页面，URL 结构为 `/<章>/<专题>/`。

| 章节 | URL | 专题数 |
| --- | --- | --- |
| 出发前准备 | `/chufaqian/` | 行前清单、行李、带钱方式、国内待办 |
| 第一章 生活篇 | `/shenghuo/` | 14（租房、饮食采购、交通、银行理财、手机网络、跨境物流、水电账单、留学预算、学生省钱攻略、消费投诉、长期用药、落地第一周、eVisa、看病与 NHS） |
| 第二章 学业篇 | `/xueye/` | 9（高等教育特点、听课笔记、Essay 写作、导师沟通、考试与 Presentation、毕业论文、挂科延期与申诉、小组作业、学术诚信与 AI） |
| 第三章 社交与文化篇 | `/shejiao/` | 5（跨文化交流、拓展社交圈、防诈骗与法律、心理健康、歧视骚扰与关系伤害求助） |
| 第四章 工作与实习篇 | `/gongzuo/` | 8（打工政策、兼职类型、找工作、简历求职信、面试、职场礼仪、实习与 Placement、毕业求职实战） |
| 第五章 生活进阶篇 | `/jinjie/` | 5（驾照、税务、职业发展、回国发展、搬家与离英交接） |
| 第六章 旅游篇 | `/lvxing/` | 5（出行规划与签证总览、申根签证、免签与易签国家、廉航与订票、英国境内旅行） |
| 第七章 安全与应急篇 | `/anquan/` | 4（紧急电话、突发情况、个人防范、应急包） |
| 第八章 买房篇 | `/maifang/` | 6（买还是继续租、预算与贷款、找房看房与出价、税费总账、从 offer 到交房、苏格兰买房） |
| 结语 | `/jieyu/` | — |
| 附录1. 速查表 | `/fulu/` | 紧急电话、关键数字、落地 30 天清单、有时限的事项 |
| 附录2. 优惠与返利 | `/youhui/` | 合作链接集中页 |
| 附录3. 常用英语 | `/yingyu/` | 中英文对照表（178 条，口语说法与正式表达） |
| 关于 / 隐私政策 | `/about/`、`/privacy/` | — |

## 网站

本仓库是一个 [Jekyll](https://jekyllrb.com/) 网站。线上地址：<https://ukzhinan.com>。

内容组织：

- `_chapters/<章>.md` 是章目录页（`layout: chapter-hub`），`_chapters/<章>/<专题>.md` 是专题页（`layout: section`）
- 顺序由 frontmatter 的 `weight` 决定（章 = 序号×100，专题 = 章 weight + 小节号），侧边栏、上下页导航、sitemap 都据此生成；调整顺序只改 `weight`，URL 不受影响
- 每页需要 `description`（用于 meta 与 JSON-LD）和 `updated`（用于显示与 `dateModified`）
- `_data/affiliates.yml` 是合作链接清单，驱动 GA4 点击追踪与页面顶部的披露提示
- 每个专题页末尾的**常见问题**由 frontmatter 的 `faq:` 列表驱动（`_includes/faq.html`），同时输出 FAQPage 结构化数据；任意页面加 `faq:` 即可启用
- **`index.md` 顶部的开场语是作者原文（落款 Steven，2025-08-09），改版首页时必须原样保留**；它排在版本行之后、`## 从这里开始` 之前，不要为了让任务入口靠前而删改或压缩
- 专题页的 `action:` 需要 `audience`、`prepare`、`steps`、`help` 四个非空字符串，由 `_includes/action-summary.html` 渲染在目录之前（行前页与速查页同样使用）；摘要要写明适用地区或资格，不能把正文里的例外简化成绝对承诺
- `updated` 在页面上显示为「内容编辑」，只说明这页被编辑过，不代表整页政策同日复核；核对日期与来源写在对应段落里
- 专题拆分后旧锚点要保留（例如饮食页的 `sec-3`–`sec-6` 仍指向医疗入口，正文已迁至 `/shenghuo/nhs-kanbing/`），旧书签不能失效
- 图示统一用内联 SVG，包在 `.figure > .figure-scroll` 里（窄屏横向滚动），并写 `<title>`/`<desc>` 供读屏使用
- `sidebar: false` 的页面不进侧边栏与上下页导航（目前只有隐私政策），但仍保留在页脚、sitemap 与「关于」页的正文链接中
- 联盟链接的 `rel="sponsored nofollow noopener"` 由 `_plugins/affiliate_rel.rb` 按 `_data/affiliates.yml` 自动补齐，不要手写
- CI 会校验：构建产物、frontmatter 能解析且字段齐全、联盟链接都带 rel。**frontmatter 的 YAML 出错时 Jekyll 会静默丢掉整块**（`faq`、`toc` 一起消失而页面照常构建），最常见的原因是双引号字符串里又写了 ASCII 双引号——写中文引号「」或转义
- `redirects/` 下是旧 URL 的重定向页
- AdSense 广告位与站长平台验证码在 `_config.yml` 中配置，留空则不输出

### 本地运行

```bash
bundle install
bundle exec jekyll serve
```

然后访问 <http://localhost:4000/>。

### 构建

```bash
bundle exec jekyll build
python3 scripts/check_content.py
```

静态文件输出到 `_site/`。内容检查会验证本地链接、图片与脚本路径、页内锚点、重复 ID、未展开的 Liquid 和 JSON-LD；部署前自动运行。外部站点和政策内容仍须人工复核。

### 结构

- `index.md` — 首页：版本行 → 开场语 → 从这里开始（五条阶段入口）→ 按章节阅读 → 常见问题 → 关于这份指南
- `_chapters/` — 行前准备 + 八个章节 + 结语 + 三个附录（按 `weight` 排序）
- `_layouts/`、`_includes/` — Jekyll 模板
- `assets/css/main.scss` — 样式
- `assets/images/` — 图片素材

## 金额与政策的年度复核

指南里出现的金额都标了生效时点。数字会过期，但页面上的「最后更新」日期会让读者以为不会——所以下面这几项按固定节奏核，核完再动 frontmatter 的 `updated`。

| 时点 | 要核的东西 | 出现在 | 权威来源 |
| --- | --- | --- | --- |
| 每年 4 月 | 最低工资四档 | `gongzuo/dagong-zhengce`、`gongzuo/jianzhi-leixing` | [gov.uk](https://www.gov.uk/national-minimum-wage-rates) |
| 每年 4 月 | 个人免税额、ISA 额度、税务年度标注 | `jinjie/shuiwu`、`fulu` | [gov.uk](https://www.gov.uk/income-tax-rates) |
| 每年 3 月 | 伦敦公交单程价、Hopper、日封顶 | `shenghuo/jiaotong` | [TfL](https://tfl.gov.uk/fares/find-fares/bus-and-tram-fares) |
| 每年一次 | Railcard / Coachcard 年费 | `shenghuo/jiaotong`、`shenghuo/youhui-xuesheng`、`youhui` | [railcard.co.uk](https://www.railcard.co.uk/)、[National Express](https://www.nationalexpress.com/en/offers/coachcards) |
| 不定期 | 签证工时、驾照工本费 | `gongzuo/dagong-zhengce`、`jinjie/jiazhao`、`yingyu`（「打工时间限制」一条） | gov.uk |
| 每次行程前；俄罗斯旧免签试行已于 2026-09-14 到期，续期未核实 | 免签与易签国家清单、快照日期 | `lvxing/mianqian` | [外交部《中外互免签证协定一览表》](https://cs.mfa.gov.cn/gyls/lsgz/fwxx/)、IATA Travel Centre |
| 每年 4 月 | SDLT 分档、首次购房减免门槛、追加房产附加税 | `maifang/shuifei`、`fulu` | [gov.uk](https://www.gov.uk/stamp-duty-land-tax/residential-property-rates) |
| 每年 4 月 | LBTT 分档与 ADS、LTT 主表与高档表 | `maifang/shuifei`、`maifang/sugelan` | [revenue.scot](https://revenue.scot/taxes/land-buildings-transaction-tax)、[gov.wales](https://www.gov.wales/land-transaction-tax-rates-and-bands) |
| 每年 4 月 | Lifetime ISA 年额度与 £450k 房价上限 | `maifang/daikuan`、`fulu` | [gov.uk](https://www.gov.uk/lifetime-isa) |
| 不定期 | 海外买家 2% 附加税、Freedom to Buy 条件、Land Registry 费档 | `maifang/shuifei`、`maifang/daikuan` | gov.uk |

手机套餐、Prime Student、返现金额这类商业价格变动太频繁，页面上只写量级并注明「以官网为准」，不逐条追。

**签证与入境规则应逐目的地核对，并保留来源和核对时点；不能把全站编辑日期当作每一项政策都已确认。** `lvxing/mianqian` 已将未经逐国核验的普通护照名单改为候选目的地索引，不能直接据此订票。

**买房篇的每张税率表也各自带生效时点，同样与 frontmatter 的 `updated` 分开。**印花税分档已自 2025-04-01 回调（2022–2025 年的临时门槛 £250,000 / £425,000 已失效），而网上多数中文攻略仍在用旧数字——改错别字时不要顺手刷新这些生效时点，核实时也不要拿二手攻略当来源。

## 说明与免责声明

- 文中部分推荐链接（银行、能源、宽带、手机套餐、VPN、返现平台等）为作者的合作/返利链接，使用前请自行甄别。
- 文中涉及的政策与价格（最低工资、签证工作时长、票价、税率等）会随时间调整，请以英国政府官方（[gov.uk](https://www.gov.uk)）等权威来源的最新信息为准。

## 内容记录

每轮审阅与扩展的范围、来源和复核边界记在 `docs/` 下，README 只保留长期有效的约定：

- [2026-09-17 内容审阅记录](docs/content-audit-2026-09-17.md)
- [2026-09-19 内容扩展记录](docs/content-expansion-2026-09-19.md)
