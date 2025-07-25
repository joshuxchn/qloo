# AWS Amplify Deployment Guide - Qloo Frontend

## Project Overview

This document chronicles the complete deployment process of a Next.js 15 frontend application to AWS Amplify, including all issues encountered and their solutions.

**Project Structure:**
```
qloo/
├── backend/           # Python FastAPI backend
├── frontend/          # Next.js 15 + TypeScript + Tailwind CSS v4
│   ├── app/           # App Router pages
│   ├── components/    # shadcn/ui components
│   └── package.json
├── amplify.yml        # AWS Amplify build configuration
└── README files
```

**Tech Stack:**
- **Frontend Framework:** Next.js 15.2.4 with React 19
- **Styling:** Tailwind CSS v4 (alpha) + shadcn/ui components
- **Language:** TypeScript 5
- **Build Tool:** Turbopack
- **Deployment:** AWS Amplify

## Initial Setup Issues & Solutions

### Issue 1: Frontend Directory Not Found
**Problem:** AWS Amplify couldn't find the `frontend/` directory.
```
Error: cd: frontend: No such file or directory
```

**Root Cause:** The frontend directory wasn't committed to the git repository.

**Solution:**
1. Add frontend directory to git:
   ```bash
   cd /path/to/qloo
   git add frontend/
   git commit -m "Add Next.js frontend application"
   git push origin main
   ```

2. Create proper `amplify.yml` for monorepo structure:
   ```yaml
   version: 1
   frontend:
     phases:
       preBuild:
         commands:
           - cd frontend
           - npm ci
       build:
         commands:
           - npm run build
     artifacts:
       baseDirectory: frontend/.next
       files:
         - '**/*'
     cache:
       paths:
         - frontend/node_modules/**/*
         - frontend/.next/cache/**/*
   ```

### Issue 2: ESLint Compilation Errors
**Problem:** Build failed due to ESLint errors in React components.
```
Error: `'` can be escaped with `&apos;`, `&lsquo;`, `&#39;`, `&rsquo;`.
Error: Unexpected any. Specify a different type.
```

**Root Cause:** Unescaped apostrophes in JSX and TypeScript `any` type usage.

**Solution:** Fixed ESLint errors in `/frontend/app/list-builder/page.tsx`:
```typescript
// Before
<CardDescription>Select how you'd like to build your grocery list</CardDescription>
setInputMethod(value as any)

// After  
<CardDescription>Select how you&apos;d like to build your grocery list</CardDescription>
setInputMethod(value as "manual" | "ai" | "recipe" | "photo")
```

### Issue 3: Node.js Version Compatibility
**Problem:** Build warnings about incompatible Node.js version.
```
npm warn EBADENGINE Unsupported engine {
  package: 'rimraf@6.0.1',
  required: { node: '20 || >=22' },
```

**Solution:** Updated `amplify.yml` to use Node.js 20:
```yaml
preBuild:
  commands:
    - cd frontend
    - nvm use 20  # Changed from 18 to 20
    - npm ci
```

## Major Issue: White Screen of Death

### The Problem
After successful builds, the deployed application showed only a **white screen** with no content, affecting:
- Main landing page
- All React routes (/dashboard, /list-builder, /profile)
- Even test pages with inline styles

**Browser console:** No JavaScript errors visible
**Network tab:** All resources loaded successfully

### Attempted Solutions (Failed)

#### Attempt 1: Tailwind CSS v4 → v3 Downgrade ❌
**Hypothesis:** Tailwind CSS v4 (alpha) was incompatible with AWS Amplify.

**Actions Taken:**
- Downgraded from `tailwindcss: "^4"` to `tailwindcss: "^3.4.16"`
- Added `autoprefixer` and `postcss` configuration
- Converted CSS from Tailwind v4 syntax to v3 syntax
- Updated `package.json` dependencies

**Result:** UI looked "horrendous" and white screen persisted.

**Reversal:** Restored original Tailwind CSS v4 configuration because:
- UI design was severely degraded
- Didn't solve the actual problem
- Tailwind v4 worked fine locally

#### Attempt 2: Next.js Configuration Tweaks ❌
**Actions Taken:**
- Disabled `reactStrictMode`
- Set `images: { unoptimized: true }`
- Tried various experimental flags

**Result:** White screen persisted.

### Root Cause Analysis

**Key Discovery:** Even a simple test page with inline styles showed white screen:
```tsx
// /frontend/app/test/page.tsx
export default function TestPage() {
  return (
    <div style={{
      backgroundColor: 'red',
      color: 'white',
      fontSize: '24px'
    }}>
      TEST PAGE - If you see this, JavaScript is working!
    </div>
  )
}
```

**Conclusion:** The issue was not CSS-related but **JavaScript execution/React hydration failure** in AWS Amplify's SSR environment.

### Final Solution: Static Export ✅

**Approach:** Switch from server-side rendering to static HTML generation.

#### Configuration Changes

1. **Updated `next.config.ts`:**
   ```typescript
   import type { NextConfig } from "next";

   const nextConfig: NextConfig = {
     // Static export for AWS Amplify compatibility
     output: 'export',
     trailingSlash: true,
     poweredByHeader: false,
     images: {
       unoptimized: true, // Required for static export
     },
     reactStrictMode: false,
   };

   export default nextConfig;
   ```

2. **Updated `amplify.yml` build output:**
   ```yaml
   artifacts:
     baseDirectory: frontend/out  # Changed from frontend/.next
     files:
       - '**/*'
   ```

3. **Enhanced build debugging:**
   ```yaml
   build:
     commands:
       - echo "Starting static export build..."
       - npm run build
       - echo "Checking for index.html..."
       - find . -name "index.html" -type f
   ```

#### Results
- **Local build:** Generated static HTML files in `/out` directory
- **File structure:** Proper `index.html`, CSS, and JS files created
- **Deployment:** ✅ Successful with proper content rendering

## Complete File Configurations

### amplify.yml (Final Version)
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - nvm use 20
        - node --version
        - npm --version
        - echo "Installing dependencies..."
        - npm ci
        - echo "Dependencies installed successfully"
    build:
      commands:
        - echo "Starting static export build..."
        - npm run build
        - echo "Build completed, checking output directories..."
        - ls -la
        - echo "Checking out directory..."
        - ls -la out/ || echo "No out directory found"
        - echo "Checking for index.html..."
        - find . -name "index.html" -type f
  artifacts:
    baseDirectory: frontend/out
    files:
      - '**/*'
  cache:
    paths:
      - frontend/node_modules/**/*
      - frontend/.next/cache/**/*
```

### next.config.ts (Final Version)
```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Static export for AWS Amplify compatibility
  output: 'export',
  trailingSlash: true,
  poweredByHeader: false,
  // Critical: Disable image optimization for static export
  images: {
    unoptimized: true,
  },
  // Fix potential hydration issues
  reactStrictMode: false,
};

export default nextConfig;
```

### package.json (Key Dependencies)
```json
{
  "dependencies": {
    "next": "15.2.4",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@radix-ui/react-*": "^1.3.x",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "lucide-react": "^0.525.0",
    "tailwind-merge": "^3.3.1"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4",
    "tailwindcss": "^4",
    "tw-animate-css": "^1.3.5",
    "typescript": "^5"
  }
}
```

## Debugging Techniques Used

### 1. Progressive Isolation
- Started with complex React components
- Moved to simple test pages with inline styles
- Created pure HTML files in `/public`
- Identified the exact failure point

### 2. Build Output Analysis
```bash
# Local testing
npm run build
ls -la out/
cat out/index.html

# AWS Amplify debugging commands in amplify.yml
- find . -name "index.html" -type f
- ls -la out/
```

### 3. Static Test Files
Created `/public/static-test.html` for pure HTML testing:
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background-color: red; color: white; }
    </style>
</head>
<body>
    <h1>STATIC HTML TEST</h1>
    <script>
        document.body.innerHTML += '<p>JavaScript working!</p>';
    </script>
</body>
</html>
```

## Lessons Learned

### 1. AWS Amplify + Next.js SSR Issues
- AWS Amplify's Node.js environment can have issues with Next.js server-side rendering
- Static export (`output: 'export'`) is more reliable for complex React applications
- Always test with the simplest possible components first

### 2. Monorepo Configuration
- Frontend code must be committed to git repository
- Use proper `amplify.yml` with correct directory navigation
- Specify exact Node.js version for consistency

### 3. Modern Framework Compatibility
- Tailwind CSS v4 (alpha) works fine when properly configured
- Next.js 15 + React 19 requires careful configuration for static export
- Always check build output directory (`out` vs `.next`)

### 4. Debugging Strategies
- Use progressive isolation to identify root causes
- Add extensive logging to build process
- Test static HTML files to separate CSS from JavaScript issues
- Don't assume the obvious cause is correct

## Troubleshooting Checklist

### White Screen Issues
1. ✅ Check browser console for JavaScript errors
2. ✅ Verify all static assets are loading (Network tab)
3. ✅ Test with simple inline styles
4. ✅ Create pure HTML test file
5. ✅ Check build output directory structure
6. ✅ Consider static export vs SSR

### Build Failures
1. ✅ Verify correct Node.js version
2. ✅ Check ESLint/TypeScript errors
3. ✅ Ensure all files committed to git
4. ✅ Test build locally first
5. ✅ Check amplify.yml syntax

### Styling Issues
1. ✅ Verify CSS framework version compatibility
2. ✅ Check PostCSS configuration
3. ✅ Test with inline styles first
4. ✅ Validate CSS custom properties

## Final Deployment Configuration

**AWS Amplify Settings:**
- **Build Command:** (handled by amplify.yml)
- **Build Output Directory:** (handled by amplify.yml)
- **Node.js Version:** 20.x (specified in amplify.yml)

**Repository Structure:**
```
qloo/
├── amplify.yml                 # AWS Amplify configuration
├── frontend/
│   ├── next.config.ts         # Static export configuration
│   ├── package.json           # Dependencies
│   ├── app/                   # Next.js App Router
│   ├── components/            # shadcn/ui components
│   ├── public/
│   │   └── static-test.html   # Debug file
│   └── out/                   # Generated static files
└── backend/                   # Python backend (separate deployment)
```

**Commit History Summary:**
1. `7452c32` - Add Next.js frontend application
2. `2b2eda9` - Add AWS Amplify configuration  
3. `9d70e3b` - Fix AWS Amplify build configuration
4. `4be0401` - Fix white screen issue: Downgrade to Tailwind CSS v3 (REVERTED)
5. `1e4da36` - Restore Tailwind CSS v4 and add white screen debugging
6. `00861c3` - Switch to Next.js static export for AWS Amplify ✅

**Final Status:** ✅ Successfully deployed with static export approach.