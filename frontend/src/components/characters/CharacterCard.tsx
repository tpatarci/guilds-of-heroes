import type { Character } from '../../types';
import { colors, fonts } from '../../styles/theme';
import { PixelCard } from '../common/PixelCard';

interface CharacterCardProps {
  character: Character;
}

const ABILITY_LABELS: Record<string, string> = {
  strength: 'STR',
  dexterity: 'DEX',
  constitution: 'CON',
  intelligence: 'INT',
  wisdom: 'WIS',
  charisma: 'CHA',
};

function abilityModifier(score: number): string {
  const mod = Math.floor((score - 10) / 2);
  return mod >= 0 ? `+${mod}` : `${mod}`;
}

export function CharacterCard({ character }: CharacterCardProps) {
  return (
    <PixelCard>
      {/* Character header */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          marginBottom: '16px',
        }}
      >
        <div>
          <h3
            style={{
              fontFamily: fonts.heading,
              fontSize: '12px',
              color: colors.treasureGold,
              marginBottom: '4px',
            }}
            className="gold-glow"
          >
            {character.name}
          </h3>
          <div
            style={{
              fontFamily: fonts.body,
              fontSize: '13px',
              color: colors.parchment,
            }}
          >
            {character.race} {character.class}
          </div>
        </div>
        <div
          className="pixel-border"
          style={{
            background: colors.darkPurple,
            padding: '6px 12px',
            textAlign: 'center',
          }}
        >
          <div
            style={{
              fontFamily: fonts.heading,
              fontSize: '8px',
              color: colors.dimText,
              marginBottom: '2px',
            }}
          >
            LVL
          </div>
          <div
            style={{
              fontFamily: fonts.heading,
              fontSize: '16px',
              color: colors.treasureGold,
            }}
          >
            {character.level}
          </div>
        </div>
      </div>

      {/* HP and AC */}
      <div
        style={{
          display: 'flex',
          gap: '16px',
          marginBottom: '16px',
        }}
      >
        <div
          className="pixel-border-red"
          style={{
            background: colors.dungeonBlack,
            padding: '8px 16px',
            textAlign: 'center',
            flex: 1,
          }}
        >
          <div
            style={{
              fontFamily: fonts.heading,
              fontSize: '7px',
              color: colors.dragonRed,
              marginBottom: '4px',
            }}
          >
            HP
          </div>
          <div
            style={{
              fontFamily: fonts.heading,
              fontSize: '18px',
              color: colors.dragonRed,
            }}
          >
            {character.hit_points}
          </div>
        </div>
        <div
          className="pixel-border"
          style={{
            background: colors.dungeonBlack,
            padding: '8px 16px',
            textAlign: 'center',
            flex: 1,
          }}
        >
          <div
            style={{
              fontFamily: fonts.heading,
              fontSize: '7px',
              color: colors.treasureGold,
              marginBottom: '4px',
            }}
          >
            AC
          </div>
          <div
            style={{
              fontFamily: fonts.heading,
              fontSize: '18px',
              color: colors.treasureGold,
            }}
          >
            {character.armor_class}
          </div>
        </div>
      </div>

      {/* Ability scores grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '8px',
          marginBottom: '16px',
        }}
      >
        {Object.entries(ABILITY_LABELS).map(([key, label]) => {
          const score = character.ability_scores?.[key] ?? 10;
          return (
            <div
              key={key}
              style={{
                background: colors.dungeonBlack,
                padding: '8px',
                textAlign: 'center',
                border: `1px solid ${colors.stoneGray}`,
              }}
            >
              <div
                style={{
                  fontFamily: fonts.heading,
                  fontSize: '7px',
                  color: colors.dimText,
                  marginBottom: '4px',
                }}
              >
                {label}
              </div>
              <div
                style={{
                  fontFamily: fonts.heading,
                  fontSize: '14px',
                  color: colors.parchment,
                }}
              >
                {score}
              </div>
              <div
                style={{
                  fontFamily: fonts.body,
                  fontSize: '11px',
                  color: colors.lightGold,
                }}
              >
                {abilityModifier(score)}
              </div>
            </div>
          );
        })}
      </div>

      {/* Backstory */}
      {character.backstory && (
        <div
          style={{
            borderTop: `1px solid ${colors.dungeonBlack}`,
            paddingTop: '12px',
          }}
        >
          <div
            style={{
              fontFamily: fonts.heading,
              fontSize: '8px',
              color: colors.dimText,
              marginBottom: '6px',
              textTransform: 'uppercase',
            }}
          >
            Backstory
          </div>
          <p
            style={{
              fontFamily: fonts.body,
              fontSize: '12px',
              color: colors.parchment,
              lineHeight: '1.6',
            }}
          >
            {character.backstory}
          </p>
        </div>
      )}
    </PixelCard>
  );
}
