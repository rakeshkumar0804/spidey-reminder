import React from 'react';
import { Download, PlusCircle, Bell } from 'lucide-react';

export const HowItWorks: React.FC = () => {
  const steps = [
    {
      number: "01",
      icon: <Download className="w-6 h-6 text-red-500" />,
      title: "Download & Run",
      description: "Download the standalone SpideyReminder.exe file. Run it directly without installer wizards or administrator permissions.",
    },
    {
      number: "02",
      icon: <PlusCircle className="w-6 h-6 text-blue-500" />,
      title: "Create Your Reminders",
      description: "Set your own custom one-time tasks or repeating intervals. Choose optional templates like Eye Break or Hydration if desired.",
    },
    {
      number: "03",
      icon: <Bell className="w-6 h-6 text-amber-500" />,
      title: "Get Reminded Smoothly",
      description: "When a reminder is due, Spider-Man descends from the top edge of your monitor to display your message without stealing focus.",
    },
  ];

  return (
    <section id="how-it-works" className="py-20 md:py-28 bg-stone-100/60 border-y border-stone-200/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl sm:text-5xl font-black text-slate-900 tracking-tight mb-4">
            How it works in 3 simple steps.
          </h2>
          <p className="text-slate-600 text-lg">
            No complicated setup. Download, configure your reminders, and let Spider-Man take care of the rest.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          {steps.map((step, idx) => (
            <div
              key={idx}
              className="relative p-8 rounded-2xl bg-white border border-stone-200 shadow-sm flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-6">
                  <div className="w-12 h-12 rounded-xl bg-stone-100 flex items-center justify-center">
                    {step.icon}
                  </div>
                  <span className="text-3xl font-black text-stone-300 font-mono">
                    {step.number}
                  </span>
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-3">
                  {step.title}
                </h3>
                <p className="text-slate-600 text-sm leading-relaxed">
                  {step.description}
                </p>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
};
