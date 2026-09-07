# 英国生存手册

一份面向中国留学生的英国适应指南，覆盖**生活、学业、社交文化、工作实习、生活进阶、安全应急**六大方面，共 6 章 + 附录速查表。

- **作者**：Steven在英国（邮箱 [xdaiuk@gmail.com](mailto:xdaiuk@gmail.com)）
- **版本**：第一版（2025年8月 / v1.1）
- **网页版（实时更新）**：<https://silken-mule-579.notion.site/23a3dcda1bed8042a8fae1f7bd2a3873>

## 目录

每章拆分为独立的专题页面，URL 结构为 `/<章>/<专题>/`。

| 章节 | URL | 专题数 |
| --- | --- | --- |
| 第一章 生活篇 | `/shenghuo/` | 5（租房、饮食健康、交通、银行理财、手机网络） |
| 第二章 学业篇 | `/xueye/` | 5（高等教育特点、听课笔记、Essay 写作、导师沟通、考试与 Presentation） |
| 第三章 社交与文化篇 | `/shejiao/` | 4（跨文化交流、拓展社交圈、防诈骗与法律、心理健康） |
| 第四章 工作与实习篇 | `/gongzuo/` | 6（打工政策、兼职类型、找工作、简历求职信、面试、职场礼仪） |
| 第五章 生活进阶篇 | `/jinjie/` | 5（国际旅行、驾照、税务、学生优惠、职业发展） |
| 第六章 安全与应急篇 | `/anquan/` | 4（紧急电话、突发情况、个人防范、应急包） |
| 结语 | `/jieyu/` | — |
| 附录 | `/fulu/` | 一页速查表：电话、网站、APP、生活技能 |
| 优惠与返利合集 | `/youhui/` | 合作链接集中页 |
| 关于 / 隐私政策 | `/about/`、`/privacy/` | — |

## 网站

本仓库是一个 [Jekyll](https://jekyllrb.com/) 网站。线上地址：<https://ukzhinan.com>。

内容组织：

- `_chapters/<章>.md` 是章目录页（`layout: chapter-hub`），`_chapters/<章>/<专题>.md` 是专题页（`layout: section`）
- 顺序由 frontmatter 的 `weight` 决定（章 = 序号×100，专题 = 章 weight + 小节号），侧边栏、上下页导航、sitemap 都据此生成；调整顺序只改 `weight`，URL 不受影响
- 每页需要 `description`（用于 meta 与 JSON-LD）和 `updated`（用于显示与 `dateModified`）
- `_data/affiliates.yml` 是合作链接清单，驱动 GA4 点击追踪与页面顶部的披露提示
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
- `_chapters/` — 六个章节 + 结语 + 附录（按 `order` 排序）
- `_layouts/`、`_includes/` — Jekyll 模板
- `assets/css/main.scss` — 样式
- `assets/images/` — 图片素材

## 说明与免责声明

- 文中部分推荐链接（银行、能源、宽带、手机套餐、VPN、返现平台等）为作者的合作/返利链接，使用前请自行甄别。
- 文中涉及的政策与价格（最低工资、签证工作时长、票价、税率等）会随时间调整，请以英国政府官方（[gov.uk](https://www.gov.uk)）等权威来源的最新信息为准。
