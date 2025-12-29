/**
 * Error Display Component
 * Replaces alert() with user-friendly error messages
 * @param {Object} props - Component props
 * @param {string} props.message - Error message to display
 * @param {Function} props.onDismiss - Function to call when dismissing error
 * @param {boolean} props.show - Whether to show the error
 */
export default function ErrorDisplay({ message, onDismiss, show = true }) {
  if (!show || !message) return null;

  return (
    <div 
      className="bg-[#FEF2F2] border-2 border-[#EF4444] rounded-lg p-4 mb-4 animate-fade-in"
      role="alert"
      aria-live="assertive"
    >
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <svg className="h-5 w-5 text-[#EF4444]" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="ml-3 flex-1">
          <h3 className="text-sm font-semibold text-[#991B1B] mb-1">
            Error
          </h3>
          <p className="text-sm text-[#7F1D1D]">
            {message}
          </p>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="ml-4 flex-shrink-0 text-[#991B1B] hover:text-[#7F1D1D] focus:outline-none"
            aria-label="Dismiss error"
          >
            <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}

