import React from 'react';
import { Github, Download, Heart } from 'lucide-react';
import { APP_CONFIG } from '../config';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-900 text-slate-400 py-16 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">
          
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-red-500 flex items-center justify-center text-lg">
                🕷️
              </div>
              <span className="font-extrabold text-xl text-white tracking-tight">
                {APP_CONFIG.appName}
              </span>
            </div>
            <p className="text-sm text-slate-400 max-w-sm leading-relaxed">
              An open-source custom break companion for Windows. Built for focus, eye health, hydration, and task management.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4">Quick Links</h4>
            <ul className="space-y-2.5 text-sm">
              <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
              <li><a href="#demo" className="hover:text-white transition-colors">Interactive Demo</a></li>
              <li><a href="#how-it-works" className="hover:text-white transition-colors">How it Works</a></li>
              <li><a href="#faq" className="hover:text-white transition-colors">FAQs</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4">Download & Source</h4>
            <div className="space-y-3">
              <a
                href={APP_CONFIG.downloadUrl}
                className="inline-flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-xl text-xs font-bold transition-colors shadow-sm"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Windows Download ({APP_CONFIG.currentVersion})</span>
              </a>
              <div>
                <a
                  href={APP_CONFIG.githubUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors"
                >
                  <Github className="w-4 h-4" />
                  <span>GitHub Repository</span>
                </a>
              </div>
            </div>
          </div>

        </div>

        <div className="pt-8 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© {new Date().getFullYear()} Spidey Reminder. Open Source Software.</p>
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
