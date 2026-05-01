export interface TrendingHotel {
  id: string;
  name: string;
  location: string;
  platform: 'Traveloka' | 'Booking.com' | 'DQN' | 'Agoda' | 'Tiket.com';
  pricePerNight: string;
  rating: number;
  trendScore: number;
  imageUrl: string;
  discount?: string;
  timestamp: Date;
}

export interface TrendingNotification {
  id: string;
  hotel: TrendingHotel;
  read: boolean;
  timestamp: Date;
}

export interface TrendingNotificationContextType {
  notifications: TrendingNotification[];
  unreadCount: number;
  trendingHotels: TrendingHotel[];
  markAsRead: (id: string) => void;
  markAllAsRead: () => void;
  isNotificationPanelOpen: boolean;
  setIsNotificationPanelOpen: (open: boolean) => void;
}
