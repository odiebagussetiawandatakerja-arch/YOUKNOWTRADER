import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Button } from '@/components/ui/button';
import { Check, ExternalLink } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const features = [
  'No subscription fee',
  'No setup fee',
  'Pause or stop anytime',
];

const exchanges = ['Binance', 'Bybit', 'BingX'];

const PricingSection = () => {
  const sectionRef = useRef<HTMLDivElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const cardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    const header = headerRef.current;
    const card = cardRef.current;

    if (!section || !header || !card) return;

    const ctx = gsap.context(() => {
      // Header animation
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

      // Card animation
      gsap.fromTo(
        card,
        { opacity: 0, y: 50, rotateX: 12 },
        {
          opacity: 1,
          y: 0,
          rotateX: 0,
          duration: 0.8,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: card,
            start: 'top 72%',
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
      id="pricing"
      className="relative w-full py-20 lg:py-32 bg-navy"
    >
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        {/* Header */}
        <div ref={headerRef} className="text-center mb-12">
          <h2 className="font-display text-3xl lg:text-4xl xl:text-5xl font-bold text-foreground mb-4">
            Simple pricing.{' '}
            <span className="text-gradient">No hidden fees.</span>
          </h2>
        </div>

        {/* Pricing Card */}
        <div
          ref={cardRef}
          className="max-w-lg mx-auto"
          style={{ perspective: '1000px' }}
        >
          <div className="relative p-8 lg:p-10 rounded-2xl bg-navy-light border border-white/[0.08] shadow-card">
            {/* Glow effect */}
            <div className="absolute inset-0 rounded-2xl bg-neon-lime/5 opacity-50" />

            <div className="relative">
              {/* Plan Name */}
              <span className="font-mono text-xs tracking-[0.12em] uppercase text-muted-foreground block mb-6">
                COPY-TRADING
              </span>

              {/* Price */}
              <div className="flex items-baseline gap-2 mb-2">
                <span className="font-display text-6xl lg:text-7xl font-bold text-neon-lime">
                  10%
                </span>
              </div>
              <p className="text-muted-foreground text-sm mb-8">
                performance fee on profitable months
              </p>

              {/* Features */}
              <ul className="space-y-3 mb-8">
                {features.map((feature, index) => (
                  <li
                    key={index}
                    className="flex items-center gap-3 text-foreground"
                  >
                    <div className="w-5 h-5 rounded-full bg-neon-lime/20 flex items-center justify-center">
                      <Check className="w-3 h-3 text-neon-lime" />
                    </div>
                    <span className="text-sm">{feature}</span>
                  </li>
                ))}
              </ul>

              {/* CTA */}
              <Button
                size="lg"
                className="w-full bg-neon-lime text-navy hover:bg-neon-lime/90 transition-all duration-300 font-semibold mb-4"
              >
                Connect Exchange & Start
                <ExternalLink className="w-4 h-4 ml-2" />
              </Button>

              {/* Exchanges note */}
              <p className="text-center text-xs text-muted-foreground">
                Available on{' '}
                {exchanges.map((exchange, index) => (
                  <span key={exchange}>
                    <span className="text-foreground">{exchange}</span>
                    {index < exchanges.length - 1 ? ' / ' : ''}
                  </span>
                ))}{' '}
                (depending on region)
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default PricingSection;
