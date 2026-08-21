# VISION LOOP — GITHUB ACCOUNT & GITHUB.IO PAGES DEPLOYMENT GUIDE
*Complete Step-by-Step Guide for Creating the GitHub Account, Pushing Code, and Hosting the Live Website*

---

## 🐙 1. GitHub Account & Organization Creation

### Step 1: Sign up on GitHub
1. Open **[https://github.com/signup](https://github.com/signup)**
2. Enter the corporate email: **`visionloop.india@gmail.com`** (or your preferred email).
3. Choose a username:
   * Recommended Organization / Username: **`visionloop-org`** or **`visionloop-india`** or **`visionloop`**.
4. Set a strong password and complete the verification captcha.

---

## 🚀 2. Create the Remote Repository on GitHub

1. Once logged in, click **"New Repository"** (or visit `https://github.com/new`).
2. **Repository Name:** `visionloop` (or `visionloop.github.io` for user-root site).
3. **Visibility:** `Public` (or `Private` with GitHub Pages Pro).
4. **Initialize with README:** *Unchecked* (we already have a complete codebase and docs).
5. Click **"Create repository"**.

---

## 💻 3. Push Local Codebase to GitHub

Run the following standard Git commands in PowerShell inside `d:\VisionLoop`:

```powershell
# 1. Initialize Git repository if not already initialized
git init

# 2. Add all files (codebase, packages, docs, and datasets)
git add .

# 3. Create the initial release commit
git commit -m "feat: initial release of Vision Loop autonomous asset leasing platform"

# 4. Set default branch to main
git branch -M main

# 5. Link to your new GitHub repository (replace with your actual GitHub username)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/visionloop.git

# 6. Push code to GitHub
git push -u origin main
```

---

## 🌐 4. Enable Free Live Hosting on GitHub Pages (`github.io`)

1. Open your repository on GitHub: `https://github.com/YOUR_GITHUB_USERNAME/visionloop`.
2. Click **Settings** (top right gear icon).
3. In the left sidebar under *Code and automation*, click **Pages**.
4. Under **Build and deployment -> Branch**:
   * Select branch: **`main`**.
   * Select folder: **`/docs`** *(This is where `index.html`, `styles.css`, and `app.js` are stored!)*.
5. Click **Save**.
6. GitHub will build the site and deploy your live URL within 60 seconds:
   $$\mathbf{https://YOUR\_GITHUB\_USERNAME.github.io/visionloop}$$

---

## 🏷️ 5. Optional: Link Custom Domain (`visionloop.in`)

To connect `visionloop.in` to your GitHub Pages:
1. In **Settings -> Pages -> Custom domain**, enter `visionloop.in`.
2. Add DNS `A` records in your registrar (GoDaddy / Cloudflare / Namecheap) pointing to GitHub Pages IPs:
   * `185.199.108.153`
   * `185.199.109.153`
   * `185.199.110.153`
   * `185.199.111.153`
3. Enable **Enforce HTTPS** (free automated SSL certificate provided by GitHub).
