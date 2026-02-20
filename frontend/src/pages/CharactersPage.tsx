import { useEffect, useState } from 'react';
import * as apiClient from '../api/client';
import { CharacterCard } from '../components/characters/CharacterCard';
import { PixelButton } from '../components/common/PixelButton';
import { PixelCard } from '../components/common/PixelCard';
import { PixelInput, PixelTextarea } from '../components/common/PixelInput';
import { colors, fonts } from '../styles/theme';
import type { Character } from '../types';

const D20_RACES = [
  'Human', 'Elf', 'Dwarf', 'Halfling', 'Half-Elf',
  'Half-Orc', 'Gnome', 'Tiefling', 'Dragonborn', 'Other',
];

const D20_CLASSES = [
  'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter',
  'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer',
  'Warlock', 'Wizard', 'Artificer', 'Blood Hunter', 'Other',
];

export default function CharactersPage() {
  const [characters, setCharacters] = useState<Character[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Form state
  const [name, setName] = useState('');
  const [race, setRace] = useState('Human');
  const [charClass, setCharClass] = useState('Fighter');
  const [level, setLevel] = useState('1');
  const [str, setStr] = useState('10');
  const [dex, setDex] = useState('10');
  const [con, setCon] = useState('10');
  const [int, setInt] = useState('10');
  const [wis, setWis] = useState('10');
  const [cha, setCha] = useState('10');
  const [hp, setHp] = useState('10');
  const [ac, setAc] = useState('10');
  const [backstory, setBackstory] = useState('');

  async function loadCharacters() {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiClient.getCharacters();
      setCharacters(data);
    } catch {
      setError('Failed to load characters');
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadCharacters();
  }, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim()) return;

    setIsSubmitting(true);
    setFormError(null);
    try {
      await apiClient.createCharacter({
        name: name.trim(),
        race,
        class: charClass,
        level: parseInt(level, 10) || 1,
        strength: parseInt(str, 10) || 10,
        dexterity: parseInt(dex, 10) || 10,
        constitution: parseInt(con, 10) || 10,
        intelligence: parseInt(int, 10) || 10,
        wisdom: parseInt(wis, 10) || 10,
        charisma: parseInt(cha, 10) || 10,
        hit_points: parseInt(hp, 10) || 10,
        armor_class: parseInt(ac, 10) || 10,
        backstory: backstory.trim() || undefined,
      });
      setName('');
      setBackstory('');
      setShowForm(false);
      await loadCharacters();
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to create character';
      setFormError(msg);
    } finally {
      setIsSubmitting(false);
    }
  }

  const statField = (
    label: string,
    value: string,
    setter: (v: string) => void,
  ) => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
      <label
        style={{
          fontFamily: fonts.heading,
          fontSize: '7px',
          color: colors.dimText,
          textAlign: 'center',
          textTransform: 'uppercase',
        }}
      >
        {label}
      </label>
      <input
        type="number"
        value={value}
        min={1}
        max={30}
        onChange={(e) => setter(e.target.value)}
        className="pixel-border"
        style={{
          width: '60px',
          background: colors.dungeonBlack,
          color: colors.parchment,
          fontFamily: fonts.heading,
          fontSize: '14px',
          padding: '6px',
          border: 'none',
          outline: 'none',
          textAlign: 'center',
        }}
      />
    </div>
  );

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
          🧙 Character Vault
        </h2>
        <PixelButton
          variant="green"
          size="sm"
          onClick={() => setShowForm((v) => !v)}
        >
          {showForm ? 'Cancel' : '+ New Character'}
        </PixelButton>
      </div>

      {/* Create character form */}
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
            Create Character
          </h3>
          <form
            onSubmit={handleCreate}
            style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}
          >
            <PixelInput
              label="Character Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Thorin Ironforge..."
              required
            />

            <div style={{ display: 'flex', gap: '12px' }}>
              <div style={{ flex: 1 }}>
                <label
                  style={{
                    display: 'block',
                    fontFamily: fonts.heading,
                    fontSize: '8px',
                    color: colors.treasureGold,
                    marginBottom: '6px',
                    textTransform: 'uppercase',
                  }}
                >
                  Race
                </label>
                <select
                  value={race}
                  onChange={(e) => setRace(e.target.value)}
                  style={{
                    width: '100%',
                    background: colors.dungeonBlack,
                    color: colors.parchment,
                    border: `1px solid ${colors.stoneGray}`,
                    padding: '8px 12px',
                    fontFamily: fonts.body,
                    fontSize: '13px',
                  }}
                >
                  {D20_RACES.map((r) => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </select>
              </div>
              <div style={{ flex: 1 }}>
                <label
                  style={{
                    display: 'block',
                    fontFamily: fonts.heading,
                    fontSize: '8px',
                    color: colors.treasureGold,
                    marginBottom: '6px',
                    textTransform: 'uppercase',
                  }}
                >
                  Class
                </label>
                <select
                  value={charClass}
                  onChange={(e) => setCharClass(e.target.value)}
                  style={{
                    width: '100%',
                    background: colors.dungeonBlack,
                    color: colors.parchment,
                    border: `1px solid ${colors.stoneGray}`,
                    padding: '8px 12px',
                    fontFamily: fonts.body,
                    fontSize: '13px',
                  }}
                >
                  {D20_CLASSES.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>
              <div style={{ width: '80px' }}>
                <PixelInput
                  label="Level"
                  type="number"
                  value={level}
                  onChange={(e) => setLevel(e.target.value)}
                  min={1}
                  max={20}
                />
              </div>
            </div>

            {/* Ability scores */}
            <div>
              <div
                style={{
                  fontFamily: fonts.heading,
                  fontSize: '8px',
                  color: colors.treasureGold,
                  marginBottom: '10px',
                  textTransform: 'uppercase',
                }}
              >
                Ability Scores
              </div>
              <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                {statField('STR', str, setStr)}
                {statField('DEX', dex, setDex)}
                {statField('CON', con, setCon)}
                {statField('INT', int, setInt)}
                {statField('WIS', wis, setWis)}
                {statField('CHA', cha, setCha)}
              </div>
            </div>

            <div style={{ display: 'flex', gap: '12px' }}>
              <div style={{ width: '100px' }}>
                <PixelInput
                  label="HP"
                  type="number"
                  value={hp}
                  onChange={(e) => setHp(e.target.value)}
                  min={1}
                />
              </div>
              <div style={{ width: '100px' }}>
                <PixelInput
                  label="Armor Class"
                  type="number"
                  value={ac}
                  onChange={(e) => setAc(e.target.value)}
                  min={1}
                />
              </div>
            </div>

            <PixelTextarea
              label="Backstory"
              value={backstory}
              onChange={(e) => setBackstory(e.target.value)}
              placeholder="Born under a cursed moon..."
              rows={3}
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
                {isSubmitting ? 'Creating...' : 'Create Character'}
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
          Summoning characters...
        </div>
      )}

      {!isLoading && characters.length === 0 && !error && (
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
          No characters yet.<br />
          Roll for initiative and create your first hero!
        </div>
      )}

      {characters.map((character) => (
        <CharacterCard key={character.id} character={character} />
      ))}
    </div>
  );
}
