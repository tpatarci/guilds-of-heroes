import type { CSSProperties, ReactNode } from 'react';

interface PixelCardProps {
  children: ReactNode;
  variant?: 'gold' | 'red' | 'green';
  style?: CSSProperties;
  className?: string;
  static?: boolean;
}

const borderClassMap = {
  gold: 'pixel-border',
  red: 'pixel-border-red',
  green: 'pixel-border-green',
};

export function PixelCard({
  children,
  variant = 'gold',
  style,
  className = '',
  static: isStatic = false,
}: PixelCardProps) {
  const classes = [
    'pixel-card',
    borderClassMap[variant],
    isStatic ? 'pixel-card--static' : '',
    className,
  ].filter(Boolean).join(' ');

  return (
    <div className={classes} style={style}>
      {children}
    </div>
  );
}
