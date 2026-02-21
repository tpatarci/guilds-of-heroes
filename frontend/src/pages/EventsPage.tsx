import { useEffect, useState } from 'react';
import * as apiClient from '../api/client';
import { useAuth } from '../hooks/useAuth';
import { EventCard } from '../components/events/EventCard';
import { PixelButton } from '../components/common/PixelButton';
import { PixelCard } from '../components/common/PixelCard';
import { PixelInput, PixelTextarea } from '../components/common/PixelInput';
import { ScrollIcon } from '../components/common/Icons';
import { EventCardSkeleton } from '../components/common/Skeleton';
import type { Event } from '../types';

export default function EventsPage() {
  const { user } = useAuth();
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [title, setTitle] = useState('');
  const [eventType, setEventType] = useState('one_shot');
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [startTime, setStartTime] = useState('');
  const [maxPlayers, setMaxPlayers] = useState('');

  async function loadEvents() {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiClient.getEvents();
      setEvents(data);
    } catch {
      setError('Failed to load events');
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadEvents();
  }, []);

  async function handleCreateEvent(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim() || !startTime) return;

    setIsSubmitting(true);
    setFormError(null);
    try {
      await apiClient.createEvent({
        title: title.trim(),
        event_type: eventType,
        description: description.trim() || undefined,
        location: location.trim() || undefined,
        start_time: new Date(startTime).toISOString(),
        max_players: maxPlayers ? parseInt(maxPlayers, 10) : undefined,
        min_players: 2,
      });
      setTitle('');
      setDescription('');
      setLocation('');
      setStartTime('');
      setMaxPlayers('');
      setShowForm(false);
      await loadEvents();
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to create event';
      setFormError(msg);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div className="page-header">
        <h2 className="page-title">
          <ScrollIcon size={18} />
          Quest Board
        </h2>
        {user && (
          <PixelButton
            variant="green"
            size="sm"
            onClick={() => setShowForm((v) => !v)}
          >
            {showForm ? 'Cancel' : '+ Post Quest'}
          </PixelButton>
        )}
      </div>

      {showForm && (
        <PixelCard static>
          <h3 style={{ marginBottom: 16 }}>Post a New Quest</h3>
          <form onSubmit={handleCreateEvent} className="form-group">
            <PixelInput
              label="Quest Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="The Dragon's Lair..."
              required
            />

            <div>
              <label className="pixel-input__label">Quest Type</label>
              <select
                value={eventType}
                onChange={(e) => setEventType(e.target.value)}
                className="pixel-select"
              >
                <option value="one_shot">One Shot</option>
                <option value="campaign_session">Campaign Session</option>
                <option value="tournament">Tournament</option>
                <option value="social">Social Gathering</option>
              </select>
            </div>

            <PixelTextarea
              label="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Brave adventurers needed..."
            />

            <PixelInput
              label="Location / Platform"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="Roll20, Discord, Local Tavern..."
            />

            <PixelInput
              label="Start Time"
              type="datetime-local"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
              required
            />

            <PixelInput
              label="Max Players"
              type="number"
              value={maxPlayers}
              onChange={(e) => setMaxPlayers(e.target.value)}
              placeholder="6"
              min="1"
              max="20"
            />

            {formError && <div className="error-banner">{formError}</div>}

            <div className="form-actions">
              <PixelButton
                type="button"
                variant="red"
                size="sm"
                onClick={() => setShowForm(false)}
              >
                Cancel
              </PixelButton>
              <PixelButton
                type="submit"
                variant="gold"
                size="sm"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Posting...' : 'Post Quest'}
              </PixelButton>
            </div>
          </form>
        </PixelCard>
      )}

      {error && <div className="error-banner">{error}</div>}

      {isLoading && (
        <>
          <EventCardSkeleton />
          <EventCardSkeleton />
          <EventCardSkeleton />
        </>
      )}

      {!isLoading && events.length === 0 && !error && (
        <div className="empty-state">
          No quests on the board.<br />
          Be the first to post one!
        </div>
      )}

      {events.map((event) => (
        <EventCard key={event.id} event={event} onRsvp={loadEvents} />
      ))}
    </div>
  );
}
