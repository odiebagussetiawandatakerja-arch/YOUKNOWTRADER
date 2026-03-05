import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { MessageSquare, BarChart3, Layers } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const proofCards = [
  {
    icon: MessageSquare,
    title: 'Discord Community',
    description: 'Daily bias + Q&A. No spam, no paid shills.',
  },
  {
    icon: BarChart3,
    title: 'Trade Recaps',
    description: "Weekly breakdowns of what worked—and what didn't.",
  },
  {
    icon: Layers,
    title: 'On-Chain + Technical',
    description: 'I combine orderflow with price action.',
  },
];

const CommunitySection = () => {
  const sectionRef = useRef<HTMLDivElement>(null);
  const quoteRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    const quote = quoteRef.current;
    const cards = cardsRef.current;

    if (!section || !quote || !cards) return;

    const ctx = gsap.context(() => {
      // Quote animation
      gsap.fromTo(
        quote,
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: quote,
            start: 'top 80%',
            end: 'top 55%',
            scrub: 0.5,
          },
        }
      );

      // Cards animation
      const cardElements = cards.querySelectorAll('.proof-card');
      gsap.fromTo(
        cardElements,
        { opacity: 0, x: '6vw', rotateZ: 2 },
        {
          opacity: 1,
          x: 0,
          rotateZ: 0,
          duration: 0.8,
          stagger: 0.12,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: cards,
            start: 'top 75%',
            end: 'top 50%',
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
      style={{
        background:
          'radial-gradient(ellipse at top center, rgba(11,15,28,0.6) 0%, transparent 50%), #070A12',
      }}
    >
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col lg:flex-row gap-12 lg:gap-16 items-start">
            {/* Quote Block */}
            <div ref={quoteRef} className="w-full lg:w-1/2">
              <div className="relative">
                {/* Quote marks */}
                <div className="absolute -top-4 -left-2 text-6xl text-neon-lime/20 font-serif">
                  "
                </div>

                <blockquote className="relative text-2xl lg:text-3xl xl:text-4xl font-display text-foreground leading-snug mb-6 pl-6">
                  I joined to copy. I stayed because the process actually makes
                  sense.
                </blockquote>

                <cite className="pl-6 text-sm text-muted-foreground not-italic">
                  — Member since 2022
                </cite>
              </div>
            </div>

            {/* Proof Cards */}
            <div
              ref={cardsRef}
              className="w-full lg:w-1/2 space-y-4"
            >
              {proofCards.map((card, index) => (
                <div
                  key={index}
                  className="proof-card group flex items-start gap-4 p-5 rounded-xl bg-navy-light border border-white/[0.06] hover:border-neon-lime/30 transition-all duration-300"
                >
                  {/* Icon */}
                  <div className="w-10 h-10 rounded-lg bg-neon-lime/10 flex items-center justify-center shrink-0 group-hover:bg-neon-lime/20 transition-colors">
                    <card.icon className="w-5 h-5 text-neon-lime" />
                  </div>

                  {/* Content */}
                  <div>
                    <h4 className="font-display text-base font-semibold text-foreground mb-1">
                      {card.title}
                    </h4>
                    <p className="text-sm text-muted-foreground">
                      {card.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CommunitySection;
