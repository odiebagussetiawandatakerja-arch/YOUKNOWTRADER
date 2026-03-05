import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { TrendingUp, Target, Shield, RefreshCw } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const principles = [
  {
    icon: TrendingUp,
    text: 'Trade with the higher timeframe trend.',
  },
  {
    icon: Target,
    text: 'Enter at key levels—never chase.',
  },
  {
    icon: Shield,
    text: 'Risk is fixed before reward is imagined.',
  },
  {
    icon: RefreshCw,
    text: 'Review every session. Adjust weekly.',
  },
];

const StrategySection = () => {
  const sectionRef = useRef<HTMLDivElement>(null);
  const bgRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const principlesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    const bg = bgRef.current;
    const content = contentRef.current;
    const principlesEl = principlesRef.current;

    if (!section || !bg || !content || !principlesEl) return;

    const ctx = gsap.context(() => {
      const scrollTl = gsap.timeline({
        scrollTrigger: {
          trigger: section,
          start: 'top top',
          end: '+=130%',
          pin: true,
          scrub: 0.6,
        },
      });

      // ENTRANCE (0% - 30%)
      scrollTl
        .fromTo(
          bg,
          { scale: 1.1, opacity: 0.8 },
          { scale: 1, opacity: 1, ease: 'none' },
          0
        )
        .fromTo(
          content.querySelector('h2'),
          { x: '-35vw', opacity: 0 },
          { x: 0, opacity: 1, ease: 'power2.out' },
          0
        )
        .fromTo(
          content.querySelector('p'),
          { x: '-35vw', opacity: 0 },
          { x: 0, opacity: 1, ease: 'power2.out' },
          0.05
        )
        .fromTo(
          principlesEl.children,
          { x: '-18vw', opacity: 0 },
          { x: 0, opacity: 1, stagger: 0.02, ease: 'power2.out' },
          0.1
        );

      // SETTLE (30% - 70%) - hold position

      // EXIT (70% - 100%)
      scrollTl
        .fromTo(
          content,
          { y: 0, opacity: 1 },
          { y: '-10vh', opacity: 0, ease: 'power2.in' },
          0.7
        )
        .fromTo(
          bg,
          { y: 0 },
          { y: '-6vh', ease: 'power2.in' },
          0.7
        );
    }, section);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      className="relative w-full h-screen overflow-hidden z-30"
    >
      {/* Background Image */}
      <div
        ref={bgRef}
        className="absolute inset-0 w-full h-full"
        style={{
          backgroundImage: 'url(/images/strategy_green_corridor.jpg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        {/* Gradient Overlay */}
        <div
          className="absolute inset-0"
          style={{
            background:
              'linear-gradient(90deg, rgba(7,10,18,0.82) 0%, rgba(7,10,18,0.45) 60%, rgba(7,10,18,0.25) 100%)',
          }}
        />
      </div>

      {/* Grain Overlay */}
      <div className="absolute inset-0 grain-overlay pointer-events-none" />

      {/* Content */}
      <div className="relative z-10 flex items-center h-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div
          ref={contentRef}
          className="w-full max-w-2xl"
        >
          {/* Headline */}
          <h2 className="font-display text-3xl sm:text-4xl lg:text-5xl font-bold text-foreground leading-tight mb-6">
            I don't predict.{' '}
            <span className="text-gradient">I respond.</span>
          </h2>

          {/* Body */}
          <p className="text-muted-foreground text-base lg:text-lg mb-10 max-w-lg">
            The market moves. I measure momentum, structure, and risk—then I
            take the trade.
          </p>

          {/* Principles List */}
          <div ref={principlesRef} className="space-y-4">
            {principles.map((principle, index) => (
              <div
                key={index}
                className="flex items-center gap-4 p-4 rounded-xl bg-navy/60 border border-white/[0.06] backdrop-blur-sm"
              >
                {/* Accent line */}
                <div className="w-1 h-8 bg-neon-lime rounded-full shrink-0" />

                {/* Icon */}
                <div className="w-10 h-10 rounded-lg bg-neon-lime/10 flex items-center justify-center shrink-0">
                  <principle.icon className="w-5 h-5 text-neon-lime" />
                </div>

                {/* Text */}
                <span className="text-foreground text-sm lg:text-base">
                  {principle.text}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default StrategySection;
