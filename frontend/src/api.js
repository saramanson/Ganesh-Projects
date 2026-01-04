import axios from 'axios';
import { API_BASE_URL } from './config';

const API_URL = API_BASE_URL;

// Configure axios to send credentials (cookies) with requests
axios.defaults.withCredentials = true;
axios.defaults.timeout = 5000; // 5 seconds timeout

// Authentication API
export const register = async (username, email, password) => {
    const response = await axios.post(`${API_URL}/auth/register`, { username, email, password });
    return response.data;
};

export const login = async (username, password) => {
    const response = await axios.post(`${API_URL}/auth/login`, { username, password });
    return response.data;
};

export const resetPassword = async (username, email, newPassword) => {
    const response = await axios.post(`${API_URL}/auth/reset-password`, { username, email, newPassword });
    return response.data;
};

export const logout = async () => {
    const response = await axios.post(`${API_URL}/auth/logout`);
    return response.data;
};

export const checkAuth = async () => {
    const response = await axios.get(`${API_URL}/auth/check`);
    return response.data;
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
    // We explicitly set withCredentials to ensure cookies are sent
    const response = await axios.post(`${API_URL}/transactions`, transaction, {
        withCredentials: true
    });
    return response.data;
};

export const deleteTransaction = async (id) => {
    const response = await axios.delete(`${API_URL}/transactions/${id}`);
    return response.data;
};
