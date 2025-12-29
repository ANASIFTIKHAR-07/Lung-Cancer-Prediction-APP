# Lung Cancer Risk Prediction Tool

A full-stack web application for lung cancer risk prediction using machine learning. The application provides a professional interface for users to input biological sequence data and risk factors to receive personalized risk assessments.

## 🎯 Project Overview

This is a research tool that combines a modern React frontend with a FastAPI backend to deliver lung cancer risk predictions. The application emphasizes that it is **not a medical diagnosis** and is designed for research purposes only.

## 🏗️ Project Structure

```
Cancer App/
├── Frontend/          # React application (Vite + React Router)
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── context/       # State management
│   │   ├── utils/         # Utility functions
│   │   └── config/        # Configuration
│   └── README.md          # Frontend documentation
│
└── Backend/           # FastAPI backend (to be implemented)
    └── README.md          # Backend documentation
```

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 19.2.0
- **Build Tool**: Vite 7.2.4
- **Routing**: React Router DOM v7.11.0
- **Styling**: Tailwind CSS v3.4.19
- **State Management**: React Context API

### Backend (Planned)
- **Framework**: FastAPI
- **Language**: Python
- **ML Model**: (To be integrated)

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18 or higher) - for Frontend
- **Python** (3.9+) - for Backend (when implemented)
- **npm** (v9 or higher)

### Frontend Setup

1. Navigate to the Frontend directory:
   ```bash
   cd Frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment file:
   ```bash
   cp .env.example .env
   ```

4. Start development server:
   ```bash
   npm run dev
   ```

5. Open `http://localhost:5173` in your browser

For detailed Frontend documentation, see [Frontend/README.md](./Frontend/README.md)

### Backend Setup

*Backend implementation coming soon*

## 📄 Application Features

### Current Features (Frontend)
- ✅ Professional landing page with hero section
- ✅ Comprehensive prediction form with validation
- ✅ Results page with risk level visualization
- ✅ Mock prediction algorithm (ready for ML integration)
- ✅ Production-grade error handling
- ✅ Input sanitization and XSS protection
- ✅ Responsive mobile-first design
- ✅ Code splitting and lazy loading

### Planned Features (Backend)
- 🔄 FastAPI REST API
- 🔄 ML model integration
- 🔄 Database for prediction history
- 🔄 Authentication (if needed)
- 🔄 API documentation (Swagger/OpenAPI)

## 🔌 API Integration

The frontend is designed to integrate with a FastAPI backend. The integration points are documented in:

- **Frontend**: See [Frontend/README.md](./Frontend/README.md#-future-fastapi-integration)
- **Backend**: (Documentation coming soon)

### Expected API Endpoint

```
POST /api/predict
Content-Type: application/json

{
  "sequence": "ATCGATCG...",
  "age": 65,
  "smoking_status": "Current Smoker",
  "gender": "Male",
  "family_history": true
}
```

### Expected Response

```json
{
  "risk_level": "High" | "Medium" | "Low",
  "confidence": 0.85,
  "explanation": "Detailed explanation...",
  "contributing_factors": [
    {
      "name": "Age",
      "impact": "High"
    }
  ]
}
```

## 🧪 Development

### Frontend Development

```bash
cd Frontend
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

### Backend Development

*Commands coming soon*

## 📦 Project Status

- [x] Frontend application complete
- [x] Mock prediction algorithm
- [x] Production-ready features (error handling, sanitization, etc.)
- [x] Environment configuration
- [ ] Backend API implementation
- [ ] ML model integration
- [ ] Database setup
- [ ] Testing suite

## 🛡️ Security & Privacy

- ✅ Input sanitization (XSS protection)
- ✅ Error boundary for crash protection
- ✅ Environment variable configuration
- ✅ Security headers in HTML
- ⚠️ **Important**: This tool is for research purposes only
- ⚠️ **Not a medical diagnosis** - Always consult healthcare professionals

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Documentation

- **Frontend**: [Frontend/README.md](./Frontend/README.md) - Complete frontend documentation
- **Backend**: (Coming soon)

## ⚠️ Important Disclaimer

**This tool is for research purposes only and is not a medical diagnosis.** 

Users should always consult with qualified healthcare professionals for proper medical evaluation and advice. This application is designed for research and educational purposes.

## 📄 License

This project is for research and educational purposes.

## 👥 Team

*Add team members here*
Muhammad Anas Iftikhar (Lead Developer + Ml)
Muhammad Nadeem (Machine learning lead)
---

**Built with ❤️ for early cancer detection research**

