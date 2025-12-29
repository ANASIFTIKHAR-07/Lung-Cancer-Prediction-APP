import { useNavigate } from 'react-router-dom';
import Button from './Button';

/**
 * Landing/Home Page Component
 * Professional introduction with call-to-action
 */
export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col">
      {/* Hero Section */}
      <main className="flex-1 flex items-center justify-center px-4 py-12 md:py-20">
        <div className="max-w-4xl w-full text-center">
          {/* Hero Content */}
          <div className="bg-gradient-to-br from-[#2563EB] to-[#1D4ED8] rounded-2xl p-8 md:p-12 text-white shadow-2xl mb-8">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4">
              Lung Cancer Risk Prediction Tool
            </h1>
            <p className="text-xl md:text-2xl mb-6 opacity-95">
              Early Detection Through Advanced Machine Learning
            </p>
            <p className="text-lg md:text-xl opacity-90 max-w-2xl mx-auto leading-relaxed">
              Our advanced machine learning model analyzes biological sequences and risk factors 
              to provide personalized risk assessments. This tool helps identify potential risk 
              factors early, enabling proactive healthcare decisions.
            </p>
          </div>

          {/* CTA Button */}
          <div className="mb-12">
            <Button
              variant="primary"
              size="lg"
              onClick={() => navigate('/predict')}
              className="w-full md:w-auto min-w-[280px]"
            >
              Start Prediction
            </Button>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white rounded-lg p-6 shadow-md">
              <div className="text-3xl mb-3">🔬</div>
              <h3 className="text-xl font-semibold mb-2 text-[#111827]">Advanced Analysis</h3>
              <p className="text-[#6B7280]">
                State-of-the-art ML models analyze biological data
              </p>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-md">
              <div className="text-3xl mb-3">⚡</div>
              <h3 className="text-xl font-semibold mb-2 text-[#111827]">Quick Results</h3>
              <p className="text-[#6B7280]">
                Get instant risk assessments in seconds
              </p>
            </div>
            <div className="bg-white rounded-lg p-6 shadow-md">
              <div className="text-3xl mb-3">🛡️</div>
              <h3 className="text-xl font-semibold mb-2 text-[#111827]">Privacy First</h3>
              <p className="text-[#6B7280]">
                Your data is processed securely and privately
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-[#E5E7EB] py-6 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-[#6B7280] text-sm md:text-base">
            <strong className="text-[#EF4444]">⚠️ For Research Purposes Only</strong> - 
            This tool is not a medical diagnosis. Please consult with a healthcare professional 
            for proper evaluation and medical advice.
          </p>
        </div>
      </footer>
    </div>
  );
}

