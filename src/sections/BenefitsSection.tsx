import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Zap, Scale, Eye } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const benefits = [
  {
    icon: Zap,
    title: 'Auto-Execution',
    description:
      'No missed entries. No emotional delays. The trade happens while you sleep.',
  },
  {
    icon: Scale,
    title: 'Same Risk Profile',
    description:
      'Your sizing scales to your account—my stop is your stop.',
  },
  {
    icon: Eye,
    title: 'Transparent History',
    description:
      'Every trade is logged. Win, loss, break-even—you see it all.',
  },
];

const BenefitsSection = () => {
  const sectionRef = useRef<HTMLDivElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    const header = headerRef.current;
    const cards = cardsRef.current;

    if (!section || !header || !cards) return;

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

      // Cards animation
      const cardElements = cards.querySelectorAll('.benefit-card');
      gsap.fromTo(
        cardElements,
        { opacity: 0, y: 50, scale: 0.98 },
        {
          opacity: 1,
          y: 0,
          scale: 1,
          duration: 0.8,
          stagger: 0.12,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: cards,
            start: 'top 78%',
            end: 'top 48%',
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
      className="relative w-full py-20 lg:py-32 bg-navy"
    >
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        {/* Header */}
        <div ref={headerRef} className="text-center mb-16">
          <h2 className="font-display text-3xl lg:text-4xl xl:text-5xl font-bold text-foreground mb-4">
            Why copy instead of following signals?
          </h2>
          <p className="text-muted-foreground text-base lg:text-lg max-w-xl mx-auto">
            Execution beats intention. Here's what changes when you copy.
          </p>
        </div>

        {/* Cards */}
        <div
          ref={cardsRef}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8 max-w-6xl mx-auto"
        >
          {benefits.map((benefit, index) => (
            <div
              key={index}
              className="benefit-card group relative p-6 lg:p-8 rounded-2xl bg-navy-light border border-white/[0.08] hover:border-neon-lime/30 transition-all duration-500"
            >
              {/* Glow effect on hover */}
              <div className="absolute inset-0 rounded-2xl bg-neon-lime/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

              {/* Icon */}
              <div className="relative mb-6">
                <div className="w-12 h-12 rounded-xl bg-neon-lime/10 flex items-center justify-center group-hover:bg-neon-lime/20 transition-colors duration-300">
                  <benefit.icon className="w-6 h-6 text-neon-lime" />
                </div>
              </div>

              {/* Content */}
              <div className="relative">
                <h3 className="font-display text-xl font-semibold text-foreground mb-3">
                  {benefit.title}
                </h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  {benefit.description}
                </p>
              </div>

              {/* Accent line */}
              <div className="absolute bottom-0 left-6 right-6 h-[2px] bg-gradient-to-r from-neon-lime/0 via-neon-lime/50 to-neon-lime/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default BenefitsSection;
