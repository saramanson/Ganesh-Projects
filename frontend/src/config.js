// API Configuration for Web and Mobile
const getApiBaseUrl = () => {
    // Check if running in Capacitor (mobile app)
    if (window.Capacitor && window.Capacitor.isNativePlatform()) {
        // For mobile, use your computer's local IP or deployed backend URL
        // Replace this with your actual backend URL when deployed
        // For local development, use your computer's IP address (not localhost)
        // Example: return 'http://192.168.1.100:5000/api';
        return 'http://10.0.2.2:5000/api'; // Android emulator special IP for localhost
    }

    // Check for production environment variable
    if (import.meta.env.VITE_API_URL) {
        return import.meta.env.VITE_API_URL;
    }

    // Fallback for specific Render deployment
    if (window.location.hostname.includes('onrender.com')) {
        return 'https://expense-tracker-backend-hxst.onrender.com/api';
    }

    // For web development (local), use relative path to leverage Vite Proxy
    // This avoids CORS/Cookie issues by treating backend as same-origin
    if (import.meta.env.DEV) {
        return '/api';
    }

    // Default fallback for built local preview or other scenarios
    return `http://${window.location.hostname}:5000/api`;
};

export const API_BASE_URL = getApiBaseUrl();

// Helper to check if running on mobile
export const isMobile = () => {
    return window.Capacitor && window.Capacitor.isNativePlatform();
};

// Helper to get platform
export const getPlatform = () => {
    if (!window.Capacitor) return 'web';
    return window.Capacitor.getPlatform();
};
