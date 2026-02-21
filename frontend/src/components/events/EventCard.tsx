import { useState } from 'react';
import * as apiClient from '../../api/client';
import type { Event } from '../../types';
import { colors } from '../../styles/theme';
import { PixelButton } from '../common/PixelButton';
import { PixelCard } from '../common/PixelCard';

interface EventCardProps {
  event: Event;
  onRsvp?: () => void;
}

function formatDateTime(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

const EVENT_TYPE_COLORS: Record<string, string> = {
  one_shot: colors.potionGreen,
  campaign_session: colors.darkPurple,
  tournament: colors.dragonRed,
  social: colors.lightGold,
};

export function EventCard({ event, onRsvp }: EventCardProps) {
  const [isRsvping, setIsRsvping] = useState(false);

  const handleRsvp = async () => {
    setIsRsvping(true);
    try {
      await apiClient.rsvpEvent(event.id, 'going');
      onRsvp?.();
    } catch {
      // silently fail
    } finally {
      setIsRsvping(false);
    }
  };

  const typeColor = EVENT_TYPE_COLORS[event.event_type] || colors.treasureGold;

  return (
    <PixelCard>
      <div className="event-card__header">
        <div className="flex-1">
          <h3 className="event-card__title">{event.title}</h3>
          <span
            className="badge"
            style={{ background: typeColor, color: colors.dungeonBlack }}
          >
            {event.event_type.replace('_', ' ')}
          </span>
        </div>

        <div style={{ textAlign: 'right', flexShrink: 0 }}>
          <div className="event-card__status-label">Status</div>
          <div
            className="event-card__status-value"
            style={{
              color: event.status === 'open' ? colors.potionGreen : colors.dimText,
            }}
          >
            {event.status}
          </div>
        </div>
      </div>

      {event.description && (
        <p className="event-card__description">{event.description}</p>
      )}

      <div className="event-card__details">
        <div>
          <span className="event-card__detail-key">When: </span>
          {formatDateTime(event.start_time)}
        </div>
        {event.location && (
          <div>
            <span className="event-card__detail-key">Where: </span>
            {event.location}
          </div>
        )}
        <div>
          <span className="event-card__detail-key">Players: </span>
          {event.going_count ?? 0}/{event.max_players ?? event.min_players}+
        </div>
        <div>
          <span className="event-card__detail-key">Organizer: </span>
          {event.organizer_username}
        </div>
      </div>

      {event.status === 'open' && (
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <PixelButton
            onClick={handleRsvp}
            disabled={isRsvping}
            variant="green"
            size="sm"
          >
            {isRsvping ? 'Joining...' : "I'm Going!"}
          </PixelButton>
        </div>
      )}
    </PixelCard>
  );
}
