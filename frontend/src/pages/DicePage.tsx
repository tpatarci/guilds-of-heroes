import { DiceRoller } from '../components/dice/DiceRoller';
import { colors, fonts } from '../styles/theme';

export default function DicePage() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <h2
        style={{
          fontFamily: fonts.heading,
          fontSize: '14px',
          color: colors.treasureGold,
          marginBottom: '8px',
        }}
      >
        🎲 Dice Tower
      </h2>
      <p
        style={{
          fontFamily: fonts.body,
          fontSize: '13px',
          color: colors.dimText,
          lineHeight: '1.6',
          marginBottom: '8px',
        }}
      >
        Type any dice expression (e.g. <code style={{ color: colors.lightGold }}>2d6+3</code>,{' '}
        <code style={{ color: colors.lightGold }}>1d20</code>,{' '}
        <code style={{ color: colors.lightGold }}>4d8-1</code>) or pick a quick roll below.
        Press Enter or click Roll!
      </p>
      <DiceRoller />
    </div>
  );
}
