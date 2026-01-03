# Expense Splitting Features - Documentation

## Overview
This application now includes comprehensive expense splitting capabilities alongside the existing expense tracker. You can manage groups, friends, split expenses in multiple ways, track balances, and record settlements.

## Core Capabilities

### 1. Groups & Friends Management

#### Friends
- **Add Friends**: Create a list of friends/contacts who you share expenses with
  - Name (required)
  - Email (optional)
- **View Friends**: See all your friends in the sidebar with avatar initials
- **Delete Friends**: Remove friends from your list

#### Groups
- **Create Groups**: Organize friends into groups for different purposes
  - Trip groups (e.g., "Vegas Trip 2024")
  - Roommate groups (e.g., "Apartment 3B")
  - Event groups (e.g., "Sarah's Birthday")
- **Group Details**:
  - Name (required)
  - Description (optional)
  - Select multiple members from your friends list
- **View Groups**: See all groups with member counts
- **Delete Groups**: Remove groups when no longer needed

### 2. Expense Splitting

The application supports **4 different split types**:

#### a) Equal Split
- Divides the expense equally among all selected participants
- Example: $100 dinner split 4 ways = $25 per person

#### b) Unequal Split
- Manually specify exact amounts for each person
- Example: Person A pays $60, Person B pays $40
- Useful when people ordered different amounts

#### c) Percentage Split
- Split by percentage (must total 100%)
- Example: Person A: 60%, Person B: 40%
- Great for proportional sharing

#### d) Shares Split
- Split by shares/units
- Example: Person A: 2 shares, Person B: 1 share
- Useful for splitting based on consumption or usage

#### Adding an Expense
1. Select a group
2. Click "Add Expense"
3. Enter:
   - Description (e.g., "Dinner at Restaurant")
   - Total amount
   - Who paid for it
   - Split type
   - Split details for each participant
4. The system automatically calculates each person's share

### 3. Balance Tracking

#### Smart Balance Calculation
- Automatically tracks who owes whom across all expenses
- Considers all expenses in a group
- Subtracts any recorded settlements
- Shows net balances (simplified)

#### Debt Simplification Algorithm
The app uses an intelligent algorithm to minimize the number of transactions needed:

**Example:**
- Without simplification:
  - Alice owes Bob $20
  - Bob owes Charlie $20
  - Result: 2 transactions

- With simplification:
  - Alice owes Charlie $20
  - Result: 1 transaction

This reduces complexity and makes settling up easier!

#### Viewing Balances
- Navigate to the "Balances" tab
- See simplified list of who owes whom
- Visual indicators:
  - Red name = person who owes
  - Green name = person who is owed
  - Arrow shows direction of payment

### 4. Settlements

#### Recording Payments
When someone pays their debt:
1. Go to "Balances" tab
2. Click "Record Payment"
3. Enter:
   - Who paid
   - Who received the payment
   - Amount
   - Optional notes
4. The balance automatically updates

#### Settlement History
- View all past settlements in the "Settlements" tab
- See payment dates and amounts
- Add notes for reference
- Delete settlements if recorded in error

## User Interface

### Navigation
- **💰 Expense Tracker**: Your personal expense tracking (original feature)
- **👥 Split Expenses**: Group expense splitting (new feature)

### Split Expenses Layout

#### Left Sidebar
- **Friends Section**: Manage your friends list
- **Groups Section**: View and select groups

#### Main Area
When a group is selected:

1. **Group Header**
   - Group name and description
   - Member chips showing all participants

2. **Three Tabs**:
   - **Expenses**: View and add shared expenses
   - **Balances**: See who owes whom (simplified)
   - **Settlements**: View payment history

### Visual Design
- Modern gradient backgrounds
- Glassmorphism effects
- Smooth animations and transitions
- Color-coded information:
  - Purple/blue gradients for primary actions
  - Red for debts/expenses
  - Green for credits/payments
- Responsive design for mobile and desktop

## API Endpoints

### Friends
- `GET /api/friends` - Get all friends
- `POST /api/friends` - Add a friend
- `DELETE /api/friends/<id>` - Delete a friend

### Groups
- `GET /api/groups` - Get all groups
- `POST /api/groups` - Create a group
- `PUT /api/groups/<id>` - Update a group
- `DELETE /api/groups/<id>` - Delete a group

### Shared Expenses
- `GET /api/shared-expenses?group_id=<id>` - Get expenses for a group
- `POST /api/shared-expenses` - Add a shared expense
- `DELETE /api/shared-expenses/<id>` - Delete an expense

### Balances
- `GET /api/balances?group_id=<id>` - Get simplified balances for a group

### Settlements
- `GET /api/settlements?group_id=<id>` - Get settlements for a group
- `POST /api/settlements` - Record a settlement
- `DELETE /api/settlements/<id>` - Delete a settlement

## Data Storage

All data is stored in JSON files in the `backend/storage/` directory:

- `friends.json` - Friends list
- `groups.json` - Groups and their members
- `shared_expenses.json` - All shared expenses
- `settlements.json` - Payment history

## Example Workflow

### Scenario: Weekend Trip with Friends

1. **Setup**
   ```
   - Add friends: Alice, Bob, Charlie
   - Create group: "Weekend Getaway"
   - Add all three as members
   ```

2. **Add Expenses**
   ```
   - Hotel: $300 (paid by Alice, split equally)
     → Each owes: $100
   
   - Dinner: $90 (paid by Bob, split equally)
     → Each owes: $30
   
   - Gas: $60 (paid by Charlie, split by shares)
     → Alice: 2 shares, Bob: 1 share, Charlie: 1 share
     → Alice: $30, Bob: $15, Charlie: $15
   ```

3. **Check Balances**
   ```
   Simplified balances show:
   - Bob owes Alice: $70
   - Charlie owes Alice: $85
   ```

4. **Record Settlements**
   ```
   - Bob pays Alice $70
   - Charlie pays Alice $85
   - All settled! 🎉
   ```

## Tips for Best Use

1. **Create Groups Early**: Set up groups before trips or shared living arrangements
2. **Add Expenses Promptly**: Record expenses as they happen to avoid forgetting
3. **Use Appropriate Split Types**: 
   - Equal for most shared meals
   - Unequal when amounts vary significantly
   - Percentage for proportional sharing (like rent based on room size)
   - Shares for usage-based splitting
4. **Check Balances Regularly**: Review the Balances tab to know who owes what
5. **Record Settlements**: Always record payments to keep balances accurate
6. **Add Notes**: Use the notes field in settlements for reference

## Future Enhancements (Potential)

- Export expense reports
- Recurring expenses
- Multiple currencies
- Email notifications
- Mobile app
- Receipt photo uploads for shared expenses
- Group statistics and charts
- Expense categories for shared expenses

## Technical Details

### Backend
- **Framework**: Flask with Blueprint architecture
- **Storage**: JSON file-based storage
- **Algorithm**: Greedy debt simplification algorithm

### Frontend
- **Framework**: React with Hooks
- **Styling**: Custom CSS with modern design patterns
- **State Management**: React useState and useEffect

### Key Algorithms

**Debt Simplification**:
1. Calculate net balance for each person
2. Separate into debtors (negative balance) and creditors (positive balance)
3. Match largest debtor with largest creditor
4. Transfer minimum of debt and credit
5. Repeat until all balanced

This minimizes the number of transactions needed to settle all debts!
