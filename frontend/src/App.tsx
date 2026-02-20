import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './hooks/useAuth';
import { AppShell } from './components/layout/AppShell';

import { LoginPage } from './pages/LoginPage';
import FeedPage from './pages/FeedPage';
import ProfilePage from './pages/ProfilePage';
import EventsPage from './pages/EventsPage';
import CharactersPage from './pages/CharactersPage';
import CampaignsPage from './pages/CampaignsPage';
import DicePage from './pages/DicePage';
import NotFoundPage from './pages/NotFoundPage';

import './styles/pixel.css';

/** Guard: redirect unauthenticated users to /login */
function RequireAuth({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          fontFamily: "'Press Start 2P', cursive",
          fontSize: '12px',
          color: '#e2b714',
          background: '#1a1a2e',
        }}
      >
        Loading...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

/** Guard: redirect authenticated users away from /login */
function RedirectIfAuth({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) return null;
  if (isAuthenticated) return <Navigate to="/feed" replace />;
  return <>{children}</>;
}

function AppRoutes() {
  return (
    <Routes>
      {/* Public */}
      <Route
        path="/login"
        element={
          <RedirectIfAuth>
            <LoginPage />
          </RedirectIfAuth>
        }
      />

      {/* Protected — wrapped in AppShell layout */}
      <Route
        element={
          <RequireAuth>
            <AppShell />
          </RequireAuth>
        }
      >
        <Route index element={<Navigate to="/feed" replace />} />
        <Route path="/feed" element={<FeedPage />} />
        <Route path="/profile/:userId" element={<ProfilePage />} />
        <Route path="/events" element={<EventsPage />} />
        <Route path="/characters" element={<CharactersPage />} />
        <Route path="/campaigns" element={<CampaignsPage />} />
        <Route path="/dice" element={<DicePage />} />
      </Route>

      {/* 404 */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}
