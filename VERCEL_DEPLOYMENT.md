# 🚀 Vercel Deployment Guide

## Issues Fixed

Your Flask app was crashing on Vercel because it wasn't configured for serverless environments. Here's what was fixed:

### 1. **Created `vercel.json` Configuration**
   - Configured Vercel to use `@vercel/python` runtime
   - Set up proper routing for static files and API routes
   - Added `VERCEL=1` environment variable

### 2. **Updated File Upload Handling**
   - Changed upload directory from `uploads/` to `/tmp` for Vercel (serverless functions only have write access to `/tmp`)
   - Added unique filename generation to avoid conflicts in serverless environment

### 3. **Fixed NLTK Data Handling**
   - Configured NLTK to use `/tmp/nltk_data` for Vercel
   - Added fallback mechanisms if NLTK data download fails
   - Improved error handling for serverless environments

### 4. **Created `.vercelignore`**
   - Excludes unnecessary files from deployment (cache, uploads, etc.)

## Deployment Steps

1. **Commit and push your changes:**
   ```bash
   git add .
   git commit -m "Fix Vercel deployment configuration"
   git push
   ```

2. **Deploy to Vercel:**
   - If using Vercel CLI:
     ```bash
     vercel --prod
     ```
   - Or connect your GitHub repository to Vercel dashboard
   - Vercel will automatically detect the `vercel.json` file

3. **Monitor the deployment:**
   - Check Vercel dashboard for build logs
   - Test the health endpoint: `https://your-app.vercel.app/api/health`
   - Test the main page: `https://your-app.vercel.app/`

## Important Notes

### File Uploads
- Files are now stored in `/tmp` directory (Vercel's writable location)
- Files are automatically cleaned up after processing
- Maximum file size: 16MB (configured in `app.py`)

### NLTK Data
- NLTK data will be downloaded to `/tmp/nltk_data` on first use
- If download fails, the app will use fallback keyword extraction
- This may cause a slight delay on first request

### Environment Variables
- `VERCEL=1` is automatically set by Vercel
- No additional environment variables needed for basic functionality

## Troubleshooting

### If deployment still fails:

1. **Check Vercel logs:**
   - Go to your project dashboard → Functions → View logs
   - Look for Python errors or import issues

2. **Verify dependencies:**
   - Ensure all packages in `requirements.txt` are compatible with Python 3.11
   - Some packages might need updates for serverless environments

3. **Test locally with Vercel CLI:**
   ```bash
   npm i -g vercel
   vercel dev
   ```

4. **Common issues:**
   - **NLTK timeout**: First request may be slow while downloading NLTK data
   - **File size limits**: Vercel has a 50MB function size limit
   - **Timeout**: Vercel functions have a 10s timeout on Hobby plan, 60s on Pro

## Next Steps

1. ✅ Deploy to Vercel
2. ✅ Test all endpoints
3. ✅ Monitor function logs
4. ✅ Set up custom domain (optional)
5. ✅ Configure environment variables if needed

## Support

If you encounter issues:
- Check Vercel function logs
- Verify all dependencies are installed
- Test the health endpoint first: `/api/health`
- Ensure file uploads are working with `/tmp` directory

---

**Status**: ✅ Ready for Vercel deployment!

