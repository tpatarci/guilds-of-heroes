import { Link } from 'react-router-dom';
import type { Post } from '../../types';
import { colors, fonts } from '../../styles/theme';
import { PixelCard } from '../common/PixelCard';

interface PostCardProps {
  post: Post;
}

function timeAgo(dateString: string): string {
  const now = new Date();
  const date = new Date(dateString);
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
  return date.toLocaleDateString();
}

export function PostCard({ post }: PostCardProps) {
  return (
    <PixelCard>
      {/* Author header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          marginBottom: '12px',
        }}
      >
        {/* Avatar placeholder */}
        <div
          style={{
            width: '36px',
            height: '36px',
            background: colors.darkPurple,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontFamily: fonts.heading,
            fontSize: '14px',
            color: colors.treasureGold,
            flexShrink: 0,
          }}
          className="pixel-border"
        >
          {post.author.display_name?.[0]?.toUpperCase() ||
            post.author.username[0].toUpperCase()}
        </div>

        <div style={{ flex: 1 }}>
          <Link
            to={`/profile/${post.author_id}`}
            style={{
              fontFamily: fonts.heading,
              fontSize: '10px',
              color: colors.lightGold,
              textDecoration: 'none',
            }}
          >
            {post.author.display_name || post.author.username}
          </Link>
          <div
            style={{
              fontFamily: fonts.body,
              fontSize: '11px',
              color: colors.dimText,
            }}
          >
            @{post.author.username}
          </div>
        </div>

        <span
          style={{
            fontFamily: fonts.body,
            fontSize: '11px',
            color: colors.dimText,
          }}
        >
          {timeAgo(post.created_at)}
        </span>
      </div>

      {/* Post content */}
      <div
        style={{
          fontFamily: fonts.body,
          fontSize: '14px',
          color: colors.parchment,
          lineHeight: '1.6',
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
        }}
      >
        {post.content}
      </div>

      {/* Post image */}
      {post.image_url && (
        <img
          src={post.image_url}
          alt="Post attachment"
          style={{
            maxWidth: '100%',
            marginTop: '12px',
            border: `2px solid ${colors.treasureGold}`,
          }}
        />
      )}

      {/* Post type badge */}
      {post.post_type && post.post_type !== 'text' && (
        <div style={{ marginTop: '10px' }}>
          <span
            style={{
              fontFamily: fonts.heading,
              fontSize: '7px',
              color: colors.dungeonBlack,
              background: colors.treasureGold,
              padding: '3px 8px',
              textTransform: 'uppercase',
            }}
          >
            {post.post_type}
          </span>
        </div>
      )}
    </PixelCard>
  );
}
