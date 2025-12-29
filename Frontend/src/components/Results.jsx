import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePrediction } from '../context/PredictionContext';
import Button from './Button';
import RiskBadge from './RiskBadge';

/**
 * Results Page Component
 * Displays prediction results with risk level and explanation
 */
export default function Results() {
  const navigate = useNavigate();
  const { results, resetForm, resetResults } = usePrediction();

  // Redirect if no results
  useEffect(() => {
    if (!results) {
      navigate('/predict');
    }
  }, [results, navigate]);

  if (!results) {
    return null;
  }

  const handleNewPrediction = () => {
    resetForm();
    resetResults();
    navigate('/predict');
  };

  const handleGoHome = () => {
    resetForm();
    resetResults();
    navigate('/');
  };

  // Confidence progress bar color
  const getConfidenceColor = () => {
    if (results.riskLevel === 'High') return 'bg-high-risk';
    if (results.riskLevel === 'Medium') return 'bg-medium-risk';
    return 'bg-low-risk';
  };

  return (
    <div className="min-h-screen bg-background py-8 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-text-primary mb-3 tracking-tight">
            Prediction Results
          </h1>
          <p className="text-text-secondary text-lg">
            Analysis completed on {new Date(results.timestamp).toLocaleString()}
          </p>
        </div>

        {/* Risk Badge */}
        <div className="mb-8 animate-fade-in">
          <RiskBadge riskLevel={results.riskLevel} confidence={results.confidence} />
        </div>

        {/* Confidence Score with Progress Bar */}
        <div className="bg-card-bg rounded-xl shadow-large p-6 md:p-8 mb-8 border border-border/50">
          <h2 className="text-2xl font-semibold text-text-primary mb-4">
            Confidence Score
          </h2>
          <div className="mb-2">
            <div className="flex justify-between items-center mb-3">
              <span className="text-lg font-semibold text-text-primary">
                {results.confidence}%
              </span>
            </div>
            <div className="w-full bg-border rounded-full h-5 overflow-hidden shadow-soft">
              <div
                className={`h-full ${getConfidenceColor()} transition-all duration-1000 ease-out rounded-full`}
                style={{ width: `${results.confidence}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Explanation Section */}
        <div className="bg-card-bg rounded-xl shadow-large p-6 md:p-8 mb-8 border border-border/50">
          <div className="flex items-start">
            <div className="w-10 h-10 bg-primary-light/10 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
              <svg className="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-semibold text-text-primary mb-3">
                Analysis Explanation
              </h2>
              <p className="text-text-secondary text-lg leading-relaxed">
                {results.explanation}
              </p>
            </div>
          </div>
        </div>

        {/* Contributing Factors */}
        {results.factors && results.factors.length > 0 && (
          <div className="bg-card-bg rounded-xl shadow-large p-6 md:p-8 mb-8 border border-border/50">
            <h2 className="text-2xl font-semibold text-text-primary mb-4">
              Contributing Factors
            </h2>
            <div className="space-y-3">
              {results.factors.map((factor, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-background rounded-lg border border-border/50 hover:border-border transition-colors">
                  <span className="text-text-primary font-medium">{factor.name}</span>
                  <span className={`px-4 py-1.5 rounded-full text-sm font-semibold ${
                    factor.impact === 'High' 
                      ? 'bg-high-risk text-white' 
                      : factor.impact === 'Medium'
                      ? 'bg-medium-risk text-white'
                      : 'bg-low-risk text-white'
                  }`}>
                    {factor.impact} Impact
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Disclaimer Box */}
        <div className="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-6 mb-8">
          <div className="flex items-start">
            <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
              <svg className="w-5 h-5 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div>
              <h3 className="font-semibold text-text-primary mb-2">Important Disclaimer</h3>
              <p className="text-text-secondary">
                This prediction is not a medical diagnosis. Please consult with a healthcare 
                professional for proper evaluation and medical advice. This tool is for 
                research purposes only.
              </p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          <Button
            variant="primary"
            onClick={handleNewPrediction}
            className="flex-1"
          >
            Try Another Prediction
          </Button>
          <Button
            variant="outline"
            onClick={handleGoHome}
            className="flex-1"
          >
            Return to Home
          </Button>
        </div>
      </div>
    </div>
  );
}

