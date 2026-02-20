import axios from 'axios';
import type {
  AuthResponse,
  Campaign,
  Character,
  DiceRoll,
  Event,
  Notification,
  Post,
  User,
} from '../types';

const API_BASE = import.meta.env.VITE_API_URL || '/api/v1';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor: attach Bearer token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: handle 401 by attempting token refresh
let isRefreshing = false;
let failedQueue: Array<{
  resolve: (token: string) => void;
  reject: (err: unknown) => void;
}> = [];

function processQueue(error: unknown, token: string | null) {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token!);
    }
  });
  failedQueue = [];
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({
            resolve: (token: string) => {
              originalRequest.headers.Authorization = `Bearer ${token}`;
              resolve(api(originalRequest));
            },
            reject,
          });
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(error);
      }

      try {
        const { data } = await axios.post(`${API_BASE}/auth/refresh`, {
          refresh_token: refreshToken,
        });
        const newAccessToken = data.access_token;
        const newRefreshToken = data.refresh_token;

        localStorage.setItem('access_token', newAccessToken);
        localStorage.setItem('refresh_token', newRefreshToken);

        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        processQueue(null, newAccessToken);
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  },
);

// ─── Auth ────────────────────────────────────────────────────────────────────

export async function register(
  username: string,
  email: string,
  password: string,
  displayName?: string,
): Promise<AuthResponse> {
  const { data } = await api.post('/auth/register', {
    username,
    email,
    password,
    display_name: displayName,
  });
  return data;
}

export async function login(
  username: string,
  password: string,
): Promise<AuthResponse> {
  const { data } = await api.post('/auth/login', { username, password });
  return data;
}

export async function logout(refreshToken: string): Promise<void> {
  await api.post('/auth/logout', { refresh_token: refreshToken });
}

export async function getMe(): Promise<User> {
  const { data } = await api.get('/auth/me');
  return data;
}

export async function refreshTokens(
  refreshToken: string,
): Promise<{ access_token: string; refresh_token: string }> {
  const { data } = await api.post('/auth/refresh', {
    refresh_token: refreshToken,
  });
  return data;
}

// ─── Posts ───────────────────────────────────────────────────────────────────

export async function getPosts(
  authorId: number,
  limit = 50,
  offset = 0,
): Promise<Post[]> {
  const { data } = await api.get(`/posts/by/${authorId}`, {
    params: { limit, offset },
  });
  return data;
}

export async function createPost(
  content: string,
  postType = 'text',
  imageUrl?: string,
): Promise<Post> {
  const { data } = await api.post('/posts', {
    content,
    post_type: postType,
    image_url: imageUrl,
  });
  return data;
}

export async function getTimeline(limit = 50, offset = 0): Promise<Post[]> {
  const { data } = await api.get('/posts/timeline', {
    params: { limit, offset },
  });
  return data;
}

export async function getFeed(limit = 50, offset = 0): Promise<Post[]> {
  const { data } = await api.get('/posts/feed', {
    params: { limit, offset },
  });
  return data;
}

// ─── Events ──────────────────────────────────────────────────────────────────

export async function getEvents(): Promise<Event[]> {
  const { data } = await api.get('/events');
  return data;
}

export async function createEvent(eventData: {
  title: string;
  event_type?: string;
  description?: string;
  location?: string;
  start_time: string;
  end_time?: string;
  min_players?: number;
  max_players?: number;
}): Promise<Event> {
  const { data } = await api.post('/events', eventData);
  return data;
}

export async function rsvpEvent(
  eventId: number,
  status = 'going',
): Promise<void> {
  await api.post(`/events/${eventId}/rsvp`, { status });
}

// ─── Characters ──────────────────────────────────────────────────────────────

export async function getCharacters(): Promise<Character[]> {
  const { data } = await api.get('/characters/mine');
  return data;
}

export async function createCharacter(charData: {
  name: string;
  race?: string;
  class?: string;
  level?: number;
  strength?: number;
  dexterity?: number;
  constitution?: number;
  intelligence?: number;
  wisdom?: number;
  charisma?: number;
  hit_points?: number;
  armor_class?: number;
  backstory?: string;
}): Promise<Character> {
  const { data } = await api.post('/characters', charData);
  return data;
}

// ─── Campaigns ───────────────────────────────────────────────────────────────

export async function getCampaigns(): Promise<Campaign[]> {
  const { data } = await api.get('/campaigns');
  return data;
}

export async function createCampaign(campaignData: {
  name: string;
  description?: string;
  max_players?: number;
}): Promise<Campaign> {
  const { data } = await api.post('/campaigns', campaignData);
  return data;
}

export async function joinCampaign(
  campaignId: number,
  characterId?: number,
): Promise<void> {
  await api.post(`/campaigns/${campaignId}/join`, {
    character_id: characterId,
  });
}

// ─── Dice ────────────────────────────────────────────────────────────────────

export async function rollDice(
  expression: string,
  campaignId?: number,
): Promise<DiceRoll> {
  const { data } = await api.post('/dice/roll', {
    expression,
    campaign_id: campaignId,
  });
  return data;
}

export async function getDiceHistory(
  limit = 20,
  campaignId?: number,
): Promise<DiceRoll[]> {
  const { data } = await api.get('/dice/history', {
    params: { limit, campaign_id: campaignId },
  });
  return data;
}

// ─── Notifications ───────────────────────────────────────────────────────────

export async function getNotifications(): Promise<Notification[]> {
  const { data } = await api.get('/notifications');
  return data;
}

export async function getUnreadCount(): Promise<number> {
  const { data } = await api.get('/notifications/unread-count');
  return data.unread;
}

export async function markNotificationRead(
  notificationId: number,
): Promise<void> {
  await api.put(`/notifications/${notificationId}/read`);
}

export async function markAllNotificationsRead(): Promise<void> {
  await api.put('/notifications/read-all');
}

// ─── Users / Follows ─────────────────────────────────────────────────────────

export async function getUser(userId: number): Promise<User> {
  const { data } = await api.get(`/users/${userId}`);
  return data;
}

export async function searchUsers(query: string): Promise<User[]> {
  const { data } = await api.get('/users/search', { params: { q: query } });
  return data;
}

export async function followUser(userId: number): Promise<void> {
  await api.post(`/follows/${userId}`);
}

export async function unfollowUser(userId: number): Promise<void> {
  await api.delete(`/follows/${userId}`);
}

export default api;
