import { useFeed } from '../hooks/useFeed';
import { useAuth } from '../hooks/useAuth';
import { PostComposer } from '../components/feed/PostComposer';
import { PostCard } from '../components/feed/PostCard';
import { PixelButton } from '../components/common/PixelButton';
import { PostCardSkeleton } from '../components/common/Skeleton';
import { SwordIcon } from '../components/common/Icons';

export default function FeedPage() {
  const { user } = useAuth();
  const { posts, isLoading, error, hasMore, loadMore, refresh } = useFeed({
    mode: 'feed',
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div className="page-header">
        <h2 className="page-title">
          <SwordIcon size={18} />
          The Tavern Board
        </h2>
      </div>

      {user && <PostComposer onPostCreated={refresh} />}

      {error && <div className="error-banner">{error}</div>}

      {isLoading && posts.length === 0 && (
        <>
          <PostCardSkeleton />
          <PostCardSkeleton />
          <PostCardSkeleton />
        </>
      )}

      {!isLoading && posts.length === 0 && !error && (
        <div className="empty-state">
          The tavern board is empty.<br />
          Follow other adventurers to see their tales here.
        </div>
      )}

      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}

      {hasMore && posts.length > 0 && (
        <div className="text-center" style={{ padding: 16 }}>
          <PixelButton onClick={loadMore} disabled={isLoading} variant="gold">
            {isLoading ? 'Loading...' : 'Load More Tales'}
          </PixelButton>
        </div>
      )}
    </div>
  );
}
