import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '80vh',
      textAlign: 'center',
      padding: '2rem',
    }}>
      <h1 style={{
        fontFamily: 'var(--font-heading)',
        fontSize: '3rem',
        color: 'var(--dragon-red)',
        textShadow: '0 0 20px rgba(192, 57, 43, 0.5)',
        marginBottom: '1rem',
        lineHeight: 1.4,
      }}>
        YOU DIED
      </h1>
      <p style={{
        fontFamily: 'var(--font-heading)',
        fontSize: '0.7rem',
        color: 'var(--dim-text)',
        marginBottom: '2rem',
        lineHeight: 2,
      }}>
        The page you seek has fallen<br />
        into the dungeon abyss.<br />
        Error 404 — Page Not Found
      </p>
      <div style={{
        fontSize: '4rem',
        marginBottom: '2rem',
        filter: 'grayscale(50%)',
      }}>
        💀
      </div>
      <Link to="/" style={{
        fontFamily: 'var(--font-heading)',
        fontSize: '0.6rem',
        color: 'var(--treasure-gold)',
        border: '2px solid var(--treasure-gold)',
        padding: '0.75rem 1.5rem',
        textDecoration: 'none',
        display: 'inline-block',
        marginTop: '1rem',
      }}>
        ← RESPAWN AT TAVERN
      </Link>
    </div>
  );
}
