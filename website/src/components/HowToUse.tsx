import React from 'react';

interface HowToUseProps {
  navigate: (path: string) => void;
}

export const HowToUse: React.FC<HowToUseProps> = ({ navigate }) => {
  const steps = [
    {
      number: '1',
      bgClass: 'bg-[#18181B]',
      title: 'Download & Run',
      description: 'Download the Windows app and open SpideyReminder.exe. No Python installation needed.',
    },
    {
      number: '2',
      bgClass: 'bg-[#18181B]',
      title: 'Create Your Reminder',
      description: 'Open Reminder Manager from the system tray. Add your message and choose a one-time or repeating schedule.',
    },
    {
      number: '3',
      bgClass: 'bg-red-600',
      title: 'Let Spidey Remind You',
      description: 'Spider-Man drops in when your reminder is due. Choose Done, snooze for 5 minutes, or let it close automatically after 20 seconds.',
    },
  ];

  return (
    <section className="py-16 sm:py-20 bg-[#FAF8F5]">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Heading */}
        <h2 className="text-3xl sm:text-4xl font-extrabold text-stone-900 tracking-tight text-center mb-12 sm:mb-16">
          How to use it
        </h2>

        {/* 3 Step Columns */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 sm:gap-10">
          {steps.map((step) => (
            <div key={step.number} className="flex flex-col items-start text-left">
              {/* Numbered Rounded Square */}
              <div
                className={`w-12 h-12 rounded-2xl ${step.bgClass} text-white flex items-center justify-center font-black text-xl shadow-md mb-4`}
              >
                {step.number}
              </div>

              {/* Step Title & Description */}
              <h3 className="text-lg font-bold text-stone-900 mb-2 tracking-tight">
                {step.title}
              </h3>
              <p className="text-stone-600 text-sm leading-relaxed">
                {step.description}
              </p>
            </div>
          ))}
        </div>

        {/* Manual Page Link */}
        <div className="mt-12 sm:mt-16 text-center">
          <button
            onClick={() => navigate('/manual')}
            className="inline-flex items-center gap-1.5 text-stone-700 hover:text-stone-950 font-semibold text-sm underline underline-offset-4 decoration-stone-400 hover:decoration-stone-900 transition-colors"
          >
            Read the Manual & FAQs &rarr;
          </button>
        </div>

      </div>
    </section>
  );
};
