import type { InputHTMLAttributes } from 'react';

interface PixelInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export function PixelInput({ label, id, ...rest }: PixelInputProps) {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className="pixel-input">
      {label && (
        <label htmlFor={inputId} className="pixel-input__label">
          {label}
        </label>
      )}
      <input
        id={inputId}
        className="pixel-input__field pixel-border"
        {...rest}
      />
    </div>
  );
}

interface PixelTextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
}

export function PixelTextarea({ label, id, ...rest }: PixelTextareaProps) {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className="pixel-input">
      {label && (
        <label htmlFor={inputId} className="pixel-input__label">
          {label}
        </label>
      )}
      <textarea
        id={inputId}
        className="pixel-input__field pixel-border"
        {...rest}
      />
    </div>
  );
}
