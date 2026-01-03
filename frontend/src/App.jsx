import React, { useState, useEffect } from 'react';
import { getTransactions, addTransaction, deleteTransaction, checkAuth, logout } from './api';
import { API_BASE_URL } from './config';
import TransactionList from './components/TransactionList';
import AddTransaction from './components/AddTransaction';
import Sidebar from './components/Sidebar';
import ExpenseChart from './components/ExpenseChart';
import Groups from './components/Groups';
import Login from './components/Login';
import Register from './components/Register';
import './index.css';

function App() {
  const [transactions, setTransactions] = useState([]);
  const [selectedYear, setSelectedYear] = useState(null);
  const [selectedMonth, setSelectedMonth] = useState(null);
  const [activeView, setActiveView] = useState('tracker'); // 'tracker' or 'groups'
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [authView, setAuthView] = useState('login'); // 'login' or 'register'
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthentication();
  }, []);

  const checkAuthentication = async () => {
    try {
      const response = await checkAuth();
      if (response.authenticated) {
        setIsAuthenticated(true);
        setCurrentUser(response.user);
        fetchTransactions();
      }
    } catch (error) {
      console.error('Auth check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTransactions = async () => {
    try {
      const data = await getTransactions();
      setTransactions(data);
    } catch (error) {
      console.error("Error fetching transactions:", error);
    }
  };

  const handleAddTransaction = async (transaction) => {
    try {
      const newTransaction = await addTransaction(transaction);
      setTransactions([newTransaction, ...transactions]);

      // Auto-switch view to the transaction's year
      const newYear = newTransaction.date.split('-')[0];
      if (newYear !== selectedYear) {
        setSelectedYear(newYear);
        setSelectedMonth(null);
      }
    } catch (error) {
      console.error("Error adding transaction:", error);
      alert("Failed to add transaction: " + (error.response?.data?.error || error.message));
    }
  };

  const handleDeleteTransaction = async (id) => {
    try {
      await deleteTransaction(id);
      setTransactions(transactions.filter(t => t.id !== id));
    } catch (error) {
      console.error("Error deleting transaction:", error);
    }
  };

  // Extract unique years
  const years = [...new Set(transactions.map(t => t.date.split('-')[0]))].sort((a, b) => b - a);

  // Filter transactions
  const filteredTransactions = transactions.filter(t => {
    if (!selectedYear) return true;
    const date = new Date(t.date);
    const yearMatch = date.getFullYear().toString() === selectedYear;
    if (!selectedMonth) return yearMatch;
    const monthMatch = date.getMonth() + 1 === selectedMonth;
    return yearMatch && monthMatch;
  });

  const amounts = filteredTransactions.map(transaction => transaction.type === 'credit' ? transaction.amount : -transaction.amount);
  const total = amounts.reduce((acc, item) => acc + item, 0).toFixed(2);
  const income = amounts
    .filter(item => item > 0)
    .reduce((acc, item) => acc + item, 0)
    .toFixed(2);
  const expense = (
    amounts.filter(item => item < 0).reduce((acc, item) => acc + item, 0) *
    -1
  ).toFixed(2);

  const handleSelectYear = (year) => {
    setSelectedYear(year);
    setSelectedMonth(null); // Reset month when year changes
  };

  const handleSelectMonth = (year, month) => {
    setSelectedYear(year);
    setSelectedMonth(month);
  };

  const handleLoginSuccess = (user) => {
    setIsAuthenticated(true);
    setCurrentUser(user);
    fetchTransactions();
  };

  const handleRegisterSuccess = (user) => {
    setIsAuthenticated(true);
    setCurrentUser(user);
    fetchTransactions();
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      setIsAuthenticated(false);
      setCurrentUser(null);
      setTransactions([]);
    }
  };

  // Show loading state
  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        fontSize: '1.5rem',
        color: '#667eea'
      }}>
        Loading...
      </div>
    );
  }

  // Show authentication views if not authenticated
  if (!isAuthenticated) {
    if (authView === 'login') {
      return (
        <Login
          onLoginSuccess={handleLoginSuccess}
          onSwitchToRegister={() => setAuthView('register')}
        />
      );
    } else {
      return (
        <Register
          onRegisterSuccess={handleRegisterSuccess}
          onSwitchToLogin={() => setAuthView('login')}
        />
      );
    }
  }

  if (activeView === 'groups') {
    return (
      <div>
        <div className="main-nav">
          <button
            className={`nav-btn ${activeView === 'tracker' ? 'active' : ''}`}
            onClick={() => setActiveView('tracker')}
          >
            💰 Expense Tracker
          </button>
          <button
            className={`nav-btn ${activeView === 'groups' ? 'active' : ''}`}
            onClick={() => setActiveView('groups')}
          >
            👥 Split Expenses
          </button>
          <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '15px', color: 'white' }}>
            <span>👤 {currentUser?.username}</span>
            <button onClick={handleLogout} className="nav-btn" style={{ flex: 'none', padding: '10px 20px' }}>
              Logout
            </button>
          </div>
        </div>
        <Groups currentUser={currentUser} />
      </div>
    );
  }

  return (
    <div>
      <div className="main-nav">
        <button
          className={`nav-btn ${activeView === 'tracker' ? 'active' : ''}`}
          onClick={() => setActiveView('tracker')}
          title="Expense Tracker"
        >
          💰 Tracker
        </button>
        <button
          className={`nav-btn ${activeView === 'groups' ? 'active' : ''}`}
          onClick={() => setActiveView('groups')}
          title="Split Expenses"
        >
          👥 Split
        </button>
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '15px', color: 'white' }}>
          <span>👤 {currentUser?.username}</span>
          <button onClick={handleLogout} className="nav-btn" style={{ flex: 'none', padding: '10px 20px' }}>
            Logout
          </button>
        </div>
      </div>

      <div className="app-container">
        <Sidebar
          years={years}
          onSelectYear={handleSelectYear}
          onSelectMonth={handleSelectMonth}
          selectedYear={selectedYear}
          selectedMonth={selectedMonth}
        />

        <div className="main-content">
          <div className="header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h1>Expense Tracker</h1>
            {selectedYear && (
              <button
                onClick={() => {
                  const params = new URLSearchParams();
                  params.append('year', selectedYear);
                  if (selectedMonth) params.append('month', selectedMonth);
                  window.open(`${API_BASE_URL}/transactions/export?${params.toString()}`, '_blank');
                }}
                style={{
                  padding: '8px 16px',
                  backgroundColor: '#4a5568',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                ⬇️ Download CSV
              </button>
            )}
          </div>

          <div className="balance-card">
            <h4>Your Balance {selectedYear ? `(${selectedYear}${selectedMonth ? `/${selectedMonth}` : ''})` : ''}</h4>
            <h1 className="balance-amount">${total}</h1>
            <div className="inc-exp-container">
              <div>
                <h4>Income</h4>
                <p className="money plus">+${income}</p>
              </div>
              <div>
                <h4>Expense</h4>
                <p className="money minus">-${expense}</p>
              </div>
            </div>
          </div>

          <AddTransaction onAdd={handleAddTransaction} />
          <ExpenseChart transactions={filteredTransactions} />
          <TransactionList transactions={filteredTransactions} onDelete={handleDeleteTransaction} />
        </div>
      </div>
    </div>
  );
}

export default App;

