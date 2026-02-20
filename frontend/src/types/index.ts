export interface User {
  id: number;
  username: string;
  email?: string;
  display_name: string;
  role: string;
  avatar: string | null;
  bio: string;
  email_verified?: boolean;
  created_at: string;
  followers_count?: number;
  following_count?: number;
}

export interface Post {
  id: number;
  author_id: number;
  content: string;
  post_type: string;
  image_url: string | null;
  created_at: string;
  author: {
    username: string;
    display_name: string;
    avatar: string | null;
  };
}

export interface Event {
  id: number;
  organizer_id: number;
  organizer_username: string;
  title: string;
  description: string;
  event_type: string;
  location: string | null;
  start_time: string;
  end_time: string | null;
  min_players: number;
  max_players: number | null;
  status: string;
  going_count?: number;
  rsvps?: RSVP[];
  created_at: string;
}

export interface RSVP {
  id: number;
  event_id: number;
  user_id: number;
  status: string;
  username: string;
  display_name: string;
}

export interface Character {
  id: number;
  owner_id: number;
  name: string;
  race: string;
  class: string;
  level: number;
  ability_scores: Record<string, number>;
  hit_points: number;
  armor_class: number;
  backstory: string;
  portrait: string | null;
  campaign_id: number | null;
  created_at: string;
}

export interface Campaign {
  id: number;
  dm_id: number;
  dm_username: string;
  name: string;
  description: string;
  status: string;
  max_players: number;
  members?: CampaignMember[];
  member_count?: number;
  created_at: string;
}

export interface CampaignMember {
  campaign_id: number;
  user_id: number;
  username: string;
  display_name: string;
  role: string;
}

export interface SessionLog {
  id: number;
  campaign_id: number;
  author_id: number;
  author_username: string;
  session_number: number;
  title: string;
  summary: string;
  session_date: string;
}

export interface DiceRoll {
  id?: number;
  expression: string;
  results: number[];
  total: number;
  campaign_id?: number | null;
  created_at?: string;
}

export interface Notification {
  id: number;
  user_id: number;
  type: string;
  title: string;
  body: string;
  link: string | null;
  is_read: boolean;
  source_user_id: number | null;
  created_at: string;
}

export interface AuthResponse {
  user: User;
  access_token: string;
  refresh_token: string;
}
