import { createContext, useContext, useState } from 'react';

const PredictionContext = createContext();

export function PredictionProvider({ children }) {
  const [formData, setFormData] = useState({
    biologicalSequence: '',
    age: 50,
    smokingHistory: '',
    gender: '',
    familyHistory: false
  });

  const [results, setResults] = useState(null);

  const updateFormData = (newData) => {
    setFormData(prev => ({ ...prev, ...newData }));
  };

  const resetForm = () => {
    setFormData({
      biologicalSequence: '',
      age: 50,
      smokingHistory: '',
      gender: '',
      familyHistory: false
    });
  };

  const resetResults = () => {
    setResults(null);
  };

  return (
    <PredictionContext.Provider
      value={{
        formData,
        results,
        updateFormData,
        setResults,
        resetForm,
        resetResults
      }}
    >
      {children}
    </PredictionContext.Provider>
  );
}

export function usePrediction() {
  const context = useContext(PredictionContext);
  if (!context) {
    throw new Error('usePrediction must be used within PredictionProvider');
  }
  return context;
}

