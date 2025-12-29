import { Component } from 'react';
import Button from './Button';

/**
 * Error Boundary Component
 * Catches JavaScript errors in child components and displays fallback UI
 * Prevents entire app from crashing
 */
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log error to console (in production, this would go to error tracking service)
    console.error('Error caught by boundary:', error, errorInfo);
    this.setState({
      error,
      errorInfo
    });

    // In production, send to error tracking service (e.g., Sentry, LogRocket)
    // Example: logErrorToService(error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    // Optionally reload the page or navigate to home
    window.location.href = '/';
  };

  render() {
    if (this.state.hasError) {
      // Custom fallback UI
      return (
        <div className="min-h-screen bg-[#F9FAFB] flex items-center justify-center px-4">
          <div className="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8 text-center">
            <div className="text-6xl mb-4">⚠️</div>
            <h1 className="text-3xl font-bold text-[#111827] mb-4">
              Something went wrong
            </h1>
            <p className="text-[#6B7280] text-lg mb-6">
              We're sorry, but something unexpected happened. Please try refreshing the page or return to the home page.
            </p>
            
            {process.env.NODE_ENV === 'development' && this.state.error && (
              <details className="mb-6 text-left bg-[#F9FAFB] p-4 rounded-lg">
                <summary className="cursor-pointer text-sm font-semibold text-[#111827] mb-2">
                  Error Details (Development Only)
                </summary>
                <pre className="text-xs text-[#6B7280] overflow-auto mt-2">
                  {this.state.error.toString()}
                  {this.state.errorInfo?.componentStack}
                </pre>
              </details>
            )}

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                variant="primary"
                onClick={this.handleReset}
              >
                Return to Home
              </Button>
              <Button
                variant="outline"
                onClick={() => window.location.reload()}
              >
                Refresh Page
              </Button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

