import { useState, useCallback, useEffect, useRef, type ReactNode } from 'react';
import { toast } from 'sonner';
import type { TrendingHotel, TrendingNotification } from '@/types/trending';
import { TrendingNotificationContext } from '@/contexts/trending-context';

const MOCK_HOTELS: TrendingHotel[] = [
  {
    id: '1',
    name: 'The Mulia Resort',
    location: 'Bali, Indonesia',
    platform: 'Traveloka',
    pricePerNight: 'Rp 3.200.000',
    rating: 4.9,
    trendScore: 98,
    imageUrl: '',
    discount: '35% OFF',
    timestamp: new Date(),
  },
  {
    id: '2',
    name: 'Marina Bay Sands',
    location: 'Singapore',
    platform: 'Booking.com',
    pricePerNight: '$420',
    rating: 4.8,
    trendScore: 95,
    imageUrl: '',
    discount: '20% OFF',
    timestamp: new Date(),
  },
  {
    id: '3',
    name: 'Ayana Resort',
    location: 'Bali, Indonesia',
    platform: 'DQN',
    pricePerNight: 'Rp 2.800.000',
    rating: 4.7,
    trendScore: 92,
    imageUrl: '',
    discount: '40% OFF',
    timestamp: new Date(),
  },
  {
    id: '4',
    name: 'Shangri-La Hotel',
    location: 'Bangkok, Thailand',
    platform: 'Agoda',
    pricePerNight: '฿4,500',
    rating: 4.8,
    trendScore: 90,
    imageUrl: '',
    discount: '25% OFF',
    timestamp: new Date(),
  },
  {
    id: '5',
    name: 'Grand Hyatt Jakarta',
    location: 'Jakarta, Indonesia',
    platform: 'Tiket.com',
    pricePerNight: 'Rp 1.900.000',
    rating: 4.6,
    trendScore: 88,
    imageUrl: '',
    discount: '30% OFF',
    timestamp: new Date(),
  },
  {
    id: '6',
    name: 'Capella Ubud',
    location: 'Ubud, Bali',
    platform: 'Booking.com',
    pricePerNight: '$650',
    rating: 4.9,
    trendScore: 96,
    imageUrl: '',
    discount: '15% OFF',
    timestamp: new Date(),
  },
  {
    id: '7',
    name: 'W Hotel Seminyak',
    location: 'Seminyak, Bali',
    platform: 'Traveloka',
    pricePerNight: 'Rp 4.100.000',
    rating: 4.7,
    trendScore: 89,
    imageUrl: '',
    timestamp: new Date(),
  },
  {
    id: '8',
    name: 'Raffles Hotel',
    location: 'Singapore',
    platform: 'DQN',
    pricePerNight: '$580',
    rating: 4.9,
    trendScore: 94,
    imageUrl: '',
    discount: '10% OFF',
    timestamp: new Date(),
  },
];

const INCOMING_HOTELS: TrendingHotel[] = [
  {
    id: '9',
    name: 'Four Seasons Resort',
    location: 'Jimbaran, Bali',
    platform: 'Traveloka',
    pricePerNight: 'Rp 5.500.000',
    rating: 4.9,
    trendScore: 97,
    imageUrl: '',
    discount: '20% OFF',
    timestamp: new Date(),
  },
  {
    id: '10',
    name: 'Ritz-Carlton Langkawi',
    location: 'Langkawi, Malaysia',
    platform: 'Booking.com',
    pricePerNight: 'MYR 1,200',
    rating: 4.8,
    trendScore: 91,
    imageUrl: '',
    discount: '30% OFF',
    timestamp: new Date(),
  },
  {
    id: '11',
    name: 'Hotel Indonesia Kempinski',
    location: 'Jakarta, Indonesia',
    platform: 'Tiket.com',
    pricePerNight: 'Rp 2.400.000',
    rating: 4.7,
    trendScore: 87,
    imageUrl: '',
    discount: '45% OFF',
    timestamp: new Date(),
  },
  {
    id: '12',
    name: 'Aman Tokyo',
    location: 'Tokyo, Japan',
    platform: 'Agoda',
    pricePerNight: '¥85,000',
    rating: 4.9,
    trendScore: 99,
    imageUrl: '',
    discount: '15% OFF',
    timestamp: new Date(),
  },
];

function getPlatformColor(platform: TrendingHotel['platform']): string {
  const colors: Record<TrendingHotel['platform'], string> = {
    Traveloka: '#0194f3',
    'Booking.com': '#003580',
    DQN: '#ff6b35',
    Agoda: '#5542f6',
    'Tiket.com': '#0064d2',
  };
  return colors[platform];
}

export function TrendingNotificationProvider({ children }: { children: ReactNode }) {
  const [trendingHotels, setTrendingHotels] = useState<TrendingHotel[]>(MOCK_HOTELS);
  const [notifications, setNotifications] = useState<TrendingNotification[]>([]);
  const [isNotificationPanelOpen, setIsNotificationPanelOpen] = useState(false);
  const incomingIndexRef = useRef(0);

  const addNotification = useCallback((hotel: TrendingHotel) => {
    const notification: TrendingNotification = {
      id: `notif-${hotel.id}-${Date.now()}`,
      hotel,
      read: false,
      timestamp: new Date(),
    };
    setNotifications((prev) => [notification, ...prev].slice(0, 20));

    const color = getPlatformColor(hotel.platform);
    toast(`${hotel.name} sedang trending!`, {
      description: `${hotel.platform} · ${hotel.location} · ${hotel.pricePerNight}${hotel.discount ? ` · ${hotel.discount}` : ''}`,
      duration: 5000,
      style: {
        borderLeft: `4px solid ${color}`,
      },
    });
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      if (incomingIndexRef.current < INCOMING_HOTELS.length) {
        const hotel = INCOMING_HOTELS[incomingIndexRef.current];
        const newHotel = { ...hotel, timestamp: new Date() };
        setTrendingHotels((prev) => [newHotel, ...prev].slice(0, 12));
        addNotification(newHotel);
        incomingIndexRef.current += 1;
      }
    }, 8000);

    return () => clearInterval(interval);
  }, [addNotification]);

  const markAsRead = useCallback((id: string) => {
    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, read: true } : n))
    );
  }, []);

  const markAllAsRead = useCallback(() => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  }, []);

  const unreadCount = notifications.filter((n) => !n.read).length;

  return (
    <TrendingNotificationContext.Provider
      value={{
        notifications,
        unreadCount,
        trendingHotels,
        markAsRead,
        markAllAsRead,
        isNotificationPanelOpen,
        setIsNotificationPanelOpen,
      }}
    >
      {children}
    </TrendingNotificationContext.Provider>
  );
}
