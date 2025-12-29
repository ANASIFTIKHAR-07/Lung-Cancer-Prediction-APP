/**
 * Mock prediction algorithm for lung cancer risk assessment
 * This will be replaced with real API calls in the future
 */

/**
 * Generate mock prediction based on form data
 * @param {Object} formData - User input data
 * @returns {Object} Prediction results with risk level, confidence, and explanation
 */
export function generateMockPrediction(formData) {
  let riskScore = 0;

  // Age factor
  if (formData.age > 70) riskScore += 40;
  else if (formData.age > 60) riskScore += 30;
  else if (formData.age > 50) riskScore += 20;
  else if (formData.age > 40) riskScore += 10;

  // Smoking factor (highest weight)
  if (formData.smokingHistory === 'Current Smoker') riskScore += 40;
  else if (formData.smokingHistory === 'Former Smoker') riskScore += 20;

  // Family history
  if (formData.familyHistory) riskScore += 15;

  // Random variation (±5)
  riskScore += Math.floor(Math.random() * 10) - 5;
  riskScore = Math.max(0, Math.min(100, riskScore)); // Clamp between 0-100

  // Determine risk level
  let riskLevel, confidence;
  if (riskScore >= 60) {
    riskLevel = 'High';
    confidence = 80 + Math.floor(Math.random() * 15); // 80-95%
  } else if (riskScore >= 30) {
    riskLevel = 'Medium';
    confidence = 70 + Math.floor(Math.random() * 15); // 70-85%
  } else {
    riskLevel = 'Low';
    confidence = 75 + Math.floor(Math.random() * 20); // 75-95%
  }

  return {
    riskLevel,
    confidence,
    explanation: getExplanation(riskLevel),
    factors: getContributingFactors(formData),
    timestamp: new Date()
  };
}

/**
 * Get explanation text based on risk level
 * @param {string} riskLevel - Risk level (Low, Medium, High)
 * @returns {string} Explanation text
 */
function getExplanation(riskLevel) {
  const explanations = {
    Low: 'Based on the provided data, the model indicates a low risk of lung cancer. However, regular health check-ups are still recommended.',
    Medium: 'The analysis suggests moderate risk factors are present. We recommend consulting with a healthcare professional for further evaluation and lifestyle recommendations.',
    High: 'The model has detected significant risk factors for lung cancer. We strongly recommend immediate consultation with a healthcare professional for comprehensive screening and evaluation.'
  };
  return explanations[riskLevel];
}

/**
 * Get contributing factors based on form data
 * @param {Object} formData - User input data
 * @returns {Array} Array of contributing factors
 */
function getContributingFactors(formData) {
  const factors = [];

  if (formData.age > 60) {
    factors.push({ name: 'Age', impact: 'High' });
  } else if (formData.age > 50) {
    factors.push({ name: 'Age', impact: 'Medium' });
  }

  if (formData.smokingHistory === 'Current Smoker') {
    factors.push({ name: 'Smoking History', impact: 'High' });
  } else if (formData.smokingHistory === 'Former Smoker') {
    factors.push({ name: 'Smoking History', impact: 'Medium' });
  }

  if (formData.familyHistory) {
    factors.push({ name: 'Family History', impact: 'Medium' });
  }

  return factors;
}

/**
 * Mock API call with delay to simulate network request
 * @param {Object} formData - User input data
 * @returns {Promise<Object>} Prediction results
 */
export async function mockPredict(formData) {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  return generateMockPrediction(formData);
}

/**
 * Future API integration function (documented for ML teammate)
 * @param {Object} formData - User input data
 * @returns {Promise<Object>} Prediction results from API
 */
export async function realPredict(formData) {
  // Import config dynamically to avoid circular dependencies
  const { config } = await import('../config/env');
  
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
  
  try {
    const response = await fetch(config.api.fullUrl(), {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        sequence: formData.biologicalSequence,
        age: formData.age,
        smoking_status: formData.smokingHistory,
        gender: formData.gender,
        family_history: formData.familyHistory
      }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    
    // Validate response structure
    if (!data.risk_level || !data.confidence) {
      throw new Error('Invalid response format from API');
    }
    
    return data;
  } catch (error) {
    clearTimeout(timeoutId);
    
    if (error.name === 'AbortError') {
      throw new Error('Request timeout. Please try again.');
    }
    
    if (error.message) {
      throw error;
    }
    
    throw new Error('Network error. Please check your connection and try again.');
  }
}

