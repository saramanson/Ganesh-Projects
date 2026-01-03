# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-01-02

### Added
- **Authentication System**:
    - User registration and login functionality.
    - Session management with `Flask-Login`.
    - Secure password hashing with `bcrypt`.
    - Protected routes ensuring data privacy.
- **Group Expense Splitting**:
    - Create and manage groups.
    - Add friends to groups.
    - Split expenses equally, unequally, by percentage, or by shares.
    - **Fully Paid** split option managed.
    - **Default Payer** selection (auto-selects logged-in user).
    - "Add Member" to existing groups functionality.
    - Balance tracking and debt simplification algorithm.
    - Settlement recording.
- **Mobile Support**:
    - Capacitor integration for Android and iOS.
    - Mobile-responsive UI design.
- **Backend**:
    - SQLite database for users and transactions.
    - JSON file storage for user-specific transaction data.
    - User-specific storage directories (`storage/user_{id}/`).

### Changed
- **Frontend Architecture**:
    - Ported to Vite for faster development and better build performance.
    - Updated UI with modern gradient aesthetics.
    - Improved navigation structure.
- **API**:
    - All transaction endpoints are now user-scoped.
    - Added comprehensive Auth and Group APIs.

### Fixed
- CORS configuration to support Vite development server (port 5173).
- Data synchronization issues between User and Friends/Groups.
