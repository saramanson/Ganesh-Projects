# Expense Tracker & Expense Splitter

A comprehensive financial management application with personal expense tracking AND group expense splitting capabilities. Built with Flask backend and React frontend.

## Features

### 💰 Personal Expense Tracker
- 📊 Track income and expenses with categories
- 📅 Date-based organization (Year/Month filtering)
- 📸 Attach bill images to transactions
- 📈 Visual expense breakdown by category
- 🗂️ Sidebar navigation for easy filtering
- 💾 Persistent storage with JSON files

### 👥 Group Expense Splitting (NEW!)
- **Groups & Friends**: Create groups for trips, roommates, or any shared expenses
- **Flexible Splitting**: Split expenses equally, unequally, by percentage, or by shares
- **Balance Tracking**: Track who owes whom across all groups
- **Debt Simplification**: Minimize the number of transactions needed to settle debts
- **Settlements**: Record payments and track settlement history
- **Smart Calculations**: Automatic balance updates and debt optimization

### 📱 Mobile App (NEW!)
- **Native Apps**: Available for Android and iOS
- **Same Features**: All web features work on mobile
- **Offline Ready**: Works with local or cloud backend
- **Easy Deployment**: One codebase for web + mobile

## Platforms

- 🌐 **Web App**: Works in any modern browser
- 🤖 **Android**: Native Android app via Capacitor
- 🍎 **iOS**: Native iOS app via Capacitor (requires Mac)

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## Usage

### Personal Expense Tracking
1. Click **💰 Expense Tracker** in the navigation
2. Add income/expense transactions
3. Filter by year and month using the sidebar
4. View expense charts by category

### Group Expense Splitting
1. Click **👥 Split Expenses** in the navigation
2. Add friends to your list
3. Create groups and add members
4. Add shared expenses with flexible split options:
   - **Equal**: Split evenly among all participants
   - **Unequal**: Specify exact amounts for each person
   - **Percentage**: Split by percentage (e.g., 60/40)
   - **Shares**: Split by shares/units
5. View simplified balances (who owes whom)
6. Record settlements when payments are made

### Example: Weekend Trip
```
1. Create group "Vegas Trip 2024"
2. Add friends: Alice, Bob, Charlie
3. Add expenses:
   - Hotel: $300 (Alice paid, split equally)
   - Dinner: $90 (Bob paid, split unequally)
   - Gas: $60 (Charlie paid, split by shares)
4. Check balances to see simplified debts
5. Record settlements as payments are made
```

See [EXPENSE_SPLITTING_GUIDE.md](EXPENSE_SPLITTING_GUIDE.md) for detailed documentation.

## Mobile App Deployment

### Quick Start (Test Now!)
See [MOBILE_QUICK_START.md](MOBILE_QUICK_START.md) for immediate testing on Android emulator or device.

### Full Deployment Guide
See [MOBILE_DEPLOYMENT.md](MOBILE_DEPLOYMENT.md) for complete instructions on:
- Building Android APK
- Building iOS app
- Publishing to Google Play Store
- Publishing to Apple App Store
- Backend deployment for mobile

### Mobile Build Commands
```bash
cd frontend

# Build and open Android Studio
npm run android

# Build and open Xcode (Mac only)
npm run ios

# Build and sync to mobile platforms
npm run build:mobile
```

## Web Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions to Render, Vercel, or other platforms.

## Tech Stack

- **Backend**: Flask (with Blueprints), Python
- **Frontend**: React, Vite, Chart.js
- **Storage**: JSON files (year-based organization)
- **Algorithms**: Greedy debt simplification algorithm

## API Endpoints

### Personal Expenses
- `GET/POST /api/transactions` - Manage personal transactions
- `DELETE /api/transactions/<id>` - Delete a transaction

### Groups & Friends
- `GET/POST /api/friends` - Manage friends
- `GET/POST /api/groups` - Manage groups
- `GET/POST /api/shared-expenses` - Manage shared expenses
- `GET /api/balances` - Get simplified balances
- `GET/POST /api/settlements` - Manage settlements

## Testing

Test the expense splitting API:
```bash
cd backend
python test_groups_api.py
```

## Categories

Grocery, Gas, Clothing, Medicine, Services, Internet, Water Bill, Electricity, Petrol, Insurance, Others

## Publishing to Google Play Store

### Quick Start
See [PLAY_STORE_CHECKLIST.md](PLAY_STORE_CHECKLIST.md) for a quick checklist of all steps.

### Complete Guide
See [GOOGLE_PLAY_STORE_GUIDE.md](GOOGLE_PLAY_STORE_GUIDE.md) for detailed step-by-step instructions on:
- Creating Google Play Developer account
- Preparing your app for release
- Building signed release AAB
- Creating store listing with screenshots
- Submitting for review
- Publishing to millions of users

### Key Requirements
- Google Play Developer account ($25 one-time fee)
- App icon and screenshots
- Privacy policy (template included: `privacy-policy.html`)
- Deployed backend (recommended: Render.com)
- Signed release build

### Publishing Timeline
1. **Day 1**: Prepare app and create developer account
2. **Day 1-3**: Wait for account verification
3. **Day 3**: Complete store listing and submit
4. **Day 4-10**: Google review process
5. **Day 10+**: App is LIVE on Play Store! 🎉

## Documentation

- **README.md** - This file, general overview
- **EXPENSE_SPLITTING_GUIDE.md** - Feature documentation
- **MOBILE_QUICK_START.md** - Test mobile app quickly
- **MOBILE_DEPLOYMENT.md** - Complete mobile deployment guide
- **MOBILE_CONVERSION_SUMMARY.md** - Mobile conversion details
- **GOOGLE_PLAY_STORE_GUIDE.md** - Play Store publishing guide
- **PLAY_STORE_CHECKLIST.md** - Quick publishing checklist
- **ARCHITECTURE.txt** - System architecture
- **DEPLOYMENT.md** - Web deployment guide

## License

This project is open source and available for personal and commercial use.
