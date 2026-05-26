#!/usr/bin/env python3
"""
Blogger Atom XML -> Markdown 변환 스크립트
"""

import json
import re
import os
import sys
from html.parser import HTMLParser
from html import unescape
import xml.etree.ElementTree as ET

# ── 설정 ──────────────────────────────────────────────────────────────────────
SOURCE = (
    "/root/.claude/projects/-home-user-yskkkkkk-github-io/"
    "0947b323-f5c4-45bc-a058-8341fa08c420/tool-results/"
    "mcp-github-get_file_contents-1779780997312.txt"
)
OUTPUT_DIR = "/home/user/yskkkkkk.github.io/src/content/blog"

NS_ATOM    = "http://www.w3.org/2005/Atom"
NS_BLOGGER = "http://schemas.google.com/blogger/2018"
NS_APP     = "http://www.w3.org/2007/app"

# ── HTML → Markdown 변환기 ─────────────────────────────────────────────────────

class HtmlToMarkdown(HTMLParser):
    """Stateful HTML to Markdown 변환기."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._buf = []
        self._output = []
        self._tag_stack = []
        self._list_stack = []
        self._list_counter = []
        self._skip = 0
        self._link_href = []
        self.has_image = False

    def _flush(self):
        text = "".join(self._buf).strip()
        if text:
            self._output.append(text)
        self._buf = []

    def _buf_pop_all(self):
        t = "".join(self._buf)
        self._buf = []
        return t

    def _indent(self):
        return "  " * (len(self._list_stack) - 1) if self._list_stack else ""

    def handle_starttag(self, tag, attrs):
        if self._skip:
            self._skip += 1
            return
        if tag in ("script", "style"):
            self._skip = 1
            return

        attrmap = dict(attrs)
        self._tag_stack.append(tag)

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush()
            level = int(tag[1])
            self._buf.append("\n\n" + "#" * level + " ")

        elif tag == "p":
            self._flush()
            self._buf.append("\n\n")

        elif tag == "br":
            self._buf.append("  \n")

        elif tag == "hr":
            self._flush()
            self._output.append("\n\n---\n\n")

        elif tag in ("strong", "b"):
            self._buf.append("**")

        elif tag in ("em", "i"):
            self._buf.append("*")

        elif tag == "code":
            parent = self._tag_stack[-2] if len(self._tag_stack) >= 2 else None
            if parent != "pre":
                self._buf.append("`")

        elif tag == "pre":
            self._flush()
            self._buf.append("\n\n```\n")

        elif tag == "blockquote":
            self._flush()
            self._buf.append("\n\n> ")

        elif tag == "ul":
            self._flush()
            self._list_stack.append("ul")
            self._list_counter.append(0)

        elif tag == "ol":
            self._flush()
            self._list_stack.append("ol")
            self._list_counter.append(0)

        elif tag == "li":
            self._flush()
            if self._list_stack:
                kind = self._list_stack[-1]
                indent = self._indent()
                if kind == "ul":
                    self._buf.append(f"\n{indent}- ")
                else:
                    self._list_counter[-1] += 1
                    n = self._list_counter[-1]
                    self._buf.append(f"\n{indent}{n}. ")
            else:
                self._buf.append("\n- ")

        elif tag == "a":
            href = attrmap.get("href", "")
            self._buf.append("[")
            self._link_href.append(href)

        elif tag == "img":
            src = attrmap.get("src", "")
            alt = attrmap.get("alt", "")
            if src:
                self.has_image = True
                self._buf.append(f"![{alt}]({src})")

        elif tag == "div":
            self._buf.append("\n")

    def handle_endtag(self, tag):
        if self._skip:
            self._skip -= 1
            return

        if self._tag_stack and self._tag_stack[-1] == tag:
            self._tag_stack.pop()

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            text = self._buf_pop_all()
            self._output.append(text)
            self._buf.append("\n\n")

        elif tag == "p":
            self._buf.append("\n\n")

        elif tag in ("strong", "b"):
            self._buf.append("**")

        elif tag in ("em", "i"):
            self._buf.append("*")

        elif tag == "code":
            parent = self._tag_stack[-1] if self._tag_stack else None
            if parent != "pre":
                self._buf.append("`")

        elif tag == "pre":
            self._buf.append("\n```\n\n")

        elif tag == "a":
            href = self._link_href.pop() if self._link_href else ""
            self._buf.append(f"]({href})")

        elif tag in ("ul", "ol"):
            if self._list_stack:
                self._list_stack.pop()
                self._list_counter.pop()
            self._buf.append("\n")

        elif tag == "div":
            self._buf.append("\n")

    def handle_data(self, data):
        if self._skip:
            return
        self._buf.append(data)

    def result(self):
        self._flush()
        text = "\n".join(self._output) + "".join(self._buf)
        text = re.sub(r'\n{3,}', '\n\n', text)
        lines = []
        for line in text.split('\n'):
            # 두 공백 줄바꿈(  ) 은 유지, 일반 줄 끝 공백 제거
            if line.endswith('  '):
                lines.append(line.rstrip() + '  ')
            else:
                lines.append(line.rstrip())
        return '\n'.join(lines).strip()


def html_to_markdown(html):
    """HTML 문자열을 마크다운으로 변환. (markdown, has_image) 반환."""
    parser = HtmlToMarkdown()
    parser.feed(html)
    return parser.result(), parser.has_image


# ── 텍스트 유틸 ──────────────────────────────────────────────────────────────

def strip_html(html):
    text = re.sub(r'<[^>]+>', ' ', html)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def make_description(html, length=150):
    return strip_html(html)[:length]


def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text, flags=re.UNICODE)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-') or "untitled"


def escape_yaml_string(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')


# ── XML 파싱 ──────────────────────────────────────────────────────────────────

def parse_blogger_xml(xml_text):
    root = ET.fromstring(xml_text)

    A  = f"{{{NS_ATOM}}}"
    B  = f"{{{NS_BLOGGER}}}"
    AP = f"{{{NS_APP}}}"

    entries = root.findall(f"{A}entry")
    posts = []

    for entry in entries:
        btype_el = entry.find(f"{B}type")
        btype = (btype_el.text or "").strip() if btype_el is not None else ""
        if btype != "POST":
            continue

        title_el = entry.find(f"{A}title")
        title = (title_el.text or "").strip() if title_el is not None else ""

        pub_el = entry.find(f"{A}published")
        pub_raw = (pub_el.text or "").strip() if pub_el is not None else ""
        pub_date = pub_raw[:10] if pub_raw else "1970-01-01"

        content_el = entry.find(f"{A}content")
        content_html = ""
        if content_el is not None:
            content_html = content_el.text or ""

        # 슬러그: blogger:filename 우선
        fn_el = entry.find(f"{B}filename")
        fn = (fn_el.text or "").strip() if fn_el is not None else ""
        slug = ""
        if fn:
            basename = fn.rstrip("/").split("/")[-1]
            slug = re.sub(r'\.html?$', '', basename)
        if not slug:
            for link in entry.findall(f"{A}link"):
                if link.attrib.get("rel") == "alternate":
                    href = link.attrib.get("href", "")
                    seg = href.rstrip("/").split("/")[-1]
                    slug = re.sub(r'\.html?$', '', seg)
                    break
        if not slug:
            slug = slugify(title) if title else "untitled"

        # 태그
        tags = []
        for cat in entry.findall(f"{A}category"):
            term = cat.attrib.get("term", "")
            scheme = cat.attrib.get("scheme", "")
            if "kind#" in term:
                continue
            if not term:
                continue
            if term.startswith("http"):
                tag_val = term.rstrip("/").split("/")[-1]
            else:
                tag_val = term
            if tag_val:
                tags.append(tag_val)

        # draft 여부
        draft = False
        control_el = entry.find(f"{AP}control")
        if control_el is not None:
            draft_el = control_el.find(f"{AP}draft")
            if draft_el is not None and (draft_el.text or "").strip().lower() == "yes":
                draft = True
        status_el = entry.find(f"{B}status")
        if status_el is not None and (status_el.text or "").strip().upper() == "DRAFT":
            draft = True

        posts.append({
            "title": title,
            "pub_date": pub_date,
            "slug": slug,
            "content_html": content_html,
            "tags": tags,
            "draft": draft,
        })

    return posts


# ── 마크다운 생성 ─────────────────────────────────────────────────────────────

def build_markdown(post):
    title       = post["title"] or "Untitled"
    pub_date    = post["pub_date"]
    tags        = post["tags"]
    draft       = post["draft"]
    html        = post["content_html"]

    description = make_description(html)
    body_md, has_image = html_to_markdown(html)

    tags_yaml = "[" + ", ".join(f'"{t}"' for t in tags) + "]"

    frontmatter = (
        "---\n"
        f'title: "{escape_yaml_string(title)}"\n'
        f"pubDate: {pub_date}\n"
        f'description: "{escape_yaml_string(description)}"\n'
        f"tags: {tags_yaml}\n"
        'series: ""\n'
        'heroImage: ""\n'
        f"draft: {str(draft).lower()}\n"
        "---"
    )

    parts = [frontmatter]
    if has_image:
        parts.append("\n<!-- TODO: migrate images -->")
    parts.append("\n" + body_md)

    return "\n".join(parts)


# ── 메인 ─────────────────────────────────────────────────────────────────────

def main():
    print("1. JSON 파일 로드 중...")
    with open(SOURCE, encoding="utf-8") as f:
        data = json.load(f)

    xml_text = None
    for item in data:
        if item.get("type") == "text" and len(item.get("text", "")) > 1000:
            xml_text = item["text"]
            break

    if not xml_text:
        print("ERROR: XML 텍스트를 찾을 수 없습니다.")
        sys.exit(1)

    xml_text = re.sub(r'^\[Resource[^\]]*\]\s*', '', xml_text)
    print(f"   XML 크기: {len(xml_text):,} 바이트")

    print("2. XML 파싱 중...")
    posts = parse_blogger_xml(xml_text)
    print(f"   POST 항목 수: {len(posts)}")

    print("3. 마크다운 파일 생성 중...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    created = []
    errors  = []

    for post in posts:
        try:
            filename = f"{post['pub_date']}-{post['slug']}.md"
            filepath = os.path.join(OUTPUT_DIR, filename)
            content = build_markdown(post)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            created.append({
                "file": filename,
                "date": post["pub_date"],
                "title": post["title"] or "(제목 없음)",
                "draft": post["draft"],
            })
        except Exception as e:
            errors.append({"slug": post.get("slug"), "error": str(e)})
            print(f"   ERROR: {post.get('slug')} -> {e}")

    print()
    print("=" * 70)
    print(f"완료: {len(created)}개 파일 생성  /  오류: {len(errors)}개")
    print("=" * 70)
    print(f"\n{'파일명':<58} {'날짜':<12} 제목")
    print("-" * 110)
    for item in sorted(created, key=lambda x: x["date"]):
        draft_marker = " [DRAFT]" if item["draft"] else ""
        title = item["title"][:38]
        print(f"{item['file']:<58} {item['date']:<12} {title}{draft_marker}")

    if errors:
        print("\n=== 오류 항목 ===")
        for err in errors:
            print(f"  {err['slug']}: {err['error']}")

    return len(created), errors


if __name__ == "__main__":
    main()
