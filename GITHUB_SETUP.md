# GitHub Setup Instructions

## Step 1: Create a New Repository on GitHub

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **+** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `fang-resume-enhancer` (or any name you prefer)
   - **Description**: "Resume enhancement web application for FANG companies"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

## Step 2: Copy the Repository URL

After creating the repository, GitHub will show you a page with setup instructions. Copy the repository URL. It will look like:
- `https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git`
- Or: `git@github.com:YOUR-USERNAME/YOUR-REPO-NAME.git`

## Step 3: Add Remote and Push

Once you have the URL, run these commands (replace with your actual URL):

```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
git branch -M main
git push -u origin main
```

## Alternative: Quick Setup Script

If you provide me with your GitHub repository URL, I can run these commands for you automatically!

---

**Note**: If you haven't configured Git with your GitHub credentials, you may need to:
- Set up SSH keys, OR
- Use a Personal Access Token for HTTPS authentication

For HTTPS push, GitHub now requires a Personal Access Token instead of password:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` permissions
3. Use the token as your password when pushing

