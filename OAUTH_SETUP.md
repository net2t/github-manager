# GitHub OAuth Setup Guide

This guide will help you set up GitHub OAuth authentication for GH Manager Pro.

## 🚀 Quick Setup

### 1. Create GitHub OAuth App

1. Go to [GitHub Settings > Developer settings > OAuth Apps](https://github.com/settings/applications/new)
2. Click **"New OAuth App"**
3. Fill in the details:
   - **Application name**: `GH Manager Pro`
   - **Homepage URL**: `http://localhost:8000`
   - **Authorization callback URL**: `http://localhost:8000/github-manager-v2.html`
4. Click **"Register application"**

### 2. Get Your Credentials

After creating the app, you'll see:
- **Client ID**: Copy this (e.g., `Iv1.9d1b3c7a8f2e6d4a`)
- **Client Secret**: Generate and copy this

### 3. Configure Frontend

Edit `github-manager-v2.html` and update:

```javascript
// Line ~588
const GITHUB_CLIENT_ID = 'YOUR_ACTUAL_CLIENT_ID_HERE';

// Line ~590 (optional, if your backend runs on different port)
const OAUTH_BACKEND_URL = 'http://localhost:3000/oauth/github';
```

### 4. Set Up Backend Server

```bash
# Install dependencies
npm install

# Start the OAuth server
npm start
```

The server will run on `http://localhost:3000`

### 5. Configure Backend

Edit `oauth-server.js` and update:

```javascript
// Line ~12
const GITHUB_CLIENT_ID = 'YOUR_ACTUAL_CLIENT_ID_HERE';

// Line ~13
const GITHUB_CLIENT_SECRET = 'YOUR_ACTUAL_CLIENT_SECRET_HERE';
```

### 6. Start Web Server

```bash
# Start the web server for the frontend
python -m http.server 8000
```

### 7. Test OAuth Login

1. Open `http://localhost:8000/github-manager-v2.html`
2. Click **"GitHub Login"** tab
3. Click **"Login with GitHub"**
4. Authorize the application on GitHub
5. You should be logged in!

## 🔧 Detailed Configuration

### Frontend Configuration

The frontend handles:
- OAuth URL construction
- State parameter security
- Redirect handling
- Token exchange with backend

### Backend Server

The backend server:
- Exchanges authorization code for access token
- Handles GitHub API communication
- Provides secure token storage
- Returns access token to frontend

### Security Features

- **CSRF Protection**: Random state parameters
- **Token Validation**: Proper GitHub OAuth flow
- **CORS Support**: Cross-origin requests allowed
- **Error Handling**: Comprehensive error messages

## 🛠️ Troubleshooting

### Common Issues

**"Setup Required" Error**
- Check if Client ID is properly configured
- Ensure GitHub OAuth App is created

**"Backend Required" Error**
- Start the OAuth server: `npm start`
- Check if backend URL is correct

**"Backend error"**
- Verify Client Secret is correct
- Check if callback URL matches GitHub OAuth App settings
- Ensure backend server is running

**"Invalid redirect_uri"**
- Make sure callback URL in GitHub OAuth App matches exactly:
  `http://localhost:8000/github-manager-v2.html`

### Debug Mode

Enable console logging in browser to see detailed OAuth flow information.

## 📝 Environment Variables (Optional)

For production, you can use environment variables:

```bash
export GITHUB_CLIENT_ID="your_client_id"
export GITHUB_CLIENT_SECRET="your_client_secret"
export PORT=3000
```

Then update `oauth-server.js` to use `process.env.GITHUB_CLIENT_ID`.

## 🔒 Security Notes

- Never expose Client Secret in frontend code
- Use HTTPS in production
- Regularly rotate your Client Secret
- Limit OAuth App permissions to only what's needed

## 🚀 Production Deployment

For production deployment:

1. Use HTTPS URLs
2. Set proper environment variables
3. Use a production-grade server (PM2, Docker, etc.)
4. Implement proper session management
5. Add rate limiting and security headers

## 📞 Support

If you encounter issues:

1. Check browser console for errors
2. Verify all configuration values
3. Ensure both servers are running
4. Check GitHub OAuth App settings

Happy coding! 🎉
