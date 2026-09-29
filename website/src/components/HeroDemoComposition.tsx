import React, { useState, useEffect } from 'react';
import { Play, Clock, CheckCircle2, RotateCcw } from 'lucide-react';

export const HeroDemoComposition: React.FC = () => {
  const [customMessage, setCustomMessage] = useState('Time to drink water! 💧');
  const [scheduleType, setScheduleType] = useState<'once' | 'repeat'>('once');
  const [scheduleTime, setScheduleTime] = useState('08:00');
  const [ampm, setAmpm] = useState<'AM' | 'PM'>('AM');
  const [repeatInterval, setRepeatInterval] = useState('20');

  const [animState, setAnimState] = useState<'idle' | 'shooting_web' | 'descending' | 'settling' | 'card_open' | 'active' | 'exiting'>('active');
  const [spideyY, setSpideyY] = useState(-10); // px relative to panel top
  const [cardOpacity, setCardOpacity] = useState(1);
  const [countdown, setCountdown] = useState(20);

  const startDemo = () => {
    setAnimState('shooting_web');
    setSpideyY(-220);
    setCardOpacity(0);
    setCountdown(20);
  };

  const dismissDemo = () => {
    setAnimState('exiting');
  };

  // State machine animation loop
  useEffect(() => {
    if (animState === 'shooting_web') {
      const duration = 400;
      const start = Date.now();
      const interval = setInterval(() => {
        const p = Math.min(1, (Date.now() - start) / duration);
        if (p >= 1) {
          clearInterval(interval);
          setTimeout(() => setAnimState('descending'), 100);
        }
      }, 16);
      return () => clearInterval(interval);
    }

    if (animState === 'descending') {
      const duration = 900;
      const start = Date.now();
      const interval = setInterval(() => {
        const p = Math.min(1, (Date.now() - start) / duration);
        const eased = 1 - Math.pow(1 - p, 3);
        setSpideyY(-220 + (-10 - (-220)) * eased);
        if (p >= 1) {
          clearInterval(interval);
          setAnimState('settling');
        }
      }, 16);
      return () => clearInterval(interval);
    }

    if (animState === 'settling') {
      const duration = 300;
      const start = Date.now();
      const interval = setInterval(() => {
        const p = Math.min(1, (Date.now() - start) / duration);
        const sway = Math.sin(p * Math.PI * 2) * 4 * (1 - p);
        setSpideyY(-10 + sway);
        if (p >= 1) {
          clearInterval(interval);
          setSpideyY(-10);
          setTimeout(() => setAnimState('card_open'), 150);
        }
      }, 16);
      return () => clearInterval(interval);
    }

    if (animState === 'card_open') {
      const duration = 280;
      const start = Date.now();
      const interval = setInterval(() => {
        const p = Math.min(1, (Date.now() - start) / duration);
        setCardOpacity(p);
        if (p >= 1) {
          clearInterval(interval);
          setAnimState('active');
        }
      }, 16);
      return () => clearInterval(interval);
    }

    if (animState === 'active') {
      const interval = setInterval(() => {
        setCountdown((prev) => {
          if (prev <= 1) {
            clearInterval(interval);
            dismissDemo();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      return () => clearInterval(interval);
    }

    if (animState === 'exiting') {
      const duration = 400;
      const start = Date.now();
      const interval = setInterval(() => {
        const p = Math.min(1, (Date.now() - start) / duration);
        setCardOpacity(1 - p);
        setSpideyY(-10 - 220 * p);
        if (p >= 1) {
          clearInterval(interval);
          setAnimState('idle');
        }
      }, 16);
      return () => clearInterval(interval);
    }

    return undefined;
  }, [animState]);

  return (
    <div className="relative max-w-5xl mx-auto mt-10 mb-12 px-4 sm:px-6">
      
      {/* Dark Burgundy Rounded Panel */}
      <div className="relative rounded-[32px] sm:rounded-[40px] bg-[#1C090D] border border-red-950/40 shadow-2xl p-6 sm:p-10 lg:p-12">
        
        {/* Subtle top background glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-2/3 h-40 bg-red-600/10 blur-3xl rounded-full pointer-events-none" />

        {/* Main Composition Grid */}
        <div className="relative max-w-4xl mx-auto flex flex-col md:flex-row items-center md:items-start justify-between gap-8 z-10">
          
          {/* Left: Interactive Demo Card */}
          <div className="w-full md:w-[440px] bg-[#140608] border border-red-950/80 rounded-3xl p-6 shadow-2xl text-stone-200 space-y-5">
            
            {/* Header & Subtitle */}
            <div>
              <h3 className="text-base font-bold text-white tracking-tight">Spider Reminder</h3>
              <p className="text-xs text-stone-400 font-medium mt-0.5">Try a sample reminder right in your browser.</p>
            </div>

            {/* MESSAGE Input Field */}
            <div className="space-y-1.5">
              <label className="text-[10px] font-bold text-stone-400 uppercase tracking-widest block">
                MESSAGE
              </label>
              <input
                type="text"
                value={customMessage}
                onChange={(e) => setCustomMessage(e.target.value)}
                placeholder="Time to drink water! 💧"
                className="w-full px-3.5 py-2.5 bg-[#0C0304] border border-stone-800/80 rounded-xl text-stone-100 text-xs sm:text-sm font-medium focus:outline-none focus:border-red-600 transition-colors"
              />
            </div>

            {/* SCHEDULE Controls */}
            <div className="space-y-2.5">
              <label className="text-[10px] font-bold text-stone-400 uppercase tracking-widest block">
                SCHEDULE
              </label>
              
              {/* Tab Selector */}
              <div className="flex items-center bg-[#0C0304] p-1 rounded-xl border border-stone-800/80 text-xs font-semibold">
                <button
                  onClick={() => setScheduleType('once')}
                  className={`flex-1 py-1.5 rounded-lg transition-all ${
                    scheduleType === 'once'
                      ? 'bg-stone-800 text-white shadow-sm'
                      : 'text-stone-400 hover:text-stone-200'
                  }`}
                >
                  At Time
                </button>
                <button
                  onClick={() => setScheduleType('repeat')}
                  className={`flex-1 py-1.5 rounded-lg transition-all ${
                    scheduleType === 'repeat'
                      ? 'bg-stone-800 text-white shadow-sm'
                      : 'text-stone-400 hover:text-stone-200'
                  }`}
                >
                  Repeat
                </button>
              </div>

              {/* Time / Repeat Picker */}
              {scheduleType === 'once' ? (
                <div className="flex items-center gap-2">
                  <div className="flex-1 flex items-center justify-center gap-1.5 bg-[#0C0304] border border-stone-800 px-3 py-2 rounded-xl text-sm font-mono font-bold text-white">
                    <input
                      type="text"
                      value={scheduleTime}
                      onChange={(e) => setScheduleTime(e.target.value)}
                      className="w-16 bg-transparent text-center focus:outline-none"
                    />
                  </div>
                  <div className="flex bg-[#0C0304] border border-stone-800 p-1 rounded-xl text-xs font-bold">
                    <button
                      onClick={() => setAmpm('AM')}
                      className={`px-2 py-1 rounded-lg ${ampm === 'AM' ? 'bg-stone-800 text-white' : 'text-stone-400'}`}
                    >
                      AM
                    </button>
                    <button
                      onClick={() => setAmpm('PM')}
                      className={`px-2 py-1 rounded-lg ${ampm === 'PM' ? 'bg-stone-800 text-white' : 'text-stone-400'}`}
                    >
                      PM
                    </button>
                  </div>
                </div>
              ) : (
                <div className="flex items-center gap-2 bg-[#0C0304] border border-stone-800 px-3 py-2 rounded-xl text-xs font-medium text-stone-300">
                  <span>Every</span>
                  <input
                    type="number"
                    value={repeatInterval}
                    onChange={(e) => setRepeatInterval(e.target.value)}
                    className="w-12 bg-stone-900 border border-stone-700 rounded px-1.5 py-0.5 text-center font-mono font-bold text-white focus:outline-none"
                  />
                  <span>minutes</span>
                </div>
              )}
            </div>

            {/* Status Indicator */}
            <div className="flex items-center justify-center gap-1.5 text-[11px] font-semibold text-stone-400">
              <span className="w-1.5 h-1.5 rounded-full bg-red-500 inline-block animate-pulse" />
              <span>• BROWSER PREVIEW ACTIVE</span>
            </div>

            {/* Action Buttons */}
            <div className="space-y-2">
              <button
                onClick={startDemo}
                className="w-full inline-flex items-center justify-center gap-2 px-5 py-3 bg-red-600 hover:bg-red-500 text-white font-bold text-xs sm:text-sm rounded-xl shadow-lg shadow-red-600/30 active:scale-98 transition-all"
              >
                <Play className="w-4 h-4 fill-white" />
                <span>Preview Reminder</span>
              </button>

              <button
                onClick={startDemo}
                className="w-full inline-flex items-center justify-center gap-2 px-5 py-2.5 bg-stone-900/90 hover:bg-stone-800 text-stone-300 font-semibold text-xs rounded-xl border border-stone-800/80 active:scale-98 transition-all"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Test Now</span>
              </button>
            </div>

            {/* Simulated Desktop Card Output */}
            {animState !== 'idle' && (
              <div
                style={{ opacity: cardOpacity }}
                className="relative bg-white rounded-2xl p-4 shadow-2xl border border-stone-200 text-stone-900 transition-opacity duration-200 mt-4"
              >
                <div className="absolute top-0 left-0 w-2 h-2 bg-red-500 rounded-tl-2xl" />
                <div className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-tr-2xl" />
                <div className="absolute bottom-0 left-0 w-2 h-2 bg-red-500 rounded-bl-2xl" />
                <div className="absolute bottom-0 right-0 w-2 h-2 bg-red-500 rounded-br-2xl" />

                <div className="text-[10px] font-bold text-red-500 tracking-wider uppercase mb-1">
                  ■ CUSTOM REMINDER
                </div>

                <p className="text-xs sm:text-sm font-semibold text-stone-800 leading-snug">
                  {customMessage}
                </p>

                <div className="mt-3 pt-2.5 border-t border-stone-100 flex items-center justify-between gap-2 text-[11px]">
                  <div className="inline-flex items-center gap-1 font-bold text-blue-600">
                    <Clock className="w-3 h-3" />
                    <span>Auto-dismiss in {countdown}s</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={dismissDemo}
                      className="px-2.5 py-1 bg-stone-900 text-white rounded font-bold hover:bg-stone-800"
                    >
                      Done
                    </button>
                    <button
                      onClick={dismissDemo}
                      className="px-2.5 py-1 bg-stone-100 text-stone-700 border border-stone-300 rounded font-semibold hover:bg-stone-200"
                    >
                      Snooze 5m
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Disclaimer Label */}
            <p className="text-[11px] text-stone-500 text-center font-medium">
              Browser preview — does not schedule desktop reminders.
            </p>

          </div>

          {/* Right: Hanging Spider-Man Overlapping Upper Panel Edge within ONE Shared Coordinate System */}
          <div className="relative w-full md:w-[320px] h-[360px] sm:h-[420px] flex items-start justify-center md:justify-end">
            
            {/* SHARED COORDINATE WRAPPER FOR SPIDER-MAN & WEB STRAND */}
            <div className="absolute top-0 left-1/2 md:left-auto md:right-4 -translate-x-1/2 md:translate-x-0 w-48 sm:w-56 z-30 pointer-events-none">
              
              {/* Thin Neutral Grey Web Strand Line connected precisely to 50% center (Spider-Man's feet) */}
              {/* Upper anchor top: -70px is safely clear of headline letters and platform badges */}
              <div
                style={{
                  height: `${Math.max(0, 70 + spideyY)}px`,
                  top: '-70px',
                }}
                className="absolute left-1/2 -translate-x-1/2 w-[1.5px] bg-[#A1A1AA] opacity-80 z-20 pointer-events-none"
              />

              {/* Hanging Spider-Man Sprite Image */}
              <div
                style={{
                  transform: `translateY(${spideyY}px)`,
                }}
                className="w-full flex justify-center transition-transform duration-100 ease-out pointer-events-none"
              >
                <img
                  src="/spiderman_hanging.png"
                  alt="Spider-Man Hanging Upside Down"
                  className="w-full h-auto drop-shadow-[0_20px_30px_rgba(0,0,0,0.85)] object-contain"
                />
              </div>

            </div>

            {/* Idle Notice when reset */}
            {animState === 'idle' && (
              <div className="mt-28 text-center p-5 rounded-2xl bg-[#140608] border border-red-950/60 text-stone-400 text-xs relative z-10">
                <CheckCircle2 className="w-8 h-8 text-red-500 mx-auto mb-2 opacity-80" />
                <p className="font-semibold text-stone-200">Spider-Man Ready</p>
                <p className="mt-1 text-[11px] text-stone-500">Click "Preview Reminder" or "Test Now" to trigger Spider-Man.</p>
              </div>
            )}

          </div>

        </div>

      </div>

    </div>
  );
};
