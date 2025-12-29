/**
 * Environment Configuration
 * Centralized access to environment variables with defaults
 */

export const config = {
  api: {
    baseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
    endpoint: import.meta.env.VITE_API_ENDPOINT || '/api/predict',
    fullUrl: () => {
      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const endpoint = import.meta.env.VITE_API_ENDPOINT || '/api/predict';
      return `${baseUrl}${endpoint}`;
    }
  },
  env: import.meta.env.VITE_APP_ENV || import.meta.env.MODE || 'development',
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
  enableAnalytics: import.meta.env.VITE_ENABLE_ANALYTICS === 'true'
};

export default config;

