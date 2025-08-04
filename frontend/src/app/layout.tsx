import type { Metadata } from 'next'
import { Inter, Poppins } from 'next/font/google'
import './globals.css'
import { Navigation } from '@/components/Navigation'
import { Footer } from '@/components/Footer'
import { ThemeProvider } from '@/components/ThemeProvider'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter'
})

const poppins = Poppins({ 
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-poppins'
})

export const metadata: Metadata = {
  title: 'K-Beauty Trend Agent - AI-Powered Beauty Intelligence Platform',
  description: 'Get real-time K-beauty insights, trend forecasts, and market analysis. The Bloomberg of Beauty - powered by AI for beauty professionals and enthusiasts.',
  keywords: 'K-beauty, Korean beauty, trend analysis, AI beauty, beauty intelligence, skincare trends, beauty market',
  openGraph: {
    title: 'K-Beauty Trend Agent - AI-Powered Beauty Intelligence',
    description: 'Real-time K-beauty insights and trend forecasts powered by AI',
    url: 'https://kbeauty-trend-agent.vercel.app',
    siteName: 'K-Beauty Trend Agent',
    images: [
      {
        url: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=1200&h=630&fit=crop',
        width: 1200,
        height: 630,
        alt: 'K-Beauty Trend Agent - AI-Powered Beauty Intelligence',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'K-Beauty Trend Agent - AI-Powered Beauty Intelligence',
    description: 'Real-time K-beauty insights and trend forecasts powered by AI',
    images: ['https://images.unsplash.com/photo-1556228720-195a672e8a03?w=1200&h=630&fit=crop'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} ${poppins.variable} font-sans antialiased`}>
        <ThemeProvider>
          <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-rose-50 dark:from-gray-900 dark:via-purple-900 dark:to-gray-900">
            <Navigation />
            <main className="pt-16">
              {children}
            </main>
            <Footer />
          </div>
        </ThemeProvider>
      </body>
    </html>
  )
}
