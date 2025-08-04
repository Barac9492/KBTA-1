'use client';

import { useState, useEffect } from 'react';
import { Moon, Sun, Sparkles } from 'lucide-react';

export function ThemeToggle() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    // Check system preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setIsDark(prefersDark);
    
    // Apply theme
    if (prefersDark) {
      document.documentElement.classList.add('dark');
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = !isDark;
    setIsDark(newTheme);
    
    if (newTheme) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  return (
    <button
      onClick={toggleTheme}
      className="relative p-2 rounded-lg bg-white/80 backdrop-blur-sm border border-gray-200 hover:bg-white/90 transition-all duration-300 group"
      aria-label="Toggle theme"
    >
      <div className="relative w-5 h-5">
        {isDark ? (
          <Moon className="w-5 h-5 text-purple-600 transition-all duration-300 group-hover:scale-110" />
        ) : (
          <Sun className="w-5 h-5 text-pink-500 transition-all duration-300 group-hover:scale-110" />
        )}
        <Sparkles className="absolute -top-1 -right-1 w-3 h-3 text-pink-400 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      </div>
    </button>
  );
} 