# Google OAuth Setup Guide

## Error: redirect_uri_mismatch

This error occurs when the redirect URI used by the application doesn't match the authorized redirect URIs in Google Cloud Console.

## Solution

### Step 1: Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/
2. Select your project

### Step 2: Navigate to OAuth 2.0 Client IDs
1. Go to **APIs & Services** → **Credentials**
2. Find your **OAuth 2.0 Client ID** (the one used in your app)
3. Click on it to edit

### Step 3: Add Authorized Redirect URIs
Add these URIs to the **Authorized redirect URIs** section:

```
http://localhost:3000
http://localhost:5173
http://127.0.0.1:3000
http://127.0.0.1:5173
```

**Important:** 
- Add ALL the URIs that match your development environment
- The URI must match EXACTLY (including http vs https, port number, trailing slashes)
- If your app runs on a different port, add that port too

### Step 4: Save and Wait
1. Click **Save**
2. Wait 2-5 minutes for changes to propagate
3. Try logging in again

## Finding Your Current Redirect URI

The redirect URI used by `@react-oauth/google` is:
- `window.location.origin` (e.g., `http://localhost:3000`)

Check your browser's address bar to see what port your app is running on.

## Environment Variable

Make sure you have `VITE_GOOGLE_CLIENT_ID` set in your `.env` file:

```env
VITE_GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
```

## Common Issues

1. **Wrong port**: Make sure the port in the redirect URI matches your app's port
2. **http vs https**: Use `http://` for local development, `https://` for production
3. **Trailing slash**: Don't add trailing slashes (use `http://localhost:3000` not `http://localhost:3000/`)
4. **Changes not applied**: Wait a few minutes after saving


