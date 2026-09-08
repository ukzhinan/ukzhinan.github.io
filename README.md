# 英国生存手册

一份面向中国留学生的英国适应指南，覆盖**生活、学业、社交文化、工作实习、生活进阶、旅游、安全应急**七大方面，外加**行前准备**，共 7 章 + 行前准备 + 附录速查表。

- **作者**：Steven在英国（邮箱 [xdaiuk@gmail.com](mailto:xdaiuk@gmail.com)）
- **版本**：2026年9月 / v1.3
- **网页版（实时更新）**：<https://silken-mule-579.notion.site/23a3dcda1bed8042a8fae1f7bd2a3873>

## 目录

每章拆分为独立的专题页面，URL 结构为 `/<章>/<专题>/`。

| 章节 | URL | 专题数 |
| --- | --- | --- |
| 出发前准备 | `/chufaqian/` | 行前清单、行李、带钱方式、国内待办 |
| 第一章 生活篇 | `/shenghuo/` | 6（租房、饮食健康、交通、银行理财、手机网络、跨境物流） |
| 第二章 学业篇 | `/xueye/` | 6（高等教育特点、听课笔记、Essay 写作、导师沟通、考试与 Presentation、毕业论文） |
| 第三章 社交与文化篇 | `/shejiao/` | 4（跨文化交流、拓展社交圈、防诈骗与法律、心理健康） |
| 第四章 工作与实习篇 | `/gongzuo/` | 7（打工政策、兼职类型、找工作、简历求职信、面试、职场礼仪、实习与 Placement） |
| 第五章 生活进阶篇 | `/jinjie/` | 5（驾照、税务、学生优惠、职业发展、回国发展） |
| 第六章 旅游篇 | `/lvxing/` | 5（出行规划与签证总览、申根签证、免签与易签国家、廉航与订票、英国境内旅行） |
| 第七章 安全与应急篇 | `/anquan/` | 4（紧急电话、突发情况、个人防范、应急包） |
| 结语 | `/jieyu/` | — |
| 附录1. 速查表 | `/fulu/` | 紧急电话、关键数字、落地 30 天清单、有时限的事项 |
| 附录2. 优惠与返利 | `/youhui/` | 合作链接集中页 |
| 关于 / 隐私政策 | `/about/`、`/privacy/` | — |

## 网站

本仓库是一个 [Jekyll](https://jekyllrb.com/) 网站。线上地址：<https://ukzhinan.com>。

内容组织：

- `_chapters/<章>.md` 是章目录页（`layout: chapter-hub`），`_chapters/<章>/<专题>.md` 是专题页（`layout: section`）
- 顺序由 frontmatter 的 `weight` 决定（章 = 序号×100，专题 = 章 weight + 小节号），侧边栏、上下页导航、sitemap 都据此生成；调整顺序只改 `weight`，URL 不受影响
- 每页需要 `description`（用于 meta 与 JSON-LD）和 `updated`（用于显示与 `dateModified`）
- `_data/affiliates.yml` 是合作链接清单，驱动 GA4 点击追踪与页面顶部的披露提示
- 每个专题页末尾的**常见问题**由 frontmatter 的 `faq:` 列表驱动（`_includes/faq.html`），同时输出 FAQPage 结构化数据；任意页面加 `faq:` 即可启用
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
```

静态文件输出到 `_site/`。

### 结构

- `index.md` — 首页（封面 + 引言）
- `_chapters/` — 行前准备 + 六个章节 + 结语 + 附录（按 `weight` 排序）
- `_layouts/`、`_includes/` — Jekyll 模板
- `assets/css/main.scss` — 样式
- `assets/images/` — 图片素材

## 金额与政策的年度复核

手册里出现的金额都标了生效时点。数字会过期，但页面上的「最后更新」日期会让读者以为不会——所以下面这几项按固定节奏核，核完再动 frontmatter 的 `updated`。

| 时点 | 要核的东西 | 出现在 | 权威来源 |
| --- | --- | --- | --- |
| 每年 4 月 | 最低工资四档 | `gongzuo/dagong-zhengce`、`gongzuo/jianzhi-leixing` | [gov.uk](https://www.gov.uk/national-minimum-wage-rates) |
| 每年 4 月 | 个人免税额、ISA 额度、税务年度标注 | `jinjie/shuiwu`、`fulu` | [gov.uk](https://www.gov.uk/income-tax-rates) |
| 每年 3 月 | 伦敦公交单程价、Hopper、日封顶 | `shenghuo/jiaotong` | [TfL](https://tfl.gov.uk/fares/find-fares/bus-and-tram-fares) |
| 每年一次 | Railcard / Coachcard 年费 | `shenghuo/jiaotong`、`jinjie/youhui-xuesheng`、`youhui` | [railcard.co.uk](https://www.railcard.co.uk/)、[National Express](https://www.nationalexpress.com/en/offers/coachcards) |
| 不定期 | 签证工时、驾照工本费 | `gongzuo/dagong-zhengce`、`jinjie/jiazhao` | gov.uk |

手机套餐、Prime Student、返现金额这类商业价格变动太频繁，页面上只写量级并注明「以官网为准」，不逐条追。

## 说明与免责声明

- 文中部分推荐链接（银行、能源、宽带、手机套餐、VPN、返现平台等）为作者的合作/返利链接，使用前请自行甄别。
- 文中涉及的政策与价格（最低工资、签证工作时长、票价、税率等）会随时间调整，请以英国政府官方（[gov.uk](https://www.gov.uk)）等权威来源的最新信息为准。
