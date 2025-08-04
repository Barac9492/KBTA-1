import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Footer } from '@/components/Footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'K-Beauty Trend Agent - AI-Powered Daily Trend Analysis',
  description: 'Automated daily K-beauty trend analysis using AI. Get insights from Korean beauty blogs, social media, and product reviews. Powered by GPT-4 and deployed on Vercel.',
  keywords: [
    'K-beauty',
    'Korean beauty',
    'trend analysis',
    'AI analysis',
    'beauty trends',
    'Korean cosmetics',
    'beauty insights',
    'automated analysis',
    'GPT-4',
    'Vercel'
  ],
  authors: [{ name: 'K-Beauty Trend Agent' }],
  creator: 'K-Beauty Trend Agent',
  publisher: 'K-Beauty Trend Agent',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://kbeauty-trend-agent.vercel.app'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'K-Beauty Trend Agent - AI-Powered Daily Trend Analysis',
    description: 'Automated daily K-beauty trend analysis using AI. Get insights from Korean beauty blogs, social media, and product reviews.',
    url: 'https://kbeauty-trend-agent.vercel.app',
    siteName: 'K-Beauty Trend Agent',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'K-Beauty Trend Agent Dashboard',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'K-Beauty Trend Agent - AI-Powered Daily Trend Analysis',
    description: 'Automated daily K-beauty trend analysis using AI. Get insights from Korean beauty blogs, social media, and product reviews.',
    images: ['/og-image.png'],
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
  verification: {
    google: 'your-google-verification-code',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <meta name="theme-color" content="#ec4899" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        
        {/* Structured Data */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "WebApplication",
              "name": "K-Beauty Trend Agent",
              "description": "AI-powered daily K-beauty trend analysis platform",
              "url": "https://kbeauty-trend-agent.vercel.app",
              "applicationCategory": "BusinessApplication",
              "operatingSystem": "Web",
              "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
              },
              "author": {
                "@type": "Person",
                "name": "K-Beauty Trend Agent"
              },
              "creator": {
                "@type": "Person",
                "name": "K-Beauty Trend Agent"
              }
            })
          }}
        />
      </head>
      <body className={inter.className}>
        {children}
        <Footer />
      </body>
    </html>
  )
}
