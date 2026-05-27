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

export const SERIES_META: Record<string, { slug: string; description: string }> = {
  'Redis 프로젝트 회고': {
    slug: 'redis-project',
    description: '실제 대규모 서비스에 Redis 캐시를 도입하면서 겪은 기술적 문제들과 해결 과정. 분산 캐시 동기화, 동시성 이슈, 대규모 장애 대응까지.',
  },
  '백기선 live-study (2020)': {
    slug: 'live-study',
    description: '백기선님과 함께한 자바 라이브 스터디 학습 기록. 3주차부터 12주차까지 연산자, 제어문, 클래스, 상속, 인터페이스, 예외 처리, 멀티쓰레드, 애노테이션 등을 정리했습니다.',
  },
};

const SERIES_SLUG_MAP: Record<string, string> = Object.fromEntries(
  Object.entries(SERIES_META).map(([name, m]) => [name, m.slug])
);

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
