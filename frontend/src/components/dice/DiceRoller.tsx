import { useEffect } from 'react';
import { useDice } from '../../hooks/useDice';
import { PixelButton } from '../common/PixelButton';
import { PixelCard } from '../common/PixelCard';

interface DiceRollerProps {
  campaignId?: number;
  compact?: boolean;
}

const QUICK_ROLLS = ['1d4', '1d6', '1d8', '1d10', '1d12', '1d20', '2d6', '1d100'];

export function DiceRoller({ campaignId, compact = false }: DiceRollerProps) {
  const {
    expression,
    setExpression,
    result,
    history,
    isRolling,
    error,
    roll,
    loadHistory,
  } = useDice(campaignId);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      roll();
    }
  };

  return (
    <div>
      <PixelCard static>
        <h3 className="dice-tower__title gold-glow">Dice Tower</h3>

        <div className="dice-tower__display">
          {result && !isRolling && (
            <div className="dice-tower__result">
              <div
                className="dice-tower__total"
                style={{ fontSize: compact ? 28 : 48 }}
              >
                {result.total}
              </div>
              <div className="dice-tower__breakdown">
                {result.expression} = [{result.results.join(', ')}]
              </div>
            </div>
          )}

          {isRolling && (
            <div
              className="dice-tower__rolling"
              style={{ fontSize: compact ? 28 : 48 }}
            >
              ?
            </div>
          )}

          {!result && !isRolling && (
            <div className="dice-tower__placeholder">
              Roll the dice, adventurer!
            </div>
          )}
        </div>

        <div className="dice-tower__input-row">
          <input
            type="text"
            value={expression}
            onChange={(e) => setExpression(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="e.g. 2d6+3"
            className="dice-tower__expression pixel-border"
          />
          <PixelButton onClick={roll} disabled={isRolling || !expression.trim()}>
            {isRolling ? '...' : 'Roll!'}
          </PixelButton>
        </div>

        <div className="dice-tower__quick-rolls">
          {QUICK_ROLLS.map((expr) => (
            <button
              key={expr}
              onClick={() => setExpression(expr)}
              className={`dice-tower__quick-btn ${expression === expr ? 'dice-tower__quick-btn--active' : ''}`}
            >
              {expr}
            </button>
          ))}
        </div>

        {error && <div className="dice-tower__error">{error}</div>}
      </PixelCard>

      {!compact && history.length > 0 && (
        <PixelCard static style={{ marginTop: 16 }}>
          <h3 className="dice-tower__history-title">Roll History</h3>
          <div className="dice-tower__history">
            {history.map((roll, idx) => (
              <div key={roll.id ?? idx} className="dice-tower__history-row">
                <span className="dice-tower__history-expr">{roll.expression}</span>
                <span className="dice-tower__history-rolls">
                  [{roll.results.join(', ')}]
                </span>
                <span className="dice-tower__history-total">{roll.total}</span>
              </div>
            ))}
          </div>
        </PixelCard>
      )}
    </div>
  );
}
