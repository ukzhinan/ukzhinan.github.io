#!/usr/bin/env python3
import re, pathlib, shutil, html

ROOT = pathlib.Path(".")
SRC = ROOT / "英国生存手册.md"

lines = SRC.read_text(encoding="utf-8").split("\n")

# 1. Drop leading Obsidian frontmatter (first --- ... ---)
assert lines[0].strip() == "---"
for i in range(1, len(lines)):
    if lines[i].strip() == "---":
        lines = lines[i + 1:]
        break

# 2. Locate top-level '## ' headings
h2 = [(i, l) for i, l in enumerate(lines) if l.startswith("## ")]

# 3. Header (title/cover/author/disclaimer) = everything before first '## '
header = lines[: h2[0][0]]

# 4. Build section chunks (heading line + body lines)
sections = []
for idx, (start, _heading) in enumerate(h2):
    end = h2[idx + 1][0] if idx + 1 < len(h2) else len(lines)
    sections.append((_heading, lines[start:end]))

CALL = re.compile(r'^>\s*\[!(note|tip|success|warning|info)\]\s?(.*)$')

def transform(body):
    # drop horizontal-rule separators (kept tables: their rows start with '|')
    body = [l for l in body if l.strip() != "---"]
    # rewrite image paths
    body = [re.sub(r'\(__Assets/([^)]+)\)',
                   r'({{ site.baseurl }}/assets/images/\1)', l) for l in body]
    out, i, n = [], 0, len(body)
    while i < n:
        if body[i].startswith(">"):
            j = i
            while j < n and body[j].startswith(">"):
                j += 1
            block = list(body[i:j])
            m = CALL.match(block[0])
            if m:
                ctype = m.group(1)
                block[0] = ("> " + m.group(2)).rstrip() if m.group(2) else ">"
                out.extend(block)
                out.append("{: .callout .callout-%s}" % ctype)
            else:
                out.extend(block)
            i = j
        else:
            out.append(body[i])
            i += 1
    return out

def clean(block):
    block = list(block)
    while block and block[0].strip() in ("", "---"):
        block.pop(0)
    while block and block[-1].strip() in ("", "---"):
        block.pop()
    return block

def assign_anchors(body):
    toc, out, sec = [], [], 0
    for l in body:
        m = re.match(r'^###\s+(\d+)\.(\d+)\s*(.*)$', l)
        if m:
            anchor = "%s-%s" % (m.group(1), m.group(2))
            title = l[4:].strip()
            out.append('<h3 id="%s">%s</h3>' % (anchor, html.escape(title)))
            toc.append({"title": title, "anchor": anchor})
        elif l.startswith("### "):
            sec += 1
            anchor = "sec-%d" % sec
            title = l[4:].strip()
            out.append('<h3 id="%s">%s</h3>' % (anchor, html.escape(title)))
            toc.append({"title": title, "anchor": anchor})
        else:
            out.append(l)
    return out, toc

# --- home (index.md) ---
home_body = transform(clean(header))
if home_body and home_body[0].startswith("# "):
    home_body = home_body[1:]
for i, l in enumerate(home_body):
    if "uk_survive_book_cover.png" in l:
        home_body[i] = l + "{: .cover}"
    elif "wechat.jpg" in l:
        home_body[i] = l + "{: .qr}"

# append 引言 (sections[0]) body
home_body += [""] + transform(clean(sections[0][1][1:]))

home_fm = ['---', 'layout: home',
           'title: "英国生存手册：为中国留学生提供全面的适应指南"',
           'nav: 引言', 'order: 1', '---', '']
(ROOT / "index.md").write_text("\n".join(home_fm + home_body) + "\n", encoding="utf-8")

# --- chapters ---
FILES = {1: ("01-xueye", 2), 2: ("02-shenghuo", 3), 3: ("03-gongzuo", 4),
         4: ("04-shejiao", 5), 5: ("05-anquan", 6), 6: ("06-jinjie", 7),
         7: ("07-jieyu", 8), 8: ("08-fulu", 9)}

chapters_dir = ROOT / "_chapters"
chapters_dir.mkdir(exist_ok=True)

for n in range(1, 9):
    heading, raw = sections[n]
    title = heading[3:].strip()
    nav = title.split("：")[0] if "：" in title else title
    fname, order = FILES[n]
    body_lines = transform(clean(raw[1:]))
    body_lines, toc = assign_anchors(body_lines)
    fm = ['---', 'layout: chapter', 'title: "%s"' % title,
          'nav: "%s"' % nav, 'order: %d' % order, 'toc:']
    for t in toc:
        fm.append('  - title: "%s"' % t["title"])
        fm.append('    anchor: "%s"' % t["anchor"])
    fm.append('---')
    (chapters_dir / ("%s.md" % fname)).write_text(
        "\n".join(fm + [''] + body_lines) + "\n", encoding="utf-8")

# --- move images ---
imgs = ROOT / "assets" / "images"
imgs.mkdir(parents=True, exist_ok=True)
for f in (ROOT / "__Assets").iterdir():
    if f.is_file():
        shutil.move(str(f), str(imgs / f.name))

print("split complete")
