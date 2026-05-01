import { useContext } from 'react';
import { TrendingNotificationContext } from '@/contexts/trending-context';

export function useTrendingNotifications() {
  const ctx = useContext(TrendingNotificationContext);
  if (!ctx) {
    throw new Error('useTrendingNotifications must be used within TrendingNotificationProvider');
  }
  return ctx;
}
