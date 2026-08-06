import type { APIContext } from 'astro';
import { getCollection } from 'astro:content';
import { SITE_TITLE, SITE_DESCRIPTION, SITE_URL } from '../consts';
import { SERIES_META, formatShortDate } from '../lib/utils';

export async function GET(context: APIContext) {
  const base = context.site?.href.replace(/\/$/, '') ?? SITE_URL;

  const posts = (await getCollection('blog', ({ data }) => !data.draft))
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  const line = (post: (typeof posts)[number]) => {
    const url = post.data.externalUrl ?? `${base}/blog/${post.slug}/`;
    const date = formatShortDate(post.data.pubDate);
    return `- [${post.data.title}](${url}) — ${post.data.description} (${date})`;
  };

  const sections: string[] = [];

  // 시리즈별 묶음 (SERIES_META 정의 순서를 따름)
  for (const [name, meta] of Object.entries(SERIES_META)) {
    const inSeries = posts
      .filter((p) => p.data.series === name)
      .sort((a, b) => a.data.pubDate.valueOf() - b.data.pubDate.valueOf());
    if (inSeries.length === 0) continue;

    sections.push(
      [
        `## ${name}`,
        '',
        `${meta.description}`,
        '',
        `시리즈 페이지: ${base}/series/${meta.slug}/`,
        '',
        ...inSeries.map(line),
      ].join('\n')
    );
  }

  // 시리즈에 속하지 않은 글
  const standalone = posts.filter((p) => !p.data.series);
  if (standalone.length > 0) {
    sections.push(['## 그 외 글', '', ...standalone.map(line)].join('\n'));
  }

  const hasBody = posts.filter((p) => !p.data.externalUrl).length;

  const body = [
    `# ${SITE_TITLE}`,
    '',
    `> ${SITE_DESCRIPTION}`,
    '',
    `총 ${posts.length}편의 글이 있습니다. 이 중 ${hasBody}편은 이 사이트에 본문이 있고,`,
    `나머지는 외부 프로젝트 블로그로 연결되는 글입니다.`,
    '',
    `전체 본문을 한 번에 읽으려면 ${base}/llms-full.txt 를 사용하세요.`,
    '',
    sections.join('\n\n'),
    '',
  ].join('\n');

  return new Response(body, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
