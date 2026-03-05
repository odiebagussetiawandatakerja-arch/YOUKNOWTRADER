import { useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const HeroSection = () => {
  const sectionRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const bgRef = useRef<HTMLDivElement>(null);
  const eyebrowRef = useRef<HTMLSpanElement>(null);
  const headlineRef = useRef<HTMLHeadingElement>(null);
  const subheadlineRef = useRef<HTMLParagraphElement>(null);
  const ctaRef = useRef<HTMLDivElement>(null);
  const statsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    const content = contentRef.current;
    const bg = bgRef.current;
    const eyebrow = eyebrowRef.current;
    const headline = headlineRef.current;
    const subheadline = subheadlineRef.current;
    const cta = ctaRef.current;
    const stats = statsRef.current;

    if (!section || !content || !bg || !eyebrow || !headline || !subheadline || !cta || !stats) return;

    const ctx = gsap.context(() => {
      // Initial state
      gsap.set(bg, { opacity: 0, scale: 1.06 });
      gsap.set(eyebrow, { opacity: 0, y: 12 });
      gsap.set(headline, { opacity: 0, y: 28 });
      gsap.set(subheadline, { opacity: 0, y: 18 });
      gsap.set(cta, { opacity: 0, scale: 0.96 });
      gsap.set(stats.children, { opacity: 0, y: 10 });

      // Entrance animation timeline
      const entranceTl = gsap.timeline({ delay: 0.3 });

      entranceTl
        .to(bg, { opacity: 1, scale: 1, duration: 1.1, ease: 'power2.out' })
        .to(eyebrow, { opacity: 1, y: 0, duration: 0.5 }, '-=0.6')
        .to(headline, { opacity: 1, y: 0, duration: 0.9 }, '-=0.4')
        .to(subheadline, { opacity: 1, y: 0, duration: 0.7 }, '-=0.5')
        .to(cta, { opacity: 1, scale: 1, duration: 0.55 }, '-=0.4')
        .to(stats.children, { opacity: 1, y: 0, duration: 0.6, stagger: 0.06 }, '-=0.3');

      // Scroll-driven exit animation
      const scrollTl = gsap.timeline({
        scrollTrigger: {
          trigger: section,
          start: 'top top',
          end: '+=130%',
          pin: true,
          scrub: 0.6,
          onLeaveBack: () => {
            // Reset to visible state when scrolling back
            gsap.to(content, { x: 0, opacity: 1, duration: 0.3 });
            gsap.to(bg, { scale: 1, y: 0, duration: 0.3 });
          },
        },
      });

      // EXIT phase (70% - 100%)
      scrollTl
        .fromTo(
          content,
          { x: 0, opacity: 1 },
          { x: '18vw', opacity: 0, ease: 'power2.in' },
          0.7
        )
        .fromTo(
          bg,
          { scale: 1, y: 0 },
          { scale: 1.08, y: '-6vh', ease: 'power2.in' },
          0.7
        );
    }, section);

    return () => ctx.revert();
  }, []);

  const scrollToPricing = () => {
    const element = document.querySelector('#pricing');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section
      ref={sectionRef}
      className="relative w-full h-screen overflow-hidden z-10"
    >
      {/* Background Image */}
      <div
        ref={bgRef}
        className="absolute inset-0 w-full h-full"
        style={{
          backgroundImage: 'url(/images/hero_neon_street.jpg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        {/* Gradient Overlay */}
        <div
          className="absolute inset-0"
          style={{
            background:
              'linear-gradient(90deg, rgba(7,10,18,0.25) 0%, rgba(7,10,18,0.72) 55%, rgba(7,10,18,0.92) 100%)',
          }}
        />
      </div>

      {/* Grain Overlay */}
      <div className="absolute inset-0 grain-overlay pointer-events-none" />

      {/* Content */}
      <div
        ref={contentRef}
        className="relative z-10 flex items-center justify-end h-full px-4 sm:px-6 lg:px-8 xl:px-12"
      >
        <div className="w-full max-w-xl lg:max-w-2xl xl:max-w-xl text-right lg:pr-8 xl:pr-16">
          {/* Eyebrow */}
          <span
            ref={eyebrowRef}
            className="inline-block font-mono text-xs tracking-[0.12em] uppercase text-neon-lime mb-4"
          >
            LEAD TRADER — SINCE 2019
          </span>

          {/* Headline */}
          <h1
            ref={headlineRef}
            className="font-display text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-bold text-foreground leading-[0.95] tracking-tight mb-6"
          >
            Copy the trader who sees the move{' '}
            <span className="text-gradient">before it happens.</span>
          </h1>

          {/* Subheadline */}
          <p
            ref={subheadlineRef}
            className="text-base lg:text-lg text-muted-foreground mb-8 max-w-md ml-auto"
          >
            Clear entries. Defined exits. Risk-first sizing. You get the same
            trade—automatically.
          </p>

          {/* CTA */}
          <div ref={ctaRef} className="mb-10">
            <Button
              onClick={scrollToPricing}
              size="lg"
              className="bg-transparent border-2 border-neon-lime text-neon-lime hover:bg-neon-lime hover:text-navy transition-all duration-300 px-8 py-6 text-base font-semibold glow-accent"
            >
              Start Copying
            </Button>
          </div>

          {/* Stats */}
          <div
            ref={statsRef}
            className="flex flex-wrap justify-end gap-6 lg:gap-10"
          >
            <div className="text-right">
              <div className="font-mono text-xl lg:text-2xl font-bold text-profit">
                +187%
              </div>
              <div className="font-mono text-[10px] tracking-[0.12em] uppercase text-muted-foreground">
                12M RETURN
              </div>
            </div>
            <div className="text-right">
              <div className="font-mono text-xl lg:text-2xl font-bold text-foreground">
                8.2K
              </div>
              <div className="font-mono text-[10px] tracking-[0.12em] uppercase text-muted-foreground">
                COPIERS
              </div>
            </div>
            <div className="text-right">
              <div className="font-mono text-xl lg:text-2xl font-bold text-profit">
                83%
              </div>
              <div className="font-mono text-[10px] tracking-[0.12em] uppercase text-muted-foreground">
                WIN RATE
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
