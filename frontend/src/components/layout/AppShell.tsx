import { Outlet } from 'react-router-dom';
import { Navbar } from './Navbar';

export function AppShell() {
  return (
    <div className="app-shell">
      <Navbar />
      <div className="app-content">
        <main className="app-main">
          <Outlet />
        </main>
      </div>
      <footer className="app-footer">
        Guilds of Heroes &mdash; Roll for Initiative
      </footer>
    </div>
  );
}
