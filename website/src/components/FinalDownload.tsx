import React from 'react';
import { Monitor } from 'lucide-react';
import { APP_CONFIG } from '../config';

export const FinalDownload: React.FC = () => {
  return (
    <section className="py-16 sm:py-20 bg-[#FAF8F5] border-t border-stone-200/60">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 text-center">
        
        {/* Heading */}
        <h2 className="text-3xl sm:text-4xl font-extrabold text-stone-900 tracking-tight mb-3">
          Your next reminder comes with a superhero.
        </h2>

        {/* Supporting Line */}
        <p className="text-stone-600 text-sm sm:text-base font-medium mb-8 max-w-xl mx-auto">
          Your tasks, your schedule. Start with your first custom reminder.
        </p>

        {/* Download Button */}
        <div className="flex flex-col items-center gap-3">
          <a
            href={APP_CONFIG.downloadUrl}
            className="inline-flex items-center gap-2.5 px-8 py-4 bg-[#18181B] text-white rounded-2xl font-bold text-sm sm:text-base hover:bg-stone-800 shadow-xl shadow-stone-900/10 active:scale-98 transition-all"
          >
            <Monitor className="w-5 h-5 text-red-400" />
            <span>Download for Windows</span>
          </a>

          {/* Metadata String */}
          <p className="text-xs text-stone-500 font-medium tracking-wide">
            Free · Windows 10/11 · {APP_CONFIG.currentVersion}
          </p>
        </div>

      </div>
    </section>
  );
};
