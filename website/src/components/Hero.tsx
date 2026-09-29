import React from 'react';
import { Monitor } from 'lucide-react';
import { APP_CONFIG } from '../config';
import { HeroDemoComposition } from './HeroDemoComposition';
import { HowToUse } from './HowToUse';
import { FinalDownload } from './FinalDownload';

interface HeroProps {
  navigate: (path: string) => void;
}

export const Hero: React.FC<HeroProps> = ({ navigate }) => {
  return (
    <div>
      {/* Hero Header & Demo Panel Section */}
      <section className="relative pt-10 pb-4 bg-[#FAF8F5] overflow-visible">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          
          {/* Headline matching Reference Target */}
          <h1 className="text-5xl sm:text-7xl lg:text-8xl font-black text-stone-900 tracking-tight leading-[0.98] mb-6 max-w-4xl mx-auto">
            Satisfying <br />
            <span className="relative inline-block px-3 sm:px-4 py-0.5 mx-1 text-stone-900">
              <span className="absolute inset-0 bg-[#F472B6] -rotate-1 rounded-sm -z-10 shadow-sm" />
              reminders
            </span> <br />
            with every drop
          </h1>

          {/* Download Row */}
          <div className="flex flex-wrap items-center justify-center gap-3 sm:gap-4 mb-8">
            <a
              href={APP_CONFIG.downloadUrl}
              className="inline-flex items-center gap-2.5 px-7 py-3.5 bg-[#18181B] text-white rounded-2xl font-bold text-sm sm:text-base hover:bg-stone-800 shadow-xl shadow-stone-900/10 active:scale-98 transition-all"
            >
              <Monitor className="w-5 h-5 text-red-400" />
              <span>Download for Windows</span>
            </a>

            <div className="inline-flex items-center gap-2 px-3 py-2 bg-stone-900/10 rounded-2xl text-xs sm:text-sm font-medium">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-[#18181B] text-white rounded-xl font-semibold text-xs">
                <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block" />
                100% Free
              </span>
              <span className="px-2.5 py-1 bg-[#1E293B] text-blue-300 rounded-xl font-mono text-xs font-bold">
                {APP_CONFIG.currentVersion}
              </span>
              <span className="text-stone-500 font-bold uppercase tracking-wider text-[11px] px-1">
                BUILT FOR Windows 10/11
              </span>
            </div>
          </div>

        </div>

        {/* Dark Burgundy Demo Panel & Spider-Man Overlap */}
        <HeroDemoComposition />
      </section>

      {/* How to use it Section */}
      <HowToUse navigate={navigate} />

      {/* Final Download Section */}
      <FinalDownload />
    </div>
  );
};
