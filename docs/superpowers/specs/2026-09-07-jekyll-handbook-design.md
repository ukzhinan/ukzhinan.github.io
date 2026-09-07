# Jekyll Handbook Site — Design Spec

**Date:** 2026-09-07
**Status:** Approved

## Goal

Split the single-file `英国生存手册.md` into one Markdown file per top-level
section, then wrap them in a Jekyll site so the handbook can be browsed as a
navigable handbook/docs website and deployed to GitHub Pages.

## Decisions

- **Style:** handbook / docs (sidebar navigation + per-chapter TOC). User-selected.
- **Implementation:** hand-rolled minimal Jekyll (no theme gem, no custom plugins).
  Rationale: full control over CJK typography and callout styling; clean
  GitHub Pages deployment.
- **Original file:** delete `英国生存手册.md` after the split (user-selected).
- **Search:** skip full-text search (CJK search is poor out-of-the-box); rely on
  sidebar + per-chapter TOC + appendix quick-reference (user-selected).

## Structure

```
_config.yml                 # site title/description/baseurl, chapters collection, defaults
index.md                    # home: cover + author + disclaimer + 引言
_chapters/01-xueye.md       # 第一章 学业篇
_chapters/02-shenghuo.md    # 第二章 生活篇
_chapters/03-gongzuo.md     # 第三章 工作与实习篇
_chapters/04-shejiao.md     # 第四章 社交与文化篇
_chapters/05-anquan.md      # 第五章 安全与应急篇
_chapters/06-jinjie.md      # 第六章 生活进阶篇
_chapters/07-jieyu.md       # 结语
_chapters/08-fulu.md        # 附录（一页速查表）
_layouts/default.html       # shell: head, sidebar, footer
_layouts/home.html          # hero cover + intro
_layouts/chapter.html       # body + TOC + prev/next
_includes/head.html
_includes/sidebar.html      # nav generated from chapters collection (ordered)
_includes/footer.html
assets/css/main.scss        # all styles (CJK type, callouts, tables, nav)
assets/images/              # the 2 images moved from __Assets/
```

## Content split

Top-level `## ` headings define the boundaries:

| # | File | Section |
|---|------|---------|
| — | `index.md` | frontmatter + title + cover + author + disclaimer + 引言 |
| 1 | `_chapters/01-xueye.md` | 第一章 学业篇 |
| 2 | `_chapters/02-shenghuo.md` | 第二章 生活篇 |
| 3 | `_chapters/03-gongzuo.md` | 第三章 工作与实习篇 |
| 4 | `_chapters/04-shejiao.md` | 第四章 社交与文化篇 |
| 5 | `_chapters/05-anquan.md` | 第五章 安全与应急篇 |
| 6 | `_chapters/06-jinjie.md` | 第六章 生活进阶篇 |
| 7 | `_chapters/07-jieyu.md` | 结语 |
| 8 | `_chapters/08-fulu.md` | 附录（一页速查表） |

## Conversions (applied by a split script)

1. **Callouts** — Obsidian `> [!note]` / `[!tip]` / `[!success]` / `[!warning]` /
   `[!info]` → kramdown classed blockquotes (`.callout .callout-<type>`). The
   literal `[!type]` text is removed so it doesn't leak into the page.
2. **Images** — `__Assets/*` → `assets/images/*`; references rewritten to
   `{{ site.baseurl }}/assets/images/...`.
3. **Anchors / TOC** — assign explicit stable anchors to `### ` headings (CJK
   heading slugs are unreliable in kramdown) and emit a per-chapter TOC in
   frontmatter (`toc:`).
4. **Frontmatter** — each chapter: `title`, `order`, `layout: chapter`, `toc`.

## Design

- High-readability CJK type via a system font stack (no web-font dependency).
- Subtle academic accent color; the existing book cover is the home-page hero.
- Sidebar highlights the active chapter; prev/next links at chapter bottom.
- Responsive; tables scroll horizontally on narrow screens.

## Hosting

- GitHub Pages-compatible: standard kramdown + a single SCSS file, no plugins.
- `baseurl` set in `_config.yml` so it works on a project Pages site.

## Out of scope

- Full-text search (deferred).
- Multi-language / i18n.
- Build/deploy automation beyond a standard `jekyll build`.

## Acceptance criteria

- `jekyll build` succeeds with no errors.
- Every chapter is reachable from the sidebar in order; prev/next work.
- Callouts render styled; tables render; images resolve.
- Original `英国生存手册.md` is removed; content is preserved across the split.
