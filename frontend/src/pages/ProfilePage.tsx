import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import * as apiClient from '../api/client';
import { useAuth } from '../hooks/useAuth';
import { useFeed } from '../hooks/useFeed';
import { PostCard } from '../components/feed/PostCard';
import { PixelCard } from '../components/common/PixelCard';
import { PixelButton } from '../components/common/PixelButton';
import { colors, fonts } from '../styles/theme';
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
      <div
        style={{
          fontFamily: fonts.heading,
          fontSize: '12px',
          color: colors.dragonRed,
          textAlign: 'center',
          padding: '60px',
        }}
      >
        {profileError}
      </div>
    );
  }

  if (!profile) {
    return (
      <div
        style={{
          fontFamily: fonts.heading,
          fontSize: '10px',
          color: colors.dimText,
          textAlign: 'center',
          padding: '60px',
        }}
      >
        Loading adventurer...
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Profile header */}
      <PixelCard>
        <div style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>
          {/* Avatar */}
          <div
            className="pixel-border"
            style={{
              width: '72px',
              height: '72px',
              background: colors.darkPurple,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontFamily: fonts.heading,
              fontSize: '28px',
              color: colors.treasureGold,
              flexShrink: 0,
            }}
          >
            {profile.display_name?.[0]?.toUpperCase() || profile.username[0].toUpperCase()}
          </div>

          <div style={{ flex: 1 }}>
            <h2
              style={{
                fontFamily: fonts.heading,
                fontSize: '14px',
                color: colors.treasureGold,
                marginBottom: '4px',
              }}
              className="gold-glow"
            >
              {profile.display_name || profile.username}
            </h2>
            <div
              style={{
                fontFamily: fonts.body,
                fontSize: '13px',
                color: colors.dimText,
                marginBottom: '8px',
              }}
            >
              @{profile.username}
              {profile.role && profile.role !== 'player' && (
                <span
                  style={{
                    marginLeft: '8px',
                    fontFamily: fonts.heading,
                    fontSize: '7px',
                    color: colors.dungeonBlack,
                    background: profile.role === 'admin' ? colors.dragonRed : colors.treasureGold,
                    padding: '2px 6px',
                  }}
                >
                  {profile.role.toUpperCase()}
                </span>
              )}
            </div>

            {profile.bio && (
              <p
                style={{
                  fontFamily: fonts.body,
                  fontSize: '13px',
                  color: colors.parchment,
                  lineHeight: '1.6',
                  marginBottom: '12px',
                }}
              >
                {profile.bio}
              </p>
            )}

            <div
              style={{
                display: 'flex',
                gap: '20px',
                fontFamily: fonts.body,
                fontSize: '12px',
                color: colors.dimText,
              }}
            >
              <span>
                <strong style={{ color: colors.parchment }}>
                  {profile.followers_count ?? 0}
                </strong>{' '}
                Followers
              </span>
              <span>
                <strong style={{ color: colors.parchment }}>
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

      {/* Posts */}
      <h3
        style={{
          fontFamily: fonts.heading,
          fontSize: '11px',
          color: colors.treasureGold,
        }}
      >
        ⚔ Tales & Scrolls
      </h3>

      {postsLoading && (
        <div
          style={{
            fontFamily: fonts.body,
            fontSize: '12px',
            color: colors.dimText,
            textAlign: 'center',
            padding: '20px',
          }}
        >
          Loading posts...
        </div>
      )}

      {!postsLoading && posts.length === 0 && (
        <div
          style={{
            fontFamily: fonts.body,
            fontSize: '13px',
            color: colors.dimText,
            textAlign: 'center',
            padding: '30px',
          }}
        >
          This adventurer has not yet written any tales.
        </div>
      )}

      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
