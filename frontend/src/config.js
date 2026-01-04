// API Configuration for Web and Mobile
const getApiBaseUrl = () => {
    // Check if running in Capacitor (mobile app)
    if (window.Capacitor && window.Capacitor.isNativePlatform()) {
        // For mobile, use your computer's local IP or deployed backend URL
        // Replace this with your actual backend URL when deployed
        // For local development, use your computer's IP address (not localhost)
        return 'http://10.0.2.2:5000/api'; // Android emulator special IP for localhost
    }

    // 1. Priority: Environment Variable (injected during build)
    if (import.meta.env.VITE_API_URL) {
        return import.meta.env.VITE_API_URL;
    }

    // 2. Fallback for specific Render deployment (Legacy)
    if (window.location.hostname.includes('onrender.com')) {
        return 'https://expense-tracker-backend-hxst.onrender.com/api';
    }

    // 3. For web development (local), use relative path to leverage Vite Proxy
    if (import.meta.env.DEV) {
        return '/api';
    }

    // 4. Default fallback for built local preview or other scenarios
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
