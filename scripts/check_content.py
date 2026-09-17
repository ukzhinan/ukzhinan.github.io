#!/usr/bin/env python3
"""Check rendered local links, fragments and structured data without network access.
Run after `bundle exec jekyll build`. External links require editorial verification.
"""
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.schemas = []
        self.schema = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if tag in ('a', 'link') and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag in ('img', 'script') and attrs.get('src'):
            self.links.append(attrs['src'])
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.schema = []

    def handle_data(self, data):
        if self.schema is not None:
            self.schema.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.schema is not None:
            self.schemas.append(''.join(self.schema))
            self.schema = None


def check(site):
    errors = []
    pages = {}
    for file in sorted(site.rglob('*.html')):
        text = file.read_text()
        pages[file.resolve()] = Page(text)
        if '{{' in text or '{%' in text:
            errors.append(f'{file}: unrendered Liquid')
    checked = 0
    for file, page in pages.items():
        for id_, count in Counter(page.ids).items():
            if count > 1:
                errors.append(f'{file}: duplicate id {id_}')
        for schema in page.schemas:
            try:
                data = json.loads(schema)
                if data.get('@type') == 'FAQPage':
                    for item in data['mainEntity']:
                        if not item.get('name') or not item.get('acceptedAnswer', {}).get('text'):
                            errors.append(f'{file}: empty FAQ question or answer')
            except (ValueError, KeyError, AttributeError, TypeError) as exc:
                errors.append(f'{file}: invalid JSON-LD: {exc}')
        relative = '/' + file.relative_to(site.resolve()).as_posix()
        for href in page.links:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            checked += 1
            target_url = urlsplit(urljoin(relative, href))
            target = (site / unquote(target_url.path).lstrip('/')).resolve()
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                errors.append(f'{file.relative_to(site.resolve())}: missing target {href}')
            elif target_url.fragment and target in pages:
                fragment = unquote(target_url.fragment)
                if not fragment.startswith(':~:text=') and fragment not in pages[target].ids:
                    errors.append(f'{file.relative_to(site.resolve())}: missing fragment {href}')
    if not pages:
        errors.append(f'{site}: no built HTML; build Jekyll first')
    return errors, len(pages), checked


if __name__ == '__main__':
    site = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
    errors, pages, links = check(site)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print(f'Content OK: {pages} HTML pages, {links} local links/assets, fragments and JSON-LD')
