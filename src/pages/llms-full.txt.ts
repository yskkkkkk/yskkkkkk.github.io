import type { APIContext } from 'astro';
import { getCollection } from 'astro:content';
import { SITE_TITLE, SITE_DESCRIPTION, SITE_URL } from '../consts';
import { formatShortDate } from '../lib/utils';

export async function GET(context: APIContext) {
  const base = context.site?.href.replace(/\/$/, '') ?? SITE_URL;

  // 본문이 있는 글만 — externalUrl 스텁은 원문이 외부에 있어 제외
  const posts = (await getCollection('blog', ({ data }) => !data.draft && !data.externalUrl))
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  const total = posts.length;

  const documents = posts.map((post, i) => {
    const meta = [
      `Title: ${post.data.title}`,
      `URL: ${base}/blog/${post.slug}/`,
      `Date: ${formatShortDate(post.data.pubDate)}`,
    ];
    if (post.data.updatedDate) {
      meta.push(`Updated: ${formatShortDate(post.data.updatedDate)}`);
    }
    if (post.data.series) {
      meta.push(`Series: ${post.data.series}`);
    }
    if (post.data.tags.length > 0) {
      meta.push(`Tags: ${post.data.tags.join(', ')}`);
    }
    meta.push(`Summary: ${post.data.description}`);

    return [
      // 본문에도 마크다운 헤딩(#)이 등장하므로, 문서 경계는 이 마커로만 판단합니다.
      `===== POST ${i + 1}/${total} =====`,
      ...meta,
      '',
      post.body.trim(),
    ].join('\n');
  });

  const body = [
    `${SITE_TITLE} — 전체 글 본문 모음`,
    `${SITE_DESCRIPTION}`,
    '',
    `이 파일은 AI 도구가 사이트 전체를 한 번에 읽을 수 있도록 생성됩니다.`,
    `글 목록만 필요하면 ${base}/llms.txt 를 사용하세요.`,
    '',
    `총 ${total}편, 최신순입니다.`,
    `각 글은 "===== POST n/${total} =====" 줄로 시작합니다.`,
    `본문에도 마크다운 헤딩(#)이 나오므로 문서 경계는 이 마커로만 판단하세요.`,
    `마지막 글은 POST ${total}/${total} 입니다. 여기까지 읽지 못했다면 내용이 잘린 것입니다.`,
    '',
    documents.join('\n\n'),
    '',
  ].join('\n');

  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
