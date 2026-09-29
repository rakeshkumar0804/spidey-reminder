import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { InteractiveDemo } from './components/InteractiveDemo';
import { Features } from './components/Features';
import { HowItWorks } from './components/HowItWorks';
import { Faq } from './components/Faq';
import { Footer } from './components/Footer';

export function App() {
  return (
    <div className="min-h-screen bg-[#FAF9F5] text-slate-900 font-sans selection:bg-red-500 selection:text-white">
      <Navbar />
      <main>
        <Hero />
        <InteractiveDemo />
        <Features />
        <HowItWorks />
        <Faq />
      </main>
      <Footer />
    </div>
  );
}

export default App;
