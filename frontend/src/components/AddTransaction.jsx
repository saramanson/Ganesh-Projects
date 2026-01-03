import React, { useState } from 'react';

const AddTransaction = ({ onAdd }) => {
    const [description, setDescription] = useState('');
    const [amount, setAmount] = useState('');
    const [type, setType] = useState('debit');
    const [date, setDate] = useState(new Date().toLocaleDateString('en-CA'));
    const [category, setCategory] = useState('Grocery');
    const [image, setImage] = useState(null);

    const categories = [
        'Grocery', 'Gas', 'Clothing', 'Medicine', 'Services',
        'internet', 'water bill', 'Electricity', 'Petrol',
        'Insurance', 'Tax', 'Sports', 'Electronics', 'others'
    ];

    const onSubmit = (e) => {
        e.preventDefault();

        if (!description || !amount || !date) {
            alert('Please add a description, amount, and date');
            return;
        }

        const formData = new FormData();
        formData.append('description', description);
        const cleanAmount = amount.toString().replace(/[$,]/g, '');
        formData.append('amount', cleanAmount);
        formData.append('type', type);
        formData.append('date', date);
        formData.append('category', category);
        if (image) {
            formData.append('image', image);
        }

        onAdd(formData);

        if (onAdd) { // Ensure onAdd exists
            setDescription('');
            setAmount('');
            setType('debit');
            // Reset to today
            setDate(new Date().toLocaleDateString('en-CA'));
            setCategory('Grocery');
            setImage(null);
        }
        // Reset file input manually if needed, but state reset handles logic
        document.getElementById('imageInput').value = "";
    };

    return (
        <>
            <h3>Add new transaction</h3>
            <form onSubmit={onSubmit}>
                <div className="form-control">
                    <label htmlFor="description">Description</label>
                    <input
                        type="text"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        placeholder="Enter description..."
                    />
                </div>
                <div className="form-control">
                    <label htmlFor="amount">Amount</label>
                    <input
                        type="number"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                        placeholder="Enter amount..."
                    />
                </div>
                <div className="form-control">
                    <label htmlFor="date">Date</label>
                    <input
                        type="date"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                        required
                    />
                </div>
                <div className="form-control">
                    <label htmlFor="category">Category</label>
                    <select value={category} onChange={(e) => setCategory(e.target.value)}>
                        {categories.map(cat => (
                            <option key={cat} value={cat}>{cat}</option>
                        ))}
                    </select>
                </div>
                <div className="form-control">
                    <label htmlFor="type">Type</label>
                    <select value={type} onChange={(e) => setType(e.target.value)}>
                        <option value="debit">Debit (Expense)</option>
                        <option value="credit">Credit (Income)</option>
                    </select>
                </div>
                <div className="form-control">
                    <label htmlFor="image">Bill Image (Optional)</label>
                    <input
                        id="imageInput"
                        type="file"
                        accept="image/*"
                        capture="environment"
                        onChange={(e) => setImage(e.target.files[0])}
                    />
                </div>
                <button className="btn">Add Transaction</button>
            </form>
        </>
    );
};

export default AddTransaction;
