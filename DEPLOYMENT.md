# Deployment Guide - Seismic Economics on Render

This guide will help you deploy your Seismic Economics app to Render with Python backend.

## What You Get

- **No more file downloads**: Click Save and your data is saved on the server
- **Access from anywhere**: Open the URL from any device and see your projects
- **Password protected**: Simple login page protects your data
- **Shared workspace**: Everyone with the password sees the same projects

## Prerequisites

1. A GitHub account
2. A Render account (free tier is fine) - https://render.com

## Deployment Steps

### Step 1: Push to GitHub

1. Create a new repository on GitHub (e.g., `seismic-economics`)

2. In your terminal, navigate to this folder and run:
```bash
git init
git add .
git commit -m "Initial commit - Seismic Economics with Python backend"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/seismic-economics.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to https://render.com and sign in

2. Click **"New +"** → **"Web Service"**

3. Connect your GitHub repository (authorize Render if needed)

4. Select your `seismic-economics` repository

5. Configure the service:
   - **Name**: `seismic-economics` (or any name you like)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app`
   - **Plan**: Select **Free**

6. Click **"Advanced"** and add environment variables:
   - `SECRET_KEY`: Click "Generate" (for session security)
   - `APP_PASSWORD`: Set your login password (default is `seismic2024`)

7. Click **"Create Web Service"**

8. Wait 2-3 minutes for deployment to complete

### Step 3: Access Your App

1. Once deployed, you'll see a URL like: `https://seismic-economics.onrender.com`

2. Open the URL in your browser

3. Login with the password you set (default: `seismic2024`)

4. Start working! Click the **"💾 Save"** button to save your projects to the server

## How It Works

### Saving Data
- Click **"💾 Save"** button → Data is sent to Python backend → Saved on server
- No file downloads, no manual file replacement
- Refresh the page to see your saved data

### Password Protection
- Simple login page on first visit
- Password stored in environment variable `APP_PASSWORD`
- Session-based authentication (stays logged in)

### Multi-Project Management
- All your existing features work exactly the same
- Create, switch, rename, duplicate, delete projects
- Everyone with access sees the same projects

## Configuration

### Change Password

1. Go to your Render dashboard
2. Select your service
3. Go to **Environment** tab
4. Edit `APP_PASSWORD` variable
5. Click **"Save Changes"**
6. Service will restart automatically

### Custom Domain (Optional)

1. In Render dashboard, go to **Settings**
2. Scroll to **Custom Domain**
3. Add your domain and follow DNS instructions

## Important Notes

### Free Tier Limitations
- **Spins down after 15 minutes of inactivity** (takes ~30 seconds to wake up)
- **750 hours/month** of runtime (enough for personal use)
- To upgrade: Go to Render dashboard → Select your service → Change plan

### Data Persistence
- Your `app.html` file with all project data is stored on Render's disk
- Data persists across deployments and restarts
- **Backup recommendation**: Occasionally download a backup (add a backup button if needed)

### Security
- Change the default password immediately
- Keep your `SECRET_KEY` environment variable secret
- For production use, consider stronger authentication

## Troubleshooting

### Service won't start
- Check logs in Render dashboard
- Verify `requirements.txt` is present
- Ensure `server.py` and `app.html` are in root directory

### Can't login
- Check `APP_PASSWORD` environment variable
- Clear browser cookies and try again
- Check Render logs for errors

### Save button not working
- Check browser console for errors
- Verify you're accessing via the Render URL (not opening local file)
- Check Render logs for backend errors

### App is slow
- Free tier spins down after inactivity
- First request after inactivity takes ~30 seconds
- Upgrade to paid plan for always-on service

## Local Testing (Optional)

Before deploying, you can test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
export APP_PASSWORD=your_password

# Run server
python server.py
```

Then open http://localhost:5000 in your browser.

## Files Created

- `server.py` - Flask backend with password protection and save endpoint
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment configuration
- `app.html` - Updated with backend save functionality

## Support

If you encounter issues:
1. Check Render logs in the dashboard
2. Verify all files are committed to GitHub
3. Ensure environment variables are set correctly

---

**You're all set! Deploy and start using your Seismic Economics app from anywhere!** 🚀
