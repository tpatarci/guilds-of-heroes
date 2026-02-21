import { Link } from 'react-router-dom';
import type { Post } from '../../types';
import { PixelCard } from '../common/PixelCard';

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

interface PostCardProps {
  post: Post;
}

export function PostCard({ post }: PostCardProps) {
  return (
    <PixelCard>
      <div className="post-card__header">
        <div className="post-card__avatar pixel-border">
          {post.author.display_name?.[0]?.toUpperCase() ||
            post.author.username[0].toUpperCase()}
        </div>

        <div className="flex-1">
          <Link to={`/profile/${post.author_id}`} className="post-card__author-name">
            {post.author.display_name || post.author.username}
          </Link>
          <div className="post-card__username">@{post.author.username}</div>
        </div>

        <span className="post-card__time">{timeAgo(post.created_at)}</span>
      </div>

      <div className="post-card__content">{post.content}</div>

      {post.image_url && (
        <img
          src={post.image_url}
          alt="Post attachment"
          className="post-card__image"
        />
      )}

      {post.post_type && post.post_type !== 'text' && (
        <div style={{ marginTop: 10 }}>
          <span className="badge badge--gold">
            {post.post_type.replace(/_/g, ' ')}
          </span>
        </div>
      )}
    </PixelCard>
  );
}
