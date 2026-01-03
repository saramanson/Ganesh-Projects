# Mobile App Deployment Guide

## Overview

Your Expense Tracker web app has been successfully converted into a **native mobile app** using Capacitor! This guide will help you build and deploy the app to Android and iOS devices.

## ✅ What's Been Set Up

### 1. Capacitor Configuration
- ✓ Capacitor core and CLI installed
- ✓ Android platform added
- ✓ iOS platform ready to add
- ✓ App configured with ID: `com.expensetracker.app`
- ✓ Splash screen configured with your brand colors

### 2. API Configuration
- ✓ Environment-aware API URLs
- ✓ Automatic detection of mobile vs web
- ✓ Proper backend URL handling

### 3. Build Scripts
New npm scripts added to `package.json`:
- `npm run build:mobile` - Build and sync to mobile platforms
- `npm run android` - Build and open Android Studio
- `npm run ios` - Build and open Xcode
- `npm run sync` - Sync web assets to mobile platforms

## 📱 Building for Android

### Prerequisites
1. **Install Android Studio**
   - Download from: https://developer.android.com/studio
   - Install with default settings
   - Open Android Studio and complete the setup wizard

2. **Install Java Development Kit (JDK)**
   - Android Studio includes JDK, or download separately
   - Recommended: JDK 17 or later

### Steps to Build Android App

#### 1. Open Android Project
```bash
cd frontend
npm run android
```
This will:
- Build your web app
- Sync assets to Android
- Open Android Studio

#### 2. In Android Studio

**First Time Setup:**
1. Wait for Gradle sync to complete (bottom status bar)
2. If prompted, accept SDK licenses
3. Install any missing SDK components

**Build APK (for testing):**
1. Click **Build** → **Build Bundle(s) / APK(s)** → **Build APK(s)**
2. Wait for build to complete
3. Click "locate" in the notification to find the APK
4. APK location: `frontend/android/app/build/outputs/apk/debug/app-debug.apk`

**Install on Device:**
1. Enable USB debugging on your Android device:
   - Settings → About Phone → Tap "Build Number" 7 times
   - Settings → Developer Options → Enable USB Debugging
2. Connect device via USB
3. Click the green **Run** button in Android Studio
4. Select your device from the list

**Build Release APK (for distribution):**
1. Click **Build** → **Generate Signed Bundle / APK**
2. Select **APK** → Next
3. Create a new keystore or use existing
4. Fill in keystore details
5. Select **release** build variant
6. Click **Finish**

#### 3. Test on Android Emulator

**Create Emulator:**
1. Click **Tools** → **Device Manager**
2. Click **Create Device**
3. Select a device (e.g., Pixel 5)
4. Download a system image (e.g., Android 13)
5. Click **Finish**

**Run on Emulator:**
1. Select emulator from device dropdown
2. Click green **Run** button
3. App will launch in emulator

### Important: Backend Connection for Android

The app needs to connect to your backend. You have two options:

#### Option 1: Use Android Emulator with Local Backend
The config is already set to use `http://10.0.2.2:5000/api` which is the emulator's special IP for localhost.

1. Make sure your Flask backend is running:
   ```bash
   cd backend
   python app.py
   ```

2. The emulator will automatically connect to your local backend

#### Option 2: Use Real Device with Local Backend
1. Find your computer's local IP address:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Mac/Linux: `ifconfig` (look for inet)
   
2. Update `frontend/src/config.js`:
   ```javascript
   if (window.Capacitor && window.Capacitor.isNativePlatform()) {
     return 'http://YOUR_COMPUTER_IP:5000/api'; // e.g., http://192.168.1.100:5000/api
   }
   ```

3. Make sure your phone and computer are on the same WiFi network

4. Rebuild and sync:
   ```bash
   npm run build:mobile
   ```

#### Option 3: Deploy Backend to Cloud (Recommended for Production)
Deploy your Flask backend to a cloud service and update the config:
- Render: https://render.com
- Railway: https://railway.app
- Heroku: https://heroku.com

Then update `config.js`:
```javascript
if (window.Capacitor && window.Capacitor.isNativePlatform()) {
  return 'https://your-backend.onrender.com/api';
}
```

## 🍎 Building for iOS

### Prerequisites
1. **Mac Computer** (required for iOS development)
2. **Xcode** (latest version from Mac App Store)
3. **Apple Developer Account** (free for testing, $99/year for App Store)

### Steps to Build iOS App

#### 1. Add iOS Platform
```bash
cd frontend
npx cap add ios
```

#### 2. Open iOS Project
```bash
npm run ios
```
This opens Xcode with your project.

#### 3. In Xcode

**First Time Setup:**
1. Select your development team in Signing & Capabilities
2. Change bundle identifier if needed
3. Select a deployment target (iOS version)

**Run on Simulator:**
1. Select a simulator from the device dropdown (e.g., iPhone 15)
2. Click the **Play** button
3. App will launch in simulator

**Run on Real Device:**
1. Connect iPhone via USB
2. Trust the computer on your iPhone
3. Select your iPhone from device dropdown
4. Click **Play** button
5. On iPhone: Settings → General → VPN & Device Management → Trust your developer certificate

**Build for App Store:**
1. Select **Any iOS Device** as target
2. Click **Product** → **Archive**
3. Once archived, click **Distribute App**
4. Follow the wizard to upload to App Store Connect

### Backend Connection for iOS
Update `frontend/src/config.js` similar to Android:
```javascript
if (window.Capacitor && window.Capacitor.isNativePlatform()) {
  return 'https://your-backend.onrender.com/api'; // Use deployed backend
}
```

## 🔄 Development Workflow

### Making Changes to Your App

1. **Edit your React code** in `frontend/src/`

2. **Build and sync:**
   ```bash
   npm run build:mobile
   ```

3. **For Android:**
   - Android Studio will detect changes
   - Click **Run** to rebuild and install

4. **For iOS:**
   - Xcode will detect changes
   - Click **Play** to rebuild and install

### Quick Sync (without full rebuild)
If you only changed web assets:
```bash
npm run sync
```

## 📦 App Icons and Splash Screen

### Generate App Icons

1. Create a 1024x1024 PNG icon

2. Use a tool to generate all sizes:
   - https://www.appicon.co/
   - https://capacitorjs.com/docs/guides/splash-screens-and-icons

3. **For Android:**
   - Replace icons in `android/app/src/main/res/mipmap-*/`

4. **For iOS:**
   - Replace icons in `ios/App/App/Assets.xcassets/AppIcon.appiconset/`

### Customize Splash Screen

Edit `capacitor.config.json`:
```json
{
  "plugins": {
    "SplashScreen": {
      "launchShowDuration": 2000,
      "backgroundColor": "#667eea",
      "showSpinner": true,
      "spinnerColor": "#ffffff"
    }
  }
}
```

## 🚀 Publishing to App Stores

### Google Play Store (Android)

1. **Create Google Play Developer Account** ($25 one-time fee)
   - https://play.google.com/console

2. **Build Release APK/AAB:**
   - In Android Studio: Build → Generate Signed Bundle
   - Choose **Android App Bundle** (AAB) for Play Store

3. **Upload to Play Store:**
   - Create new app in Play Console
   - Fill in app details, screenshots, description
   - Upload AAB file
   - Submit for review

### Apple App Store (iOS)

1. **Create Apple Developer Account** ($99/year)
   - https://developer.apple.com

2. **Create App in App Store Connect:**
   - https://appstoreconnect.apple.com
   - Fill in app information

3. **Archive and Upload:**
   - In Xcode: Product → Archive
   - Distribute App → App Store Connect
   - Submit for review

## 🔧 Troubleshooting

### Android Issues

**Gradle Build Failed:**
- Update Gradle: Edit `android/build.gradle`
- Clean project: Build → Clean Project
- Invalidate caches: File → Invalidate Caches

**App Crashes on Launch:**
- Check Logcat in Android Studio
- Verify API URL is correct
- Check CORS settings on backend

**Can't Connect to Backend:**
- Verify backend is running
- Check IP address is correct
- Ensure phone and computer on same network
- Check firewall settings

### iOS Issues

**Code Signing Error:**
- Select your team in Signing & Capabilities
- Use automatic signing for development

**App Crashes:**
- Check Xcode console for errors
- Verify backend URL
- Check CORS settings

## 📱 Testing Checklist

Before releasing, test these features:

- [ ] Personal expense tracking
- [ ] Add/edit/delete transactions
- [ ] Image upload for receipts
- [ ] Year/month filtering
- [ ] Expense charts
- [ ] Friends management
- [ ] Groups creation
- [ ] Shared expense splitting (all 4 types)
- [ ] Balance calculations
- [ ] Settlement recording
- [ ] Offline behavior (if applicable)
- [ ] Different screen sizes
- [ ] Orientation changes

## 🌐 Backend Deployment for Production

For production mobile apps, deploy your backend to a cloud service:

### Recommended: Render.com

1. Create account at https://render.com
2. Create new Web Service
3. Connect your GitHub repo
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add environment variables if needed
6. Deploy!

7. Update `frontend/src/config.js` with your Render URL:
   ```javascript
   return 'https://your-app.onrender.com/api';
   ```

## 📊 App Store Requirements

### Screenshots Needed

**Android (Google Play):**
- At least 2 screenshots
- Recommended: 1080 x 1920 pixels

**iOS (App Store):**
- Screenshots for different device sizes
- 6.5" iPhone (1284 x 2778)
- 5.5" iPhone (1242 x 2208)
- iPad Pro (2048 x 2732)

### App Description

Example:
```
Expense Tracker - Smart Money Management

Track your personal expenses and split costs with friends effortlessly!

FEATURES:
• Personal Expense Tracking
• Bill Image Attachments
• Category-based Organization
• Visual Expense Charts
• Group Expense Splitting
• Multiple Split Types (Equal, Unequal, Percentage, Shares)
• Smart Debt Simplification
• Settlement Tracking
• Beautiful Modern UI

Perfect for:
- Personal finance management
- Trip expense sharing
- Roommate bill splitting
- Group event costs
- Any shared expenses!
```

## 🎉 You're Ready!

Your app is now mobile-ready! Here's what you can do:

1. **Test locally** using Android Studio emulator
2. **Install on your phone** for real-world testing
3. **Deploy backend** to cloud service
4. **Publish to app stores** when ready

## 📚 Additional Resources

- Capacitor Docs: https://capacitorjs.com/docs
- Android Developer Guide: https://developer.android.com
- iOS Developer Guide: https://developer.apple.com
- React Native alternative: https://reactnative.dev

## 🆘 Need Help?

Common commands:
```bash
# Build web app
npm run build

# Sync to mobile platforms
npm run sync

# Build and open Android Studio
npm run android

# Build and open Xcode (Mac only)
npm run ios

# Clean and rebuild
rm -rf dist android ios
npm run build
npx cap add android
npx cap add ios
```

Good luck with your mobile app! 🚀📱
