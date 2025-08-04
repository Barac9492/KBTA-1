'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { 
  Home, 
  Archive, 
  Bell, 
  Sparkles,
  Menu,
  X
} from 'lucide-react';
import { ThemeToggle } from './ThemeToggle';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Archive', href: '/archive', icon: Archive },
  { name: 'Subscribe', href: '/subscribe', icon: Bell },
];

interface NavigationProps {
  children?: React.ReactNode;
}

export function Navigation({ children }: NavigationProps = {}) {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile menu */}
      <div className="lg:hidden">
        <div className="fixed inset-0 z-50">
          {mobileMenuOpen && (
            <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setMobileMenuOpen(false)} />
          )}
          
          <motion.div
            initial={{ x: '-100%' }}
            animate={{ x: mobileMenuOpen ? 0 : '-100%' }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className="relative flex w-full max-w-xs flex-1 flex-col bg-white pt-5 pb-4"
          >
            <div className="absolute top-0 right-0 -mr-12 pt-2">
              <Button
                type="button"
                variant="ghost"
                className="ml-1 flex h-10 w-10 items-center justify-center rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                onClick={() => setMobileMenuOpen(false)}
              >
                <X className="h-6 w-6 text-white" />
              </Button>
            </div>
            
            <div className="flex flex-shrink-0 items-center px-4">
              <div className="flex items-center gap-2">
                <Sparkles className="h-8 w-8 text-pink-500" />
                <span className="text-xl font-bold text-gray-900">K-Beauty Trends</span>
              </div>
            </div>
            
            <nav className="mt-5 h-full flex-1 space-y-1 px-2">
              {navigation.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md nav-item-hover ${
                      isActive
                        ? 'bg-pink-100 text-pink-700 glow-pink'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <item.icon className="mr-3 h-5 w-5" />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </motion.div>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex min-h-0 flex-1 flex-col bg-white border-r border-gray-200">
          <div className="flex flex-1 flex-col overflow-y-auto pt-5 pb-4">
            <div className="flex flex-shrink-0 items-center px-4">
              <div className="flex items-center gap-2">
                <Sparkles className="h-8 w-8 text-pink-500" />
                <span className="text-xl font-bold text-gray-900">K-Beauty Trends</span>
              </div>
              <div className="ml-auto">
                <ThemeToggle />
              </div>
            </div>
            
            <nav className="mt-8 flex-1 space-y-1 px-2">
              {navigation.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md nav-item-hover transition-colors ${
                      isActive
                        ? 'bg-pink-100 text-pink-700 glow-pink'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <item.icon className="mr-3 h-5 w-5" />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      </div>

      {/* Mobile header */}
      <div className="lg:hidden">
        <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
          <Button
            type="button"
            variant="ghost"
            className="-m-2.5 p-2.5 text-gray-700 lg:hidden"
            onClick={() => setMobileMenuOpen(true)}
          >
            <Menu className="h-6 w-6" />
          </Button>
          
          <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
            <div className="flex items-center gap-2">
              <Sparkles className="h-6 w-6 text-pink-500" />
              <span className="text-lg font-semibold text-gray-900">K-Beauty Trends</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        <main className="py-6">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
} 