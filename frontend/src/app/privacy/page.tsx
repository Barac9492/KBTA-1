'use client';

import { Navigation } from '@/components/Navigation';

export default function PrivacyPolicy() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <div className="lg:pl-64">
        <main className="py-6">
          <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-6">Privacy Policy</h1>
              
              <div className="prose max-w-none">
                <p className="text-gray-600 mb-6">
                  Last updated: August 3, 2025
                </p>

                <h2 className="text-xl font-semibold text-gray-900 mb-4">Information We Collect</h2>
                <p className="text-gray-700 mb-4">
                  K-Beauty Trend Agent collects information you provide directly to us, such as when you subscribe to our newsletter or contact us. This may include your email address and any other information you choose to provide.
                </p>

                <h2 className="text-xl font-semibold text-gray-900 mb-4">How We Use Your Information</h2>
                <p className="text-gray-700 mb-4">
                  We use the information we collect to:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li>Provide and maintain our services</li>
                  <li>Send you newsletters and updates about K-beauty trends</li>
                  <li>Respond to your comments and questions</li>
                  <li>Improve our services and develop new features</li>
                </ul>

                <h2 className="text-xl font-semibold text-gray-900 mb-4">Data Sources</h2>
                <p className="text-gray-700 mb-4">
                  Our AI analysis is based on publicly available information from Korean beauty blogs, social media, and product reviews. We do not collect personal information from these sources, and all data is anonymized and aggregated for trend analysis.
                </p>

                <h2 className="text-xl font-semibold text-gray-900 mb-4">Your Rights</h2>
                <p className="text-gray-700 mb-4">
                  You have the right to:
                </p>
                <ul className="list-disc list-inside text-gray-700 mb-4 space-y-2">
                  <li>Access the personal information we hold about you</li>
                  <li>Request correction of inaccurate information</li>
                  <li>Request deletion of your personal information</li>
                  <li>Unsubscribe from our newsletters at any time</li>
                </ul>

                <h2 className="text-xl font-semibold text-gray-900 mb-4">Contact Us</h2>
                <p className="text-gray-700 mb-4">
                  If you have any questions about this Privacy Policy, please contact us at privacy@kbeauty-trend-agent.com
                </p>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
} 