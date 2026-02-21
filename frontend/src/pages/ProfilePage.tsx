import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import * as apiClient from '../api/client';
import { useAuth } from '../hooks/useAuth';
import { useFeed } from '../hooks/useFeed';
import { PostCard } from '../components/feed/PostCard';
import { PixelCard } from '../components/common/PixelCard';
import { PixelButton } from '../components/common/PixelButton';
import { PostCardSkeleton } from '../components/common/Skeleton';
import { Skeleton } from '../components/common/Skeleton';
import { SwordIcon } from '../components/common/Icons';
import { colors } from '../styles/theme';
import type { User } from '../types';

export default function ProfilePage() {
  const { userId } = useParams<{ userId: string }>();
  const { user: currentUser } = useAuth();
  const profileId = parseInt(userId ?? '0', 10);

  const [profile, setProfile] = useState<User | null>(null);
  const [isFollowing, setIsFollowing] = useState(false);
  const [followLoading, setFollowLoading] = useState(false);
  const [profileError, setProfileError] = useState<string | null>(null);

  const { posts, isLoading: postsLoading } = useFeed({
    mode: 'user',
    userId: profileId,
  });

  useEffect(() => {
    if (!profileId) return;
    apiClient
      .getUser(profileId)
      .then(setProfile)
      .catch(() => setProfileError('Adventurer not found'));
  }, [profileId]);

  const isOwnProfile = currentUser?.id === profileId;

  async function handleFollowToggle() {
    if (!profile) return;
    setFollowLoading(true);
    try {
      if (isFollowing) {
        await apiClient.unfollowUser(profile.id);
        setIsFollowing(false);
      } else {
        await apiClient.followUser(profile.id);
        setIsFollowing(true);
      }
    } catch {
      // ignore
    } finally {
      setFollowLoading(false);
    }
  }

  if (profileError) {
    return (
      <div className="empty-state" style={{ color: colors.dragonRed }}>
        {profileError}
      </div>
    );
  }

  if (!profile) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
        <PixelCard static>
          <div style={{ display: 'flex', gap: 20 }}>
            <Skeleton variant="avatar-lg" />
            <div style={{ flex: 1 }}>
              <Skeleton variant="heading" />
              <Skeleton variant="text-short" />
              <Skeleton variant="text" />
            </div>
          </div>
        </PixelCard>
        <PostCardSkeleton />
        <PostCardSkeleton />
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <PixelCard static>
        <div className="profile-header">
          <div className="profile-avatar pixel-border">
            {profile.display_name?.[0]?.toUpperCase() || profile.username[0].toUpperCase()}
          </div>

          <div className="flex-1">
            <h2 className="profile-name gold-glow">
              {profile.display_name || profile.username}
            </h2>
            <div className="profile-username">
              @{profile.username}
              {profile.role && profile.role !== 'player' && (
                <span
                  className={`badge ${profile.role === 'admin' ? 'badge--red' : 'badge--gold'}`}
                  style={{ marginLeft: 8 }}
                >
                  {profile.role.toUpperCase()}
                </span>
              )}
            </div>

            {profile.bio && (
              <p className="profile-bio">{profile.bio}</p>
            )}

            <div className="profile-stats">
              <span>
                <strong className="profile-stats__count">
                  {profile.followers_count ?? 0}
                </strong>{' '}
                Followers
              </span>
              <span>
                <strong className="profile-stats__count">
                  {profile.following_count ?? 0}
                </strong>{' '}
                Following
              </span>
            </div>
          </div>

          {!isOwnProfile && currentUser && (
            <PixelButton
              variant={isFollowing ? 'red' : 'green'}
              size="sm"
              onClick={handleFollowToggle}
              disabled={followLoading}
            >
              {isFollowing ? 'Unfollow' : 'Follow'}
            </PixelButton>
          )}
        </div>
      </PixelCard>

      <h3 className="page-title" style={{ marginBottom: 4 }}>
        <SwordIcon size={16} />
        Tales & Scrolls
      </h3>

      {postsLoading && (
        <>
          <PostCardSkeleton />
          <PostCardSkeleton />
        </>
      )}

      {!postsLoading && posts.length === 0 && (
        <div className="empty-state">
          This adventurer has not yet written any tales.
        </div>
      )}

      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
