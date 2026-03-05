import { useEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Navigation from '@/components/Navigation';
import HeroSection from '@/sections/HeroSection';
import WhatIDoSection from '@/sections/WhatIDoSection';
import PerformanceSection from '@/sections/PerformanceSection';
import BenefitsSection from '@/sections/BenefitsSection';
import StrategySection from '@/sections/StrategySection';
import CommunitySection from '@/sections/CommunitySection';
import RiskSection from '@/sections/RiskSection';
import PricingSection from '@/sections/PricingSection';
import FAQSection from '@/sections/FAQSection';
import FinalCTASection from '@/sections/FinalCTASection';

gsap.registerPlugin(ScrollTrigger);

function App() {
  useEffect(() => {
    // Wait for all ScrollTriggers to be created
    const timeout = setTimeout(() => {
      const pinned = ScrollTrigger.getAll()
        .filter((st) => st.vars.pin)
        .sort((a, b) => a.start - b.start);

      const maxScroll = ScrollTrigger.maxScroll(window);

      if (!maxScroll || pinned.length === 0) return;

      // Build ranges and snap targets from pinned sections
      const pinnedRanges = pinned.map((st) => ({
        start: st.start / maxScroll,
        end: (st.end ?? st.start) / maxScroll,
        center:
          (st.start + ((st.end ?? st.start) - st.start) * 0.5) / maxScroll,
      }));

      // Global snap configuration
      ScrollTrigger.create({
        snap: {
          snapTo: (value: number) => {
            // Check if within any pinned range (with buffer)
            const inPinned = pinnedRanges.some(
              (r) => value >= r.start - 0.02 && value <= r.end + 0.02
            );

            if (!inPinned) return value; // Flowing section: free scroll

            // Find nearest pinned center
            const target = pinnedRanges.reduce(
              (closest, r) =>
                Math.abs(r.center - value) < Math.abs(closest - value)
                  ? r.center
                  : closest,
              pinnedRanges[0]?.center ?? 0
            );

            return target;
          },
          duration: { min: 0.15, max: 0.35 },
          delay: 0,
          ease: 'power2.out',
        },
      });
    }, 100);

    return () => {
      clearTimeout(timeout);
      ScrollTrigger.getAll().forEach((st) => st.kill());
    };
  }, []);

  return (
    <div className="relative bg-navy min-h-screen">
      <Navigation />

      <main className="relative">
        {/* Section 1: Hero - pin: true, z-10 */}
        <div className="relative z-10">
          <HeroSection />
        </div>

        {/* Section 2: What I Do - pin: false */}
        <WhatIDoSection />

        {/* Section 3: Performance - pin: true, z-20 */}
        <div className="relative z-20">
          <PerformanceSection />
        </div>

        {/* Section 4: Benefits - pin: false */}
        <BenefitsSection />

        {/* Section 5: Strategy - pin: true, z-30 */}
        <div className="relative z-30">
          <StrategySection />
        </div>

        {/* Section 6: Community - pin: false */}
        <CommunitySection />

        {/* Section 7: Risk - pin: true, z-40 */}
        <div className="relative z-40">
          <RiskSection />
        </div>

        {/* Section 8: Pricing - pin: false */}
        <PricingSection />

        {/* Section 9: FAQ - pin: false */}
        <FAQSection />

        {/* Section 10: Final CTA - pin: false */}
        <FinalCTASection />
      </main>
    </div>
  );
}

export default App;
