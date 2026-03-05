import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const metrics = [
  { label: 'Net Return', value: '+187%', color: 'text-profit' },
  { label: 'Avg Monthly', value: '+9.2%', color: 'text-profit' },
  { label: 'Max Drawdown', value: '-11%', color: 'text-loss' },
  { label: 'Win Rate', value: '83%', color: 'text-profit' },
];

const PerformanceSection = () => {
  const sectionRef = useRef<HTMLDivElement>(null);
  const bgRef = useRef<HTMLDivElement>(null);
  const headlineRef = useRef<HTMLDivElement>(null);
  const cardRef = useRef<HTMLDivElement>(null);
  const metricsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    const bg = bgRef.current;
    const headline = headlineRef.current;
    const card = cardRef.current;
    const metricsEl = metricsRef.current;

    if (!section || !bg || !headline || !card || !metricsEl) return;

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
          { scale: 1.12, opacity: 0.7 },
          { scale: 1, opacity: 1, ease: 'none' },
          0
        )
        .fromTo(
          headline,
          { x: '-40vw', opacity: 0 },
          { x: 0, opacity: 1, ease: 'power2.out' },
          0
        )
        .fromTo(
          card,
          { x: '40vw', opacity: 0, rotateY: 18 },
          { x: 0, opacity: 1, rotateY: 0, ease: 'power2.out' },
          0
        )
        .fromTo(
          metricsEl.children,
          { y: 18, opacity: 0 },
          { y: 0, opacity: 1, stagger: 0.02, ease: 'power2.out' },
          0.1
        );

      // SETTLE (30% - 70%) - hold position

      // EXIT (70% - 100%)
      scrollTl
        .fromTo(
          headline,
          { x: 0, opacity: 1 },
          { x: '-12vw', opacity: 0, ease: 'power2.in' },
          0.7
        )
        .fromTo(
          card,
          { x: 0, opacity: 1 },
          { x: '12vw', opacity: 0, ease: 'power2.in' },
          0.7
        )
        .fromTo(
          bg,
          { y: 0 },
          { y: '8vh', ease: 'power2.in' },
          0.7
        );
    }, section);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      id="performance"
      className="relative w-full h-screen overflow-hidden z-20"
    >
      {/* Background Image */}
      <div
        ref={bgRef}
        className="absolute inset-0 w-full h-full"
        style={{
          backgroundImage: 'url(/images/performance_red_corridor.jpg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        {/* Gradient Overlay */}
        <div
          className="absolute inset-0"
          style={{
            background:
              'linear-gradient(180deg, rgba(7,10,18,0.35) 0%, rgba(7,10,18,0.85) 100%)',
          }}
        />
      </div>

      {/* Grain Overlay */}
      <div className="absolute inset-0 grain-overlay pointer-events-none" />

      {/* Content */}
      <div className="relative z-10 flex items-center h-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div className="w-full flex flex-col lg:flex-row items-center justify-between gap-8 lg:gap-12">
          {/* Left Headline Block */}
          <div
            ref={headlineRef}
            className="w-full lg:w-1/2 xl:max-w-xl"
          >
            <h2 className="font-display text-3xl sm:text-4xl lg:text-5xl font-bold text-foreground leading-tight mb-6">
              Performance built on{' '}
              <span className="text-gradient">discipline—not luck.</span>
            </h2>
            <p className="text-muted-foreground text-base lg:text-lg">
              I trade a system. The numbers are a byproduct of consistency.
            </p>
          </div>

          {/* Right Performance Card */}
          <div
            ref={cardRef}
            className="w-full lg:w-auto"
            style={{ perspective: '1000px' }}
          >
            <div className="glass-panel rounded-2xl p-6 lg:p-8 max-w-sm mx-auto lg:mx-0">
              {/* Card Title */}
              <span className="font-mono text-xs tracking-[0.12em] uppercase text-muted-foreground block mb-6">
                12-MONTH SNAPSHOT
              </span>

              {/* Metrics */}
              <div ref={metricsRef} className="space-y-5">
                {metrics.map((metric, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between pb-4 border-b border-white/5 last:border-0 last:pb-0"
                  >
                    <span className="text-sm text-muted-foreground">
                      {metric.label}
                    </span>
                    <span
                      className={`font-mono text-xl font-bold ${metric.color}`}
                    >
                      {metric.value}
                    </span>
                  </div>
                ))}
              </div>

              {/* Disclaimer */}
              <p className="mt-6 text-[10px] text-muted-foreground/60 leading-relaxed">
                Past performance does not guarantee future results.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default PerformanceSection;
