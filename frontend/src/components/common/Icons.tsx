import type { SVGProps } from 'react';

type IconProps = SVGProps<SVGSVGElement> & { size?: number };

function defaults(size = 20): SVGProps<SVGSVGElement> {
  return {
    width: size,
    height: size,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    strokeWidth: 2,
    strokeLinecap: 'square' as const,
    strokeLinejoin: 'miter' as const,
  };
}

export function SwordIcon({ size, ...props }: IconProps) {
  return (
    <svg {...defaults(size)} {...props}>
      <path d="M4 20L9 15M20 4L10 14M10 14L7 11M10 14L13 17" />
      <path d="M4 20L6 18" />
    </svg>
  );
}

export function ScrollIcon({ size, ...props }: IconProps) {
  return (
    <svg {...defaults(size)} {...props}>
      <path d="M8 3H5a2 2 0 00-2 2v14c0 1.1.9 2 2 2h3" />
      <path d="M16 3h3a2 2 0 012 2v14a2 2 0 01-2 2h-3" />
      <rect x="8" y="3" width="8" height="18" />
      <line x1="10" y1="8" x2="14" y2="8" />
      <line x1="10" y1="12" x2="14" y2="12" />
    </svg>
  );
}

export function ShieldIcon({ size, ...props }: IconProps) {
  return (
    <svg {...defaults(size)} {...props}>
      <path d="M12 2L3 7v5c0 5.25 3.83 10.16 9 11.25C17.17 22.16 21 17.25 21 12V7l-9-5z" />
    </svg>
  );
}

export function DiceIcon({ size, ...props }: IconProps) {
  return (
    <svg {...defaults(size)} {...props}>
      <rect x="3" y="3" width="18" height="18" rx="1" />
      <circle cx="8" cy="8" r="1" fill="currentColor" stroke="none" />
      <circle cx="16" cy="8" r="1" fill="currentColor" stroke="none" />
      <circle cx="12" cy="12" r="1" fill="currentColor" stroke="none" />
      <circle cx="8" cy="16" r="1" fill="currentColor" stroke="none" />
      <circle cx="16" cy="16" r="1" fill="currentColor" stroke="none" />
    </svg>
  );
}

export function BellIcon({ size, ...props }: IconProps) {
  return (
    <svg {...defaults(size)} {...props}>
      <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9" />
      <path d="M13.73 21a2 2 0 01-3.46 0" />
    </svg>
  );
}

export function UserIcon({ size, ...props }: IconProps) {
  return (
    <svg {...defaults(size)} {...props}>
      <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  );
}

export function MenuIcon({ size, ...props }: IconProps) {
  return (
    <svg {...defaults(size)} {...props}>
      <line x1="3" y1="6" x2="21" y2="6" />
      <line x1="3" y1="12" x2="21" y2="12" />
      <line x1="3" y1="18" x2="21" y2="18" />
    </svg>
  );
}

export function CloseIcon({ size, ...props }: IconProps) {
  return (
    <svg {...defaults(size)} {...props}>
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  );
}

export function PlusIcon({ size, ...props }: IconProps) {
  return (
    <svg {...defaults(size)} {...props}>
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </svg>
  );
}

export function CampaignIcon({ size, ...props }: IconProps) {
  return (
    <svg {...defaults(size)} {...props}>
      <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z" />
      <line x1="4" y1="22" x2="4" y2="15" />
    </svg>
  );
}
