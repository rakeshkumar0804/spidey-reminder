import { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { ManualPage } from './components/ManualPage';
import { Footer } from './components/Footer';

export function App() {
  const [currentPath, setCurrentPath] = useState<string>(() => window.location.pathname);

  useEffect(() => {
    const handlePopState = () => {
      setCurrentPath(window.location.pathname);
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const navigate = (path: string) => {
    window.history.pushState({}, '', path);
    setCurrentPath(path);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const isManual = currentPath === '/manual' || currentPath === '/manual/';

  return (
    <div className="min-h-screen bg-[#FAF8F5] text-stone-900 font-sans selection:bg-red-500 selection:text-white flex flex-col justify-between">
      <div>
        <Navbar currentPath={currentPath} navigate={navigate} />
        <main>
          {isManual ? <ManualPage navigate={navigate} /> : <Hero navigate={navigate} />}
        </main>
      </div>
      <Footer navigate={navigate} />
    </div>
  );
}

export default App;
