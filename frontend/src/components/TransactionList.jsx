import React from 'react';

const TransactionList = ({ transactions, onDelete }) => {
    return (
        <>
            <h3>History</h3>
            <ul className="transaction-list">
                {transactions.map(transaction => (
                    <li key={transaction.id} className={`transaction-item ${transaction.type}`}>
                        <div>
                            {transaction.description} <span style={{ fontSize: '0.8rem', color: '#888', marginLeft: '5px' }}>({transaction.category})</span>
                            <div style={{ fontSize: '0.8rem', color: '#666' }}>
                                {transaction.date}
                                {transaction.image && (
                                    <span style={{ marginLeft: '10px' }}>
                                        <a href={`http://localhost:5000/api/storage/${transaction.image}`} target="_blank" rel="noopener noreferrer" style={{ color: '#007bff', textDecoration: 'none' }}>
                                            View Bill
                                        </a>
                                    </span>
                                )}
                            </div>
                        </div>
                        <span>{transaction.type === 'debit' ? '-' : '+'}${Math.abs(transaction.amount).toFixed(2)}</span>
                        <button onClick={() => onDelete(transaction.id)} className="delete-btn">x</button>
                    </li>
                ))}
            </ul>
        </>
    );
};

export default TransactionList;
