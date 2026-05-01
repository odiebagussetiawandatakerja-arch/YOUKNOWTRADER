import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { TrendingUp, Bell, Star, MapPin, Flame, Bot } from 'lucide-react';
import { useTrendingNotifications } from '@/hooks/use-trending-notifications';
import type { TrendingHotel } from '@/types/trending';

gsap.registerPlugin(ScrollTrigger);

function getPlatformBadgeClass(platform: TrendingHotel['platform']): string {
  const classes: Record<TrendingHotel['platform'], string> = {
    Traveloka: 'bg-[#0194f3]/20 text-[#0194f3]',
    'Booking.com': 'bg-[#003580]/30 text-[#4a90d9]',
    DQN: 'bg-[#ff6b35]/20 text-[#ff6b35]',
    Agoda: 'bg-[#5542f6]/20 text-[#8b7fff]',
    'Tiket.com': 'bg-[#0064d2]/20 text-[#3d8de5]',
  };
  return classes[platform];
}

function getTrendColor(score: number): string {
  if (score >= 95) return 'text-neon-lime';
  if (score >= 90) return 'text-profit';
  if (score >= 85) return 'text-neon-cyan';
  return 'text-muted-foreground';
}

const TrendingBotSection = () => {
  const sectionRef = useRef<HTMLDivElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const gridRef = useRef<HTMLDivElement>(null);
  const { trendingHotels } = useTrendingNotifications();

  useEffect(() => {
    const section = sectionRef.current;
    const header = headerRef.current;
    const grid = gridRef.current;

    if (!section || !header || !grid) return;

    const ctx = gsap.context(() => {
      gsap.fromTo(
        header,
        { opacity: 0, y: 24 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: header,
            start: 'top 80%',
            end: 'top 55%',
            scrub: 0.5,
          },
        }
      );

      const cards = grid.querySelectorAll('.trending-card');
      gsap.fromTo(
        cards,
        { opacity: 0, y: 40, scale: 0.97 },
        {
          opacity: 1,
          y: 0,
          scale: 1,
          duration: 0.8,
          stagger: 0.08,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: grid,
            start: 'top 78%',
            end: 'top 45%',
            scrub: 0.5,
          },
        }
      );
    }, section);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      id="trending"
      className="relative w-full py-20 lg:py-32 bg-navy"
      style={{
        background:
          'radial-gradient(ellipse at bottom left, rgba(57,255,20,0.03) 0%, transparent 50%), radial-gradient(ellipse at top right, rgba(0,217,255,0.03) 0%, transparent 50%), #070A12',
      }}
    >
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        {/* Header */}
        <div ref={headerRef} className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-neon-lime/10 border border-neon-lime/20 mb-6">
            <Bot className="w-4 h-4 text-neon-lime" />
            <span className="font-mono text-xs tracking-[0.12em] uppercase text-neon-lime">
              Bot Trending — Live
            </span>
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-neon-lime opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-neon-lime" />
            </span>
          </div>

          <h2 className="font-display text-3xl lg:text-4xl xl:text-5xl font-bold text-foreground mb-4">
            Hotel Trending{' '}
            <span className="text-gradient">Real-Time Alert</span>
          </h2>
          <p className="text-muted-foreground text-base lg:text-lg max-w-2xl mx-auto">
            Bot otomatis monitor hotel trending dari Traveloka, Booking.com, DQN, Agoda &amp; Tiket.com.
            Langsung notif ke kamu kalau ada deal bagus.
          </p>

          {/* Platform badges */}
          <div className="flex flex-wrap justify-center gap-3 mt-8">
            {(['Traveloka', 'Booking.com', 'DQN', 'Agoda', 'Tiket.com'] as const).map(
              (platform) => (
                <span
                  key={platform}
                  className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium ${getPlatformBadgeClass(platform)}`}
                >
                  <Bell className="w-3 h-3" />
                  {platform}
                </span>
              )
            )}
          </div>
        </div>

        {/* Trending Grid */}
        <div
          ref={gridRef}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5 max-w-7xl mx-auto"
        >
          {trendingHotels.slice(0, 8).map((hotel) => (
            <div
              key={hotel.id}
              className="trending-card group relative p-5 rounded-2xl bg-navy-light border border-white/[0.08] hover:border-neon-lime/30 transition-all duration-500"
            >
              {/* Glow effect on hover */}
              <div className="absolute inset-0 rounded-2xl bg-neon-lime/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

              <div className="relative">
                {/* Top row: Platform badge + Trend score */}
                <div className="flex items-center justify-between mb-4">
                  <span
                    className={`inline-flex items-center px-2.5 py-1 rounded-md text-[10px] font-semibold uppercase tracking-wider ${getPlatformBadgeClass(hotel.platform)}`}
                  >
                    {hotel.platform}
                  </span>
                  <div className="flex items-center gap-1">
                    <Flame className={`w-3.5 h-3.5 ${getTrendColor(hotel.trendScore)}`} />
                    <span className={`text-xs font-bold ${getTrendColor(hotel.trendScore)}`}>
                      {hotel.trendScore}
                    </span>
                  </div>
                </div>

                {/* Hotel name */}
                <h3 className="font-display text-base font-semibold text-foreground mb-1 group-hover:text-neon-lime transition-colors">
                  {hotel.name}
                </h3>

                {/* Location */}
                <div className="flex items-center gap-1 mb-3">
                  <MapPin className="w-3 h-3 text-muted-foreground" />
                  <span className="text-xs text-muted-foreground">{hotel.location}</span>
                </div>

                {/* Rating */}
                <div className="flex items-center gap-1 mb-4">
                  <Star className="w-3.5 h-3.5 text-yellow-400 fill-yellow-400" />
                  <span className="text-xs text-foreground font-medium">{hotel.rating}</span>
                </div>

                {/* Price + Discount */}
                <div className="flex items-center justify-between pt-3 border-t border-white/[0.06]">
                  <div>
                    <span className="text-sm font-bold text-foreground">{hotel.pricePerNight}</span>
                    <span className="text-[10px] text-muted-foreground ml-1">/malam</span>
                  </div>
                  {hotel.discount && (
                    <span className="px-2 py-0.5 rounded-md bg-profit/20 text-profit text-[10px] font-bold">
                      {hotel.discount}
                    </span>
                  )}
                </div>

                {/* Trending indicator bar */}
                <div className="mt-3">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[10px] text-muted-foreground">Trend Score</span>
                    <TrendingUp className={`w-3 h-3 ${getTrendColor(hotel.trendScore)}`} />
                  </div>
                  <div className="w-full h-1.5 rounded-full bg-white/[0.06] overflow-hidden">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-neon-cyan to-neon-lime transition-all duration-1000"
                      style={{ width: `${hotel.trendScore}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* Accent line */}
              <div className="absolute bottom-0 left-5 right-5 h-[2px] bg-gradient-to-r from-neon-lime/0 via-neon-lime/50 to-neon-lime/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            </div>
          ))}
        </div>

        {/* Bottom note */}
        <div className="text-center mt-12">
          <p className="text-sm text-muted-foreground">
            <Bell className="w-4 h-4 inline-block mr-1 -mt-0.5 text-neon-lime" />
            Notifikasi otomatis aktif — hotel trending baru akan muncul dan langsung notif ke kamu
          </p>
        </div>
      </div>
    </section>
  );
};

export default TrendingBotSection;
