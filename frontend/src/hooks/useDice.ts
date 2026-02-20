import { useCallback, useState } from 'react';
import * as apiClient from '../api/client';
import type { DiceRoll } from '../types';

interface UseDiceReturn {
  expression: string;
  setExpression: (expr: string) => void;
  result: DiceRoll | null;
  history: DiceRoll[];
  isRolling: boolean;
  error: string | null;
  roll: () => Promise<void>;
  loadHistory: () => Promise<void>;
}

export function useDice(campaignId?: number): UseDiceReturn {
  const [expression, setExpression] = useState('1d20');
  const [result, setResult] = useState<DiceRoll | null>(null);
  const [history, setHistory] = useState<DiceRoll[]>([]);
  const [isRolling, setIsRolling] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const roll = useCallback(async () => {
    if (!expression.trim()) return;

    setIsRolling(true);
    setError(null);

    try {
      const rollResult = await apiClient.rollDice(expression, campaignId);
      setResult(rollResult);
      setHistory((prev) => [rollResult, ...prev]);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : 'Failed to roll dice';
      setError(message);
    } finally {
      // Keep the rolling animation for a minimum duration
      setTimeout(() => {
        setIsRolling(false);
      }, 500);
    }
  }, [expression, campaignId]);

  const loadHistory = useCallback(async () => {
    try {
      const data = await apiClient.getDiceHistory(20, campaignId);
      setHistory(data);
    } catch {
      // Silently fail on history load
    }
  }, [campaignId]);

  return {
    expression,
    setExpression,
    result,
    history,
    isRolling,
    error,
    roll,
    loadHistory,
  };
}
