import React from 'react';
import { Github, Download, Heart } from 'lucide-react';
import { APP_CONFIG } from '../config';

interface FooterProps {
  navigate: (path: string) => void;
}

export const Footer: React.FC<FooterProps> = ({ navigate }) => {
  return (
    <footer className="bg-stone-950 text-stone-400 py-12 border-t border-stone-900">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8 mb-10">
          
          <div className="space-y-2">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-red-500 flex items-center justify-center text-base">
                🕷️
              </div>
              <span className="font-extrabold text-lg text-white tracking-tight">
                {APP_CONFIG.appName}
              </span>
            </div>
            <p className="text-xs sm:text-sm text-stone-400 max-w-md">
              A lightweight, open-source Windows desktop reminder companion. Built for focus, eye health, hydration, and custom task scheduling.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-6 text-xs sm:text-sm font-semibold text-stone-300">
            <a
              href="/"
              onClick={(e) => {
                e.preventDefault();
                navigate('/');
              }}
              className="hover:text-white transition-colors"
            >
              Home
            </a>
            <a
              href="/manual"
              onClick={(e) => {
                e.preventDefault();
                navigate('/manual');
              }}
              className="hover:text-white transition-colors"
            >
              Manual & FAQs
            </a>
            <a
              href={APP_CONFIG.githubUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 hover:text-white transition-colors"
            >
              <Github className="w-4 h-4" />
              <span>GitHub</span>
            </a>
            <a
              href={APP_CONFIG.downloadUrl}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 bg-red-600 hover:bg-red-500 text-white rounded-xl text-xs font-bold transition-colors shadow-sm"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download EXE ({APP_CONFIG.currentVersion})</span>
            </a>
          </div>

        </div>

        <div className="pt-6 border-t border-stone-900 flex flex-col sm:flex-row items-center justify-between text-xs text-stone-500 gap-3">
          <p>© {new Date().getFullYear()} Spidey Reminder. Open Source Software (MIT).</p>
          <div className="flex items-center gap-1">
            <span>Crafted with</span>
            <Heart className="w-3.5 h-3.5 text-red-500 fill-red-500 inline" />
            <span>for Windows developers & creators</span>
          </div>
        </div>

      </div>
    </footer>
  );
};
