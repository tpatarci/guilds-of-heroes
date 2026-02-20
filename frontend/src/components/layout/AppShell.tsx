import { Outlet } from 'react-router-dom';
import { colors, fonts } from '../../styles/theme';
import { Navbar } from './Navbar';

export function AppShell() {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh',
        background: colors.dungeonBlack,
      }}
    >
      <Navbar />

      <div
        style={{
          display: 'flex',
          flex: 1,
          maxWidth: '1200px',
          width: '100%',
          margin: '0 auto',
          padding: '24px',
          gap: '24px',
        }}
      >
        {/* Sidebar */}
        <aside
          style={{
            width: '200px',
            flexShrink: 0,
            display: 'flex',
            flexDirection: 'column',
            gap: '12px',
          }}
        >
          <div
            className="pixel-border"
            style={{
              background: colors.stoneGray,
              padding: '16px',
            }}
          >
            <h3
              style={{
                fontFamily: fonts.heading,
                fontSize: '10px',
                color: colors.treasureGold,
                marginBottom: '12px',
              }}
            >
              Quick Roll
            </h3>
            <p
              style={{
                fontFamily: fonts.body,
                fontSize: '12px',
                color: colors.dimText,
              }}
            >
              Visit the{' '}
              <a href="/dice" style={{ color: colors.lightGold }}>
                Dice Tower
              </a>{' '}
              to roll some dice!
            </p>
          </div>

          <div
            className="pixel-border"
            style={{
              background: colors.stoneGray,
              padding: '16px',
            }}
          >
            <h3
              style={{
                fontFamily: fonts.heading,
                fontSize: '10px',
                color: colors.treasureGold,
                marginBottom: '12px',
              }}
            >
              Guilds of Heroes
            </h3>
            <p
              style={{
                fontFamily: fonts.body,
                fontSize: '11px',
                color: colors.dimText,
                lineHeight: '1.6',
              }}
            >
              A social network for D&D adventurers. Find campaigns, create
              characters, and share your tales.
            </p>
          </div>
        </aside>

        {/* Main content */}
        <main style={{ flex: 1, minWidth: 0 }}>
          <Outlet />
        </main>
      </div>

      {/* Footer */}
      <footer
        style={{
          textAlign: 'center',
          padding: '16px',
          fontFamily: fonts.heading,
          fontSize: '8px',
          color: colors.dimText,
          borderTop: `1px solid ${colors.stoneGray}`,
        }}
      >
        Guilds of Heroes &mdash; Roll for Initiative
      </footer>
    </div>
  );
}
