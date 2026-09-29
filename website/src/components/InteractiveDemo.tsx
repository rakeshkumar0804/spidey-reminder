import React, { useState, useEffect, useRef } from 'react';
import { Play, Sparkles, Info } from 'lucide-react';
import { APP_CONFIG } from '../config';

export const InteractiveDemo: React.FC = () => {
  const [sampleMessage, setSampleMessage] = useState('Look 20 feet away for 20 seconds');
  const [sampleTitle, setSampleTitle] = useState('EYE BREAK');

  const [animState, setAnimState] = useState<'idle' | 'shooting_web' | 'descending' | 'settling' | 'card_opening' | 'typing' | 'active' | 'exiting'>('idle');
  const [webProgress, setWebProgress] = useState(0); // 0 to 1
  const [spideyY, setSpideyY] = useState(-240); // Y position relative to canvas top
  const [cardOpacity, setCardOpacity] = useState(0); // 0 to 1
  const [revealedWordsCount, setRevealedWordsCount] = useState(0);
  const [countdown, setCountdown] = useState(20);
  const [reducedMotion, setReducedMotion] = useState(false);

  const canvasRef = useRef<HTMLDivElement>(null);
  const words = sampleMessage.trim().split(/\s+/).filter(Boolean);

  // Target settled positions (px from canvas top edge)
  const settledWebLength = 70; // 70px web length
  const hiddenY = -240; // fully hidden above top edge

  const startDemo = () => {
    if (reducedMotion) {
      setAnimState('active');
      setWebProgress(1);
      setSpideyY(settledWebLength);
      setCardOpacity(1);
      setRevealedWordsCount(words.length);
      setCountdown(20);
      return;
    }

    setAnimState('shooting_web');
    setWebProgress(0);
    setSpideyY(hiddenY);
    setCardOpacity(0);
    setRevealedWordsCount(0);
    setCountdown(20);
  };

  const dismissDemo = () => {
    if (animState !== 'idle') {
      setAnimState('exiting');
    }
  };

  // State Machine Animation Logic
  useEffect(() => {
    if (animState === 'shooting_web') {
      const duration = 500;
      const start = Date.now();
      const interval = setInterval(() => {
        const elapsed = Date.now() - start;
        const p = Math.min(1, elapsed / duration);
        setWebProgress(p);
        if (p >= 1) {
          clearInterval(interval);
          setTimeout(() => setAnimState('descending'), 200);
        }
      }, 16);
      return () => clearInterval(interval);
    }

    if (animState === 'descending') {
      const duration = 1200;
      const start = Date.now();
      const interval = setInterval(() => {
        const elapsed = Date.now() - start;
        const p = Math.min(1, elapsed / duration);
        // Eased cubic descent
        const eased = 1 - Math.pow(1 - p, 3);
        setWebProgress(1);
        setSpideyY(hiddenY + (settledWebLength - hiddenY) * eased);
        if (p >= 1) {
          clearInterval(interval);
          setAnimState('settling');
        }
      }, 16);
      return () => clearInterval(interval);
    }

    if (animState === 'settling') {
      const duration = 400;
      const start = Date.now();
      const interval = setInterval(() => {
        const elapsed = Date.now() - start;
        const p = Math.min(1, elapsed / duration);
        // Small damped oscillation sway
        const sway = Math.sin(p * Math.PI * 2) * 4 * (1 - p);
        setSpideyY(settledWebLength + sway);
        if (p >= 1) {
          clearInterval(interval);
          setSpideyY(settledWebLength);
          setTimeout(() => setAnimState('card_opening'), 250);
        }
      }, 16);
      return () => clearInterval(interval);
    }

    if (animState === 'card_opening') {
      const duration = 300;
      const start = Date.now();
      const interval = setInterval(() => {
        const elapsed = Date.now() - start;
        const p = Math.min(1, elapsed / duration);
        setCardOpacity(p);
        if (p >= 1) {
          clearInterval(interval);
          setAnimState('typing');
        }
      }, 16);
      return () => clearInterval(interval);
    }

    if (animState === 'typing') {
      let currentWord = 0;
      const interval = setInterval(() => {
        currentWord++;
        setRevealedWordsCount(currentWord);
        if (currentWord >= words.length) {
          clearInterval(interval);
          setTimeout(() => setAnimState('active'), 200);
        }
      }, 300);
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
      const duration = 600;
      const start = Date.now();
      const interval = setInterval(() => {
        const elapsed = Date.now() - start;
        const p = Math.min(1, elapsed / duration);
        setCardOpacity(1 - p);
        setSpideyY(settledWebLength + (hiddenY - settledWebLength) * p);
        setWebProgress(1 - p);
        if (p >= 1) {
          clearInterval(interval);
          setAnimState('idle');
        }
      }, 16);
      return () => clearInterval(interval);
    }

    return undefined;
  }, [animState, words.length]);

  return (
    <section id="demo" className="py-16 md:py-24 bg-stone-900 text-white relative">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-red-500/10 text-red-400 text-xs font-semibold uppercase tracking-wider mb-4 border border-red-500/20">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Interactive Web Preview</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white mb-4">
            See Spider-Man in action.
          </h2>
          <p className="text-slate-400 text-base sm:text-lg">
            Customize a sample reminder below and test the exact entrance animation sequence.
          </p>
        </div>

        {/* Demo Controls Form */}
        <div className="max-w-2xl mx-auto bg-slate-800/80 p-6 rounded-2xl border border-slate-700/60 shadow-xl backdrop-blur-md mb-10">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Header Tag
              </label>
              <select
                value={sampleTitle}
                onChange={(e) => setSampleTitle(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-red-500"
              >
                <option value="EYE BREAK">EYE BREAK</option>
                <option value="HYDRATION">HYDRATION</option>
                <option value="CUSTOM REMINDER">CUSTOM REMINDER</option>
              </select>
            </div>

            <div className="sm:col-span-2">
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                Sample Message
              </label>
              <input
                type="text"
                value={sampleMessage}
                onChange={(e) => setSampleMessage(e.target.value)}
                placeholder="Enter sample sentence..."
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-red-500"
              />
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-slate-700/50">
            <label className="flex items-center gap-2 text-xs text-slate-400 cursor-pointer">
              <input
                type="checkbox"
                checked={reducedMotion}
                onChange={(e) => setReducedMotion(e.target.checked)}
                className="rounded text-red-500 focus:ring-0 bg-slate-900 border-slate-700"
              />
              <span>Simulate Reduced Motion</span>
            </label>

            <div className="flex items-center gap-3">
              {animState !== 'idle' && (
                <button
                  onClick={dismissDemo}
                  className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-xs font-semibold rounded-xl text-slate-200 transition-colors"
                >
                  Dismiss
                </button>
              )}
              <button
                onClick={startDemo}
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-red-600 hover:bg-red-500 text-white rounded-xl text-sm font-bold shadow-lg shadow-red-600/30 transition-all active:scale-95"
              >
                <Play className="w-4 h-4 fill-white" />
                <span>Preview Reminder</span>
              </button>
            </div>
          </div>
        </div>

        {/* Demo Virtual Desktop Monitor Frame */}
        <div className="relative max-w-4xl mx-auto rounded-2xl bg-slate-950 border-4 border-slate-800 shadow-2xl overflow-hidden flex flex-col justify-between">
          
          {/* Top Desktop Bar */}
          <div className="h-8 bg-slate-900 border-b border-slate-800/80 px-4 flex items-center justify-between text-xs text-slate-400 select-none">
            <div className="flex items-center gap-2 font-semibold text-slate-300">
              <span className="w-2.5 h-2.5 rounded-full bg-red-500"></span>
              <span>Simulated Windows Desktop</span>
            </div>
            <div className="flex items-center gap-3 text-[11px] font-mono">
              <span>{APP_CONFIG.appName} Web Preview</span>
              <span>1920 × 1080</span>
            </div>
          </div>

          {/* Virtual Screen Canvas */}
          <div
            ref={canvasRef}
            style={{ height: '460px', minHeight: '460px' }}
            className="relative bg-gradient-to-br from-slate-900 via-slate-950 to-stone-900 p-4 sm:p-6 overflow-hidden"
          >
            
            {/* Desktop Wallpaper Placeholder Text */}
            <div className="absolute inset-0 flex items-center justify-center opacity-10 pointer-events-none select-none">
              <span className="text-4xl sm:text-6xl font-black text-white tracking-widest uppercase">DESKTOP</span>
            </div>

            {/* OVERLAY STAGE: SPIDER-MAN + WEB + REMINDER CARD */}
            {animState !== 'idle' && (
              <div className="absolute top-0 right-3 sm:right-8 flex items-start gap-2.5 sm:gap-5 z-20">
                
                {/* 1. Message Card */}
                <div
                  style={{
                    opacity: cardOpacity,
                    transform: `scale(${0.9 + cardOpacity * 0.1})`,
                    transition: 'opacity 0.2s ease, transform 0.2s ease',
                  }}
                  className="w-[200px] xs:w-[240px] sm:w-72 bg-white rounded-xl p-3 sm:p-4 shadow-2xl text-slate-900 relative mt-10 sm:mt-12 border border-slate-200"
                >
                  {/* 4 Red Accent Corners */}
                  <span className="absolute top-0 left-0 w-2 h-2 bg-red-500 rounded-tl"></span>
                  <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-tr"></span>
                  <span className="absolute bottom-0 left-0 w-2 h-2 bg-red-500 rounded-bl"></span>
                  <span className="absolute bottom-0 right-0 w-2 h-2 bg-red-500 rounded-br"></span>

                  {/* Header Tag */}
                  <div className="text-[10px] font-bold text-red-500 tracking-wider mb-1">
                    ■ {sampleTitle}
                  </div>

                  {/* Word-by-Word Sentence */}
                  <div className="text-xs sm:text-sm font-semibold text-slate-900 leading-snug min-h-[40px] sm:min-h-[48px]">
                    {words.slice(0, revealedWordsCount).join(' ')}
                  </div>

                  {/* Countdown Timer */}
                  {sampleTitle === 'EYE BREAK' && (
                    <div className="text-[11px] sm:text-xs font-bold text-blue-600 mt-1.5 sm:mt-2">
                      {countdown} seconds remaining
                    </div>
                  )}

                  {/* Action Buttons */}
                  {(animState === 'active' || reducedMotion) && (
                    <div className="flex items-center gap-2 mt-2.5 sm:mt-3 pt-2 border-t border-slate-100">
                      <button
                        onClick={dismissDemo}
                        className="px-2.5 py-1 sm:px-3 sm:py-1.5 bg-slate-900 text-white rounded-md text-[11px] sm:text-xs font-bold hover:bg-slate-800 transition-colors"
                      >
                        Done
                      </button>
                      <button
                        onClick={dismissDemo}
                        className="px-2.5 py-1 sm:px-3 sm:py-1.5 bg-slate-100 text-slate-700 border border-slate-300 rounded-md text-[11px] sm:text-xs font-semibold hover:bg-slate-200 transition-colors"
                      >
                        Snooze 5m
                      </button>
                    </div>
                  )}
                </div>

                {/* 2. Spider-Man Figure & Web Strand Container */}
                <div className="relative flex flex-col items-center">
                  
                  {/* Dynamic Web Strand Line (Anchored to top-0 of canvas) */}
                  <div
                    style={{
                      height: `${webProgress * settledWebLength}px`,
                      width: '2px',
                    }}
                    className="bg-white shadow-[0_0_8px_rgba(255,255,255,0.8)] transition-all duration-75"
                  />

                  {/* Spider-Man Asset (Attached to web tip) */}
                  <img
                    src="/spiderman_hanging.png"
                    alt="Spider-Man Hanging"
                    style={{
                      transform: `translateY(${spideyY - settledWebLength}px)`,
                      opacity: animState === 'shooting_web' ? 0 : 1,
                    }}
                    className="w-24 sm:w-32 object-contain drop-shadow-2xl transition-transform duration-75 select-none"
                  />
                </div>

              </div>
            )}

            {/* Instruction Notice at bottom of screen */}
            <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between text-xs text-slate-400 bg-slate-900/80 px-4 py-2 rounded-xl backdrop-blur-md border border-slate-800">
              <div className="flex items-center gap-2">
                <Info className="w-4 h-4 text-blue-400 flex-shrink-0" />
                <span><b>Website Preview:</b> Test the interactive animation sequence above. This browser preview does not schedule desktop reminders.</span>
              </div>
            </div>

          </div>
        </div>

        </div>
    </section>
  );
};

