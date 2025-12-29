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
    if (results.riskLevel === 'High') return 'bg-[#EF4444]';
    if (results.riskLevel === 'Medium') return 'bg-[#F59E0B]';
    return 'bg-[#10B981]';
  };

  return (
    <div className="min-h-screen bg-[#F9FAFB] py-8 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-[#111827] mb-2">
            Prediction Results
          </h1>
          <p className="text-[#6B7280] text-lg">
            Analysis completed on {new Date(results.timestamp).toLocaleString()}
          </p>
        </div>

        {/* Risk Badge */}
        <div className="mb-8 animate-fade-in">
          <RiskBadge riskLevel={results.riskLevel} confidence={results.confidence} />
        </div>

        {/* Confidence Score with Progress Bar */}
        <div className="bg-white rounded-lg shadow-lg p-6 md:p-8 mb-8">
          <h2 className="text-2xl font-semibold text-[#111827] mb-4">
            Confidence Score
          </h2>
          <div className="mb-2">
            <div className="flex justify-between items-center mb-2">
              <span className="text-lg font-semibold text-[#111827]">
                {results.confidence}%
              </span>
            </div>
            <div className="w-full bg-[#E5E7EB] rounded-full h-4 overflow-hidden">
              <div
                className={`h-full ${getConfidenceColor()} transition-all duration-1000 ease-out`}
                style={{ width: `${results.confidence}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Explanation Section */}
        <div className="bg-white rounded-lg shadow-lg p-6 md:p-8 mb-8">
          <div className="flex items-start">
            <div className="text-3xl mr-4">ℹ️</div>
            <div className="flex-1">
              <h2 className="text-2xl font-semibold text-[#111827] mb-3">
                Analysis Explanation
              </h2>
              <p className="text-[#6B7280] text-lg leading-relaxed">
                {results.explanation}
              </p>
            </div>
          </div>
        </div>

        {/* Contributing Factors */}
        {results.factors && results.factors.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-6 md:p-8 mb-8">
            <h2 className="text-2xl font-semibold text-[#111827] mb-4">
              Contributing Factors
            </h2>
            <div className="space-y-3">
              {results.factors.map((factor, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-[#F9FAFB] rounded-lg">
                  <span className="text-[#111827] font-medium">{factor.name}</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    factor.impact === 'High' 
                      ? 'bg-[#EF4444] text-white' 
                      : factor.impact === 'Medium'
                      ? 'bg-[#F59E0B] text-white'
                      : 'bg-[#10B981] text-white'
                  }`}>
                    {factor.impact} Impact
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Disclaimer Box */}
        <div className="bg-yellow-50 border-2 border-yellow-200 rounded-lg p-6 mb-8">
          <div className="flex items-start">
            <div className="text-2xl mr-3">⚠️</div>
            <div>
              <h3 className="font-semibold text-[#111827] mb-2">Important Disclaimer</h3>
              <p className="text-[#6B7280]">
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

