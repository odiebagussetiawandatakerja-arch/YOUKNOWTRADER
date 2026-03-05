import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { AlertTriangle, Gauge, Pause } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const riskNotes = [
  {
    icon: AlertTriangle,
    text: 'Max drawdown is capped—and disclosed.',
  },
  {
    icon: Gauge,
    text: 'Leverage is controlled. No 100x hope trades.',
  },
  {
    icon: Pause,
    text: 'You can pause copying anytime.',
  },
];

const RiskSection = () => {
  const sectionRef = useRef<HTMLDivElement>(null);
  const bgRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    const bg = bgRef.current;
    const content = contentRef.current;
    const cards = cardsRef.current;

    if (!section || !bg || !content || !cards) return;

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
          { scale: 1.1 },
          { scale: 1, ease: 'none' },
          0
        )
        .fromTo(
          content.querySelector('h2'),
          { y: '18vh', opacity: 0 },
          { y: 0, opacity: 1, ease: 'power2.out' },
          0
        )
        .fromTo(
          content.querySelector('p'),
          { y: '10vh', opacity: 0 },
          { y: 0, opacity: 1, ease: 'power2.out' },
          0.05
        )
        .fromTo(
          cards.children,
          { y: '12vh', opacity: 0, scale: 0.98 },
          { y: 0, opacity: 1, scale: 1, stagger: 0.02, ease: 'power2.out' },
          0.1
        );

      // SETTLE (30% - 70%) - hold position

      // EXIT (70% - 100%)
      scrollTl
        .fromTo(
          content,
          { opacity: 1 },
          { opacity: 0, ease: 'power2.in' },
          0.7
        )
        .fromTo(
          cards,
          { y: 0, opacity: 1 },
          { y: '10vh', opacity: 0, ease: 'power2.in' },
          0.7
        )
        .fromTo(
          bg,
          { y: 0 },
          { y: '10vh', ease: 'power2.in' },
          0.7
        );
    }, section);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      className="relative w-full h-screen overflow-hidden z-40"
    >
      {/* Background Image */}
      <div
        ref={bgRef}
        className="absolute inset-0 w-full h-full"
        style={{
          backgroundImage: 'url(/images/risk_neon_street.jpg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        {/* Gradient Overlay */}
        <div
          className="absolute inset-0"
          style={{
            background:
              'linear-gradient(180deg, rgba(7,10,18,0.30) 0%, rgba(7,10,18,0.88) 100%)',
          }}
        />
      </div>

      {/* Grain Overlay */}
      <div className="absolute inset-0 grain-overlay pointer-events-none" />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-center h-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div ref={contentRef} className="text-center max-w-3xl mb-12">
          {/* Headline */}
          <h2 className="font-display text-3xl sm:text-4xl lg:text-5xl font-bold text-foreground leading-tight mb-6">
            Real talk:{' '}
            <span className="text-loss">trading is risky.</span>
          </h2>

          {/* Body */}
          <p className="text-muted-foreground text-base lg:text-lg">
            Copy-trading doesn't remove risk. It mirrors it. I publish my
            drawdowns, my losing months, and my rules—so you can decide with
            your eyes open.
          </p>
        </div>

        {/* Risk Cards */}
        <div
          ref={cardsRef}
          className="flex flex-col sm:flex-row gap-4 max-w-3xl w-full"
        >
          {riskNotes.map((note, index) => (
            <div
              key={index}
              className="flex-1 p-5 rounded-xl bg-navy/80 border border-white/[0.06] backdrop-blur-sm text-center"
            >
              <div className="w-10 h-10 rounded-lg bg-loss/10 flex items-center justify-center mx-auto mb-3">
                <note.icon className="w-5 h-5 text-loss" />
              </div>
              <p className="text-sm text-foreground">{note.text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default RiskSection;
