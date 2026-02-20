import { useCallback, useEffect, useState } from 'react';
import * as apiClient from '../api/client';
import type { Post } from '../types';

interface UseFeedOptions {
  mode: 'timeline' | 'feed' | 'user';
  userId?: number;
  limit?: number;
}

interface UseFeedReturn {
  posts: Post[];
  isLoading: boolean;
  error: string | null;
  hasMore: boolean;
  loadMore: () => void;
  refresh: () => void;
}

export function useFeed({
  mode,
  userId,
  limit = 20,
}: UseFeedOptions): UseFeedReturn {
  const [posts, setPosts] = useState<Post[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(true);

  const fetchPosts = useCallback(
    async (currentOffset: number, append: boolean) => {
      setIsLoading(true);
      setError(null);
      try {
        let result: Post[];
        if (mode === 'feed') {
          result = await apiClient.getFeed(limit, currentOffset);
        } else if (mode === 'user' && userId) {
          result = await apiClient.getPosts(userId, limit, currentOffset);
        } else {
          result = await apiClient.getTimeline(limit, currentOffset);
        }

        if (result.length < limit) {
          setHasMore(false);
        }

        if (append) {
          setPosts((prev) => [...prev, ...result]);
        } else {
          setPosts(result);
        }
      } catch (err) {
        const message =
          err instanceof Error ? err.message : 'Failed to load posts';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    },
    [mode, userId, limit],
  );

  useEffect(() => {
    setOffset(0);
    setHasMore(true);
    fetchPosts(0, false);
  }, [fetchPosts]);

  const loadMore = useCallback(() => {
    if (!isLoading && hasMore) {
      const newOffset = offset + limit;
      setOffset(newOffset);
      fetchPosts(newOffset, true);
    }
  }, [isLoading, hasMore, offset, limit, fetchPosts]);

  const refresh = useCallback(() => {
    setOffset(0);
    setHasMore(true);
    fetchPosts(0, false);
  }, [fetchPosts]);

  return { posts, isLoading, error, hasMore, loadMore, refresh };
}
