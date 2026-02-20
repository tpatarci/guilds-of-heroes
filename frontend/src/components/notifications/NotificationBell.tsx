import { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import * as apiClient from '../../api/client';
import { colors, fonts } from '../../styles/theme';

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
    // Poll every 30 seconds for new notifications
    const interval = setInterval(fetchUnread, 30000);
    return () => clearInterval(interval);
  }, [fetchUnread]);

  return (
    <button
      onClick={() => navigate('/notifications')}
      style={{
        position: 'relative',
        background: 'none',
        border: 'none',
        cursor: 'pointer',
        padding: '4px 8px',
        fontSize: '20px',
        color: colors.parchment,
        fontFamily: fonts.body,
      }}
      title="Notifications"
    >
      {/* Bell icon using text */}
      <span role="img" aria-label="notifications">
        {'\u{1F514}'}
      </span>
      {unreadCount > 0 && (
        <span
          style={{
            position: 'absolute',
            top: '-2px',
            right: '-2px',
            background: colors.dragonRed,
            color: colors.white,
            fontFamily: fonts.heading,
            fontSize: '8px',
            minWidth: '16px',
            height: '16px',
            lineHeight: '16px',
            textAlign: 'center',
            borderRadius: '0',
            padding: '0 3px',
            boxShadow: `
              -1px 0 0 0 ${colors.dragonRed},
              1px 0 0 0 ${colors.dragonRed},
              0 -1px 0 0 ${colors.dragonRed},
              0 1px 0 0 ${colors.dragonRed}
            `,
          }}
        >
          {unreadCount > 99 ? '99+' : unreadCount}
        </span>
      )}
    </button>
  );
}
