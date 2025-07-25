# 🧪 Frontend-Backend Integration Test Guide

## How to Test Your Connected Application

### Step 1: Start Your Backend
```bash
cd backend
python3 app.py
```
✅ **Expected:** Flask server starts on http://localhost:5001

### Step 2: Start Your Frontend (Development Mode)
```bash
cd frontend
npm run dev
```
✅ **Expected:** Next.js dev server starts on http://localhost:3000

**OR** 

### Test Production Mode (Recommended)
Since your frontend is built and served by Flask:

1. **Build frontend:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Start Flask (serves both frontend and API):**
   ```bash
   cd backend  
   python3 app.py
   ```

3. **Visit:** http://localhost:5001

## Testing Workflow

### 1. Profile Creation
1. Go to **http://localhost:5001/profile**
2. Fill in:
   - **Email:** `test@example.com`
   - **Password:** `testpass123` 
   - Select preferences
3. Click **"Create Profile & Continue"**

✅ **Expected Results:**
- User created in your PostgreSQL database
- Redirected to dashboard
- Welcome message shows username

### 2. Dashboard - Add Items
1. In the **grocery list** tab
2. Type: `milk` → Press Enter
3. Type: `bread` → Press Enter
4. Type: `apples` → Press Enter

✅ **Expected Results:**
- Real products fetched from Kroger API
- Items appear with real prices
- Data saved to database

### 3. Verify Data in Database
```sql
-- Check users table
SELECT * FROM users;

-- Check grocery lists
SELECT * FROM grocery_lists;

-- Check list items  
SELECT * FROM grocery_list_items;
```

## API Endpoints Being Tested

### ✅ Working Endpoints
- `POST /api/auth/login` - User creation/login
- `POST /api/products/search` - Kroger product search
- `POST /api/lists` - Create grocery list  
- `POST /api/lists/<id>/items` - Add items to list
- `GET /api/lists/user/<user_id>` - Get user's lists

### 🔄 Frontend Pages Using Backend
- **Profile Page** → Creates users via `/api/auth/login`
- **Dashboard** → Loads lists, adds items via multiple endpoints
- **Static Serving** → Frontend served by Flask at root URL

## Troubleshooting

### Backend Issues
- **Port 5001 in use:** Change port in `app.py`
- **Database connection:** Check PostgreSQL is running
- **Kroger API:** Check environment variables in `.env`

### Frontend Issues  
- **API calls fail:** Check `API_BASE` in `lib/api.ts`
- **Build errors:** Run `npm install` and `npm run build`
- **CORS errors:** Flask-CORS should handle this automatically

### Integration Issues
- **User not found:** Clear localStorage and recreate profile
- **Items not loading:** Check browser network tab for API errors
- **Real-time issues:** Refresh page to reload data from backend

## What's Connected vs. Mock Data

### ✅ **Connected to Backend:**
- User authentication and creation
- Adding grocery items (real Kroger products)
- Grocery list management
- Product search with real prices

### 🔄 **Still Mock Data:**
- Store locations (uses hardcoded nearby stores)
- Health scores and alternatives
- Analytics and insights
- Cultural recommendations

## Next Steps to Enhance

1. **List Builder Page**: Connect AI prompts to product search
2. **Store Integration**: Use Kroger Locations API for real stores  
3. **User Preferences**: Save dietary restrictions to backend
4. **Real-time Updates**: WebSocket for live price updates
5. **Qloo Integration**: Cultural recommendations via Qloo API