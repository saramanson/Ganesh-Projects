import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const ExpenseChart = ({ transactions }) => {
    // Filter for expenses (debit) only
    const expenses = transactions.filter(t => t.type === 'debit');

    // Group by category
    const expensesByCategory = expenses.reduce((acc, t) => {
        const category = t.category || 'Uncategorized';
        acc[category] = (acc[category] || 0) + t.amount;
        return acc;
    }, {});

    const labels = Object.keys(expensesByCategory);
    const data = Object.values(expensesByCategory);

    const chartData = {
        labels,
        datasets: [
            {
                label: 'Expenses by Category',
                data: data,
                backgroundColor: 'rgba(239, 68, 68, 0.5)', // Red color for expenses
                borderColor: 'rgba(239, 68, 68, 1)',
                borderWidth: 1,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Expense Breakdown',
            },
        },
    };

    if (expenses.length === 0) {
        return null;
    }

    return (
        <div style={{ marginBottom: '2rem', backgroundColor: 'white', padding: '1rem', borderRadius: '0.5rem', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}>
            <Bar options={options} data={chartData} />
        </div>
    );
};

export default ExpenseChart;
