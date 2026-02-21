import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { NotificationBell } from '../notifications/NotificationBell';
import { SwordIcon, ScrollIcon, ShieldIcon, DiceIcon, CampaignIcon, MenuIcon, CloseIcon } from '../common/Icons';

export function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  const isActive = (path: string) => location.pathname === path || location.pathname.startsWith(path + '/');

  return (
    <nav className="navbar">
      <Link to="/" className="navbar__logo">GOH</Link>

      <button
        className="navbar__menu-toggle"
        onClick={() => setMenuOpen(!menuOpen)}
        aria-label={menuOpen ? 'Close menu' : 'Open menu'}
      >
        {menuOpen ? <CloseIcon size={18} /> : <MenuIcon size={18} />}
      </button>

      <div className={`navbar__links ${menuOpen ? 'navbar__links--open' : ''}`}>
        <NavLink to="/feed" active={isActive('/feed')} onClick={() => setMenuOpen(false)}>
          <SwordIcon size={14} /> Feed
        </NavLink>
        <NavLink to="/events" active={isActive('/events')} onClick={() => setMenuOpen(false)}>
          <ScrollIcon size={14} /> Events
        </NavLink>
        <NavLink to="/characters" active={isActive('/characters')} onClick={() => setMenuOpen(false)}>
          <ShieldIcon size={14} /> Characters
        </NavLink>
        <NavLink to="/campaigns" active={isActive('/campaigns')} onClick={() => setMenuOpen(false)}>
          <CampaignIcon size={14} /> Campaigns
        </NavLink>
        <NavLink to="/dice" active={isActive('/dice')} onClick={() => setMenuOpen(false)}>
          <DiceIcon size={14} /> Dice
        </NavLink>
      </div>

      <div className="navbar__auth">
        {isAuthenticated ? (
          <>
            <NotificationBell />
            <Link to={`/profile/${user?.id}`} className="navbar__user">
              {user?.display_name || user?.username}
            </Link>
            <button onClick={logout} className="navbar__logout">
              Logout
            </button>
          </>
        ) : (
          <Link to="/login" className="navbar__enter">Enter</Link>
        )}
      </div>
    </nav>
  );
}

function NavLink({
  to,
  active,
  children,
  onClick,
}: {
  to: string;
  active: boolean;
  children: React.ReactNode;
  onClick: () => void;
}) {
  return (
    <Link
      to={to}
      className={`navbar__link ${active ? 'navbar__link--active' : ''}`}
      onClick={onClick}
    >
      {children}
    </Link>
  );
}
