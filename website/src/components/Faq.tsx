import React, { useState } from 'react';
import { ChevronDown, HelpCircle } from 'lucide-react';

export const Faq: React.FC = () => {
  const faqs = [
    {
      q: "What operating systems are supported?",
      a: "Spidey Reminder is designed specifically for Windows 10 and Windows 11 (64-bit). It uses native Windows DWM layered window features for translucent background rendering and focus protection.",
    },
    {
      q: "Do I need Python installed to run Spidey Reminder?",
      a: "No! The standalone executable download (SpideyReminder.exe) contains all runtime dependencies bundled together. You can download and double-click to run it instantly.",
    },
    {
      q: "Where are my settings and custom reminders stored?",
      a: "All your data is stored locally in your Windows AppData folder under %APPDATA%\\SpiderBreakCompanion\\settings.json. Your data is 100% private and never leaves your computer.",
    },
    {
      q: "How do I pause reminders or access settings?",
      a: "Spidey Reminder runs quietly in your Windows system notification tray (near the clock). Right-click the red spider icon in your system tray to open the Reminder Manager, pause/resume reminders, test animations, or quit.",
    },
    {
      q: "Does the overlay interrupt my typing or coding?",
      a: "No. The overlay uses native Windows WS_EX_NOACTIVATE window flags. When Spider-Man descends or cards appear, your keyboard focus remains 100% in your active editor, IDE, or browser.",
    },
    {
      q: "How does snoozing work?",
      a: "Clicking 'Snooze 5m' reschedules that specific reminder by 5 minutes cleanly in-place without creating duplicate occurrences or corrupting your recurring schedule.",
    },
  ];

  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section id="faq" className="py-20 md:py-28 bg-[#FAF9F5]">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-stone-200 text-slate-700 text-xs font-semibold uppercase tracking-wider mb-4">
            <HelpCircle className="w-3.5 h-3.5 text-red-500" />
            <span>Frequently Asked Questions</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-black text-slate-900 tracking-tight">
            Got questions? We've got answers.
          </h2>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, idx) => {
            const isOpen = openIndex === idx;
            return (
              <div
                key={idx}
                className="rounded-2xl bg-white border border-stone-200 overflow-hidden shadow-sm transition-all"
              >
                <button
                  onClick={() => setOpenIndex(isOpen ? null : idx)}
                  className="w-full p-6 text-left flex items-center justify-between gap-4 font-bold text-lg text-slate-900 hover:text-red-600 transition-colors"
                >
                  <span>{faq.q}</span>
                  <ChevronDown
                    className={`w-5 h-5 text-slate-400 transition-transform duration-200 shrink-0 ${
                      isOpen ? 'transform rotate-180 text-red-500' : ''
                    }`}
                  />
                </button>
                {isOpen && (
                  <div className="px-6 pb-6 text-slate-600 text-sm leading-relaxed border-t border-stone-100 pt-4">
                    {faq.a}
                  </div>
                )}
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
};
