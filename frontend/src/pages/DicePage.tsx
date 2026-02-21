import { DiceRoller } from '../components/dice/DiceRoller';
import { DiceIcon } from '../components/common/Icons';

export default function DicePage() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div className="page-header">
        <h2 className="page-title">
          <DiceIcon size={18} />
          Dice Tower
        </h2>
      </div>
      <p className="text-dim" style={{ lineHeight: 1.7, marginBottom: 8 }}>
        Type any dice expression (e.g. <code>2d6+3</code>,{' '}
        <code>1d20</code>,{' '}
        <code>4d8-1</code>) or pick a quick roll below.
        Press Enter or click Roll!
      </p>
      <DiceRoller />
    </div>
  );
}
