import { createContext } from 'react';
import type { TrendingNotificationContextType } from '@/types/trending';

export const TrendingNotificationContext = createContext<TrendingNotificationContextType | null>(null);
