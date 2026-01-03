# Quick Start: Test Your Mobile App Now!

## ✅ What's Already Done

Your web app has been converted to a mobile app! Here's what's set up:

- ✓ Capacitor installed and configured
- ✓ Android platform added
- ✓ Build scripts created
- ✓ API configured for mobile
- ✓ App built and ready to test

## 🚀 Test on Android Emulator (Easiest Way)

### Step 1: Install Android Studio
1. Download: https://developer.android.com/studio
2. Run installer with default settings
3. Open Android Studio
4. Complete the setup wizard (accept licenses, download SDK)

### Step 2: Open Your App in Android Studio
```bash
cd C:\Users\ganea\Antigravity\frontend
npm run android
```

This command will:
- Build your web app
- Sync to Android
- Open Android Studio automatically

### Step 3: Create an Emulator (First Time Only)
In Android Studio:
1. Click **Tools** → **Device Manager**
2. Click **Create Device**
3. Select **Pixel 5** → Next
4. Download **Android 13** (Tiramisu) → Next
5. Click **Finish**

### Step 4: Run the App
1. Wait for Gradle sync to finish (check bottom status bar)
2. Select your emulator from the device dropdown (top toolbar)
3. Click the green **▶ Run** button
4. Wait for emulator to start and app to install
5. Your app will launch! 🎉

### Step 5: Make Sure Backend is Running
The app needs your Flask backend:
```bash
cd C:\Users\ganea\Antigravity\backend
python app.py
```

The emulator is configured to connect to `http://10.0.2.2:5000/api` which automatically points to your localhost.

## 📱 Test on Your Real Android Phone

### Step 1: Enable Developer Mode
On your Android phone:
1. Go to **Settings** → **About Phone**
2. Tap **Build Number** 7 times
3. Go back to **Settings** → **Developer Options**
4. Enable **USB Debugging**

### Step 2: Update Backend URL
Edit `C:\Users\ganea\Antigravity\frontend\src\config.js`:

1. Find your computer's IP address:
   ```bash
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

2. Update the config:
   ```javascript
   if (window.Capacitor && window.Capacitor.isNativePlatform()) {
     return 'http://YOUR_IP_HERE:5000/api'; // e.g., http://192.168.1.100:5000/api
   }
   ```

3. Rebuild:
   ```bash
   npm run build:mobile
   ```

### Step 3: Connect Phone and Run
1. Connect phone to computer via USB
2. On phone, tap "Allow USB debugging" when prompted
3. In Android Studio, select your phone from device dropdown
4. Click **▶ Run**
5. App installs and launches on your phone!

### Step 4: Make Sure Backend is Accessible
1. Make sure Flask backend is running
2. Make sure phone and computer are on same WiFi network
3. Test backend URL in phone's browser: `http://YOUR_IP:5000/api/transactions`

## 🎯 Quick Test Checklist

Once the app is running, test these features:

### Personal Expense Tracker
- [ ] Click "💰 Expense Tracker"
- [ ] Add a transaction
- [ ] View the balance
- [ ] Check the expense chart

### Group Expense Splitting
- [ ] Click "👥 Split Expenses"
- [ ] Add a friend (e.g., "Test User")
- [ ] Create a group (e.g., "Test Group")
- [ ] Add a shared expense
- [ ] View balances
- [ ] Record a settlement

## 🔄 Making Changes

When you update your code:

1. **Edit your React files** in `frontend/src/`

2. **Rebuild and sync:**
   ```bash
   cd frontend
   npm run build:mobile
   ```

3. **In Android Studio:**
   - Click the green **▶ Run** button again
   - App will rebuild and reinstall

## 📦 Build APK for Sharing

Want to share the app with friends?

### Build Debug APK (for testing)
In Android Studio:
1. Click **Build** → **Build Bundle(s) / APK(s)** → **Build APK(s)**
2. Wait for build to complete
3. Click "locate" in the notification
4. APK is at: `frontend/android/app/build/outputs/apk/debug/app-debug.apk`
5. Share this file - anyone can install it!

### Install APK on Phone
1. Transfer APK to phone
2. Open APK file
3. Allow "Install from unknown sources" if prompted
4. Install and enjoy!

## ⚠️ Important Notes

### Backend Connection
- **Emulator**: Uses `http://10.0.2.2:5000/api` (already configured)
- **Real Device**: Needs your computer's IP address
- **Production**: Deploy backend to cloud (see MOBILE_DEPLOYMENT.md)

### CORS Settings
Your Flask backend needs to allow mobile app connections. It's already configured with CORS, but if you have issues, check `backend/app.py`:
```python
from flask_cors import CORS
CORS(app)  # This should be present
```

### Firewall
If the app can't connect to backend:
1. Check Windows Firewall
2. Allow Python through firewall
3. Or temporarily disable firewall for testing

## 🎨 Customize Your App

### Change App Name
Edit `frontend/capacitor.config.json`:
```json
{
  "appName": "My Expense App"
}
```

### Change App Icon
1. Create 1024x1024 PNG icon
2. Use https://www.appicon.co/ to generate all sizes
3. Replace icons in `frontend/android/app/src/main/res/mipmap-*/`

### Change Splash Screen Color
Edit `frontend/capacitor.config.json`:
```json
{
  "plugins": {
    "SplashScreen": {
      "backgroundColor": "#YOUR_COLOR"
    }
  }
}
```

## 🐛 Troubleshooting

### "Gradle sync failed"
- Wait for it to finish (can take 5-10 minutes first time)
- Click **File** → **Invalidate Caches** → **Invalidate and Restart**

### "App crashes on launch"
- Check Logcat in Android Studio (bottom panel)
- Verify backend is running
- Check API URL in config.js

### "Can't connect to backend"
- Verify Flask is running: `python app.py`
- Check IP address is correct
- Ensure phone and computer on same WiFi
- Try accessing backend URL in phone's browser

### "Android Studio won't open"
- Run manually: `npx cap open android`
- Or open `frontend/android` folder in Android Studio

## 📚 Next Steps

1. ✅ Test app on emulator/device
2. ✅ Verify all features work
3. 📝 Deploy backend to cloud (see MOBILE_DEPLOYMENT.md)
4. 🎨 Customize app icon and name
5. 📱 Build release APK
6. 🚀 Publish to Google Play Store (optional)

## 🆘 Need Help?

Check these files:
- `MOBILE_DEPLOYMENT.md` - Complete deployment guide
- `EXPENSE_SPLITTING_GUIDE.md` - Feature documentation
- `README.md` - General app information

Common commands:
```bash
# Build and open Android Studio
npm run android

# Just build and sync
npm run build:mobile

# Sync without rebuilding
npm run sync
```

## 🎉 You're Ready!

Your expense tracker is now a mobile app! Start testing and enjoy! 📱✨
