import React from 'react';
import { Calendar, Eye, Shield, Bell, Moon, SlidersHorizontal } from 'lucide-react';

export const Features: React.FC = () => {
  const featuresList = [
    {
      icon: <Calendar className="w-6 h-6 text-red-500" />,
      title: "Custom Schedules & Tasks",
      description: "Create one-time reminders for specific dates and times, or set repeating reminders for any number of minutes or hours.",
    },
    {
      icon: <SlidersHorizontal className="w-6 h-6 text-blue-500" />,
      title: "Optional Break Templates",
      description: "Quickly select Eye Break or Hydration templates, customize title and timing, and enable them with an explicit save.",
    },
    {
      icon: <Eye className="w-6 h-6 text-amber-500" />,
      title: "Word-by-Word Readable Text",
      description: "Reminders reveal sentence text word-by-word at a steady, readable pace so you can scan tasks without distraction.",
    },
    {
      icon: <Shield className="w-6 h-6 text-emerald-500" />,
      title: "Non-Activating Focus Protection",
      description: "Uses native Windows WS_EX_NOACTIVATE styling so overlays never steal keyboard focus while you are coding or typing.",
    },
    {
      icon: <Bell className="w-6 h-6 text-purple-500" />,
      title: "System Tray Controls & Snooze",
      description: "Pause all reminders, test animations, or snooze active reminders by 5 minutes cleanly from your Windows notification tray.",
    },
    {
      icon: <Moon className="w-6 h-6 text-stone-600" />,
      title: "100% Offline & Private",
      description: "Your reminders are stored locally on your computer.",
    },
  ];

  return (
    <section id="features" className="py-20 md:py-28 bg-[#FAF9F5]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Heading */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl sm:text-5xl font-black text-slate-900 tracking-tight mb-4">
            Designed for productivity and focus.
          </h2>
          <p className="text-slate-600 text-lg">
            Everything you need in a Windows break companion without bloated installers, background telemetry, or intrusive focus stealing.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuresList.map((feature, idx) => (
            <div
              key={idx}
              className="p-8 rounded-2xl bg-white border border-stone-200/80 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between"
            >
              <div>
                <div className="w-12 h-12 rounded-xl bg-stone-100 flex items-center justify-center mb-6">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-slate-600 text-sm leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
};
