/**
 * Banner component shown when chatbot confidence is low
 * WCAG 2.2 Level AA compliant with proper color contrast
 */

import { ExternalLink, AlertCircle } from 'lucide-react';

interface FallbackBannerProps {
  microsoftListUrl: string;
}

export function FallbackBanner({ microsoftListUrl }: FallbackBannerProps) {
  return (
    <div
      className="mx-4 mb-4 p-4 bg-yellow-50 border-l-4 border-walmart-yellow rounded-r-lg"
      role="alert"
      aria-live="polite"
    >
      <div className="flex items-start gap-3">
        <AlertCircle
          className="w-5 h-5 text-yellow-700 flex-shrink-0 mt-0.5"
          aria-hidden="true"
        />
        <div className="flex-1">
          <h3 className="text-sm font-semibold text-yellow-900 mb-1">
            Need more specific information?
          </h3>
          <p className="text-sm text-yellow-800 mb-3">
            I'm not entirely certain about this answer. For the most accurate and
            up-to-date information, please check our HR resources.
          </p>
          <a
            href={microsoftListUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-sm font-medium text-walmart-blue hover:text-walmart-dark underline focus:outline-none focus-visible:ring-2 focus-visible:ring-walmart-blue focus-visible:ring-offset-2 rounded"
            aria-label="Open HR Resources in Microsoft List (opens in new tab)"
          >
            View HR Resources
            <ExternalLink className="w-4 h-4" aria-hidden="true" />
          </a>
        </div>
      </div>
    </div>
  );
}
