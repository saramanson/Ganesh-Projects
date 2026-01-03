import React, { useState } from 'react';

const Sidebar = ({ years, onSelectYear, onSelectMonth, selectedYear, selectedMonth }) => {
    const [expandedYears, setExpandedYears] = useState({});

    const toggleYear = (year) => {
        setExpandedYears(prev => ({
            ...prev,
            [year]: !prev[year]
        }));
        onSelectYear(year);
    };

    const months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ];

    return (
        <div className="sidebar">
            <h3>Navigation</h3>
            <ul className="year-list">
                <li
                    className={!selectedYear ? 'active' : ''}
                    onClick={() => onSelectYear(null)}
                    style={{ cursor: 'pointer', marginBottom: '10px' }}
                >
                    All Transactions
                </li>
                {years.map(year => (
                    <li key={year} className="year-item">
                        <div
                            className={`year-header ${selectedYear === year && !selectedMonth ? 'active' : ''}`}
                            onClick={() => toggleYear(year)}
                        >
                            {expandedYears[year] ? '▼' : '▶'} {year}
                        </div>
                        {expandedYears[year] && (
                            <ul className="month-list">
                                {months.map((month, index) => (
                                    <li
                                        key={month}
                                        className={`month-item ${selectedYear === year && selectedMonth === index + 1 ? 'active' : ''}`}
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            onSelectMonth(year, index + 1);
                                        }}
                                    >
                                        {month}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Sidebar;
