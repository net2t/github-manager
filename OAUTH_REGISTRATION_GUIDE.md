# 🎯 GitHub OAuth App Registration - Step by Step Guide

## 📋 Your App Details:
- **Application name**: Damadam Dashboard
- **Homepage URL**: cms.brandex.pk
- **Authorization callback URL**: cms.brandex.pk/github-manager-v2.html

---

## 🚀 Step 1: Go to GitHub OAuth Apps Page

1. Open your web browser
2. Go to: https://github.com/settings/applications/new
3. If you're not logged in to GitHub, log in now

---

## 📝 Step 2: Fill in the Application Details

### **Application name**
```
Damadam Dashboard
```
✅ *Type exactly: Damadam Dashboard*

### **Homepage URL**
```
cms.brandex.pk
```
✅ *Type exactly: cms.brandex.pk*

### **Application description** (Optional)
```
GitHub repository management dashboard for Damadam
```
✅ *You can copy this or write your own*

### **Authorization callback URL**
```
cms.brandex.pk/github-manager-v2.html
```
✅ *IMPORTANT: Type exactly: cms.brandex.pk/github-manager-v2.html*

---

## ⚙️ Step 3: Configure Settings

### **Enable Device Flow**
- ❌ **Keep this UNCHECKED** (don't enable)
- We don't need Device Flow for this application

---

## ✅ Step 4: Register the Application

1. Scroll to the bottom of the page
2. Click the **"Register application"** button (green button)
3. Wait for the page to load

---

## 🔑 Step 5: Get Your Credentials

After registration, you'll see your app details. You need two things:

### **Client ID** (Easy to find)
- Look for **"Client ID"** field
- Copy the code (looks like: `Iv1.xxxxxxxxxxxxxxxx`)
- Example: `Iv1.9d1b3c7a8f2e6d4a`

### **Client Secret** (Hidden by default)
1. Click the **"Generate a new client secret"** button
2. You might need to enter your GitHub password
3. A secret will appear (looks like: `ghp_xxxxxxxxxxxxxxxxxxxx`)
4. **Copy this immediately** - you can't see it again!

---

## 📝 Step 6: Save Your Credentials

Write down both codes somewhere safe:

```
Client ID: Iv1.xxxxxxxxxxxxxxxx
Client Secret: ghp_xxxxxxxxxxxxxxxxxxxx
```

---

## 🛠️ Step 7: Update Your Code

Now we need to update 2 files:

### **File 1: github-manager-v2.html**
1. Open the file
2. Find line ~588 that says:
   ```javascript
   const GITHUB_CLIENT_ID = 'Iv1.9d1b3c7a8f2e6d4a';
   ```
3. Replace with your actual Client ID:
   ```javascript
   const GITHUB_CLIENT_ID = 'YOUR_ACTUAL_CLIENT_ID_HERE';
   ```

### **File 2: oauth-server.js**
1. Open the file
2. Find line ~12-13 that says:
   ```javascript
   const GITHUB_CLIENT_ID = 'Iv1.9d1b3c7a8f2e6d4a';
   const GITHUB_CLIENT_SECRET = 'YOUR_CLIENT_SECRET_HERE';
   ```
3. Replace with your actual credentials:
   ```javascript
   const GITHUB_CLIENT_ID = 'YOUR_ACTUAL_CLIENT_ID_HERE';
   const GITHUB_CLIENT_SECRET = 'YOUR_ACTUAL_CLIENT_SECRET_HERE';
   ```

---

## 🌐 Step 8: Update URLs for Your Domain

### **In github-manager-v2.html**
Find line ~590 and update:
```javascript
const OAUTH_BACKEND_URL = 'https://cms.brandex.pk/oauth/github';
```

### **In oauth-server.js**
Update the callback URL to match your domain:
```javascript
redirect_uri: 'https://cms.brandex.pk/github-manager-v2.html'
```

---

## ✅ Step 9: Test Your Setup

1. Upload your files to `cms.brandex.pk`
2. Visit: `https://cms.brandex.pk/github-manager-v2.html`
3. Click "GitHub Login" tab
4. Click "Login with GitHub"
5. If everything is correct, you'll be redirected to GitHub for authorization

---

## 🚨 Troubleshooting

### **If you see "Setup Required":**
- Check if you replaced the Client ID in github-manager-v2.html

### **If you see "Backend Required":**
- Make sure your OAuth server is running on your domain

### **If GitHub says "Invalid redirect_uri":**
- Double-check that the callback URL in GitHub settings exactly matches: `cms.brandex.pk/github-manager-v2.html`

### **If you lost your Client Secret:**
- Go back to your GitHub OAuth App settings
- Click "Generate a new client secret"
- Update the secret in oauth-server.js

---

## 🎉 You're Done!

Once you complete these steps, users will be able to:
1. Visit your Damadam Dashboard
2. Click "Login with GitHub"
3. Authorize the application
4. Access their GitHub repositories through your dashboard

---

## 📞 Need Help?

If you get stuck at any step:
1. Double-check that you copied the codes exactly
2. Make sure there are no extra spaces
3. Ensure your website is accessible at `cms.brandex.pk`
4. Check that both files are uploaded to your server

Good luck! 🚀
