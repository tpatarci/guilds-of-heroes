import { useEffect, useState } from 'react';
import * as apiClient from '../api/client';
import { useAuth } from '../hooks/useAuth';
import { PixelButton } from '../components/common/PixelButton';
import { PixelCard } from '../components/common/PixelCard';
import { PixelInput, PixelTextarea } from '../components/common/PixelInput';
import { CampaignIcon } from '../components/common/Icons';
import { EventCardSkeleton } from '../components/common/Skeleton';
import { colors } from '../styles/theme';
import type { Campaign } from '../types';

const STATUS_COLORS: Record<string, string> = {
  active: colors.potionGreen,
  paused: colors.treasureGold,
  completed: colors.dimText,
  archived: colors.dragonRed,
};

export default function CampaignsPage() {
  const { user } = useAuth();
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [joiningId, setJoiningId] = useState<number | null>(null);

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [maxPlayers, setMaxPlayers] = useState('6');

  async function loadCampaigns() {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiClient.getCampaigns();
      setCampaigns(data);
    } catch {
      setError('Failed to load campaigns');
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadCampaigns();
  }, []);

  async function handleCreateCampaign(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim()) return;

    setIsSubmitting(true);
    setFormError(null);
    try {
      await apiClient.createCampaign({
        name: name.trim(),
        description: description.trim() || undefined,
        max_players: parseInt(maxPlayers, 10) || 6,
      });
      setName('');
      setDescription('');
      setMaxPlayers('6');
      setShowForm(false);
      await loadCampaigns();
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to create campaign';
      setFormError(msg);
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleJoin(campaignId: number) {
    setJoiningId(campaignId);
    try {
      await apiClient.joinCampaign(campaignId);
      await loadCampaigns();
    } catch {
      // ignore
    } finally {
      setJoiningId(null);
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div className="page-header">
        <h2 className="page-title">
          <CampaignIcon size={18} />
          Campaign Hall
        </h2>
        {user && (
          <PixelButton
            variant="green"
            size="sm"
            onClick={() => setShowForm((v) => !v)}
          >
            {showForm ? 'Cancel' : '+ Start Campaign'}
          </PixelButton>
        )}
      </div>

      {showForm && (
        <PixelCard static>
          <h3 style={{ marginBottom: 16 }}>Start a New Campaign</h3>
          <form onSubmit={handleCreateCampaign} className="form-group">
            <PixelInput
              label="Campaign Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="The Lost Mine of Phandelver..."
              required
            />
            <PixelTextarea
              label="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="A story of treasure, danger, and glory..."
              rows={3}
            />
            <PixelInput
              label="Max Players"
              type="number"
              value={maxPlayers}
              onChange={(e) => setMaxPlayers(e.target.value)}
              min={2}
              max={10}
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
                {isSubmitting ? 'Creating...' : 'Start Campaign'}
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
        </>
      )}

      {!isLoading && campaigns.length === 0 && !error && (
        <div className="empty-state">
          No campaigns found.<br />
          Be the first Dungeon Master to start one!
        </div>
      )}

      {campaigns.map((campaign) => (
        <PixelCard key={campaign.id}>
          <div className="event-card__header">
            <div className="flex-1">
              <h3 className="event-card__title">{campaign.name}</h3>
              <span
                className="badge"
                style={{
                  background: STATUS_COLORS[campaign.status] || colors.dimText,
                  color: colors.dungeonBlack,
                }}
              >
                {campaign.status}
              </span>
            </div>

            {user && campaign.dm_id !== user.id && campaign.status === 'active' && (
              <PixelButton
                variant="gold"
                size="sm"
                onClick={() => handleJoin(campaign.id)}
                disabled={joiningId === campaign.id}
              >
                {joiningId === campaign.id ? 'Joining...' : 'Join Quest'}
              </PixelButton>
            )}

            {user && campaign.dm_id === user.id && (
              <span className="badge badge--red">DM</span>
            )}
          </div>

          {campaign.description && (
            <p className="event-card__description">{campaign.description}</p>
          )}

          <div className="campaign-details">
            <span>
              <span className="campaign-details__key">DM: </span>
              {campaign.dm_username}
            </span>
            <span>
              <span className="campaign-details__key">Players: </span>
              {campaign.member_count ?? 0}/{campaign.max_players}
            </span>
          </div>
        </PixelCard>
      ))}
    </div>
  );
}
