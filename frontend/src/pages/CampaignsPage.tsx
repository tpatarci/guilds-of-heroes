import { useEffect, useState } from 'react';
import * as apiClient from '../api/client';
import { useAuth } from '../hooks/useAuth';
import { PixelButton } from '../components/common/PixelButton';
import { PixelCard } from '../components/common/PixelCard';
import { PixelInput, PixelTextarea } from '../components/common/PixelInput';
import { colors, fonts } from '../styles/theme';
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

  // Form state
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
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '8px',
        }}
      >
        <h2
          style={{
            fontFamily: fonts.heading,
            fontSize: '14px',
            color: colors.treasureGold,
          }}
        >
          ⚔ Campaign Hall
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

      {/* Create campaign form */}
      {showForm && (
        <PixelCard>
          <h3
            style={{
              fontFamily: fonts.heading,
              fontSize: '11px',
              color: colors.treasureGold,
              marginBottom: '16px',
            }}
          >
            Start a New Campaign
          </h3>
          <form
            onSubmit={handleCreateCampaign}
            style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}
          >
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

            {formError && (
              <div
                style={{
                  fontFamily: fonts.body,
                  fontSize: '12px',
                  color: colors.dragonRed,
                }}
              >
                {formError}
              </div>
            )}

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px' }}>
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

      {error && (
        <div
          style={{
            fontFamily: fonts.body,
            fontSize: '13px',
            color: colors.dragonRed,
            padding: '12px',
            border: `1px solid ${colors.dragonRed}`,
          }}
        >
          {error}
        </div>
      )}

      {isLoading && (
        <div
          style={{
            fontFamily: fonts.heading,
            fontSize: '10px',
            color: colors.dimText,
            textAlign: 'center',
            padding: '40px',
          }}
        >
          Unfurling the campaign map...
        </div>
      )}

      {!isLoading && campaigns.length === 0 && !error && (
        <div
          style={{
            fontFamily: fonts.body,
            fontSize: '14px',
            color: colors.dimText,
            textAlign: 'center',
            padding: '40px',
            lineHeight: '2',
          }}
        >
          No campaigns found.<br />
          Be the first Dungeon Master to start one!
        </div>
      )}

      {campaigns.map((campaign) => (
        <PixelCard key={campaign.id}>
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
                  fontSize: '12px',
                  color: colors.treasureGold,
                  marginBottom: '6px',
                }}
              >
                {campaign.name}
              </h3>
              <span
                style={{
                  fontFamily: fonts.heading,
                  fontSize: '7px',
                  color: colors.dungeonBlack,
                  background: STATUS_COLORS[campaign.status] || colors.dimText,
                  padding: '2px 8px',
                  textTransform: 'uppercase',
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
              <span
                style={{
                  fontFamily: fonts.heading,
                  fontSize: '7px',
                  color: colors.dungeonBlack,
                  background: colors.dragonRed,
                  padding: '2px 8px',
                  textTransform: 'uppercase',
                }}
              >
                DM
              </span>
            )}
          </div>

          {campaign.description && (
            <p
              style={{
                fontFamily: fonts.body,
                fontSize: '13px',
                color: colors.parchment,
                lineHeight: '1.6',
                marginBottom: '12px',
              }}
            >
              {campaign.description}
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
              <span style={{ color: colors.treasureGold }}>DM: </span>
              {campaign.dm_username}
            </span>
            <span>
              <span style={{ color: colors.treasureGold }}>Players: </span>
              {campaign.member_count ?? 0}/{campaign.max_players}
            </span>
          </div>
        </PixelCard>
      ))}
    </div>
  );
}
