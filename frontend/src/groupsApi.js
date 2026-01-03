import { API_BASE_URL } from './config';


// ==================== FRIENDS API ====================

export const getFriends = async () => {
    const response = await fetch(`${API_BASE_URL}/friends`);
    if (!response.ok) throw new Error('Failed to fetch friends');
    return response.json();
};

export const addFriend = async (friend) => {
    const response = await fetch(`${API_BASE_URL}/friends`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(friend),
    });
    if (!response.ok) throw new Error('Failed to add friend');
    return response.json();
};

export const deleteFriend = async (friendId) => {
    const response = await fetch(`${API_BASE_URL}/friends/${friendId}`, {
        method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete friend');
    return response.json();
};

// ==================== GROUPS API ====================

export const getGroups = async () => {
    const response = await fetch(`${API_BASE_URL}/groups`);
    if (!response.ok) throw new Error('Failed to fetch groups');
    return response.json();
};

export const createGroup = async (group) => {
    const response = await fetch(`${API_BASE_URL}/groups`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(group),
    });
    if (!response.ok) throw new Error('Failed to create group');
    return response.json();
};

export const updateGroup = async (groupId, group) => {
    const response = await fetch(`${API_BASE_URL}/groups/${groupId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(group),
    });
    if (!response.ok) throw new Error('Failed to update group');
    return response.json();
};

export const deleteGroup = async (groupId) => {
    const response = await fetch(`${API_BASE_URL}/groups/${groupId}`, {
        method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete group');
    return response.json();
};

// ==================== SHARED EXPENSES API ====================

export const getSharedExpenses = async (groupId = null) => {
    const url = groupId
        ? `${API_BASE_URL}/shared-expenses?group_id=${groupId}`
        : `${API_BASE_URL}/shared-expenses`;

    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to fetch shared expenses');
    return response.json();
};

export const addSharedExpense = async (expense) => {
    const response = await fetch(`${API_BASE_URL}/shared-expenses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(expense),
    });
    if (!response.ok) throw new Error('Failed to add shared expense');
    return response.json();
};

export const deleteSharedExpense = async (expenseId) => {
    const response = await fetch(`${API_BASE_URL}/shared-expenses/${expenseId}`, {
        method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete shared expense');
    return response.json();
};

// ==================== BALANCES API ====================

export const getBalances = async (groupId = null) => {
    const url = groupId
        ? `${API_BASE_URL}/balances?group_id=${groupId}`
        : `${API_BASE_URL}/balances`;

    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to fetch balances');
    return response.json();
};

// ==================== SETTLEMENTS API ====================

export const getSettlements = async (groupId = null) => {
    const url = groupId
        ? `${API_BASE_URL}/settlements?group_id=${groupId}`
        : `${API_BASE_URL}/settlements`;

    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to fetch settlements');
    return response.json();
};

export const recordSettlement = async (settlement) => {
    const response = await fetch(`${API_BASE_URL}/settlements`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settlement),
    });
    if (!response.ok) throw new Error('Failed to record settlement');
    return response.json();
};

export const deleteSettlement = async (settlementId) => {
    const response = await fetch(`${API_BASE_URL}/settlements/${settlementId}`, {
        method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete settlement');
    return response.json();
};
