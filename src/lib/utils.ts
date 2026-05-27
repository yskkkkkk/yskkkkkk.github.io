export function readingTime(body: string): number {
  const stripped = body
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/`[^`]*`/g, ' ')
    .replace(/!\[.*?\]\(.*?\)/g, ' ')
    .replace(/\[.*?\]\(.*?\)/g, ' ');
  const words = stripped.split(/\s+/).filter(w => w.length > 0).length;
  return Math.max(1, Math.round(words / 200));
}

export function formatDate(date: Date): string {
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

const SERIES_SLUG_MAP: Record<string, string> = {
  'Redis 프로젝트 회고': 'redis-project',
  '백기선 live-study': 'live-study',
};

export function seriesSlug(name: string): string {
  return (
    SERIES_SLUG_MAP[name] ??
    name
      .toLowerCase()
      .replace(/[^\w가-힣\s]/g, '')
      .replace(/\s+/g, '-')
      .replace(/^-|-$/g, '')
  );
}
