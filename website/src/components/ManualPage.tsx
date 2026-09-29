import React from 'react';
import { Monitor, ArrowLeft, Github, CheckCircle2, ShieldCheck, HelpCircle, AlertCircle } from 'lucide-react';
import { APP_CONFIG } from '../config';

interface ManualPageProps {
  navigate: (path: string) => void;
}

export const ManualPage: React.FC<ManualPageProps> = ({ navigate }) => {
  return (
    <div className="bg-[#FAF8F5] min-h-screen pt-6 pb-20">
      <div className="max-w-3xl mx-auto px-4 sm:px-6">
        
        {/* Navigation Breadcrumb */}
        <div className="mb-8 flex items-center justify-between">
          <a
            href="/"
            onClick={(e) => {
              e.preventDefault();
              navigate('/');
            }}
            className="inline-flex items-center gap-2 text-sm font-semibold text-stone-600 hover:text-stone-900 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Home</span>
          </a>

          <a
            href={APP_CONFIG.githubUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-stone-500 hover:text-stone-900 transition-colors"
          >
            <Github className="w-4 h-4" />
            <span>GitHub Feedback</span>
          </a>
        </div>

        {/* Page Title Header */}
        <div className="border-b border-stone-200 pb-6 mb-10">
          <h1 className="text-3xl sm:text-4xl font-black text-stone-900 tracking-tight leading-tight mb-3">
            Spidey Reminder Manual & FAQs
          </h1>
          <p className="text-base text-stone-600 font-medium">
            User documentation and frequently asked questions for the Windows desktop companion ({APP_CONFIG.currentVersion}).
          </p>
        </div>

        {/* Article Body Content */}
        <div className="space-y-12 text-stone-800 text-sm sm:text-base leading-relaxed">
          
          {/* Section 1: Quick Start */}
          <section className="space-y-4">
            <h2 className="text-xl sm:text-2xl font-bold text-stone-900 tracking-tight flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-red-500 shrink-0" />
              <span>1. Quick Start & Installation</span>
            </h2>
            <p className="text-stone-700">
              Spidey Reminder is distributed as a portable standalone Windows executable (<code className="bg-stone-200/60 px-1.5 py-0.5 rounded text-xs font-mono text-stone-900">SpideyReminder.exe</code>). No installer, admin elevation, or Python setup is required.
            </p>
            <ol className="list-decimal pl-5 space-y-2 text-stone-700">
              <li>
                Download <a href={APP_CONFIG.downloadUrl} className="text-red-600 font-semibold underline hover:text-red-700">SpideyReminder.exe</a> from GitHub Releases.
              </li>
              <li>Double-click the executable file to launch.</li>
              <li>A spider icon will appear in your Windows System Tray (near the clock).</li>
              <li>On first launch, the <b>Reminder Manager</b> window will automatically open.</li>
            </ol>
          </section>

          {/* Section 2: System Tray & Controls */}
          <section className="space-y-4">
            <h2 className="text-xl sm:text-2xl font-bold text-stone-900 tracking-tight flex items-center gap-2">
              <Monitor className="w-5 h-5 text-red-500 shrink-0" />
              <span>2. System Tray & Menu Options</span>
            </h2>
            <p className="text-stone-700">
              Spidey Reminder runs quietly in the background. Right-click the spider tray icon near your Windows clock to access controls:
            </p>
            <ul className="list-disc pl-5 space-y-2 text-stone-700">
              <li><b>⚙ Reminder Manager...</b>: Open the manager window to add, edit, toggle, or remove reminders.</li>
              <li><b>🕷 Test Animation</b>: Immediately play the Spider-Man entrance sequence with a sample reminder.</li>
              <li><b>⏸ Pause Reminders / ▶ Resume Reminders</b>: Temporarily halt all scheduled notifications.</li>
              <li><b>❌ Quit</b>: Cleanly exit Spidey Reminder.</li>
            </ul>
          </section>

          {/* Section 3: Managing Reminders */}
          <section className="space-y-4">
            <h2 className="text-xl sm:text-2xl font-bold text-stone-900 tracking-tight">
              3. Creating & Managing Reminders
            </h2>
            <p className="text-stone-700">
              Fresh installations start with <b>zero active reminders</b> for a clean slate. You choose exactly what tasks and schedules to create:
            </p>
            <ul className="list-disc pl-5 space-y-2 text-stone-700">
              <li><b>One-Time Reminders</b>: Set a reminder for a specific date and time (e.g. <i>"Call doctor at 3:00 PM"</i>).</li>
              <li><b>Recurring Reminders</b>: Repeat tasks every chosen number of minutes or hours (e.g. <i>"Drink water every 60 minutes"</i>).</li>
              <li><b>Built-in Templates</b>: Choose an option from the Optional Template dropdown, then click Save Reminder to pre-fill recommended messages.</li>
            </ul>
          </section>

          {/* Section 4: Card Controls & Dismissal */}
          <section className="space-y-4">
            <h2 className="text-xl sm:text-2xl font-bold text-stone-900 tracking-tight">
              4. Reminder Overlay Controls & Dismissal
            </h2>
            <p className="text-stone-700">
              When a reminder is due, Spider-Man cleanly descends from the top edge of your monitor and hangs upside down with a message card:
            </p>
            <ul className="list-disc pl-5 space-y-2 text-stone-700">
              <li><b>Done Button</b>: Immediately completes the current break and ascends Spider-Man back off-screen.</li>
              <li><b>Snooze 5m Button</b>: Postpones the reminder for 5 minutes without disrupting future recurring schedules.</li>
              <li><b>20-Second Auto-Dismissal</b>: Every reminder includes a 20-second countdown. If unattended, it automatically closes cleanly.</li>
            </ul>
          </section>

          {/* Section 5: Preferences */}
          <section className="space-y-4">
            <h2 className="text-xl sm:text-2xl font-bold text-stone-900 tracking-tight">
              5. Preferences & Startup Options
            </h2>
            <p className="text-stone-700">
              Inside the Reminder Manager dialog, you can configure app options:
            </p>
            <ul className="list-disc pl-5 space-y-2 text-stone-700">
              <li><b>Start with Windows</b>: Automatically launch Spidey Reminder when your computer boots up.</li>
              <li><b>Reduced Motion</b>: Instantly show the full card without entrance animation for users who prefer reduced motion.</li>
            </ul>
          </section>

          {/* Section 6: Frequently Asked Questions */}
          <section className="space-y-6 pt-4 border-t border-stone-200">
            <h2 className="text-xl sm:text-2xl font-bold text-stone-900 tracking-tight flex items-center gap-2">
              <HelpCircle className="w-5 h-5 text-red-500 shrink-0" />
              <span>Frequently Asked Questions</span>
            </h2>

            <div className="space-y-4 text-stone-700">
              <div>
                <h3 className="font-bold text-stone-900">Which operating systems are supported?</h3>
                <p>Spidey Reminder is built for <b>Windows 10</b> and <b>Windows 11</b> (64-bit).</p>
              </div>

              <div>
                <h3 className="font-bold text-stone-900">Do I need Python installed to run the app?</h3>
                <p>No. The standalone <code className="bg-stone-200/60 px-1 py-0.5 rounded text-xs font-mono">SpideyReminder.exe</code> includes all runtime requirements bundled inside a single portable binary.</p>
              </div>

              <div>
                <h3 className="font-bold text-stone-900">Where are my settings and reminders saved?</h3>
                <p>All settings and custom reminders are stored locally and offline in <code className="bg-stone-200/60 px-1 py-0.5 rounded text-xs font-mono">%APPDATA%\SpiderBreakCompanion\settings.json</code>. No data is ever uploaded to external servers.</p>
              </div>

              <div>
                <h3 className="font-bold text-stone-900">Will reminders steal keyboard focus while I am typing or gaming?</h3>
                <p>No. The overlay uses native Win32 <code className="bg-stone-200/60 px-1 py-0.5 rounded text-xs font-mono">WS_EX_NOACTIVATE</code> window styling, guaranteeing that your keyboard focus, active coding window, or game remain uninterrupted.</p>
              </div>
            </div>
          </section>

          {/* Section 7: Known Display Note */}
          <section className="p-4 rounded-2xl bg-amber-50/80 border border-amber-200 text-amber-900 space-y-2 text-xs sm:text-sm">
            <div className="flex items-center gap-2 font-bold text-amber-950">
              <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
              <span>Desktop Display Behavior Note</span>
            </div>
            <p>
              Reminder text may appear all at once instead of word by word on some Windows setups. This is a known visual issue in v1.1.0.
            </p>
          </section>

          {/* Bottom Callouts */}
          <div className="pt-6 border-t border-stone-200 flex flex-col sm:flex-row items-center justify-between gap-4">
            <a
              href="/"
              onClick={(e) => {
                e.preventDefault();
                navigate('/');
              }}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-stone-900 text-white font-bold text-sm rounded-xl hover:bg-stone-800 transition-colors"
            >
              <span>Return to Homepage</span>
            </a>

            <div className="flex items-center gap-2 text-xs text-stone-500">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>100% Offline & Private Windows Desktop App</span>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};
