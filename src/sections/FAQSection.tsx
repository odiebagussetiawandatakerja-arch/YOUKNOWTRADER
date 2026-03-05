import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';

gsap.registerPlugin(ScrollTrigger);

const faqs = [
  {
    question: 'How does copy trading work?',
    answer:
      'When you connect your exchange account to my copy-trading system, every trade I make is automatically mirrored in your account proportionally to your balance. You dont need to monitor charts or execute trades manually.',
  },
  {
    question: 'What is the minimum amount to start?',
    answer:
      'The recommended minimum is $500 to ensure proper position sizing and risk management. However, you can start with as little as $100 on most supported exchanges.',
  },
  {
    question: 'Can I stop copying anytime?',
    answer:
      'Absolutely. You have full control over your account. You can pause, resume, or completely stop copying at any time with no penalties or fees.',
  },
  {
    question: 'What are the risks involved?',
    answer:
      'Trading involves significant risk. While I maintain an 83% win rate, losses do occur. My max drawdown is capped at -11%, but past performance doesnt guarantee future results. Never invest more than you can afford to lose.',
  },
  {
    question: 'How is the 10% performance fee calculated?',
    answer:
      'The 10% fee is only charged on profitable months. If your account grows by $1000 in a month, the fee would be $100. There are no fees during losing months or break-even periods.',
  },
  {
    question: 'Which exchanges are supported?',
    answer:
      'Currently supported exchanges include Binance, Bybit, and BingX. Availability may vary depending on your region due to regulatory requirements.',
  },
];

const FAQSection = () => {
  const sectionRef = useRef<HTMLDivElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const accordionRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    const header = headerRef.current;
    const accordion = accordionRef.current;

    if (!section || !header || !accordion) return;

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

      // Accordion animation
      gsap.fromTo(
        accordion,
        { opacity: 0, y: 40 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: accordion,
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
      id="faq"
      className="relative w-full py-20 lg:py-32 bg-navy"
    >
      <div className="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div className="max-w-3xl mx-auto">
          {/* Header */}
          <div ref={headerRef} className="text-center mb-12">
            <h2 className="font-display text-3xl lg:text-4xl xl:text-5xl font-bold text-foreground mb-4">
              Frequently Asked{' '}
              <span className="text-gradient">Questions</span>
            </h2>
          </div>

          {/* Accordion */}
          <div ref={accordionRef}>
            <Accordion type="single" collapsible className="space-y-4">
              {faqs.map((faq, index) => (
                <AccordionItem
                  key={index}
                  value={`item-${index}`}
                  className="border border-white/[0.06] rounded-xl px-6 bg-navy-light/50 data-[state=open]:border-neon-lime/30 transition-colors"
                >
                  <AccordionTrigger className="text-left text-foreground hover:text-neon-lime py-5 text-sm lg:text-base">
                    {faq.question}
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground text-sm pb-5">
                    {faq.answer}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FAQSection;
