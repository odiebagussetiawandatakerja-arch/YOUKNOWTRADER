import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Button } from '@/components/ui/button';
import { Mail, Send } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

const socialLinks = [
  { icon: Send, label: 'Telegram Community', href: 'https://t.me/YouKnowTraderCommunity' },
  { icon: Send, label: 'Telegram Official', href: 'https://t.me/YouKnowTraderOfficial' },
];

const FinalCTASection = () => {
  const sectionRef = useRef<HTMLDivElement>(null);
  const bgRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const contactRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    const bg = bgRef.current;
    const content = contentRef.current;
    const contact = contactRef.current;

    if (!section || !bg || !content || !contact) return;

    const ctx = gsap.context(() => {
      // Content animation
      gsap.fromTo(
        content.querySelector('h2'),
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: content,
            start: 'top 80%',
            end: 'top 55%',
            scrub: 0.5,
          },
        }
      );

      gsap.fromTo(
        content.querySelector('p'),
        { opacity: 0, y: 20 },
        {
          opacity: 1,
          y: 0,
          duration: 0.7,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: content,
            start: 'top 78%',
            end: 'top 53%',
            scrub: 0.5,
          },
        }
      );

      // Buttons animation
      const buttons = content.querySelectorAll('button');
      gsap.fromTo(
        buttons,
        { opacity: 0, scale: 0.97 },
        {
          opacity: 1,
          scale: 1,
          duration: 0.6,
          stagger: 0.1,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: content,
            start: 'top 75%',
            end: 'top 50%',
            scrub: 0.5,
          },
        }
      );

      // Contact animation
      gsap.fromTo(
        contact,
        { opacity: 0, y: 16 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: contact,
            start: 'top 90%',
            end: 'top 70%',
            scrub: 0.5,
          },
        }
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
      className="relative w-full min-h-screen overflow-hidden"
    >
      {/* Background Image */}
      <div
        ref={bgRef}
        className="absolute inset-0 w-full h-full"
        style={{
          backgroundImage: 'url(/images/final_cta_portrait.jpg)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        {/* Gradient Overlay */}
        <div
          className="absolute inset-0"
          style={{
            background:
              'linear-gradient(90deg, rgba(7,10,18,0.85) 0%, rgba(7,10,18,0.40) 100%)',
          }}
        />
      </div>

      {/* Grain Overlay */}
      <div className="absolute inset-0 grain-overlay pointer-events-none" />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-start justify-center min-h-screen px-4 sm:px-6 lg:px-8 xl:px-12 py-20">
        <div className="w-full max-w-2xl">
          <div ref={contentRef}>
            {/* Headline */}
            <h2 className="font-display text-3xl sm:text-4xl lg:text-5xl xl:text-6xl font-bold text-foreground leading-tight mb-6">
              Ready to trade{' '}
              <span className="text-gradient">with me?</span>
            </h2>

            {/* Body */}
            <p className="text-muted-foreground text-base lg:text-lg mb-10 max-w-lg">
              Connect your account. Set your limit. Let the system work.
            </p>

            {/* CTAs */}
            <div className="flex flex-col sm:flex-row gap-4 mb-16">
              <Button
                onClick={scrollToPricing}
                size="lg"
                className="bg-neon-lime text-navy hover:bg-neon-lime/90 transition-all duration-300 font-semibold px-8"
              >
                Start Copying
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="border-white/20 text-foreground hover:bg-white/5 transition-all duration-300"
              >
                Ask a Question
              </Button>
            </div>
          </div>

          {/* Contact */}
          <div ref={contactRef} className="space-y-6">
            {/* Email */}
            <a
              href="mailto:odietraderfx.crypto@gmail.com"
              className="flex items-center gap-3 text-muted-foreground hover:text-neon-lime transition-colors group"
            >
              <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center group-hover:bg-neon-lime/10 transition-colors">
                <Mail className="w-5 h-5" />
              </div>
              <span className="text-sm">odietraderfx.crypto@gmail.com</span>
            </a>

            {/* Socials */}
            <div className="flex items-center gap-4">
              {socialLinks.map((social, index) => (
                <a
                  key={index}
                  href={social.href}
                  aria-label={social.label}
                  className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center text-muted-foreground hover:text-neon-lime hover:bg-neon-lime/10 transition-all"
                >
                  <social.icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="absolute bottom-0 left-0 right-0 py-6 px-4 sm:px-6 lg:px-8 xl:px-12 border-t border-white/5">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-muted-foreground">
            © 2024 YouKnowTrader. All rights reserved.
          </p>
          <p className="text-xs text-muted-foreground">
            Trading involves risk. Past performance is not indicative of future
            results.
          </p>
        </div>
      </div>
    </section>
  );
};

export default FinalCTASection;
