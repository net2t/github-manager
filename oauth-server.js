#!/usr/bin/env node

/**
 * GitHub OAuth Backend Server
 * Run this server to handle OAuth token exchange for GH Manager Pro
 */

const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = 3000;

// GitHub OAuth Configuration
const GITHUB_CLIENT_ID = 'Iv1.9d1b3c7a8f2e6d4a'; // Replace with your actual Client ID
const GITHUB_CLIENT_SECRET = 'YOUR_CLIENT_SECRET_HERE'; // Replace with your actual Client Secret

// Middleware
app.use(cors());
app.use(express.json());

// OAuth token exchange endpoint
app.post('/oauth/github', async (req, res) => {
  const { code, redirect_uri } = req.body;
  
  if (!code) {
    return res.status(400).json({ error: 'Authorization code is required' });
  }
  
  try {
    // Exchange authorization code for access token
    const tokenResponse = await axios.post('https://github.com/login/oauth/access_token', {
      client_id: GITHUB_CLIENT_ID,
      client_secret: GITHUB_CLIENT_SECRET,
      code: code,
      redirect_uri: redirect_uri
    }, {
      headers: {
        'Accept': 'application/json'
      }
    });
    
    const { access_token, token_type, scope } = tokenResponse.data;
    
    if (!access_token) {
      return res.status(400).json({ 
        error: 'Failed to obtain access token',
        details: tokenResponse.data 
      });
    }
    
    // Return the access token to the frontend
    res.json({
      access_token: access_token,
      token_type: token_type,
      scope: scope
    });
    
  } catch (error) {
    console.error('OAuth token exchange error:', error.response?.data || error.message);
    res.status(500).json({ 
      error: 'Token exchange failed',
      details: error.response?.data || error.message 
    });
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'OAuth server is running', timestamp: new Date().toISOString() });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 GitHub OAuth Server running on http://localhost:${PORT}`);
  console.log(`📋 Endpoint: POST http://localhost:${PORT}/oauth/github`);
  console.log(`💚 Health: http://localhost:${PORT}/health`);
  console.log(`\n⚠️  Don't forget to:`);
  console.log(`   1. Replace GITHUB_CLIENT_ID with your actual GitHub OAuth App Client ID`);
  console.log(`   2. Replace GITHUB_CLIENT_SECRET with your actual GitHub OAuth App Client Secret`);
  console.log(`   3. Update OAUTH_BACKEND_URL in github-manager-v2.html if needed`);
});

module.exports = app;
