import type { Character } from '../../types';
import { PixelCard } from '../common/PixelCard';

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

interface CharacterCardProps {
  character: Character;
}

export function CharacterCard({ character }: CharacterCardProps) {
  return (
    <PixelCard>
      <div className="char-card__header">
        <div>
          <h3 className="char-card__name">{character.name}</h3>
          <div className="char-card__race-class">
            {character.race} {character.class}
          </div>
        </div>
        <div className="char-card__level pixel-border">
          <div className="char-card__level-label">LVL</div>
          <div className="char-card__level-value">{character.level}</div>
        </div>
      </div>

      <div className="char-card__vitals">
        <div className="char-card__vital pixel-border-red">
          <div className="char-card__vital-label text-red">HP</div>
          <div className="char-card__vital-value text-red">
            {character.hit_points}
          </div>
        </div>
        <div className="char-card__vital pixel-border">
          <div className="char-card__vital-label text-gold">AC</div>
          <div className="char-card__vital-value text-gold">
            {character.armor_class}
          </div>
        </div>
      </div>

      <div className="char-card__abilities">
        {Object.entries(ABILITY_LABELS).map(([key, label]) => {
          const score = character.ability_scores?.[key] ?? 10;
          return (
            <div key={key} className="char-card__ability">
              <div className="char-card__ability-label">{label}</div>
              <div className="char-card__ability-score">{score}</div>
              <div className="char-card__ability-mod">
                {abilityModifier(score)}
              </div>
            </div>
          );
        })}
      </div>

      {character.backstory && (
        <div className="char-card__backstory">
          <div className="char-card__backstory-label">Backstory</div>
          <p className="char-card__backstory-text">{character.backstory}</p>
        </div>
      )}
    </PixelCard>
  );
}
