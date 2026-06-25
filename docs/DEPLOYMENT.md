# Deployment Guide

## Backend Deployment (Railway/Render)

### Option 1: Deploy on Railway

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub account

2. **Connect Repository**
   - Click "Create New Project"
   - Select "Deploy from GitHub repo"
   - Authorize and select your repository

3. **Configure Environment Variables**
   - In Railway dashboard, go to Variables
   - Add all variables from `.env.example`:
     ```
     DATABASE_URL=postgresql://...
     SECRET_KEY=your-secret-key
     OPENAI_API_KEY=your-openai-key
     DEBUG=False
     ```

4. **Configure Procfile** (Create in backend root)
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Deploy**
   - Railway automatically deploys on push to main
   - Check deployment status in dashboard

### Option 2: Deploy on Render

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub account

2. **Create Web Service**
   - Click "Create New" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure**
   - Name: my-personal-ai-backend
   - Environment: Python 3.9
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   - Add all variables from `.env.example`
   - Use PostgreSQL database from Render

5. **Deploy**
   - Click "Create Web Service"
   - Render automatically deploys on push

## Frontend Deployment (Vercel)

1. **Create Vercel Account**
   - Go to https://vercel.com
   - Sign up with GitHub account

2. **Import Project**
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Select the frontend directory

3. **Configure**
   - Framework: Vite
   - Root Directory: `./frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Environment Variables**
   - Add environment variable:
     ```
     VITE_API_URL=https://your-backend-url.com
     ```
   - Update API_URL in frontend store files

5. **Deploy**
   - Click "Deploy"
   - Vercel automatically deploys on push to main

## Update Frontend API URL

After deploying backend, update the API URL in frontend:

**frontend/src/store/auth.js** and other store files:
```javascript
const API_URL = 'https://your-backend-url.com'
```

## Database Setup

### Using PostgreSQL on Railway/Render

1. Add PostgreSQL plugin
2. Copy the connection string
3. Set as DATABASE_URL environment variable
4. Tables are created automatically on first run

## SSL & Security

- Both Railway and Render provide free SSL certificates
- Enable HTTPS in settings
- Update CORS_ORIGINS in backend .env to include your Vercel domain

## Domain Configuration

### Vercel Custom Domain
1. In Vercel project settings
2. Go to "Domains"
3. Add your custom domain
4. Add CNAME records to your DNS provider

### Railway/Render Custom Domain
1. In service settings
2. Add custom domain
3. Update DNS records

## Monitoring & Logs

### Railway
- Dashboard shows deployment status
- View logs in "Logs" tab
- Monitor CPU and memory usage

### Render
- Dashboard shows build and deploy status
- View logs in "Logs" section
- Monitor resource usage

### Vercel
- Real-time analytics
- Performance monitoring
- Error tracking

## Troubleshooting

### Backend won't start
- Check environment variables are set
- Check database URL is correct
- Check logs for specific errors

### Frontend deployment fails
- Ensure frontend directory is correct
- Check build command and output directory
- Verify Node version is compatible

### CORS errors
- Update CORS_ORIGINS in backend
- Verify frontend URL matches allowed origins

### Database connection issues
- Test database URL locally
- Check database credentials
- Verify network access settings
