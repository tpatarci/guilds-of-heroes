interface SkeletonProps {
  variant?: 'text' | 'text-short' | 'heading' | 'avatar' | 'avatar-lg' | 'card';
  count?: number;
}

export function Skeleton({ variant = 'text', count = 1 }: SkeletonProps) {
  return (
    <>
      {Array.from({ length: count }, (_, i) => (
        <div key={i} className={`skeleton skeleton--${variant}`} />
      ))}
    </>
  );
}

export function PostCardSkeleton() {
  return (
    <div className="pixel-card pixel-border" style={{ padding: 20 }}>
      <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
        <Skeleton variant="avatar" />
        <div style={{ flex: 1 }}>
          <Skeleton variant="text-short" />
          <div className="skeleton skeleton--text" style={{ width: '30%', height: 10 }} />
        </div>
      </div>
      <Skeleton variant="text" count={3} />
      <Skeleton variant="text-short" />
    </div>
  );
}

export function CharacterCardSkeleton() {
  return (
    <div className="pixel-card pixel-border" style={{ padding: 20 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <div style={{ flex: 1 }}>
          <Skeleton variant="heading" />
          <Skeleton variant="text-short" />
        </div>
        <div className="skeleton" style={{ width: 50, height: 50 }} />
      </div>
      <div style={{ display: 'flex', gap: 16, marginBottom: 16 }}>
        <div className="skeleton" style={{ flex: 1, height: 50 }} />
        <div className="skeleton" style={{ flex: 1, height: 50 }} />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8 }}>
        {Array.from({ length: 6 }, (_, i) => (
          <div key={i} className="skeleton" style={{ height: 50 }} />
        ))}
      </div>
    </div>
  );
}

export function EventCardSkeleton() {
  return (
    <div className="pixel-card pixel-border" style={{ padding: 20 }}>
      <Skeleton variant="heading" />
      <Skeleton variant="text" count={2} />
      <Skeleton variant="text-short" />
    </div>
  );
}
