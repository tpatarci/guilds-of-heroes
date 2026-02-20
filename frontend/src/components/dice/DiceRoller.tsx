import { useEffect } from 'react';
import { useDice } from '../../hooks/useDice';
import { colors, fonts } from '../../styles/theme';
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
      <PixelCard>
        <h3
          style={{
            fontFamily: fonts.heading,
            fontSize: '12px',
            color: colors.treasureGold,
            marginBottom: '16px',
            textAlign: 'center',
          }}
          className="gold-glow"
        >
          Dice Tower
        </h3>

        {/* Result display */}
        <div
          style={{
            textAlign: 'center',
            marginBottom: '20px',
            minHeight: '80px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          {result && !isRolling && (
            <div className="dice-result">
              <div
                style={{
                  fontFamily: fonts.heading,
                  fontSize: compact ? '28px' : '48px',
                  color: colors.treasureGold,
                  textShadow: `0 0 20px ${colors.treasureGold}, 0 0 40px rgba(226, 183, 20, 0.4)`,
                }}
              >
                {result.total}
              </div>
              <div
                style={{
                  fontFamily: fonts.body,
                  fontSize: '12px',
                  color: colors.dimText,
                  marginTop: '4px',
                }}
              >
                {result.expression} = [{result.results.join(', ')}]
              </div>
            </div>
          )}

          {isRolling && (
            <div
              className="dice-rolling"
              style={{
                fontFamily: fonts.heading,
                fontSize: compact ? '28px' : '48px',
                color: colors.lightGold,
              }}
            >
              ?
            </div>
          )}

          {!result && !isRolling && (
            <div
              style={{
                fontFamily: fonts.body,
                fontSize: '13px',
                color: colors.dimText,
              }}
            >
              Roll the dice, adventurer!
            </div>
          )}
        </div>

        {/* Expression input */}
        <div
          style={{
            display: 'flex',
            gap: '8px',
            marginBottom: '16px',
          }}
        >
          <input
            type="text"
            value={expression}
            onChange={(e) => setExpression(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="e.g. 2d6+3"
            className="pixel-border"
            style={{
              flex: 1,
              background: colors.dungeonBlack,
              color: colors.parchment,
              fontFamily: fonts.body,
              fontSize: '16px',
              padding: '10px 12px',
              border: 'none',
              outline: 'none',
              textAlign: 'center',
            }}
          />
          <PixelButton onClick={roll} disabled={isRolling || !expression.trim()}>
            {isRolling ? '...' : 'Roll!'}
          </PixelButton>
        </div>

        {/* Quick roll buttons */}
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '6px',
            justifyContent: 'center',
          }}
        >
          {QUICK_ROLLS.map((expr) => (
            <button
              key={expr}
              onClick={() => {
                setExpression(expr);
                // Small delay to let state update then roll
                setTimeout(() => {
                  /* roll will use the latest expression via closure */
                }, 0);
              }}
              onDoubleClick={() => {
                setExpression(expr);
              }}
              style={{
                background:
                  expression === expr ? colors.darkPurple : colors.dungeonBlack,
                color: colors.parchment,
                fontFamily: fonts.body,
                fontSize: '11px',
                padding: '4px 10px',
                border: `1px solid ${colors.treasureGold}40`,
                cursor: 'pointer',
                transition: 'all 0.15s',
              }}
              onMouseEnter={(e) => {
                (e.target as HTMLElement).style.borderColor = colors.treasureGold;
              }}
              onMouseLeave={(e) => {
                (e.target as HTMLElement).style.borderColor = `${colors.treasureGold}40`;
              }}
            >
              {expr}
            </button>
          ))}
        </div>

        {error && (
          <div
            style={{
              fontFamily: fonts.body,
              fontSize: '12px',
              color: colors.dragonRed,
              textAlign: 'center',
              marginTop: '12px',
            }}
          >
            {error}
          </div>
        )}
      </PixelCard>

      {/* Roll history */}
      {!compact && history.length > 0 && (
        <PixelCard style={{ marginTop: '16px' }}>
          <h3
            style={{
              fontFamily: fonts.heading,
              fontSize: '10px',
              color: colors.treasureGold,
              marginBottom: '12px',
            }}
          >
            Roll History
          </h3>
          <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
            {history.map((roll, idx) => (
              <div
                key={roll.id ?? idx}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '6px 0',
                  borderBottom:
                    idx < history.length - 1
                      ? `1px solid ${colors.dungeonBlack}`
                      : 'none',
                }}
              >
                <span
                  style={{
                    fontFamily: fonts.body,
                    fontSize: '13px',
                    color: colors.parchment,
                  }}
                >
                  {roll.expression}
                </span>
                <span
                  style={{
                    fontFamily: fonts.body,
                    fontSize: '12px',
                    color: colors.dimText,
                  }}
                >
                  [{roll.results.join(', ')}]
                </span>
                <span
                  style={{
                    fontFamily: fonts.heading,
                    fontSize: '12px',
                    color: colors.treasureGold,
                  }}
                >
                  {roll.total}
                </span>
              </div>
            ))}
          </div>
        </PixelCard>
      )}
    </div>
  );
}
