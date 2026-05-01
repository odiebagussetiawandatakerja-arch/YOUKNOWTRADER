import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Menu, X, Bell, MapPin, Star, Check } from 'lucide-react';
import { useTrendingNotifications } from '@/hooks/use-trending-notifications';

const Navigation = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { notifications, unreadCount, markAsRead, markAllAsRead, isNotificationPanelOpen, setIsNotificationPanelOpen } = useTrendingNotifications();
  const panelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 100);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (panelRef.current && !panelRef.current.contains(e.target as Node)) {
        setIsNotificationPanelOpen(false);
      }
    };
    if (isNotificationPanelOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isNotificationPanelOpen, setIsNotificationPanelOpen]);

  const navLinks = [
    { label: 'How it works', href: '#how-it-works' },
    { label: 'Trending', href: '#trending' },
    { label: 'Performance', href: '#performance' },
    { label: 'Pricing', href: '#pricing' },
    { label: 'FAQ', href: '#faq' },
  ];

  const scrollToSection = (href: string) => {
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsMobileMenuOpen(false);
  };

  return (
    <>
      <nav
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
          isScrolled
            ? 'bg-navy/90 backdrop-blur-xl border-b border-white/5'
            : 'bg-transparent'
        }`}
      >
        <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
          <div className="flex items-center justify-between h-16 lg:h-20">
            {/* Logo */}
            <a
              href="#"
              className="font-mono text-sm tracking-[0.12em] uppercase text-foreground hover:text-neon-lime transition-colors"
            >
              YouKnowTrader
            </a>

            {/* Desktop Navigation */}
            <div className="hidden lg:flex items-center gap-8">
              {navLinks.map((link) => (
                <button
                  key={link.href}
                  onClick={() => scrollToSection(link.href)}
                  className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                >
                  {link.label}
                </button>
              ))}
            </div>

            {/* Notification Bell + CTA */}
            <div className="flex items-center gap-4">
              {/* Notification Bell */}
              <div className="relative" ref={panelRef}>
                <button
                  onClick={() => setIsNotificationPanelOpen(!isNotificationPanelOpen)}
                  className="relative p-2 text-muted-foreground hover:text-foreground transition-colors"
                  aria-label="Notifications"
                >
                  <Bell className="w-5 h-5" />
                  {unreadCount > 0 && (
                    <span className="absolute -top-0.5 -right-0.5 w-4.5 h-4.5 min-w-[18px] flex items-center justify-center rounded-full bg-neon-lime text-navy text-[10px] font-bold leading-none px-1">
                      {unreadCount}
                    </span>
                  )}
                </button>

                {/* Notification Panel */}
                {isNotificationPanelOpen && (
                  <div className="absolute right-0 top-full mt-2 w-[360px] max-h-[480px] rounded-2xl bg-navy-light border border-white/[0.08] shadow-card overflow-hidden z-[100]">
                    {/* Panel Header */}
                    <div className="flex items-center justify-between px-4 py-3 border-b border-white/[0.06]">
                      <div className="flex items-center gap-2">
                        <Bell className="w-4 h-4 text-neon-lime" />
                        <span className="text-sm font-semibold text-foreground">Trending Alerts</span>
                        {unreadCount > 0 && (
                          <span className="px-1.5 py-0.5 rounded-md bg-neon-lime/20 text-neon-lime text-[10px] font-bold">
                            {unreadCount}
                          </span>
                        )}
                      </div>
                      {unreadCount > 0 && (
                        <button
                          onClick={markAllAsRead}
                          className="flex items-center gap-1 text-[10px] text-muted-foreground hover:text-neon-lime transition-colors"
                        >
                          <Check className="w-3 h-3" />
                          Tandai semua
                        </button>
                      )}
                    </div>

                    {/* Notification List */}
                    <div className="overflow-y-auto max-h-[400px]">
                      {notifications.length === 0 ? (
                        <div className="flex flex-col items-center justify-center py-10 text-muted-foreground">
                          <Bell className="w-8 h-8 mb-2 opacity-30" />
                          <p className="text-xs">Belum ada notifikasi trending</p>
                        </div>
                      ) : (
                        notifications.map((notif) => (
                          <button
                            key={notif.id}
                            onClick={() => markAsRead(notif.id)}
                            className={`w-full text-left px-4 py-3 border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors ${
                              !notif.read ? 'bg-neon-lime/[0.03]' : ''
                            }`}
                          >
                            <div className="flex items-start gap-3">
                              {/* Unread indicator */}
                              <div className="mt-1.5 shrink-0">
                                {!notif.read ? (
                                  <span className="block w-2 h-2 rounded-full bg-neon-lime" />
                                ) : (
                                  <span className="block w-2 h-2 rounded-full bg-white/10" />
                                )}
                              </div>

                              <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2 mb-0.5">
                                  <span className="text-xs font-semibold text-foreground truncate">
                                    {notif.hotel.name}
                                  </span>
                                  {notif.hotel.discount && (
                                    <span className="shrink-0 px-1.5 py-0.5 rounded bg-profit/20 text-profit text-[9px] font-bold">
                                      {notif.hotel.discount}
                                    </span>
                                  )}
                                </div>
                                <div className="flex items-center gap-2 text-[10px] text-muted-foreground">
                                  <span className="font-medium text-foreground/70">{notif.hotel.platform}</span>
                                  <span>·</span>
                                  <MapPin className="w-2.5 h-2.5" />
                                  <span>{notif.hotel.location}</span>
                                </div>
                                <div className="flex items-center gap-2 mt-1 text-[10px]">
                                  <span className="text-foreground font-medium">{notif.hotel.pricePerNight}</span>
                                  <span className="text-muted-foreground">/malam</span>
                                  <span className="text-muted-foreground">·</span>
                                  <Star className="w-2.5 h-2.5 text-yellow-400 fill-yellow-400" />
                                  <span className="text-muted-foreground">{notif.hotel.rating}</span>
                                </div>
                              </div>
                            </div>
                          </button>
                        ))
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* CTA Button */}
              <div className="hidden lg:block">
                <Button
                  onClick={() => scrollToSection('#pricing')}
                  variant="outline"
                  className="border-neon-lime text-neon-lime hover:bg-neon-lime hover:text-navy transition-all duration-300"
                >
                  Start Copying
                </Button>
              </div>

              {/* Mobile Menu Button */}
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="lg:hidden p-2 text-foreground"
              >
                {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div
        className={`fixed inset-0 z-40 lg:hidden transition-all duration-300 ${
          isMobileMenuOpen ? 'opacity-100 visible' : 'opacity-0 invisible'
        }`}
      >
        <div
          className="absolute inset-0 bg-navy/95 backdrop-blur-xl"
          onClick={() => setIsMobileMenuOpen(false)}
        />
        <div className="relative flex flex-col items-center justify-center h-full gap-8">
          {navLinks.map((link) => (
            <button
              key={link.href}
              onClick={() => scrollToSection(link.href)}
              className="text-2xl font-display text-foreground hover:text-neon-lime transition-colors"
            >
              {link.label}
            </button>
          ))}
          <Button
            onClick={() => scrollToSection('#pricing')}
            className="mt-4 bg-neon-lime text-navy hover:bg-neon-lime/90"
          >
            Start Copying
          </Button>
        </div>
      </div>
    </>
  );
};

export default Navigation;
