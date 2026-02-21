import { useState } from 'react';
import * as apiClient from '../../api/client';
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
    <PixelCard static>
      <h3 style={{ marginBottom: 12 }}>Share Your Tale</h3>

      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="What adventures await, hero?"
        className="post-composer__textarea pixel-border"
      />

      <div className="post-composer__footer">
        <div className="post-composer__type">
          <span className="post-composer__type-label">Type:</span>
          <select
            value={postType}
            onChange={(e) => setPostType(e.target.value)}
            className="pixel-select"
            style={{ width: 'auto' }}
          >
            <option value="text">Text</option>
            <option value="adventure_log">Adventure Log</option>
            <option value="loot_drop">Loot Drop</option>
            <option value="character_art">Character Art</option>
          </select>
        </div>

        <div className="post-composer__actions">
          {error && <span className="text-red">{error}</span>}
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
