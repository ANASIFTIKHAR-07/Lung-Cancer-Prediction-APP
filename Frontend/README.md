# Lung Cancer Risk Prediction Tool

A professional React web application for lung cancer risk prediction using machine learning. This is a prototype application that currently uses mock data for predictions, designed for future integration with a FastAPI backend.

## 🎯 Project Overview

This application provides a clean, professional interface for users to input biological sequence data and risk factors to receive a personalized lung cancer risk assessment. The tool is designed for research purposes and emphasizes that it is not a medical diagnosis.

## 🛠️ Tech Stack

- **Framework**: React 19.2.0 (Vite)
- **Routing**: React Router DOM v7.11.0
- **Styling**: Tailwind CSS v4.1.18
- **Build Tool**: Vite 7.2.4

## 📁 Project Structure

```
Frontend/
├── src/
│   ├── components/
│   │   ├── Button.jsx           # Reusable button component
│   │   ├── Landing.jsx          # Home/landing page
│   │   ├── PredictionForm.jsx  # Input form page
│   │   ├── Results.jsx          # Results display page
│   │   └── RiskBadge.jsx        # Risk level badge component
│   ├── context/
│   │   └── PredictionContext.jsx # Global state management
│   ├── utils/
│   │   └── mockPredict.js       # Mock prediction algorithm
│   ├── App.jsx                  # Main app with routing
│   ├── App.css                  # Global styles and animations
│   ├── index.css                # Tailwind CSS configuration
│   └── main.jsx                 # Application entry point
├── public/
├── index.html
├── package.json
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites

- Node.js (v18 or higher)
- npm (v9 or higher)

### Installation

1. Navigate to the Frontend directory:
   ```bash
   cd Frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to the URL shown in the terminal (typically `http://localhost:5173`)

### Build for Production

```bash
npm run build
```

The production build will be created in the `dist` directory.

## 📄 Application Pages

### 1. Landing Page (`/`)

- Professional hero section with gradient background
- Clear call-to-action button
- Feature highlights
- Footer with medical disclaimer

### 2. Prediction Form (`/predict`)

- **Biological Sequence**: Large textarea for DNA/RNA/Protein sequences (required, min 10 characters)
- **Age**: Number input (required, 18-100)
- **Smoking History**: Dropdown select (required)
  - Options: Never, Former Smoker, Current Smoker
- **Gender**: Radio buttons (optional)
  - Options: Male, Female, Other
- **Family History**: Checkbox (optional)
- Real-time form validation
- Loading state during prediction

### 3. Results Page (`/results`)

- **Risk Level Badge**: Large, color-coded display
  - Low Risk (Green)
  - Medium Risk (Orange)
  - High Risk (Red)
- **Confidence Score**: Visual progress bar with percentage
- **Explanation**: Detailed analysis explanation
- **Contributing Factors**: List of factors that influenced the prediction
- **Disclaimer**: Medical disclaimer box
- Action buttons to try another prediction or return home

## 🎨 Design System

### Color Palette

- **Primary Blue**: `#2563EB`
- **Success Green**: `#10B981`
- **Low Risk**: `#10B981` (Green)
- **Medium Risk**: `#F59E0B` (Orange)
- **High Risk**: `#EF4444` (Red)
- **Background**: `#F9FAFB` (Light Gray)
- **Card Background**: `#FFFFFF` (White)
- **Text Primary**: `#111827` (Dark Gray)
- **Text Secondary**: `#6B7280` (Medium Gray)

### Typography

- **Headers (H1)**: 32-40px, font-bold
- **Headers (H2)**: 24-28px, font-semibold
- **Body**: 16-18px, font-normal
- **Buttons**: 18px, font-semibold
- **Font Family**: System default (sans-serif)

## 🔮 Mock Prediction Algorithm

The current mock prediction algorithm generates results based on the following factors:

1. **Age Factor**:
   - Age > 70: +40 points
   - Age > 60: +30 points
   - Age > 50: +20 points
   - Age > 40: +10 points

2. **Smoking History** (Highest Weight):
   - Current Smoker: +40 points
   - Former Smoker: +20 points

3. **Family History**:
   - Family history present: +15 points

4. **Random Variation**: ±5 points

### Risk Level Determination

- **High Risk** (≥60 points): 80-95% confidence
- **Medium Risk** (30-59 points): 70-85% confidence
- **Low Risk** (<30 points): 75-95% confidence

## ⚙️ Environment Variables

### Setup

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your values:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   VITE_API_ENDPOINT=/api/predict
   VITE_APP_ENV=development
   ```

### Important Notes

- **`.env.example`** = Template (safe to commit to Git)
- **`.env`** = Your actual config (NOT in Git, protected by `.gitignore`)
- **Frontend env vars are public** - URLs are baked into the bundle at build time
- **Never put secrets** (API keys, tokens) in frontend `.env` files
- **API URLs are fine** - They're discoverable in browser Network tab anyway

## 🔌 Future FastAPI Integration

### API Endpoint Structure

The application is designed to easily integrate with a FastAPI backend. The integration point is in `src/utils/mockPredict.js`.

#### Current Implementation (Mock)

```javascript
export async function mockPredict(formData) {
  await new Promise(resolve => setTimeout(resolve, 1000));
  return generateMockPrediction(formData);
}
```

#### Future Implementation (Real API)

```javascript
export async function realPredict(formData) {
  const response = await fetch('http://localhost:8000/api/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sequence: formData.biologicalSequence,
      age: formData.age,
      smoking_status: formData.smokingHistory,
      gender: formData.gender,
      family_history: formData.familyHistory
    })
  });

  if (!response.ok) {
    throw new Error('Prediction failed');
  }

  return await response.json();
}
```

### Expected API Response Format

The FastAPI backend should return a JSON response in the following format:

```json
{
  "risk_level": "High" | "Medium" | "Low",
  "confidence": 0.85,
  "explanation": "Detailed explanation text...",
  "contributing_factors": [
    {
      "name": "Age",
      "impact": "High"
    },
    {
      "name": "Smoking History",
      "impact": "High"
    }
  ]
}
```

### Integration Steps

1. Update `src/utils/mockPredict.js` to use the real API endpoint
2. Replace `mockPredict` calls with `realPredict` in `src/components/PredictionForm.jsx`
3. Add error handling for network failures
4. Update CORS settings on the FastAPI backend to allow requests from the frontend
5. Consider adding environment variables for API URL configuration

## ✨ Features

- ✅ Clean, professional medical-themed UI
- ✅ Responsive design (mobile-first)
- ✅ Real-time form validation
- ✅ Loading states and smooth transitions
- ✅ Color-coded risk level display
- ✅ Detailed explanation and contributing factors
- ✅ Navigation protection (prevents direct access to results)
- ✅ Accessibility features (semantic HTML, ARIA labels, keyboard navigation)
- ✅ Error handling
- ✅ Medical disclaimers

## 🧪 Testing Checklist

Before deployment, ensure:

- [x] All three pages render correctly
- [x] Navigation between pages works
- [x] Form validation works for all fields
- [x] Mock prediction generates varied results
- [x] Results display correctly for all risk levels
- [x] Mobile responsive on all pages
- [x] All buttons and links work
- [x] Loading states appear correctly
- [x] Error states display properly
- [x] Can complete full flow multiple times with different inputs

## 📝 Code Quality Standards

- Functional components with React hooks
- Proper component separation and reusability
- Meaningful variable and function names
- Comments for complex logic
- Consistent code formatting
- Small, focused components (< 200 lines)

## ⚠️ Important Disclaimer

**This tool is for research purposes only and is not a medical diagnosis.** Users should always consult with qualified healthcare professionals for proper medical evaluation and advice.

## 📄 License

This project is for research and educational purposes.

## 🚀 Production Deployment

### Quick Steps

1. **Build for production:**
   ```bash
   npm run build
   ```

2. **Set environment variables** (create `.env.production`):
   ```env
   VITE_API_BASE_URL=https://api.yourdomain.com
   VITE_API_ENDPOINT=/api/predict
   VITE_APP_ENV=production
   ```

3. **Deploy the `dist` folder** to your hosting service

### Production Features

- ✅ Error Boundary (catches crashes)
- ✅ Input sanitization (XSS protection)
- ✅ Code splitting (lazy-loaded routes)
- ✅ SEO meta tags
- ✅ Security headers
- ✅ User-friendly error messages

### Pre-Deployment Checklist

- [ ] Test production build locally: `npm run preview`
- [ ] Set production API URL in `.env.production`
- [ ] Enable HTTPS
- [ ] Test error handling
- [ ] Verify mobile responsiveness
- [ ] Test on multiple browsers

## 👥 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Future Enhancements

- [ ] Add TypeScript for type safety
- [ ] Implement unit tests
- [ ] Add E2E tests
- [ ] Add internationalization (i18n)
- [ ] Implement user authentication
- [ ] Add prediction history
- [ ] Export results as PDF
- [ ] Add more detailed risk factor analysis

---

**Built with ❤️ for early cancer detection research**
