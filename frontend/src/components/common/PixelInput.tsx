import type { InputHTMLAttributes } from 'react';
import { colors, fonts } from '../../styles/theme';

interface PixelInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export function PixelInput({ label, style, id, ...rest }: PixelInputProps) {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

  return (
    <div style={{ marginBottom: '16px' }}>
      {label && (
        <label
          htmlFor={inputId}
          style={{
            display: 'block',
            fontFamily: fonts.heading,
            fontSize: '10px',
            color: colors.treasureGold,
            marginBottom: '6px',
            textTransform: 'uppercase',
          }}
        >
          {label}
        </label>
      )}
      <input
        id={inputId}
        className="pixel-border"
        style={{
          width: '100%',
          background: colors.dungeonBlack,
          color: colors.parchment,
          fontFamily: fonts.body,
          fontSize: '14px',
          padding: '10px 12px',
          border: 'none',
          outline: 'none',
          ...style,
        }}
        {...rest}
      />
    </div>
  );
}

interface PixelTextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
}

export function PixelTextarea({
  label,
  style,
  id,
  ...rest
}: PixelTextareaProps) {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

  return (
    <div style={{ marginBottom: '16px' }}>
      {label && (
        <label
          htmlFor={inputId}
          style={{
            display: 'block',
            fontFamily: fonts.heading,
            fontSize: '10px',
            color: colors.treasureGold,
            marginBottom: '6px',
            textTransform: 'uppercase',
          }}
        >
          {label}
        </label>
      )}
      <textarea
        id={inputId}
        className="pixel-border"
        style={{
          width: '100%',
          background: colors.dungeonBlack,
          color: colors.parchment,
          fontFamily: fonts.body,
          fontSize: '14px',
          padding: '10px 12px',
          border: 'none',
          outline: 'none',
          resize: 'vertical',
          minHeight: '80px',
          ...style,
        }}
        {...rest}
      />
    </div>
  );
}
