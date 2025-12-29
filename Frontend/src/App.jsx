import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { PredictionProvider } from './context/PredictionContext';
import Landing from './components/Landing';
import PredictionForm from './components/PredictionForm';
import Results from './components/Results';
import './App.css';

function App() {
  return (
    <PredictionProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/predict" element={<PredictionForm />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </Router>
    </PredictionProvider>
  );
}

export default App;
