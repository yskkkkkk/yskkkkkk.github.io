import type { APIContext } from 'astro';
import { getCollection } from 'astro:content';
import { SITE_TITLE, SITE_DESCRIPTION, SITE_URL } from '../consts';
import { formatShortDate } from '../lib/utils';

export async function GET(context: APIContext) {
  const base = context.site?.href.replace(/\/$/, '') ?? SITE_URL;

  // 본문이 있는 글만 — externalUrl 스텁은 원문이 외부에 있어 제외
  const posts = (await getCollection('blog', ({ data }) => !data.draft && !data.externalUrl))
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  const documents = posts.map((post) => {
    const meta = [
      `URL: ${base}/blog/${post.slug}/`,
      `작성일: ${formatShortDate(post.data.pubDate)}`,
    ];
    if (post.data.updatedDate) {
      meta.push(`수정일: ${formatShortDate(post.data.updatedDate)}`);
    }
    if (post.data.series) {
      meta.push(`시리즈: ${post.data.series}`);
    }
    if (post.data.tags.length > 0) {
      meta.push(`태그: ${post.data.tags.join(', ')}`);
    }

    return [
      `# ${post.data.title}`,
      '',
      ...meta,
      '',
      post.data.description,
      '',
      '---',
      '',
      post.body.trim(),
    ].join('\n');
  });

  const body = [
    `<!--`,
    `${SITE_TITLE} — 전체 글 본문 모음`,
    `${SITE_DESCRIPTION}`,
    ``,
    `이 파일은 AI 도구가 사이트 전체를 한 번에 읽을 수 있도록 생성됩니다.`,
    `글 목록만 필요하면 ${base}/llms.txt 를 사용하세요.`,
    ``,
    `총 ${posts.length}편 (최신순). 각 글은 "====" 구분선으로 나뉩니다.`,
    `-->`,
    '',
    documents.join('\n\n====\n\n'),
    '',
  ].join('\n');

  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
