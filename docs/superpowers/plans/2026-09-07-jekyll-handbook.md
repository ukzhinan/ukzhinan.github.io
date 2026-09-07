# Jekyll Handbook Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split `英国生存手册.md` into one Markdown file per section and wrap them in a hand-rolled Jekyll site deployable to GitHub Pages.

**Architecture:** A Jekyll `chapters` collection (ordered via `order` frontmatter) rendered through three layouts (`home`, `chapter`, `default`) with a sidebar built from the collection and a per-chapter TOC. One SCSS file handles all styling. No theme gem, no custom plugins.

**Tech Stack:** Jekyll 4.4, kramdown, SCSS, Python 3 (one-off split script), Ruby 3.2.

**Spec:** `docs/superpowers/specs/2026-09-07-jekyll-handbook-design.md`

## Global Constraints

- Content is Simplified Chinese; use a system CJK font stack, no web fonts.
- Deploy target is GitHub Pages → no custom plugins; standard kramdown + SCSS only.
- `baseurl: "/uk-handbook"` in `_config.yml`.
- All image references use `{{ site.baseurl }}/assets/images/<file>`.
- Delete `英国生存手册.md` when the split is verified (per user decision).
- Skip full-text search (per user decision).
- Obsidian callouts → `<div class="callout callout-<type>" markdown="1">…</div>`.

---

### Task 1: Jekyll scaffold (config + layouts + includes + CSS)

**Files:**
- Create: `_config.yml`
- Create: `_layouts/default.html`, `_layouts/home.html`, `_layouts/chapter.html`
- Create: `_includes/head.html`, `_includes/sidebar.html`, `_includes/footer.html`
- Create: `assets/css/main.scss`

**Interfaces:**
- Produces: `site.chapters` collection (Task 2 fills it), layouts `home`/`chapter`/`default`, CSS classes `.callout .callout-<type>`, `.sidebar`, `.toc`, `.chapter-nav`.
- Consumes: frontmatter keys `title`, `nav`, `order`, `toc` (list of `{title, anchor}`).

- [ ] **Step 1: Create `_config.yml`**

```yaml
title: 英国生存手册
description: 为中国留学生提供全面的英国适应指南
baseurl: "/uk-handbook"
url: ""

collections:
  chapters:
    output: true
    permalink: /:name/

defaults:
  - scope:
      path: ""
      type: "chapters"
    values:
      layout: chapter

exclude:
  - README.md
  - docs/
  - tools/
  - 英国生存手册.md
```

- [ ] **Step 2: Create `_includes/head.html`** — charset/viewport/meta, a `<title>` using `page.title` + `site.title`, and a link to the stylesheet via `{{ "/assets/css/main.css" | relative_url }}`.

- [ ] **Step 3: Create `_includes/sidebar.html`** — render `index` ("引言", order 1) plus every chapter sorted by `order`; each link is `{{ doc.url | relative_url }}`; mark the active page with class `active` when `page.url == doc.url`.

- [ ] **Step 4: Create `_includes/footer.html`** — author credit and the Notion web-version link.

- [ ] **Step 5: Create `_layouts/default.html`** — `<html>` shell pulling in `head`, `sidebar`, then `{{ content }}`, then `footer`.

- [ ] **Step 6: Create `_layouts/home.html`** (`layout: default`) — hero wrapper for the cover image + `{{ content }}`.

- [ ] **Step 7: Create `_layouts/chapter.html`** (`layout: default`) — render `page.title` as `<h1>`, a `.toc` block from `page.toc` (anchor links), `{{ content }}`, and prev/next `.chapter-nav` by `order`.

- [ ] **Step 8: Create `assets/css/main.scss`** — front matter `---\n---`, then: reset, CJK system font stack on `body`, sidebar layout (fixed left, content right), `.callout` base + `.callout-note/.tip/.success/.warning/.info` color variants, `.toc`, table `overflow-x: auto`, responsive collapse for narrow screens.

- [ ] **Step 9: Build to verify scaffold compiles**

Run: `bundle exec jekyll build` (or `jekyll build`)
Expected: build succeeds (may warn about no posts); `_site/` produced. An empty `index.md` is created now so the build has a home page.

- [ ] **Step 10: Commit**

```bash
git add _config.yml _layouts _includes assets
git commit -m "feat: add Jekyll scaffold (config, layouts, css)"
```

---

### Task 2: Split content into index.md + 9 chapter files

**Files:**
- Create: `tools/split.py` (one-off; removed in Task 3)
- Create: `index.md`, `_chapters/01-xueye.md` … `_chapters/08-fulu.md`
- Create: `assets/images/` (moved from `__Assets/`)

**Interfaces:**
- Produces: `site.chapters` entries with `title`, `nav`, `order`, `toc`; `index.md` with `layout: home`.
- Consumes: `英国生存手册.md` (unmodified input), `__Assets/*` images.

- [ ] **Step 1: Write the split script `tools/split.py`** (full content below)

```python
#!/usr/bin/env python3
import re, pathlib, shutil

ROOT = pathlib.Path(".")
SRC = ROOT / "英国生存手册.md"

lines = SRC.read_text(encoding="utf-8").split("\n")

# 1. Drop leading Obsidian frontmatter (first --- ... ---)
assert lines[0].strip() == "---"
for i in range(1, len(lines)):
    if lines[i].strip() == "---":
        lines = lines[i+1:]
        break

# 2. Locate top-level '## ' headings
h2 = [(i, l) for i, l in enumerate(lines) if l.startswith("## ")]

# 3. Header (title/cover/author/disclaimer) = everything before first '## '
header = lines[: h2[0][0]]

# 4. Build section chunks
sections = []
for idx, (start, _heading) in enumerate(h2):
    end = h2[idx + 1][0] if idx + 1 < len(h2) else len(lines)
    sections.append((_heading, lines[start:end]))

CALL = re.compile(r'^>\s*\[!(note|tip|success|warning|info)\]\s?(.*)$')

def transform(body):
    # rewrite image paths
    body = [re.sub(r'\(__Assets/([^)]+)\)',
                   r'({{ site.baseurl }}/assets/images/\1)', l) for l in body]
    out, i = [], 0
    while i < len(body):
        if body[i].startswith(">"):
            j = i
            while j < len(body) and body[j].startswith(">"):
                j += 1
            block = body[i:j]
            m = CALL.match(block[0])
            if m:
                ctype = m.group(2)
                inner = [l[1:].lstrip() for l in block]  # drop '>'
                inner[0] = m.group(3) if m.group(3) else inner[0]
                out.append(f'<div class="callout callout-{ctype}" markdown="1">')
                out.append("")
                out.extend(inner)
                out.append("")
                out.append("</div>")
            else:
                out.extend(block)
            i = j
        else:
            out.append(body[i])
            i += 1
    return out

def clean(block):
    # strip leading/trailing blanks and '---' separators
    block = list(block)
    while block and block[0].strip() in ("", "---"):
        block.pop(0)
    while block and block[-1].strip() in ("", "---"):
        block.pop()
    return block

def assign_anchors(body):
    # add {:#anchor} after each '### ' heading; collect toc entries
    toc, out, sec = [], [], 0
    for l in body:
        out.append(l)
        m = re.match(r'^###\s+(\d+)\.(\d+)\s*(.*)$', l)
        if m:
            anchor = f"{m.group(1)}-{m.group(2)}"
            title = l[4:].strip()
            out.append(f"{{:#{anchor}}}")
            toc.append({"title": title, "anchor": anchor})
        elif l.startswith("### "):
            sec += 1
            anchor = f"sec-{sec}"
            out.append(f"{{:#{anchor}}}")
            toc.append({"title": l[4:].strip(), "anchor": anchor})
    return out, toc

# --- index.md (home) ---
home_fm = ['---', 'layout: home',
           'title: "英国生存手册：为中国留学生提供全面的适应指南"',
           'nav: 引言', 'order: 1', '---', '']
home_body = transform(clean(header))
(ROOT / "index.md").write_text("\n".join(home_fm + home_body) + "\n", encoding="utf-8")

# --- chapter files ---
NAV_ORDER = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9}
FILES = {1: "01-xueye", 2: "02-shenghuo", 3: "03-gongzuo", 4: "04-shejiao",
         5: "05-anquan", 6: "06-jinjie", 7: "07-jieyu", 8: "08-fulu"}

chapters_dir = ROOT / "_chapters"
chapters_dir.mkdir(exist_ok=True)

for n, (heading, raw) in enumerate(sections, start=1):
    title = heading[3:].strip()                      # strip '## '
    nav = title.split("：")[0] if "：" in title else title
    body_lines = transform(clean(raw[1:]))           # drop the '## ' line itself
    body_lines, toc = assign_anchors(body_lines)
    fm = ['---', 'layout: chapter', f'title: "{title}"',
          f'nav: "{nav}"', f'order: {NAV_ORDER[n]}', 'toc:']
    for t in toc:
        fm.append(f'  - title: "{t["title"]}"')
        fm.append(f'    anchor: "{t["anchor"]}"')
    fm.append('---')
    out_path = chapters_dir / f"{FILES[n]}.md"
    out_path.write_text("\n".join(fm + [''] + body_lines) + "\n", encoding="utf-8")

# --- move images ---
imgs = ROOT / "assets" / "images"
imgs.mkdir(parents=True, exist_ok=True)
for f in (ROOT / "__Assets").iterdir():
    if f.is_file():
        shutil.move(str(f), str(imgs / f.name))
```

- [ ] **Step 2: Run the split**

Run: `python3 tools/split.py`
Expected: exit 0; creates `index.md`, 8 files under `_chapters/`, moves 2 images into `assets/images/`.

- [ ] **Step 3: Verify content is preserved**

Run: `grep -c "第一章" _chapters/01-xueye.md` (expect >0); spot-check that `英国生存手册.md` and `_chapters/*.md` have equal total line counts minus the header (approximately); confirm `__Assets` now empty.

- [ ] **Step 4: Commit**

```bash
git add index.md _chapters assets/images
git commit -m "feat: split handbook into Jekyll chapters"
```

---

### Task 3: Delete original + housekeeping

**Files:**
- Delete: `英国生存手册.md`, `tools/split.py`
- Modify: `README.md`, `.gitignore`

- [ ] **Step 1: Update `.gitignore`** — add `_site/`, `.jekyll-cache/`, `.bundle/`, `vendor/`.

- [ ] **Step 2: Update `README.md`** — add a "网站" section: local run (`bundle install && bundle exec jekyll serve`), build (`jekyll build`), and note the site lives in `_chapters/` + `index.md`.

- [ ] **Step 3: Delete the original and the one-off script**

Run: `rm 英国生存手册.md tools/split.py && rmdir tools __Assets 2>/dev/null || true`

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: remove single-file source and split script"
```

---

### Task 4: Build, verify, and finalize

- [ ] **Step 1: Clean build**

Run: `bundle exec jekyll build` (or `jekyll build`)
Expected: build succeeds with no errors; `_site/` contains `index.html` and 8 chapter pages.

- [ ] **Step 2: Verify no leftover artifacts**

Run: `grep -rn "\[!note\]\|\[!tip\]\|\[!success\]\|\[!warning\]\|\[!info\]\|__Assets" _chapters index.md assets || echo "clean"`
Expected: `clean`.

- [ ] **Step 3: Verify output links/images resolve**

Run: `grep -rn "uk_survive_book_cover\|wechat" _site | head` — confirm image URLs point under `/uk-handbook/assets/images/`.

- [ ] **Step 4: Visual smoke check**

Run: `bundle exec jekyll serve` and open a chapter page; confirm sidebar order, active highlight, TOC anchors, callout styling, tables, prev/next.

- [ ] **Step 5: Commit and push**

```bash
git add -A && git commit -m "chore: finalize Jekyll site build" && git push
```

---

## Self-Review

- **Spec coverage:** config → T1; split + conversions → T2; delete original → T3; README/.gitignore → T3; build/verify + acceptence criteria → T4. All spec sections covered.
- **Placeholders:** none — split script and config are fully specified.
- **Type consistency:** frontmatter keys `title/nav/order/toc` are defined once (T1 Interfaces) and reused verbatim in T2's script. Layout names `home`/`chapter`/`default` match.
