import { useEffect, useState } from 'react';
import * as apiClient from '../api/client';
import { CharacterCard } from '../components/characters/CharacterCard';
import { PixelButton } from '../components/common/PixelButton';
import { PixelCard } from '../components/common/PixelCard';
import { PixelInput, PixelTextarea } from '../components/common/PixelInput';
import { ShieldIcon } from '../components/common/Icons';
import { CharacterCardSkeleton } from '../components/common/Skeleton';
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

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div className="page-header">
        <h2 className="page-title">
          <ShieldIcon size={18} />
          Character Vault
        </h2>
        <PixelButton
          variant="green"
          size="sm"
          onClick={() => setShowForm((v) => !v)}
        >
          {showForm ? 'Cancel' : '+ New Character'}
        </PixelButton>
      </div>

      {showForm && (
        <PixelCard static>
          <h3 style={{ marginBottom: 16 }}>Create Character</h3>
          <form onSubmit={handleCreate} className="form-group">
            <PixelInput
              label="Character Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Thorin Ironforge..."
              required
            />

            <div className="form-row">
              <div>
                <label className="pixel-input__label">Race</label>
                <select
                  value={race}
                  onChange={(e) => setRace(e.target.value)}
                  className="pixel-select"
                >
                  {D20_RACES.map((r) => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="pixel-input__label">Class</label>
                <select
                  value={charClass}
                  onChange={(e) => setCharClass(e.target.value)}
                  className="pixel-select"
                >
                  {D20_CLASSES.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>
              <div style={{ maxWidth: 80 }}>
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

            <div>
              <label className="pixel-input__label">Ability Scores</label>
              <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                <StatInput label="STR" value={str} onChange={setStr} />
                <StatInput label="DEX" value={dex} onChange={setDex} />
                <StatInput label="CON" value={con} onChange={setCon} />
                <StatInput label="INT" value={int} onChange={setInt} />
                <StatInput label="WIS" value={wis} onChange={setWis} />
                <StatInput label="CHA" value={cha} onChange={setCha} />
              </div>
            </div>

            <div className="form-row">
              <div style={{ maxWidth: 100 }}>
                <PixelInput
                  label="HP"
                  type="number"
                  value={hp}
                  onChange={(e) => setHp(e.target.value)}
                  min={1}
                />
              </div>
              <div style={{ maxWidth: 100 }}>
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
                {isSubmitting ? 'Creating...' : 'Create Character'}
              </PixelButton>
            </div>
          </form>
        </PixelCard>
      )}

      {error && <div className="error-banner">{error}</div>}

      {isLoading && (
        <>
          <CharacterCardSkeleton />
          <CharacterCardSkeleton />
        </>
      )}

      {!isLoading && characters.length === 0 && !error && (
        <div className="empty-state">
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

function StatInput({
  label,
  value,
  onChange,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <div className="stat-input">
      <label className="stat-input__label">{label}</label>
      <input
        type="number"
        value={value}
        min={1}
        max={30}
        onChange={(e) => onChange(e.target.value)}
        className="stat-input__field pixel-border"
      />
    </div>
  );
}
