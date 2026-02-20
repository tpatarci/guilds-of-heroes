import type { CSSProperties, ReactNode } from 'react';
import { colors } from '../../styles/theme';

interface PixelCardProps {
  children: ReactNode;
  variant?: 'gold' | 'red' | 'green';
  style?: CSSProperties;
  className?: string;
}

export function PixelCard({
  children,
  variant = 'gold',
  style,
  className = '',
}: PixelCardProps) {
  const borderClass =
    variant === 'red'
      ? 'pixel-border-red'
      : variant === 'green'
        ? 'pixel-border-green'
        : 'pixel-border';

  return (
    <div
      className={`${borderClass} ${className}`}
      style={{
        background: colors.stoneGray,
        padding: '20px',
        marginBottom: '16px',
        ...style,
      }}
    >
      {children}
    </div>
  );
}
