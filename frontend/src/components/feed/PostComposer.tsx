import { useState } from 'react';
import * as apiClient from '../../api/client';
import { colors, fonts } from '../../styles/theme';
import { PixelButton } from '../common/PixelButton';
import { PixelCard } from '../common/PixelCard';

interface PostComposerProps {
  onPostCreated: () => void;
}

export function PostComposer({ onPostCreated }: PostComposerProps) {
  const [content, setContent] = useState('');
  const [postType, setPostType] = useState('text');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!content.trim()) return;

    setIsSubmitting(true);
    setError(null);

    try {
      await apiClient.createPost(content.trim(), postType);
      setContent('');
      setPostType('text');
      onPostCreated();
    } catch (err) {
      const message =
        err instanceof Error ? err.message : 'Failed to create post';
      setError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <PixelCard>
      <h3
        style={{
          fontFamily: fonts.heading,
          fontSize: '11px',
          color: colors.treasureGold,
          marginBottom: '12px',
        }}
      >
        Share Your Tale
      </h3>

      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="What adventures await, hero?"
        className="pixel-border"
        style={{
          width: '100%',
          minHeight: '100px',
          background: colors.dungeonBlack,
          color: colors.parchment,
          fontFamily: fonts.body,
          fontSize: '14px',
          padding: '12px',
          border: 'none',
          outline: 'none',
          resize: 'vertical',
          marginBottom: '12px',
        }}
      />

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '12px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <label
            style={{
              fontFamily: fonts.heading,
              fontSize: '8px',
              color: colors.dimText,
              textTransform: 'uppercase',
            }}
          >
            Type:
          </label>
          <select
            value={postType}
            onChange={(e) => setPostType(e.target.value)}
            style={{
              background: colors.dungeonBlack,
              color: colors.parchment,
              fontFamily: fonts.body,
              fontSize: '12px',
              padding: '4px 8px',
              border: `1px solid ${colors.treasureGold}`,
              outline: 'none',
              cursor: 'pointer',
            }}
          >
            <option value="text">Text</option>
            <option value="adventure_log">Adventure Log</option>
            <option value="loot_drop">Loot Drop</option>
            <option value="character_art">Character Art</option>
          </select>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {error && (
            <span
              style={{
                fontFamily: fonts.body,
                fontSize: '11px',
                color: colors.dragonRed,
              }}
            >
              {error}
            </span>
          )}
          <PixelButton
            onClick={handleSubmit}
            disabled={isSubmitting || !content.trim()}
            size="sm"
          >
            {isSubmitting ? 'Posting...' : 'Post'}
          </PixelButton>
        </div>
      </div>
    </PixelCard>
  );
}
