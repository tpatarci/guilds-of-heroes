import { useState } from 'react';
import * as apiClient from '../../api/client';
import type { Event } from '../../types';
import { colors, fonts } from '../../styles/theme';
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
      {/* Header row */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          marginBottom: '12px',
        }}
      >
        <div style={{ flex: 1 }}>
          <h3
            style={{
              fontFamily: fonts.heading,
              fontSize: '11px',
              color: colors.treasureGold,
              marginBottom: '6px',
            }}
          >
            {event.title}
          </h3>
          <span
            style={{
              fontFamily: fonts.heading,
              fontSize: '7px',
              color: colors.dungeonBlack,
              background: typeColor,
              padding: '2px 8px',
              textTransform: 'uppercase',
            }}
          >
            {event.event_type.replace('_', ' ')}
          </span>
        </div>

        <div
          style={{
            textAlign: 'right',
            flexShrink: 0,
          }}
        >
          <div
            style={{
              fontFamily: fonts.heading,
              fontSize: '8px',
              color: colors.dimText,
              textTransform: 'uppercase',
            }}
          >
            Status
          </div>
          <div
            style={{
              fontFamily: fonts.heading,
              fontSize: '10px',
              color:
                event.status === 'open' ? colors.potionGreen : colors.dimText,
              textTransform: 'uppercase',
            }}
          >
            {event.status}
          </div>
        </div>
      </div>

      {/* Description */}
      {event.description && (
        <p
          style={{
            fontFamily: fonts.body,
            fontSize: '13px',
            color: colors.parchment,
            lineHeight: '1.6',
            marginBottom: '12px',
          }}
        >
          {event.description}
        </p>
      )}

      {/* Details row */}
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '16px',
          marginBottom: '12px',
          fontFamily: fonts.body,
          fontSize: '12px',
          color: colors.dimText,
        }}
      >
        <div>
          <span style={{ color: colors.treasureGold }}>When: </span>
          {formatDateTime(event.start_time)}
        </div>
        {event.location && (
          <div>
            <span style={{ color: colors.treasureGold }}>Where: </span>
            {event.location}
          </div>
        )}
        <div>
          <span style={{ color: colors.treasureGold }}>Players: </span>
          {event.going_count ?? 0}/{event.max_players ?? event.min_players}+
        </div>
        <div>
          <span style={{ color: colors.treasureGold }}>Organizer: </span>
          {event.organizer_username}
        </div>
      </div>

      {/* RSVP button */}
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
