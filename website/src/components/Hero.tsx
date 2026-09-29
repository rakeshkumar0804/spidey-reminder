import React from 'react';
import { Download, Play, ShieldCheck, Sparkles, Monitor } from 'lucide-react';
import { APP_CONFIG } from '../config';

export const Hero: React.FC = () => {
  return (
    <section className="relative pt-12 pb-20 md:pt-20 md:pb-28 overflow-hidden">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
        
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-stone-200/70 text-slate-800 text-xs font-semibold uppercase tracking-wider mb-8 border border-stone-300/50 shadow-sm">
          <Monitor className="w-3.5 h-3.5 text-red-500" />
          <span>Windows Desktop Companion</span>
        </div>

        {/* Main Headline */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-black text-slate-900 tracking-tight leading-[1.1] mb-6">
          Your custom Windows <br className="hidden sm:inline" />
          <span className="text-red-500 underline decoration-red-400/40 decoration-wavy decoration-2">desktop reminder</span> app.
        </h1>

        {/* Subtitle */}
        <p className="max-w-2xl mx-auto text-lg sm:text-xl text-slate-600 leading-relaxed mb-8 font-normal">
          Create your own custom tasks, eye breaks, or hydration schedules. A friendly animated Spider-Man cleanly descends from the top edge of your screen when it’s time.
        </p>



        {/* Primary CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
          <a
            href={APP_CONFIG.downloadUrl}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-3 px-8 py-4 bg-slate-900 text-white rounded-2xl font-bold text-base hover:bg-slate-800 shadow-xl shadow-slate-900/10 hover:shadow-slate-900/20 active:scale-98 transition-all"
          >
            <Download className="w-5 h-5 text-red-400" />
            <span>Download for Windows</span>
            <span className="text-xs font-normal text-stone-400 bg-slate-800 px-2 py-0.5 rounded-md">
              {APP_CONFIG.currentVersion}
            </span>
          </a>

          <a
            href="#demo"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-4 bg-white text-slate-800 rounded-2xl font-semibold text-base border border-stone-300 hover:bg-stone-100 shadow-sm active:scale-98 transition-all"
          >
            <Play className="w-4 h-4 text-red-500 fill-red-500" />
            <span>Interactive Demo</span>
          </a>
        </div>

        {/* Portable EXE Badge & Info */}
        <div className="flex flex-wrap items-center justify-center gap-6 text-xs text-slate-500 font-medium">
          <div className="flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Portable Standalone Executable (.exe)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-amber-500" />
            <span>100% Offline & Private (Local AppData)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Monitor className="w-4 h-4 text-blue-500" />
            <span>Windows 10 & 11 Compatible</span>
          </div>
        </div>

      </div>
    </section>
  );
};
