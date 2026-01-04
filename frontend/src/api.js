import axios from 'axios';
import { API_BASE_URL } from './config';

const API_URL = API_BASE_URL;

// Configure axios default settings
axios.defaults.withCredentials = true; // Still needed for CORS credential handling, though we use headers
axios.defaults.timeout = 60000; // 60 seconds timeout (Render Free Tier Cold Start)

// Add a request interceptor to include the JWT token
axios.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Authentication API
export const register = async (username, email, password) => {
    const response = await axios.post(`${API_URL}/auth/register`, { username, email, password });
    if (response.data.token) {
        localStorage.setItem('token', response.data.token);
    }
    return response.data;
};

export const login = async (username, password) => {
    const response = await axios.post(`${API_URL}/auth/login`, { username, password });
    if (response.data.token) {
        localStorage.setItem('token', response.data.token);
    }
    return response.data;
};

export const resetPassword = async (username, email, newPassword) => {
    const response = await axios.post(`${API_URL}/auth/reset-password`, { username, email, newPassword });
    return response.data;
};

export const logout = async () => {
    try {
        await axios.post(`${API_URL}/auth/logout`);
    } catch (e) {
        console.warn('Logout server call failed', e);
    } finally {
        localStorage.removeItem('token');
    }
    return { message: 'Logged out' };
};

export const checkAuth = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        return { authenticated: false };
    }

    try {
        const response = await axios.get(`${API_URL}/auth/check`);
        return response.data;
    } catch (err) {
        // If token is invalid/expired
        localStorage.removeItem('token');
        return { authenticated: false };
    }
};

export const getCurrentUser = async () => {
    const response = await axios.get(`${API_URL}/auth/me`);
    return response.data;
};

// Transaction API
export const getTransactions = async () => {
    const response = await axios.get(`${API_URL}/transactions`);
    return response.data;
};

export const addTransaction = async (transaction) => {
    // If transaction is FormData, axios will automatically set the correct Content-Type (multipart/form-data)
    // The interceptor will add the Authorization header
    const response = await axios.post(`${API_URL}/transactions`, transaction);
    return response.data;
};

export const deleteTransaction = async (id) => {
    const response = await axios.delete(`${API_URL}/transactions/${id}`);
    return response.data;
};
