import { useNavigate } from 'react-router-dom';
import Button from './Button';
import { AnalysisIcon, SpeedIcon, SecurityIcon } from './Icons';

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
          <div className="bg-gradient-to-br from-[#1E40AF] via-[#3B82F6] to-[#60A5FA] rounded-2xl p-8 md:p-12 text-white shadow-large mb-8 relative overflow-hidden">
            {/* Subtle pattern overlay */}
            <div className="absolute inset-0 opacity-10">
              <div className="absolute inset-0" style={{
                backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
              }}></div>
            </div>
            <div className="relative z-10">
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4 tracking-tight">
                Lung Cancer Risk Prediction Tool
              </h1>
              <p className="text-xl md:text-2xl mb-6 opacity-95 font-medium">
                Early Detection Through Advanced Machine Learning
              </p>
              <p className="text-lg md:text-xl opacity-90 max-w-2xl mx-auto leading-relaxed">
                Our advanced machine learning model analyzes biological sequences and risk factors 
                to provide personalized risk assessments. This tool helps identify potential risk 
                factors early, enabling proactive healthcare decisions.
              </p>
            </div>
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
            <div className="bg-card-bg rounded-xl p-8 shadow-medium hover:shadow-large transition-all duration-300 border border-border/50 group">
              <div className="w-14 h-14 bg-primary-light/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-primary-light/20 transition-colors">
                <AnalysisIcon className="w-7 h-7 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-text-primary">Advanced Analysis</h3>
              <p className="text-text-secondary leading-relaxed">
                State-of-the-art ML models analyze biological data with precision
              </p>
            </div>
            <div className="bg-card-bg rounded-xl p-8 shadow-medium hover:shadow-large transition-all duration-300 border border-border/50 group">
              <div className="w-14 h-14 bg-secondary-light/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-secondary-light/20 transition-colors">
                <SpeedIcon className="w-7 h-7 text-secondary" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-text-primary">Quick Results</h3>
              <p className="text-text-secondary leading-relaxed">
                Get instant risk assessments in seconds
              </p>
            </div>
            <div className="bg-card-bg rounded-xl p-8 shadow-medium hover:shadow-large transition-all duration-300 border border-border/50 group">
              <div className="w-14 h-14 bg-accent/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-accent/20 transition-colors">
                <SecurityIcon className="w-7 h-7 text-accent" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-text-primary">Privacy First</h3>
              <p className="text-text-secondary leading-relaxed">
                Your data is processed securely and privately
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-card-bg border-t border-border py-8 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-text-secondary text-sm md:text-base leading-relaxed">
            <strong className="text-high-risk font-semibold">⚠️ For Research Purposes Only</strong> - 
            This tool is not a medical diagnosis. Please consult with a healthcare professional 
            for proper evaluation and medical advice.
          </p>
        </div>
      </footer>
    </div>
  );
}

