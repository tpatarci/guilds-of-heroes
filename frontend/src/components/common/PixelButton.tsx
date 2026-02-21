import type { ButtonHTMLAttributes, ReactNode } from 'react';

interface PixelButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'gold' | 'red' | 'green';
  size?: 'sm' | 'md' | 'lg';
}

const borderClassMap = {
  gold: 'pixel-border',
  red: 'pixel-border-red',
  green: 'pixel-border-green',
};

export function PixelButton({
  children,
  variant = 'gold',
  size = 'md',
  className = '',
  ...rest
}: PixelButtonProps) {
  const classes = [
    'pixel-btn',
    borderClassMap[variant],
    `pixel-btn--${variant}`,
    size !== 'md' ? `pixel-btn--${size}` : '',
    className,
  ].filter(Boolean).join(' ');

  return (
    <button className={classes} {...rest}>
      {children}
    </button>
  );
}
