import React, { useState } from 'react';
import { resetPassword } from '../api';
import './Auth.css';

function ResetPassword({ onResetSuccess, onSwitchToLogin }) {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');
        setLoading(true);

        try {
            await resetPassword(username, email, newPassword);
            setMessage('Password reset successful! You can now login.');
            setTimeout(() => {
                onResetSuccess();
            }, 2000);
        } catch (err) {
            console.error('Reset error:', err);
            setError(err.response?.data?.error || 'Failed to reset password. information may be incorrect.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h1>💰 Expense Tracker</h1>
                    <h2>Reset Password</h2>
                    <p>Enter your details to create a new password</p>
                </div>

                <form onSubmit={handleSubmit} className="auth-form">
                    {error && <div className="error-message">{error}</div>}
                    {message && <div className="success-message" style={{ color: 'green', marginBottom: '15px' }}>{message}</div>}

                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter your username"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Enter your email"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="newPassword">New Password</label>
                        <input
                            type="password"
                            id="newPassword"
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
                            placeholder="Create new password (min 6 chars)"
                            required
                        />
                    </div>

                    <button type="submit" className="auth-button" disabled={loading}>
                        {loading ? 'Processing...' : 'Reset Password'}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>
                        Remember your password?{' '}
                        <button onClick={onSwitchToLogin} className="link-button">
                            Sign in
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default ResetPassword;
