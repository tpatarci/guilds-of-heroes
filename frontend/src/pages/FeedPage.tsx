import { useFeed } from '../hooks/useFeed';
import { useAuth } from '../hooks/useAuth';
import { PostComposer } from '../components/feed/PostComposer';
import { PostCard } from '../components/feed/PostCard';
import { colors, fonts } from '../styles/theme';
import { PixelButton } from '../components/common/PixelButton';

export default function FeedPage() {
  const { user } = useAuth();
  const { posts, isLoading, error, hasMore, loadMore, refresh } = useFeed({
    mode: 'feed',
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <h2
        style={{
          fontFamily: fonts.heading,
          fontSize: '14px',
          color: colors.treasureGold,
          marginBottom: '8px',
        }}
      >
        ⚔ The Tavern Board
      </h2>

      {user && <PostComposer onPostCreated={refresh} />}

      {error && (
        <div
          style={{
            fontFamily: fonts.body,
            fontSize: '13px',
            color: colors.dragonRed,
            padding: '12px',
            border: `1px solid ${colors.dragonRed}`,
            background: 'rgba(192, 57, 43, 0.1)',
          }}
        >
          {error}
        </div>
      )}

      {isLoading && posts.length === 0 && (
        <div
          style={{
            fontFamily: fonts.heading,
            fontSize: '10px',
            color: colors.dimText,
            textAlign: 'center',
            padding: '40px',
          }}
        >
          Loading scrolls...
        </div>
      )}

      {!isLoading && posts.length === 0 && !error && (
        <div
          style={{
            fontFamily: fonts.body,
            fontSize: '14px',
            color: colors.dimText,
            textAlign: 'center',
            padding: '40px',
            lineHeight: '2',
          }}
        >
          The tavern board is empty.<br />
          Follow other adventurers to see their tales here.
        </div>
      )}

      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}

      {hasMore && posts.length > 0 && (
        <div style={{ textAlign: 'center', padding: '16px' }}>
          <PixelButton onClick={loadMore} disabled={isLoading} variant="gold">
            {isLoading ? 'Loading...' : 'Load More Tales'}
          </PixelButton>
        </div>
      )}
    </div>
  );
}
