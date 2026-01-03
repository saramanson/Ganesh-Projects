import React, { useState, useEffect } from 'react';
import {
    getGroups,
    createGroup,
    updateGroup,
    deleteGroup,
    getFriends,
    addFriend,
    deleteFriend,
    getSharedExpenses,
    addSharedExpense,
    deleteSharedExpense,
    getBalances,
    getSettlements,
    recordSettlement,
    deleteSettlement
} from '../groupsApi';
import { API_BASE_URL } from '../config';
import ExpenseChart from './ExpenseChart';
import '../styles/Groups.css';

function Groups({ currentUser }) {
    const [friends, setFriends] = useState([]);
    const [groups, setGroups] = useState([]);
    const [selectedGroup, setSelectedGroup] = useState(null);
    const [sharedExpenses, setSharedExpenses] = useState([]);
    const [balances, setBalances] = useState([]);
    const [settlements, setSettlements] = useState([]);
    const [activeTab, setActiveTab] = useState('expenses'); // expenses, balances, settlements

    // Form states
    const [showAddFriend, setShowAddFriend] = useState(false);
    const [showAddGroup, setShowAddGroup] = useState(false);
    const [showAddExpense, setShowAddExpense] = useState(false);
    const [showRecordSettlement, setShowRecordSettlement] = useState(false);
    const [showAddMember, setShowAddMember] = useState(false);
    const [showChart, setShowChart] = useState(false);

    const [newFriend, setNewFriend] = useState({ name: '', email: '' });
    const [newGroup, setNewGroup] = useState({ name: '', description: '', member_ids: [] });
    const [newExpense, setNewExpense] = useState({
        description: '',
        amount: '',
        category: 'General',
        date: new Date().toLocaleDateString('en-CA'),
        paid_by: '',
        split_type: 'equal',
        splits: []
    });
    const [newSettlement, setNewSettlement] = useState({
        paid_by: '',
        paid_to: '',
        amount: '',
        notes: ''
    });
    const [memberToAdd, setMemberToAdd] = useState('');

    useEffect(() => {
        fetchFriends();
        fetchGroups();
    }, []);

    useEffect(() => {
        if (selectedGroup) {
            fetchGroupData(selectedGroup.id);
        }
    }, [selectedGroup]);

    useEffect(() => {
        if (showAddExpense && currentUser && selectedGroup && friends.length > 0) {
            const normalize = (str) => str ? str.toLowerCase().trim() : '';

            const me = friends.find(f =>
                (f.email && currentUser.email && normalize(f.email) === normalize(currentUser.email)) ||
                normalize(f.name) === normalize(currentUser.username)
            );

            if (me && selectedGroup.member_ids.includes(me.id)) {
                setNewExpense(prev => ({ ...prev, paid_by: me.id }));
            }
        }
    }, [showAddExpense, currentUser, selectedGroup, friends]);

    const fetchFriends = async () => {
        try {
            const data = await getFriends();
            setFriends(data);
        } catch (error) {
            console.error('Error fetching friends:', error);
        }
    };

    const fetchGroups = async () => {
        try {
            const data = await getGroups();
            setGroups(data);
        } catch (error) {
            console.error('Error fetching groups:', error);
        }
    };

    const fetchGroupData = async (groupId) => {
        try {
            const [expensesData, balancesData, settlementsData] = await Promise.all([
                getSharedExpenses(groupId),
                getBalances(groupId),
                getSettlements(groupId)
            ]);
            setSharedExpenses(expensesData);
            setBalances(balancesData);
            setSettlements(settlementsData);
        } catch (error) {
            console.error('Error fetching group data:', error);
        }
    };

    const handleAddFriend = async (e) => {
        e.preventDefault();
        try {
            const friend = await addFriend(newFriend);
            setFriends([...friends, friend]);
            setNewFriend({ name: '', email: '' });
            setShowAddFriend(false);
        } catch (error) {
            console.error('Error adding friend:', error);
        }
    };

    const handleDeleteFriend = async (friendId) => {
        if (!window.confirm('Are you sure you want to delete this friend?')) return;
        try {
            await deleteFriend(friendId);
            setFriends(friends.filter(f => f.id !== friendId));
        } catch (error) {
            console.error('Error deleting friend:', error);
        }
    };

    const handleCreateGroup = async (e) => {
        e.preventDefault();
        try {
            const group = await createGroup(newGroup);
            setGroups([...groups, group]);
            setNewGroup({ name: '', description: '', member_ids: [] });
            setShowAddGroup(false);
        } catch (error) {
            console.error('Error creating group:', error);
        }
    };

    const handleDeleteGroup = async (groupId) => {
        if (!window.confirm('Are you sure you want to delete this group?')) return;
        try {
            await deleteGroup(groupId);
            setGroups(groups.filter(g => g.id !== groupId));
            if (selectedGroup?.id === groupId) {
                setSelectedGroup(null);
            }
        } catch (error) {
            console.error('Error deleting group:', error);
        }
    };

    const handleAddMemberToGroup = async (e) => {
        e.preventDefault();
        try {
            if (!memberToAdd) return;

            const updatedMemberIds = [...selectedGroup.member_ids, memberToAdd];
            const updatedGroup = await updateGroup(selectedGroup.id, {
                ...selectedGroup,
                member_ids: updatedMemberIds
            });

            setGroups(groups.map(g => g.id === selectedGroup.id ? updatedGroup : g));
            setSelectedGroup(updatedGroup);
            setMemberToAdd('');
            setShowAddMember(false);
        } catch (error) {
            console.error('Error adding member to group:', error);
        }
    };

    const handleAddExpense = async (e) => {
        e.preventDefault();
        try {
            const expenseData = {
                ...newExpense,
                group_id: selectedGroup.id
            };

            const expense = await addSharedExpense(expenseData);
            setSharedExpenses([expense, ...sharedExpenses]);
            setNewExpense({
                description: '',
                amount: '',
                category: 'General',
                date: new Date().toLocaleDateString('en-CA'),
                paid_by: '',
                split_type: 'equal',
                splits: []
            });
            setShowAddExpense(false);

            // Refresh balances
            const balancesData = await getBalances(selectedGroup.id);
            setBalances(balancesData);
        } catch (error) {
            console.error('Error adding expense:', error);
        }
    };

    const handleDeleteExpense = async (expenseId) => {
        if (!window.confirm('Are you sure you want to delete this expense?')) return;
        try {
            await deleteSharedExpense(expenseId);
            setSharedExpenses(sharedExpenses.filter(e => e.id !== expenseId));

            // Refresh balances
            const balancesData = await getBalances(selectedGroup.id);
            setBalances(balancesData);
        } catch (error) {
            console.error('Error deleting expense:', error);
        }
    };

    const handleRecordSettlement = async (e) => {
        e.preventDefault();
        try {
            const settlementData = {
                ...newSettlement,
                group_id: selectedGroup.id,
                date: new Date().toISOString()
            };

            const settlement = await recordSettlement(settlementData);
            setSettlements([settlement, ...settlements]);
            setNewSettlement({
                paid_by: '',
                paid_to: '',
                amount: '',
                notes: ''
            });
            setShowRecordSettlement(false);

            // Refresh balances
            const balancesData = await getBalances(selectedGroup.id);
            setBalances(balancesData);
        } catch (error) {
            console.error('Error recording settlement:', error);
        }
    };

    const handleDeleteSettlement = async (settlementId) => {
        if (!window.confirm('Are you sure you want to delete this settlement?')) return;
        try {
            await deleteSettlement(settlementId);
            setSettlements(settlements.filter(s => s.id !== settlementId));

            // Refresh balances
            const balancesData = await getBalances(selectedGroup.id);
            setBalances(balancesData);
        } catch (error) {
            console.error('Error deleting settlement:', error);
        }
    };

    const toggleMemberSelection = (friendId) => {
        const currentMembers = newGroup.member_ids;
        if (currentMembers.includes(friendId)) {
            setNewGroup({
                ...newGroup,
                member_ids: currentMembers.filter(id => id !== friendId)
            });
        } else {
            setNewGroup({
                ...newGroup,
                member_ids: [...currentMembers, friendId]
            });
        }
    };

    const initializeExpenseSplits = (splitType) => {
        if (!selectedGroup) return;

        const groupMembers = friends.filter(f => selectedGroup.member_ids.includes(f.id));

        let splits = [];
        if (splitType === 'equal') {
            splits = groupMembers.map(f => ({ friend_id: f.id }));
        } else if (splitType === 'unequal') {
            splits = groupMembers.map(f => ({ friend_id: f.id, amount: 0 }));
        } else if (splitType === 'percentage') {
            splits = groupMembers.map(f => ({ friend_id: f.id, percentage: 0 }));
        } else if (splitType === 'shares') {
            splits = groupMembers.map(f => ({ friend_id: f.id, shares: 1 }));
        } else if (splitType === 'full') {
            // Default to the first member or the payer if possible is not relevant here yet as we don't know amount
            // We just need one entry to hold the "target"
            // Default to the first member of the group
            if (groupMembers.length > 0) {
                splits = [{ friend_id: groupMembers[0].id }];
            }
        }

        setNewExpense({ ...newExpense, split_type: splitType, splits });
    };

    const updateSplitValue = (friendId, field, value) => {
        const updatedSplits = newExpense.splits.map(split =>
            split.friend_id === friendId
                ? { ...split, [field]: parseFloat(value) || 0 }
                : split
        );
        setNewExpense({ ...newExpense, splits: updatedSplits });
    };

    const getFriendName = (friendId) => {
        const friend = friends.find(f => f.id === friendId);
        return friend ? friend.name : 'Unknown';
    };

    const getGroupMembers = (group) => {
        return friends.filter(f => group.member_ids.includes(f.id));
    };

    return (
        <div className="groups-container">
            <div className="groups-sidebar">
                <div className="sidebar-section">
                    <div className="section-header">
                        <h3>Friends</h3>
                        <button
                            className="btn-add"
                            onClick={() => setShowAddFriend(!showAddFriend)}
                        >
                            +
                        </button>
                    </div>

                    {showAddFriend && (
                        <form onSubmit={handleAddFriend} className="add-form">
                            <input
                                type="text"
                                placeholder="Name"
                                value={newFriend.name}
                                onChange={(e) => setNewFriend({ ...newFriend, name: e.target.value })}
                                required
                            />
                            <input
                                type="email"
                                placeholder="Email (optional)"
                                value={newFriend.email}
                                onChange={(e) => setNewFriend({ ...newFriend, email: e.target.value })}
                            />
                            <div className="form-actions">
                                <button type="submit" className="btn-primary">Add</button>
                                <button
                                    type="button"
                                    className="btn-secondary"
                                    onClick={() => setShowAddFriend(false)}
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    )}

                    <div className="friends-list">
                        {friends.map(friend => (
                            <div key={friend.id} className="friend-item">
                                <div className="friend-info">
                                    <div className="friend-avatar">{friend.name.charAt(0).toUpperCase()}</div>
                                    <div>
                                        <div className="friend-name">{friend.name}</div>
                                        {friend.email && <div className="friend-email">{friend.email}</div>}
                                    </div>
                                </div>
                                <button
                                    className="btn-delete"
                                    onClick={() => handleDeleteFriend(friend.id)}
                                >
                                    ×
                                </button>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="sidebar-section">
                    <div className="section-header">
                        <h3>Groups</h3>
                        <button
                            className="btn-add"
                            onClick={() => setShowAddGroup(!showAddGroup)}
                        >
                            +
                        </button>
                    </div>

                    {showAddGroup && (
                        <form onSubmit={handleCreateGroup} className="add-form">
                            <input
                                type="text"
                                placeholder="Group Name"
                                value={newGroup.name}
                                onChange={(e) => setNewGroup({ ...newGroup, name: e.target.value })}
                                required
                            />
                            <textarea
                                placeholder="Description (optional)"
                                value={newGroup.description}
                                onChange={(e) => setNewGroup({ ...newGroup, description: e.target.value })}
                            />
                            <div className="member-selection">
                                <label>Select Members:</label>
                                {friends.map(friend => (
                                    <label key={friend.id} className="checkbox-label">
                                        <input
                                            type="checkbox"
                                            checked={newGroup.member_ids.includes(friend.id)}
                                            onChange={() => toggleMemberSelection(friend.id)}
                                        />
                                        {friend.name}
                                    </label>
                                ))}
                            </div>
                            <div className="form-actions">
                                <button type="submit" className="btn-primary">Create</button>
                                <button
                                    type="button"
                                    className="btn-secondary"
                                    onClick={() => setShowAddGroup(false)}
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    )}

                    <div className="groups-list">
                        {groups.map(group => (
                            <div
                                key={group.id}
                                className={`group-item ${selectedGroup?.id === group.id ? 'active' : ''}`}
                                onClick={() => setSelectedGroup(group)}
                            >
                                <div className="group-info">
                                    <div className="group-name">{group.name}</div>
                                    <div className="group-members">
                                        {getGroupMembers(group).length} members
                                    </div>
                                </div>
                                <button
                                    className="btn-delete"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        handleDeleteGroup(group.id);
                                    }}
                                >
                                    ×
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="groups-main">
                {selectedGroup ? (
                    <>
                        <div className="group-header">
                            <div className="group-header-top">
                                <h2>{selectedGroup.name}</h2>
                                <button
                                    className="btn-secondary btn-sm"
                                    onClick={() => setShowAddMember(!showAddMember)}
                                    title="Add Member"
                                >
                                    +👤
                                </button>
                            </div>
                            {selectedGroup.description && (
                                <p className="group-description">{selectedGroup.description}</p>
                            )}

                            {showAddMember && (
                                <form onSubmit={handleAddMemberToGroup} className="add-member-form">
                                    <select
                                        value={memberToAdd}
                                        onChange={(e) => setMemberToAdd(e.target.value)}
                                        required
                                    >
                                        <option value="">Select a friend</option>
                                        {friends
                                            .filter(f => !selectedGroup.member_ids.includes(f.id))
                                            .map(friend => (
                                                <option key={friend.id} value={friend.id}>
                                                    {friend.name}
                                                </option>
                                            ))
                                        }
                                    </select>
                                    <div className="form-actions-inline">
                                        <button type="submit" className="btn-primary btn-sm">Add</button>
                                        <button
                                            type="button"
                                            className="btn-secondary btn-sm"
                                            onClick={() => setShowAddMember(false)}
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </form>
                            )}

                            <div className="group-members-chips">
                                {getGroupMembers(selectedGroup).map(member => (
                                    <span key={member.id} className="member-chip">
                                        {member.name}
                                    </span>
                                ))}
                            </div>
                        </div>

                        <div className="tabs">
                            <button
                                className={`tab ${activeTab === 'expenses' ? 'active' : ''}`}
                                onClick={() => setActiveTab('expenses')}
                                title="Expenses"
                            >
                                💸
                            </button>
                            <button
                                className={`tab ${activeTab === 'balances' ? 'active' : ''}`}
                                onClick={() => setActiveTab('balances')}
                                title="Balances"
                            >
                                ⚖️
                            </button>
                            <button
                                className={`tab ${activeTab === 'settlements' ? 'active' : ''}`}
                                onClick={() => setActiveTab('settlements')}
                                title="Settlements"
                            >
                                🤝
                            </button>
                        </div>

                        {activeTab === 'expenses' && (
                            <div className="tab-content">
                                <div className="content-header">
                                    <h3>Shared Expenses</h3>
                                    <div style={{ display: 'flex', gap: '10px' }}>
                                        <button
                                            className="btn-secondary"
                                            onClick={() => setShowChart(!showChart)}
                                            style={{ padding: '8px 12px' }}
                                        >
                                            📊 Chart
                                        </button>
                                        <button
                                            className="btn-secondary"
                                            onClick={() => window.open(`${API_BASE_URL}/groups/${selectedGroup.id}/export`, '_blank')}
                                            style={{ padding: '8px 12px' }}
                                        >
                                            ⬇️ Download
                                        </button>
                                        <button
                                            className="btn-primary"
                                            onClick={() => {
                                                setShowAddExpense(!showAddExpense);
                                                if (!showAddExpense) {
                                                    initializeExpenseSplits('equal');
                                                }
                                            }}
                                            title="Add Expense"
                                        >
                                            +
                                        </button>
                                    </div>
                                </div>

                                {showChart && (
                                    <div style={{ marginBottom: '20px' }}>
                                        <ExpenseChart transactions={sharedExpenses.map(e => ({ ...e, type: 'debit' }))} />
                                    </div>
                                )}

                                {showAddExpense && (
                                    <form onSubmit={handleAddExpense} className="expense-form">
                                        <div className="form-row">
                                            <input
                                                type="text"
                                                placeholder="Description"
                                                value={newExpense.description}
                                                onChange={(e) => setNewExpense({ ...newExpense, description: e.target.value })}
                                                required
                                            />
                                            <input
                                                type="number"
                                                step="0.01"
                                                placeholder="Amount"
                                                value={newExpense.amount}
                                                onChange={(e) => setNewExpense({ ...newExpense, amount: e.target.value })}
                                                required
                                            />
                                            <select
                                                value={newExpense.category}
                                                onChange={(e) => setNewExpense({ ...newExpense, category: e.target.value })}
                                                style={{ flex: 1, padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }}
                                            >
                                                <option value="General">General</option>
                                                <option value="Food">Food</option>
                                                <option value="Transport">Transport</option>
                                                <option value="Accommodation">Accommodation</option>
                                                <option value="Entertainment">Entertainment</option>
                                                <option value="Utilities">Utilities</option>
                                                <option value="Shopping">Shopping</option>
                                            </select>
                                            <input
                                                type="date"
                                                value={newExpense.date}
                                                onChange={(e) => setNewExpense({ ...newExpense, date: e.target.value })}
                                                required
                                            />
                                        </div>

                                        <div className="form-row">
                                            <select
                                                value={newExpense.paid_by}
                                                onChange={(e) => setNewExpense({ ...newExpense, paid_by: e.target.value })}
                                                required
                                            >
                                                <option value="">Who paid?</option>
                                                {getGroupMembers(selectedGroup).map(member => (
                                                    <option key={member.id} value={member.id}>
                                                        {member.name}
                                                    </option>
                                                ))}
                                            </select>

                                            <select
                                                value={newExpense.split_type}
                                                onChange={(e) => initializeExpenseSplits(e.target.value)}
                                            >
                                                <option value="equal">Split Equally</option>
                                                <option value="unequal">Unequal Amounts</option>
                                                <option value="percentage">By Percentage</option>
                                                <option value="shares">By Shares</option>
                                                <option value="full">Fully Paid (Full Amount)</option>
                                            </select>
                                        </div>

                                        <div className="splits-section">
                                            <h4>Split Details:</h4>

                                            {newExpense.split_type === 'full' ? (
                                                <div className="split-row">
                                                    <span className="split-name">Full amount allocated to:</span>
                                                    <select
                                                        value={newExpense.splits[0]?.friend_id || ''}
                                                        onChange={(e) => {
                                                            const updatedSplits = [{ friend_id: e.target.value }];
                                                            setNewExpense({ ...newExpense, splits: updatedSplits });
                                                        }}
                                                        style={{ flex: 1, marginLeft: '10px' }}
                                                    >
                                                        {getGroupMembers(selectedGroup).map(member => (
                                                            <option key={member.id} value={member.id}>
                                                                {member.name}
                                                            </option>
                                                        ))}
                                                    </select>
                                                </div>
                                            ) : (
                                                newExpense.splits.map(split => (
                                                    <div key={split.friend_id} className="split-row">
                                                        <span className="split-name">{getFriendName(split.friend_id)}</span>
                                                        {newExpense.split_type === 'equal' && (
                                                            <span className="split-value">Equal share</span>
                                                        )}
                                                        {newExpense.split_type === 'unequal' && (
                                                            <input
                                                                type="number"
                                                                step="0.01"
                                                                placeholder="Amount"
                                                                value={split.amount || ''}
                                                                onChange={(e) => updateSplitValue(split.friend_id, 'amount', e.target.value)}
                                                            />
                                                        )}
                                                        {newExpense.split_type === 'percentage' && (
                                                            <input
                                                                type="number"
                                                                step="0.01"
                                                                placeholder="Percentage"
                                                                value={split.percentage || ''}
                                                                onChange={(e) => updateSplitValue(split.friend_id, 'percentage', e.target.value)}
                                                            />
                                                        )}
                                                        {newExpense.split_type === 'shares' && (
                                                            <input
                                                                type="number"
                                                                step="1"
                                                                placeholder="Shares"
                                                                value={split.shares || ''}
                                                                onChange={(e) => updateSplitValue(split.friend_id, 'shares', e.target.value)}
                                                            />
                                                        )}
                                                    </div>
                                                ))
                                            )}
                                        </div>

                                        <div className="form-actions">
                                            <button type="submit" className="btn-primary">Add Expense</button>
                                            <button
                                                type="button"
                                                className="btn-secondary"
                                                onClick={() => setShowAddExpense(false)}
                                            >
                                                Cancel
                                            </button>
                                        </div>
                                    </form>
                                )}

                                <div className="expenses-list">
                                    {sharedExpenses.map(expense => (
                                        <div key={expense.id} className="expense-card">
                                            <div className="expense-header">
                                                <div>
                                                    <h4>{expense.description}</h4>
                                                    <p className="expense-date">
                                                        {new Date(expense.date).toLocaleDateString()}
                                                    </p>
                                                </div>
                                                <div className="expense-amount">${expense.amount.toFixed(2)}</div>
                                            </div>
                                            <div className="expense-details">
                                                <p>Paid by: <strong>{getFriendName(expense.paid_by)}</strong></p>
                                                <p>Split: <strong>{expense.split_type}</strong></p>
                                                <div className="expense-splits">
                                                    {expense.splits.map(split => (
                                                        <div key={split.friend_id} className="split-detail">
                                                            {getFriendName(split.friend_id)}: ${split.amount.toFixed(2)}
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                            <button
                                                className="btn-delete-expense"
                                                onClick={() => handleDeleteExpense(expense.id)}
                                            >
                                                Delete
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {activeTab === 'balances' && (
                            <div className="tab-content">
                                <div className="content-header">
                                    <h3>Who Owes Whom</h3>
                                    <button
                                        className="btn-primary"
                                        onClick={() => setShowRecordSettlement(!showRecordSettlement)}
                                    >
                                        Record Payment
                                    </button>
                                </div>

                                {showRecordSettlement && (
                                    <form onSubmit={handleRecordSettlement} className="settlement-form">
                                        <div className="form-row">
                                            <select
                                                value={newSettlement.paid_by}
                                                onChange={(e) => setNewSettlement({ ...newSettlement, paid_by: e.target.value })}
                                                required
                                            >
                                                <option value="">Who paid?</option>
                                                {getGroupMembers(selectedGroup).map(member => (
                                                    <option key={member.id} value={member.id}>
                                                        {member.name}
                                                    </option>
                                                ))}
                                            </select>

                                            <select
                                                value={newSettlement.paid_to}
                                                onChange={(e) => setNewSettlement({ ...newSettlement, paid_to: e.target.value })}
                                                required
                                            >
                                                <option value="">Paid to?</option>
                                                {getGroupMembers(selectedGroup).map(member => (
                                                    <option key={member.id} value={member.id}>
                                                        {member.name}
                                                    </option>
                                                ))}
                                            </select>

                                            <input
                                                type="number"
                                                step="0.01"
                                                placeholder="Amount"
                                                value={newSettlement.amount}
                                                onChange={(e) => setNewSettlement({ ...newSettlement, amount: e.target.value })}
                                                required
                                            />
                                        </div>

                                        <textarea
                                            placeholder="Notes (optional)"
                                            value={newSettlement.notes}
                                            onChange={(e) => setNewSettlement({ ...newSettlement, notes: e.target.value })}
                                        />

                                        <div className="form-actions">
                                            <button type="submit" className="btn-primary">Record Payment</button>
                                            <button
                                                type="button"
                                                className="btn-secondary"
                                                onClick={() => setShowRecordSettlement(false)}
                                            >
                                                Cancel
                                            </button>
                                        </div>
                                    </form>
                                )}

                                <div className="balances-list">
                                    {balances.length === 0 ? (
                                        <div className="empty-state">
                                            <p>All settled up! 🎉</p>
                                        </div>
                                    ) : (
                                        balances.map((balance, index) => (
                                            <div key={index} className="balance-card">
                                                <div className="balance-info">
                                                    <span className="balance-from">{getFriendName(balance.from)}</span>
                                                    <span className="balance-arrow">→</span>
                                                    <span className="balance-to">{getFriendName(balance.to)}</span>
                                                </div>
                                                <div className="balance-amount">${balance.amount.toFixed(2)}</div>
                                            </div>
                                        ))
                                    )}
                                </div>
                            </div>
                        )}

                        {activeTab === 'settlements' && (
                            <div className="tab-content">
                                <h3>Settlement History</h3>
                                <div className="settlements-list">
                                    {settlements.map(settlement => (
                                        <div key={settlement.id} className="settlement-card">
                                            <div className="settlement-header">
                                                <div>
                                                    <p className="settlement-info">
                                                        <strong>{getFriendName(settlement.paid_by)}</strong> paid{' '}
                                                        <strong>{getFriendName(settlement.paid_to)}</strong>
                                                    </p>
                                                    <p className="settlement-date">
                                                        {new Date(settlement.date).toLocaleDateString()}
                                                    </p>
                                                </div>
                                                <div className="settlement-amount">${settlement.amount.toFixed(2)}</div>
                                            </div>
                                            {settlement.notes && (
                                                <p className="settlement-notes">{settlement.notes}</p>
                                            )}
                                            <button
                                                className="btn-delete-settlement"
                                                onClick={() => handleDeleteSettlement(settlement.id)}
                                            >
                                                Delete
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </>
                ) : (
                    <div className="empty-state-main">
                        <h2>Select a group to get started</h2>
                        <p>Create a group and add friends to start splitting expenses</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Groups;
