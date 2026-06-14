export function readingTime(body: string | undefined): number {
  const stripped = (body ?? '')
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

export const SERIES_META: Record<string, { slug: string; description: string; heroBg: string }> = {
  '피카밈 개발기': {
    slug: 'pika-a-meme',
    description: '가벼운 가챠형 밈 서비스 뒤에 실무 수준 백엔드를 의도적으로 설계한 1개월 풀스택 기록. 토이 프로젝트에도 Clean Architecture·DDD를 적용한 이유, 분산 락 기반 하트 동시성 제어, Redis 캐시·Rate Limiting·OAuth2 디버깅까지 기술적 선택과 실패를 솔직하게 담았습니다.',
    heroBg: '#0e0c10',
  },
  'Pet-Pass 개발기': {
    slug: 'pet-pass',
    description: 'AI 페어코딩만으로 서비스를 처음부터 끝까지 출시할 수 있는지 검증한 첫 풀스택 실험. 웹 스크래핑의 한계를 공공데이터 파이프라인으로 전환하고, GitHub Actions로 사람 손 없이 매일 데이터가 갱신되는 구조를 만든 과정을 기록합니다.',
    heroBg: 'linear-gradient(135deg,#3d2a0f 0%,#6b4c1e 55%,#a87840 100%)',
  },
  'Redis 프로젝트 회고': {
    slug: 'redis-project',
    description: '실제 대규모 서비스에 Redis 캐시를 도입하면서 겪은 기술적 문제들과 해결 과정. 분산 캐시 동기화, 동시성 이슈, 대규모 장애 대응까지.',
    heroBg: 'linear-gradient(135deg,#7f1d1d 0%,#b91c1c 55%,#dc2626 100%)',
  },
  '백기선 live-study (2020)': {
    slug: 'live-study',
    description: '백기선님과 함께한 자바 라이브 스터디 학습 기록. 3주차부터 12주차까지 연산자, 제어문, 클래스, 상속, 인터페이스, 예외 처리, 멀티쓰레드, 애노테이션 등을 정리했습니다.',
    heroBg: 'linear-gradient(135deg,#78350f 0%,#b45309 55%,#d97706 100%)',
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
