import React, { useState } from 'react';
import { Menu, X } from 'lucide-react';
import { APP_CONFIG } from '../config';

interface NavbarProps {
  currentPath: string;
  navigate: (path: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ currentPath, navigate }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const isManual = currentPath === '/manual' || currentPath === '/manual/';

  const handleNav = (path: string, e: React.MouseEvent) => {
    e.preventDefault();
    navigate(path);
    setMobileMenuOpen(false);
  };

  return (
    <nav className="sticky top-0 z-50 bg-[#FAF8F5]/95 backdrop-blur-md transition-all">
      <div className="w-full px-6 sm:px-10 lg:px-12">
        <div className="flex items-center justify-between h-20">
          
          {/* Left: Logo & Product Name */}
          <a
            href="/"
            onClick={(e) => handleNav('/', e)}
            className="flex items-center gap-2.5 group"
          >
            <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-red-500 flex items-center justify-center shadow-md shadow-red-500/20 group-hover:scale-105 transition-transform">
              <span className="text-xl leading-none">🕷️</span>
            </div>
            <span className="font-black text-lg sm:text-xl tracking-tight text-stone-900 group-hover:text-red-600 transition-colors">
              {APP_CONFIG.appName}
            </span>
          </a>

          {/* Right: Manual Link & Download Button matching Reference Image 2 */}
          <div className="hidden sm:flex items-center gap-7 lg:gap-8">
            <a
              href="/manual"
              onClick={(e) => handleNav('/manual', e)}
              className={`text-[17px] font-semibold transition-opacity ${
                isManual
                  ? 'text-stone-950 opacity-100 font-bold'
                  : 'text-stone-900 opacity-90 hover:opacity-100'
              }`}
            >
              Manual & FAQs
            </a>

            <a
              href={APP_CONFIG.downloadUrl}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#F1F5F9] hover:bg-slate-200/80 text-stone-900 rounded-full font-semibold text-sm sm:text-base active:scale-95 transition-all shadow-sm"
            >
              {/* Small near-black Windows Icon */}
              <svg className="w-4 h-4 text-stone-900 fill-current" viewBox="0 0 24 24">
                <path d="M0 3.449L9.75 2.1v9.451H0zM10.55 2v9.55H24V0zM10.55 12.45V22L24 24V12.45zM0 12.45h9.75V21.9L0 20.55z" />
              </svg>
              <span>Download for Windows</span>
            </a>
          </div>

          {/* Mobile Menu Toggle */}
          <div className="flex sm:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-stone-700 hover:bg-stone-200/50 transition-colors"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="sm:hidden bg-[#FAF8F5] px-6 pt-3 pb-6 space-y-4 border-b border-stone-200/40">
          <a
            href="/"
            onClick={(e) => handleNav('/', e)}
            className={`block text-base font-semibold ${
              !isManual ? 'text-red-600 font-bold' : 'text-stone-900'
            }`}
          >
            Home
          </a>
          <a
            href="/manual"
            onClick={(e) => handleNav('/manual', e)}
            className={`block text-base font-semibold ${
              isManual ? 'text-red-600 font-bold' : 'text-stone-900'
            }`}
          >
            Manual & FAQs
          </a>
          <a
            href={APP_CONFIG.downloadUrl}
            className="w-full flex items-center justify-center gap-2 px-5 py-3 bg-[#F1F5F9] text-stone-900 rounded-full font-semibold text-sm shadow-sm mt-2"
          >
            <svg className="w-4 h-4 text-stone-900 fill-current" viewBox="0 0 24 24">
              <path d="M0 3.449L9.75 2.1v9.451H0zM10.55 2v9.55H24V0zM10.55 12.45V22L24 24V12.45zM0 12.45h9.75V21.9L0 20.55z" />
            </svg>
            <span>Download for Windows ({APP_CONFIG.currentVersion})</span>
          </a>
        </div>
      )}
    </nav>
  );
};
