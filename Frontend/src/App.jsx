import { lazy, Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { PredictionProvider } from './context/PredictionContext';
import ErrorBoundary from './components/ErrorBoundary';
import './App.css';

// Lazy load components for code splitting and better performance
const Landing = lazy(() => import('./components/Landing'));
const PredictionForm = lazy(() => import('./components/PredictionForm'));
const Results = lazy(() => import('./components/Results'));

// Loading fallback component
function LoadingFallback() {
  return (
    <div className="min-h-screen bg-[#F9FAFB] flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#2563EB] mx-auto mb-4"></div>
        <p className="text-[#6B7280]">Loading...</p>
      </div>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <PredictionProvider>
        <Router>
          <Suspense fallback={<LoadingFallback />}>
            <Routes>
              <Route path="/" element={<Landing />} />
              <Route path="/predict" element={<PredictionForm />} />
              <Route path="/results" element={<Results />} />
            </Routes>
          </Suspense>
        </Router>
      </PredictionProvider>
    </ErrorBoundary>
  );
}

export default App;
