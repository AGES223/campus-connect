# Campus Connect - Deployment Guide

## Render Deployment (Free Tier)

### Prerequisites
✅ GitHub Desktop installed
✅ Render account (free at render.com)
✅ GitHub account

### Step-by-Step Deployment

#### 1. Setup Git Repository
```bash
git init
git add .
git commit -m "Initial commit - Campus Connect app"
```

#### 2. Create GitHub Repository
1. Open GitHub Desktop
2. Click "Create a New Repository on your hard drive"
3. Choose your CampusConnect folder
4. Publish to GitHub

#### 3. Deploy to Render
1. Go to https://render.com and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select your campus-connect repository
5. Configure:
   - **Name**: campus-connect (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Click "Create Web Service"

#### 4. Environment Variables (Important!)
In Render dashboard → Environment tab, add:
- **SECRET_KEY**: Click "Generate" for a secure random key
- **FLASK_ENV**: `production`

#### 5. Wait for Deployment
- First deployment takes 5-10 minutes
- Render will show build logs
- You'll get a URL like: `https://campus-connect-xxxx.onrender.com`

### Database Options

**Option A: Start with SQLite (Easiest)**
- No additional setup needed
- Good for initial testing
- Database resets on each deployment

**Option B: Add PostgreSQL (Recommended for production)**
1. In Render dashboard: New + → PostgreSQL
2. Choose free tier
3. Copy the "External Database URL"
4. Add as `DATABASE_URL` environment variable

### Post-Deployment
- Test all features (registration, login, events, study groups)
- Share your app URL with users
- Monitor usage in Render dashboard

### Troubleshooting
- Build fails: Check build logs in Render dashboard
- App won't start: Verify environment variables are set
- Database issues: Ensure DATABASE_URL is correct

### Free Tier Limitations
- 750 hours/month (enough for most student projects)
- App sleeps after 15 minutes of inactivity
- Wakes up automatically when accessed (30-60 second delay)

### Updating Your App
1. Make changes to your code
2. Commit and push to GitHub
3. Render automatically redeploys!
