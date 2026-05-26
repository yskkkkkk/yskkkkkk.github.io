#!/usr/bin/env python3
"""
Blogger Atom XML → Markdown 변환 스크립트
"""

import json
import os
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from html import unescape
from datetime import datetime

INPUT_FILE = "/root/.claude/projects/-home-user-yskkkkkk-github-io/0947b323-f5c4-45bc-a058-8341fa08c420/tool-results/mcp-github-get_file_contents-1779780997312.txt"
OUTPUT_DIR = "/home/user/yskkkkkk.github.io/src/content/blog"

# ── HTML → Markdown 변환기 ──────────────────────────────────────────────────

class HtmlToMarkdown(HTMLParser):
    """HTML을 마크다운으로 변환하는 파서"""

    BLOCK_TAGS = {"p", "div", "section", "article", "header", "footer",
                  "h1", "h2", "h3", "h4", "h5", "h6",
                  "pre", "blockquote", "ul", "ol", "li", "hr", "table"}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.result = []
        self._stack = []          # 열린 태그 스택
        self._list_stack = []     # ("ul"|"ol", 카운터) 스택
        self._in_pre = False
        self._skip_content = 0   # script/style 안이면 > 0
        self._link_href = None
        self._link_text_parts = []
        self._in_link = False
        self.has_image = False    # <img> 발견 여부

    # ── 내부 헬퍼 ───────────────────────────────────────────────────────────

    def _emit(self, text):
        self.result.append(text)

    def _current_text(self):
        return "".join(self.result)

    # ── 이벤트 핸들러 ────────────────────────────────────────────────────────

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs_dict = dict(attrs)

        if tag in ("script", "style"):
            self._skip_content += 1
            return

        if self._skip_content:
            return

        self._stack.append(tag)

        if tag in ("br",):
            if self._in_pre:
                self._emit("\n")
            else:
                self._emit("  \n")

        elif tag == "hr":
            self._emit("\n\n---\n\n")

        elif tag in ("h1","h2","h3","h4","h5","h6"):
            level = int(tag[1])
            self._emit(f"\n\n{'#'*level} ")

        elif tag == "p":
            self._emit("\n\n")

        elif tag == "pre":
            self._in_pre = True
            self._emit("\n\n```\n")

        elif tag == "blockquote":
            self._emit("\n\n> ")

        elif tag == "ul":
            self._list_stack.append(("ul", 0))
            self._emit("\n")

        elif tag == "ol":
            self._list_stack.append(("ol", 0))
            self._emit("\n")

        elif tag == "li":
            if self._list_stack:
                kind, cnt = self._list_stack[-1]
                if kind == "ol":
                    cnt += 1
                    self._list_stack[-1] = ("ol", cnt)
                    self._emit(f"\n{cnt}. ")
                else:
                    self._emit("\n- ")
            else:
                self._emit("\n- ")

        elif tag in ("strong", "b"):
            self._emit("**")

        elif tag in ("em", "i"):
            self._emit("*")

        elif tag == "code":
            if not self._in_pre:
                self._emit("`")

        elif tag == "a":
            href = attrs_dict.get("href", "")
            self._link_href = href
            self._in_link = True
            self._link_text_parts = []

        elif tag == "img":
            src = attrs_dict.get("src", "")
            alt = attrs_dict.get("alt", "")
            self._emit(f"![{alt}]({src})")
            self.has_image = True

        elif tag == "div":
            self._emit("\n\n")

        elif tag == "span":
            pass  # 인라인, 아무것도 안 함

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag in ("script", "style"):
            self._skip_content = max(0, self._skip_content - 1)
            return

        if self._skip_content:
            return

        # 스택에서 제거 (최근 동일 태그)
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i] == tag:
                self._stack.pop(i)
                break

        if tag in ("h1","h2","h3","h4","h5","h6"):
            self._emit("\n\n")

        elif tag == "p":
            self._emit("\n\n")

        elif tag == "pre":
            self._in_pre = False
            self._emit("\n```\n\n")

        elif tag == "blockquote":
            self._emit("\n\n")

        elif tag in ("ul", "ol"):
            if self._list_stack:
                self._list_stack.pop()
            self._emit("\n")

        elif tag in ("strong", "b"):
            self._emit("**")

        elif tag in ("em", "i"):
            self._emit("*")

        elif tag == "code":
            if not self._in_pre:
                self._emit("`")

        elif tag == "a":
            text = "".join(self._link_text_parts).strip()
            href = self._link_href or ""
            if text or href:
                self._emit(f"[{text}]({href})")
            self._in_link = False
            self._link_href = None
            self._link_text_parts = []

        elif tag == "div":
            pass

    def handle_data(self, data):
        if self._skip_content:
            return

        decoded = unescape(data)
        # &nbsp; 처리
        decoded = decoded.replace("\xa0", " ")

        if self._in_link:
            self._link_text_parts.append(decoded)
        else:
            self._emit(decoded)

    def handle_entityref(self, name):
        if self._skip_content:
            return
        text = unescape(f"&{name};")
        if self._in_link:
            self._link_text_parts.append(text)
        else:
            self._emit(text)

    def handle_charref(self, name):
        if self._skip_content:
            return
        text = unescape(f"&#{name};")
        if self._in_link:
            self._link_text_parts.append(text)
        else:
            self._emit(text)

    def get_markdown(self):
        md = "".join(self.result)
        # 연속 빈줄 정리 (3줄 이상 → 2줄)
        md = re.sub(r'\n{3,}', '\n\n', md)
        return md.strip()


def html_to_markdown(html_content):
    """HTML 문자열 → (markdown 문자열, has_image 여부)"""
    parser = HtmlToMarkdown()
    parser.feed(html_content or "")
    return parser.get_markdown(), parser.has_image


def strip_html_for_description(html_content, max_len=150):
    """HTML 태그 제거 후 앞 max_len 자 반환 (description용)"""
    # 태그 제거
    text = re.sub(r'<[^>]+>', '', html_content or '')
    text = unescape(text)
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_len]


# ── 슬러그 생성 ──────────────────────────────────────────────────────────────

def title_to_slug(title):
    """제목을 슬러그로 변환"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s가-힣-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug).strip('-')
    return slug or "post"


def extract_slug_from_filename(filename):
    """blogger:filename (예: /2021/08/foo.html) 에서 슬러그 추출"""
    if not filename:
        return None
    base = filename.rstrip('/').split('/')[-1]
    base = re.sub(r'\.html?$', '', base)
    return base if base else None


# ── Atom 네임스페이스 ─────────────────────────────────────────────────────────

ATOM = "http://www.w3.org/2005/Atom"
BLOGGER = "http://schemas.google.com/blogger/2018"
APP = "http://purl.org/atom/app#"

def tag(ns, local):
    return f"{{{ns}}}{local}"


def get_text(elem, ns, local, default=""):
    child = elem.find(tag(ns, local))
    return child.text.strip() if child is not None and child.text else default


# ── 메인 변환 로직 ───────────────────────────────────────────────────────────

def parse_and_convert():
    # 1. JSON 파일에서 XML 추출
    print("JSON 파일 로딩...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    xml_raw = None
    for item in data:
        if item.get('type') == 'text' and '<?xml' in item.get('text', ''):
            xml_raw = item['text']
            break

    if not xml_raw:
        raise ValueError("XML 텍스트를 찾을 수 없습니다.")

    start = xml_raw.find('<?xml')
    xml_text = xml_raw[start:]
    print(f"XML 크기: {len(xml_text):,} bytes")

    # 2. XML 파싱
    root = ET.fromstring(xml_text)
    entries = root.findall(tag(ATOM, "entry"))
    print(f"총 entry 수: {len(entries)}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    created = []
    errors = []
    skipped = 0

    for idx, entry in enumerate(entries):
        try:
            # blogger:type 이 POST 인 것만 처리
            btype = get_text(entry, BLOGGER, "type")
            if btype != "POST":
                skipped += 1
                continue

            # title
            title = get_text(entry, ATOM, "title", "Untitled")

            # published date
            pub_raw = get_text(entry, ATOM, "published")
            if pub_raw:
                pub_dt = datetime.fromisoformat(pub_raw.replace('Z', '+00:00'))
                pub_date = pub_dt.strftime("%Y-%m-%d")
            else:
                pub_date = "1970-01-01"

            # draft 여부: blogger:status == "DRAFT"
            status = get_text(entry, BLOGGER, "status")
            is_draft = (status == "DRAFT")

            # 슬러그
            filename_elem = entry.find(tag(BLOGGER, "filename"))
            filename_val = filename_elem.text.strip() if filename_elem is not None and filename_elem.text else ""
            slug = extract_slug_from_filename(filename_val) or title_to_slug(title)

            # tags (카테고리)
            tags = []
            for cat in entry.findall(tag(ATOM, "category")):
                term = cat.get("term", "")
                # kind# 으로 시작하는 scheme은 제외 (없음 - 이 포맷에선 term이 태그명)
                if "blogger.com" in cat.get("scheme", ""):
                    # scheme이 blogger의 블로그 ID 기반이면 태그
                    tags.append(term)
                elif "/" in term:
                    tags.append(term.rstrip("/").split("/")[-1])
                else:
                    tags.append(term)

            # content (HTML)
            content_elem = entry.find(tag(ATOM, "content"))
            html_content = ""
            if content_elem is not None:
                html_content = content_elem.text or ""
                # ET가 text를 그대로 주므로 HTML 엔티티가 이미 디코딩된 상태일 수 있음
                # content_elem의 하위 요소도 있을 수 있으니 전체 내부 텍스트 수집
                if list(content_elem):
                    import io
                    buf = io.StringIO()
                    buf.write(html_content or "")
                    for child in content_elem:
                        buf.write(ET.tostring(child, encoding='unicode'))
                        if child.tail:
                            buf.write(child.tail)
                    html_content = buf.getvalue()

            # description (HTML 태그 제거 후 앞 150자)
            description = strip_html_for_description(html_content, 150)
            # 따옴표 이스케이프
            description = description.replace('"', '\\"')

            # HTML → Markdown
            body_md, has_image = html_to_markdown(html_content)

            # 파일명
            file_name = f"{pub_date}-{slug}.md"
            file_path = os.path.join(OUTPUT_DIR, file_name)

            # tags JSON 표현
            tags_str = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
            title_escaped = title.replace('"', '\\"')

            # Frontmatter
            frontmatter_lines = [
                "---",
                f'title: "{title_escaped}"',
                f"pubDate: {pub_date}",
                f'description: "{description}"',
                f"tags: {tags_str}",
                'series: ""',
                'heroImage: ""',
                f"draft: {'true' if is_draft else 'false'}",
                "---",
                "",
            ]

            # 이미지 마이그레이션 주석
            if has_image:
                frontmatter_lines.append("<!-- TODO: migrate images -->")
                frontmatter_lines.append("")

            content_lines = frontmatter_lines + [body_md]
            file_content = "\n".join(content_lines)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)

            created.append((file_name, pub_date, title))

        except Exception as e:
            title_safe = ""
            try:
                title_safe = get_text(entry, ATOM, "title", f"entry[{idx}]")
            except:
                title_safe = f"entry[{idx}]"
            errors.append((title_safe, str(e)))
            print(f"  [ERROR] {title_safe}: {e}")

    # ── 결과 출력 ────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"변환 완료: {len(created)}개 생성, {len(errors)}개 오류, {skipped}개 건너뜀")
    print(f"{'='*60}")
    print("\n[생성된 파일 목록]")
    for fname, date, title in sorted(created):
        print(f"  {date}  {fname}")
        print(f"           {title}")

    if errors:
        print(f"\n[오류 목록]")
        for title, err in errors:
            print(f"  - {title}: {err}")

    return created, errors


if __name__ == "__main__":
    created, errors = parse_and_convert()
    print(f"\n총 {len(created)}개 파일이 {OUTPUT_DIR} 에 생성되었습니다.")
