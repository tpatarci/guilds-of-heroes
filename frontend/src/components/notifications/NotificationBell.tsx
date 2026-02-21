import { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import * as apiClient from '../../api/client';
import { BellIcon } from '../common/Icons';

export function NotificationBell() {
  const [unreadCount, setUnreadCount] = useState(0);
  const navigate = useNavigate();

  const fetchUnread = useCallback(async () => {
    try {
      const count = await apiClient.getUnreadCount();
      setUnreadCount(count);
    } catch {
      // Silently fail — user may not be authenticated
    }
  }, []);

  useEffect(() => {
    fetchUnread();
    const interval = setInterval(fetchUnread, 30000);
    return () => clearInterval(interval);
  }, [fetchUnread]);

  return (
    <button
      onClick={() => navigate('/notifications')}
      className="notification-bell"
      title="Notifications"
      aria-label={`Notifications${unreadCount > 0 ? ` (${unreadCount} unread)` : ''}`}
    >
      <BellIcon size={22} className="notification-bell__icon" />
      {unreadCount > 0 && (
        <span className="notification-bell__badge pixel-border-red">
          {unreadCount > 99 ? '99+' : unreadCount}
        </span>
      )}
    </button>
  );
}
