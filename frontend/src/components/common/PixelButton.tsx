import type { ButtonHTMLAttributes, ReactNode } from 'react';
import { colors, fonts } from '../../styles/theme';

interface PixelButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'gold' | 'red' | 'green';
  size?: 'sm' | 'md' | 'lg';
}

const variantMap = {
  gold: {
    border: colors.treasureGold,
    text: colors.treasureGold,
    hoverBg: 'rgba(226, 183, 20, 0.15)',
  },
  red: {
    border: colors.dragonRed,
    text: colors.dragonRed,
    hoverBg: 'rgba(192, 57, 43, 0.15)',
  },
  green: {
    border: colors.potionGreen,
    text: colors.potionGreen,
    hoverBg: 'rgba(39, 174, 96, 0.15)',
  },
};

const sizeMap = {
  sm: { padding: '6px 12px', fontSize: '10px' },
  md: { padding: '10px 20px', fontSize: '12px' },
  lg: { padding: '14px 28px', fontSize: '14px' },
};

export function PixelButton({
  children,
  variant = 'gold',
  size = 'md',
  style,
  disabled,
  ...rest
}: PixelButtonProps) {
  const v = variantMap[variant];
  const s = sizeMap[size];

  return (
    <button
      className={`pixel-border${variant === 'red' ? '-red' : variant === 'green' ? '-green' : ''}`}
      style={{
        background: disabled ? '#333' : colors.dungeonBlack,
        color: disabled ? colors.dimText : v.text,
        fontFamily: fonts.heading,
        fontSize: s.fontSize,
        padding: s.padding,
        border: 'none',
        cursor: disabled ? 'not-allowed' : 'pointer',
        transition: 'all 0.2s ease',
        textTransform: 'uppercase',
        letterSpacing: '1px',
        opacity: disabled ? 0.5 : 1,
        ...style,
      }}
      disabled={disabled}
      onMouseEnter={(e) => {
        if (!disabled) {
          (e.currentTarget as HTMLButtonElement).style.background = v.hoverBg;
          (e.currentTarget as HTMLButtonElement).style.textShadow =
            `0 0 10px ${v.border}, 0 0 20px ${v.border}40`;
        }
      }}
      onMouseLeave={(e) => {
        (e.currentTarget as HTMLButtonElement).style.background =
          colors.dungeonBlack;
        (e.currentTarget as HTMLButtonElement).style.textShadow = 'none';
      }}
      {...rest}
    >
      {children}
    </button>
  );
}
