import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { colors, fonts } from '../../styles/theme';
import { NotificationBell } from '../notifications/NotificationBell';

export function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <nav
      className="pixel-border"
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '12px 24px',
        background: colors.stoneGray,
        position: 'sticky',
        top: 0,
        zIndex: 100,
      }}
    >
      {/* Logo + Title */}
      <Link
        to="/"
        style={{
          fontFamily: fonts.heading,
          fontSize: '20px',
          color: colors.treasureGold,
          textDecoration: 'none',
          textShadow: `0 0 10px ${colors.treasureGold}, 0 0 20px rgba(226, 183, 20, 0.3)`,
        }}
      >
        GOH
      </Link>

      {/* Navigation links */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '20px',
        }}
      >
        <NavLink to="/">Feed</NavLink>
        <NavLink to="/events">Events</NavLink>
        <NavLink to="/characters">Characters</NavLink>
        <NavLink to="/campaigns">Campaigns</NavLink>
        <NavLink to="/dice">Dice</NavLink>
      </div>

      {/* Auth area */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        {isAuthenticated ? (
          <>
            <NotificationBell />
            <Link
              to={`/profile/${user?.id}`}
              style={{
                fontFamily: fonts.body,
                fontSize: '14px',
                color: colors.lightGold,
                textDecoration: 'none',
              }}
            >
              {user?.display_name || user?.username}
            </Link>
            <button
              onClick={logout}
              style={{
                background: 'none',
                border: `1px solid ${colors.dragonRed}`,
                color: colors.dragonRed,
                fontFamily: fonts.heading,
                fontSize: '8px',
                padding: '6px 12px',
                cursor: 'pointer',
                textTransform: 'uppercase',
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <Link
            to="/login"
            style={{
              fontFamily: fonts.heading,
              fontSize: '10px',
              color: colors.treasureGold,
              textDecoration: 'none',
              border: `1px solid ${colors.treasureGold}`,
              padding: '6px 16px',
            }}
          >
            Enter
          </Link>
        )}
      </div>
    </nav>
  );
}

function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  return (
    <Link
      to={to}
      style={{
        fontFamily: fonts.heading,
        fontSize: '9px',
        color: colors.parchment,
        textDecoration: 'none',
        textTransform: 'uppercase',
        letterSpacing: '1px',
        transition: 'color 0.2s',
      }}
      onMouseEnter={(e) => {
        (e.target as HTMLElement).style.color = colors.treasureGold;
      }}
      onMouseLeave={(e) => {
        (e.target as HTMLElement).style.color = colors.parchment;
      }}
    >
      {children}
    </Link>
  );
}
