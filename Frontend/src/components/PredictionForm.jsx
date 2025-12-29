import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { usePrediction } from '../context/PredictionContext';
import { mockPredict } from '../utils/mockPredict';
import Button from './Button';

/**
 * Prediction Form Page Component
 * Collects biological data and risk factors for prediction
 */
export default function PredictionForm() {
  const navigate = useNavigate();
  const { formData, updateFormData, setResults } = usePrediction();
  
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  // Validation rules
  const validate = () => {
    const newErrors = {};

    if (!formData.biologicalSequence.trim()) {
      newErrors.biologicalSequence = 'Biological sequence is required';
    } else if (formData.biologicalSequence.trim().length < 10) {
      newErrors.biologicalSequence = 'Sequence must be at least 10 characters';
    }

    if (!formData.age || formData.age < 18 || formData.age > 100) {
      if (!formData.age) {
        newErrors.age = 'Age is required';
      } else if (formData.age < 18 || formData.age > 100) {
        newErrors.age = 'Age must be between 18 and 100';
      }
    }

    if (!formData.smokingHistory) {
      newErrors.smokingHistory = 'Smoking history is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (field, value) => {
    updateFormData({ [field]: value });
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validate()) {
      return;
    }

    setIsLoading(true);
    
    try {
      const prediction = await mockPredict(formData);
      setResults(prediction);
      navigate('/results');
    } catch (error) {
      console.error('Prediction error:', error);
      alert('An error occurred during prediction. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const isFormValid = formData.biologicalSequence.trim().length >= 10 &&
                     formData.age >= 18 && formData.age <= 100 &&
                     formData.smokingHistory;

  return (
    <div className="min-h-screen bg-[#F9FAFB] py-8 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-[#111827] mb-2">
            Lung Cancer Risk Assessment
          </h1>
          <p className="text-[#6B7280] text-lg">
            Please provide the following information for analysis
          </p>
        </div>

        {/* Form Card */}
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-6 md:p-8">
          {/* Biological Sequence */}
          <div className="mb-6">
            <label htmlFor="biologicalSequence" className="block text-sm font-semibold text-[#111827] mb-2">
              Biological Sequence <span className="text-[#EF4444]">*</span>
            </label>
            <textarea
              id="biologicalSequence"
              rows="5"
              value={formData.biologicalSequence}
              onChange={(e) => handleChange('biologicalSequence', e.target.value)}
              placeholder="Enter biological sequence data (DNA/RNA/Protein sequence)"
              className={`w-full px-4 py-3 border-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB] transition-all ${
                errors.biologicalSequence 
                  ? 'border-[#EF4444]' 
                  : 'border-[#E5E7EB] focus:border-[#2563EB]'
              }`}
              disabled={isLoading}
            />
            <div className="flex justify-between items-center mt-1">
              <span className="text-sm text-[#6B7280]">
                {formData.biologicalSequence.length} characters
              </span>
              {errors.biologicalSequence && (
                <span className="text-sm text-[#EF4444]">{errors.biologicalSequence}</span>
              )}
            </div>
          </div>

          {/* Age */}
          <div className="mb-6">
            <label htmlFor="age" className="block text-sm font-semibold text-[#111827] mb-2">
              Age <span className="text-[#EF4444]">*</span>
            </label>
            <input
              type="number"
              id="age"
              min="18"
              max="100"
              value={formData.age || ''}
              onChange={(e) => handleChange('age', parseInt(e.target.value) || '')}
              className={`w-full h-12 px-4 border-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB] transition-all ${
                errors.age 
                  ? 'border-[#EF4444]' 
                  : 'border-[#E5E7EB] focus:border-[#2563EB]'
              }`}
              disabled={isLoading}
            />
            {errors.age && (
              <span className="text-sm text-[#EF4444] mt-1 block">{errors.age}</span>
            )}
          </div>

          {/* Smoking History */}
          <div className="mb-6">
            <label htmlFor="smokingHistory" className="block text-sm font-semibold text-[#111827] mb-2">
              Smoking History <span className="text-[#EF4444]">*</span>
            </label>
            <select
              id="smokingHistory"
              value={formData.smokingHistory}
              onChange={(e) => handleChange('smokingHistory', e.target.value)}
              className={`w-full h-12 px-4 border-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB] transition-all ${
                errors.smokingHistory 
                  ? 'border-[#EF4444]' 
                  : 'border-[#E5E7EB] focus:border-[#2563EB]'
              }`}
              disabled={isLoading}
            >
              <option value="">Select smoking history</option>
              <option value="Never">Never</option>
              <option value="Former Smoker">Former Smoker</option>
              <option value="Current Smoker">Current Smoker</option>
            </select>
            {errors.smokingHistory && (
              <span className="text-sm text-[#EF4444] mt-1 block">{errors.smokingHistory}</span>
            )}
          </div>

          {/* Gender */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-[#111827] mb-2">
              Gender (Optional)
            </label>
            <div className="flex gap-6">
              {['Male', 'Female', 'Other'].map((gender) => (
                <label key={gender} className="flex items-center cursor-pointer">
                  <input
                    type="radio"
                    name="gender"
                    value={gender}
                    checked={formData.gender === gender}
                    onChange={(e) => handleChange('gender', e.target.value)}
                    className="w-4 h-4 text-[#2563EB] focus:ring-[#2563EB]"
                    disabled={isLoading}
                  />
                  <span className="ml-2 text-[#111827]">{gender}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Family History */}
          <div className="mb-8">
            <label className="flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={formData.familyHistory}
                onChange={(e) => handleChange('familyHistory', e.target.checked)}
                className="w-5 h-5 text-[#2563EB] rounded focus:ring-[#2563EB]"
                disabled={isLoading}
              />
              <span className="ml-2 text-[#111827]">
                Family history of lung cancer (Optional)
              </span>
            </label>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/')}
              disabled={isLoading}
              className="flex-1"
            >
              Back
            </Button>
            <Button
              type="submit"
              variant="primary"
              disabled={!isFormValid || isLoading}
              className="flex-1"
            >
              {isLoading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing...
                </span>
              ) : (
                'Predict'
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

