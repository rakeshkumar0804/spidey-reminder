import React, { useState } from 'react';
import { Download, Github, Menu, X } from 'lucide-react';
import { APP_CONFIG } from '../config';

export const Navbar: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-[#FAF9F5]/90 backdrop-blur-md border-b border-stone-200/60 transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Logo & Product Name */}
          <a href="#" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-red-500 flex items-center justify-center shadow-md shadow-red-500/20 group-hover:scale-105 transition-transform">
              <span className="text-xl">🕷️</span>
            </div>
            <div className="flex flex-col">
              <span className="font-extrabold text-xl tracking-tight text-slate-900 group-hover:text-red-600 transition-colors">
                {APP_CONFIG.appName}
              </span>
              <span className="text-xs font-semibold text-slate-400">Windows Companion</span>
            </div>
          </a>

          {/* Desktop Nav Links */}
          <div className="hidden md:flex items-center gap-8 font-medium text-slate-600 text-sm">
            <a href="#features" className="hover:text-slate-900 transition-colors">Features</a>
            <a href="#demo" className="hover:text-slate-900 transition-colors">Interactive Demo</a>
            <a href="#how-it-works" className="hover:text-slate-900 transition-colors">How it Works</a>
            <a href="#faq" className="hover:text-slate-900 transition-colors">FAQs</a>
          </div>

          {/* Desktop Right CTAs */}
          <div className="hidden md:flex items-center gap-4">
            <a
              href={APP_CONFIG.githubUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="p-2.5 text-slate-600 hover:text-slate-900 hover:bg-stone-200/50 rounded-xl transition-all"
              aria-label="GitHub Repository"
            >
              <Github className="w-5 h-5" />
            </a>
            <a
              href={APP_CONFIG.downloadUrl}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-slate-900 text-white rounded-xl font-semibold text-sm hover:bg-slate-800 active:scale-95 transition-all shadow-sm"
            >
              <Download className="w-4 h-4 text-red-400" />
              <span>Download for Windows</span>
            </a>
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-slate-700 hover:bg-stone-200/50 transition-colors"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-stone-200 bg-[#FAF9F5] px-4 pt-2 pb-6 space-y-4">
          <a
            href="#features"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-base font-medium text-slate-700 hover:text-slate-900"
          >
            Features
          </a>
          <a
            href="#demo"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-base font-medium text-slate-700 hover:text-slate-900"
          >
            Interactive Demo
          </a>
          <a
            href="#how-it-works"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-base font-medium text-slate-700 hover:text-slate-900"
          >
            How it Works
          </a>
          <a
            href="#faq"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-base font-medium text-slate-700 hover:text-slate-900"
          >
            FAQs
          </a>
          <div className="pt-2 flex flex-col gap-3">
            <a
              href={APP_CONFIG.downloadUrl}
              className="w-full flex items-center justify-center gap-2 px-5 py-3 bg-slate-900 text-white rounded-xl font-semibold text-sm shadow-md"
            >
              <Download className="w-4 h-4 text-red-400" />
              <span>Download for Windows ({APP_CONFIG.currentVersion})</span>
            </a>
            <a
              href={APP_CONFIG.githubUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full flex items-center justify-center gap-2 px-5 py-3 border border-stone-300 text-slate-700 rounded-xl font-medium text-sm"
            >
              <Github className="w-4 h-4" />
              <span>View Source on GitHub</span>
            </a>
          </div>
        </div>
      )}
    </nav>
  );
};
