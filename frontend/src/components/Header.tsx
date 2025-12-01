/**
 * Header component with branding
 * WCAG 2.2 Level AA compliant
 */

import { MessageCircle } from 'lucide-react';

export function Header() {
  return (
    <header
      className="bg-walmart-blue text-white shadow-md"
      role="banner"
    >
      <div className="max-w-6xl mx-auto px-4 py-4">
        <div className="flex items-center gap-3">
          <MessageCircle className="w-8 h-8" aria-hidden="true" />
          <div>
            <h1 className="text-xl md:text-2xl font-bold">
              Walmart HR Assistant
            </h1>
            <p className="text-sm text-blue-100">
              Your 24/7 HR support companion
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}
