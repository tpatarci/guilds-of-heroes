import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { colors, fonts } from '../styles/theme';
import { PixelButton } from '../components/common/PixelButton';
import { PixelCard } from '../components/common/PixelCard';
import { PixelInput } from '../components/common/PixelInput';

export function LoginPage() {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      if (isRegister) {
        await register(username, email, password, displayName || undefined);
      } else {
        await login(username, password);
      }
      navigate('/');
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else if (
        typeof err === 'object' &&
        err !== null &&
        'response' in err
      ) {
        const axiosErr = err as { response?: { data?: { error?: string } } };
        setError(
          axiosErr.response?.data?.error || 'Authentication failed',
        );
      } else {
        setError('Authentication failed');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        background: colors.dungeonBlack,
        padding: '24px',
      }}
    >
      {/* Title */}
      <h1
        style={{
          fontFamily: fonts.heading,
          fontSize: '32px',
          color: colors.treasureGold,
          marginBottom: '8px',
          textShadow: `0 0 20px ${colors.treasureGold}, 0 0 40px rgba(226, 183, 20, 0.3)`,
        }}
      >
        GOH
      </h1>
      <p
        style={{
          fontFamily: fonts.heading,
          fontSize: '10px',
          color: colors.dimText,
          marginBottom: '32px',
          textAlign: 'center',
        }}
      >
        Guilds of Heroes
      </p>

      <div style={{ width: '100%', maxWidth: '400px' }}>
        <PixelCard>
          <h2
            style={{
              fontFamily: fonts.heading,
              fontSize: '14px',
              color: colors.treasureGold,
              marginBottom: '24px',
              textAlign: 'center',
            }}
          >
            {isRegister ? 'Create Character' : 'Enter the Realm'}
          </h2>

          <form onSubmit={handleSubmit}>
            <PixelInput
              label="Username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Your hero name"
              required
              autoComplete="username"
            />

            {isRegister && (
              <>
                <PixelInput
                  label="Email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="hero@guilds.com"
                  required
                  autoComplete="email"
                />
                <PixelInput
                  label="Display Name"
                  type="text"
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  placeholder="How shall we call you?"
                  autoComplete="name"
                />
              </>
            )}

            <PixelInput
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Your secret passphrase"
              required
              autoComplete={isRegister ? 'new-password' : 'current-password'}
            />

            {error && (
              <div
                style={{
                  fontFamily: fonts.body,
                  fontSize: '12px',
                  color: colors.dragonRed,
                  marginBottom: '16px',
                  textAlign: 'center',
                  padding: '8px',
                  background: 'rgba(192, 57, 43, 0.1)',
                }}
                className="pixel-border-red"
              >
                {error}
              </div>
            )}

            <PixelButton
              type="submit"
              disabled={isLoading}
              style={{ width: '100%', marginBottom: '16px' }}
            >
              {isLoading
                ? 'Loading...'
                : isRegister
                  ? 'Begin Adventure'
                  : 'Enter'}
            </PixelButton>
          </form>

          <div style={{ textAlign: 'center' }}>
            <button
              onClick={() => {
                setIsRegister(!isRegister);
                setError(null);
              }}
              style={{
                background: 'none',
                border: 'none',
                fontFamily: fonts.body,
                fontSize: '12px',
                color: colors.lightGold,
                cursor: 'pointer',
                textDecoration: 'underline',
              }}
            >
              {isRegister
                ? 'Already have an account? Login'
                : 'New hero? Register'}
            </button>
          </div>
        </PixelCard>
      </div>

      {/* Flavor text */}
      <p
        style={{
          fontFamily: fonts.body,
          fontSize: '11px',
          color: colors.dimText,
          marginTop: '24px',
          textAlign: 'center',
          maxWidth: '400px',
          lineHeight: '1.6',
        }}
      >
        "Many brave adventurers have gathered here before you. Enter the realm
        and find your guild."
      </p>
    </div>
  );
}
