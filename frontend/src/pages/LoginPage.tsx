import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
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
    <div className="login-page">
      <h1 className="login-title">GOH</h1>
      <p className="login-subtitle">Guilds of Heroes</p>

      <div className="login-form">
        <PixelCard static>
          <h2 className="login-form__title">
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
              <div className="error-message pixel-border-red">{error}</div>
            )}

            <PixelButton
              type="submit"
              disabled={isLoading}
              style={{ width: '100%', marginBottom: 16 }}
            >
              {isLoading
                ? 'Loading...'
                : isRegister
                  ? 'Begin Adventure'
                  : 'Enter'}
            </PixelButton>
          </form>

          <div className="text-center">
            <button
              onClick={() => {
                setIsRegister(!isRegister);
                setError(null);
              }}
              className="login-form__toggle"
            >
              {isRegister
                ? 'Already have an account? Login'
                : 'New hero? Register'}
            </button>
          </div>
        </PixelCard>
      </div>

      <p className="login-flavor">
        "Many brave adventurers have gathered here before you. Enter the realm
        and find your guild."
      </p>
    </div>
  );
}
