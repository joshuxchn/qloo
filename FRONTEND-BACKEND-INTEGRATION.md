# 🚀 Frontend-Backend Integration Guide

## Project Overview

This document details the complete integration between the **Next.js frontend** and **Flask backend** for the Qloo Grocery Optimization Platform. The integration connects React components to live PostgreSQL database and Kroger API through REST endpoints.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [API Layer Implementation](#api-layer-implementation)
3. [Frontend Components Integration](#frontend-components-integration)
4. [Authentication Flow](#authentication-flow)
5. [Data Flow Examples](#data-flow-examples)
6. [Error Handling & UX](#error-handling--ux)
7. [Testing & Debugging](#testing--debugging)
8. [Deployment Configuration](#deployment-configuration)
9. [Troubleshooting Guide](#troubleshooting-guide)
10. [Future Enhancements](#future-enhancements)

---

## Architecture Overview

### Tech Stack Integration
```
Frontend (Next.js 15)
├── React 19 + TypeScript
├── Tailwind CSS + Radix UI
├── API Layer (lib/api.ts)
└── Static Build Output

Backend (Flask)
├── Python 3.11+ with Flask
├── PostgreSQL Database
├── Kroger API Integration
├── CORS Enabled
└── Serves Frontend + API

External APIs
├── Kroger Catalog API (Live Products)
├── Kroger Locations API (Store Data)
└── Qloo API (Cultural Recommendations)
```

### Request Flow
```
User Action → React Component → API Function → Flask Endpoint → Database/Kroger API → Response → UI Update
```

---

## API Layer Implementation

### Core API Utility (`/lib/api.ts`)

**Purpose:** Centralized API communication layer that handles all backend interactions.

#### Key Features:
- **Type Safety:** Full TypeScript interfaces matching backend models
- **Error Handling:** Consistent error responses across all endpoints
- **Environment Detection:** Automatic API URL switching (dev/prod)
- **User Management:** Local storage integration for authentication
- **Helper Functions:** Price formatting, inventory status, etc.

#### API Base Configuration:
```typescript
const API_BASE = process.env.NODE_ENV === 'production' 
  ? '/api'  // Production: Same Flask server
  : 'http://localhost:5001/api'  // Development: Proxy to Flask
```

#### Core API Functions:

##### User Management
```typescript
// Create/Login User
export async function loginUser(email: string, password: string)
// Returns: { success: boolean, data?: { user: User }, error?: string }

// Local Storage Management
export function storeUser(user: User): void
export function getStoredUser(): User | null
export function clearStoredUser(): void
```

##### Product Operations
```typescript
// Search Kroger Products
export async function searchProducts(query: string, limit: number = 5)
// Returns: { success: boolean, data?: { products: Product[], count: number } }
```

##### Grocery List Management
```typescript
// Create New List
export async function createGroceryList(userId: string)

// Add Item to List
export async function addItemToList(listId: string, itemName: string, quantity: number = 1)

// Get User's Lists
export async function getUserLists(userId: string)
```

##### Health Check
```typescript
// Backend Status
export async function checkBackendHealth()
// Returns: { status: string, database: string, kroger_api: string }
```

#### Type Definitions:
```typescript
export interface User {
  id: string
  username: string
  email: string
  preferred_location: string
}

export interface Product {
  name: string
  price: number
  promo_price?: number
  brand: string
  upc: string
  size?: string
  inventory: string
  fulfillment_type: string
  location_id: string
}

export interface GroceryList {
  id: string
  user_id: string
  timestamp: string
  items: GroceryItem[]
  total_cost: number
  item_count: number
}
```

---

## Frontend Components Integration

### 1. Profile Page (`/app/profile/page.tsx`)

**Purpose:** User registration and preference setup with backend integration.

#### Integration Features:
- **Real User Creation:** Calls `loginUser()` API function
- **Form Validation:** Client-side validation with backend error handling
- **Auto-redirect:** Automatically redirects to dashboard after successful signup
- **Loading States:** Shows loading spinner during API calls
- **Error Display:** User-friendly error messages from backend

#### Key Changes Made:
```typescript
// Added state management
const [email, setEmail] = useState("")
const [password, setPassword] = useState("")
const [isLoading, setIsLoading] = useState(false)
const [error, setError] = useState<string | null>(null)

// Backend integration function
const handleSubmit = async () => {
  const response = await loginUser(email, password)
  if (response.success && response.data) {
    storeUser(response.data.user)
    router.push('/dashboard')
  } else {
    setError(response.error || "Failed to create profile")
  }
}
```

#### Form Integration:
- **Controlled Components:** All inputs connected to React state
- **Real-time Validation:** Immediate feedback on form errors
- **Submit Handling:** Prevents multiple submissions with loading states

### 2. Dashboard Page (`/app/dashboard/page.tsx`)

**Purpose:** Main application interface with full backend integration.

#### Integration Features:
- **User Authentication Check:** Redirects to profile if not logged in
- **Real Grocery Lists:** Loads actual user data from database
- **Live Product Search:** Integrates with Kroger API for real products
- **Auto-list Creation:** Creates grocery lists for new users automatically
- **Real-time Updates:** Immediate UI updates when adding items

#### Key Changes Made:

##### User Authentication & Data Loading:
```typescript
useEffect(() => {
  const loadUserData = async () => {
    const storedUser = getStoredUser()
    if (!storedUser) {
      router.push('/profile')  // Redirect if not logged in
      return
    }

    // Load real grocery lists from backend
    const listsResponse = await getUserLists(storedUser.id)
    if (listsResponse.success && listsResponse.data) {
      setUserLists(listsResponse.data.lists)
      // Use first existing list or prepare for new one
      if (listsResponse.data.lists.length > 0) {
        const firstList = listsResponse.data.lists[0]
        setCurrentListId(firstList.id)
        setGroceryList(/* map real data to UI format */)
      }
    }
  }
  
  loadUserData()
}, [])
```

##### Smart Item Addition:
```typescript
const addItem = async () => {
  // Auto-create list if none exists
  let listId = currentListId
  if (!listId) {
    const createListResponse = await createGroceryList(user.id)
    if (createListResponse.success) {
      listId = createListResponse.data.list.id
      setCurrentListId(listId)
    }
  }

  // Search for real product in Kroger API
  const searchResponse = await searchProducts(newItem.trim(), 1)
  if (searchResponse.success && searchResponse.data?.products.length > 0) {
    const product = searchResponse.data.products[0]
    
    // Add to backend
    const addResponse = await addItemToList(listId!, newItem.trim(), 1)
    if (addResponse.success) {
      // Update UI with real product data
      const newGroceryItem: GroceryItem = {
        id: product.upc,
        name: product.name,
        price: product.price || 0,
        store: "Kroger",
        inStock: product.inventory !== "OUT_OF_STOCK"
      }
      setGroceryList([...groceryList, newGroceryItem])
      setNewItem("")
    }
  }
}
```

##### UI Enhancements:
- **Loading States:** Spinner in button while processing
- **Error Display:** Red error boxes with specific messages
- **Real-time Feedback:** Console logging for debugging
- **User Welcome:** Shows logged-in user's name in header

---

## Authentication Flow

### Complete User Journey:

#### 1. Initial Visit
```
User visits site → Check localStorage for stored user → Redirect to /profile if none found
```

#### 2. Profile Creation
```
Fill form → Submit → API call to /api/auth/login → User created in PostgreSQL → Store user locally → Redirect to /dashboard
```

#### 3. Dashboard Access
```
Load dashboard → Check stored user → Load user's grocery lists → Display real data from database
```

#### 4. Session Persistence
```
User data stored in localStorage → Persists across browser sessions → Auto-login on return visits
```

### Authentication Implementation:

#### Frontend Storage:
```typescript
// Store user data after login
export function storeUser(user: User): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('qloo_user', JSON.stringify(user))
  }
}

// Retrieve stored user
export function getStoredUser(): User | null {
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem('qloo_user')
    return stored ? JSON.parse(stored) : null
  }
  return null
}
```

#### Backend Integration:
```python
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    # Use existing GroceryOptimizationApp logic
    user = grocery_app.get_or_create_user(email, password)
    
    if user:
        return jsonify({
            'success': True,
            'user': {
                'id': user.user_id,
                'username': user.username,
                'email': user.email,
                'preferred_location': user.preferred_location
            }
        })
```

---

## Data Flow Examples

### Example 1: Adding a Product

#### Step-by-step Flow:
1. **User Input:** Types "milk" in dashboard input field
2. **Frontend Validation:** Checks if input is not empty
3. **API Call:** `searchProducts("milk", 1)` called
4. **Backend Processing:** Flask calls Kroger API to search for milk products
5. **Kroger Response:** Returns real milk products with prices
6. **List Management:** If no list exists, creates one automatically
7. **Add to List:** `addItemToList(listId, "milk", 1)` called
8. **Database Update:** Product added to PostgreSQL grocery_list_items table
9. **UI Update:** Real product appears in frontend with actual Kroger data

#### Network Requests:
```
POST /api/products/search
{
  "query": "milk",
  "limit": 1
}

Response:
{
  "success": true,
  "products": [{
    "name": "Simple Truth Organic® 2% Reduced Fat Milk Half Gallon",
    "price": 4.49,
    "brand": "Simple Truth Organic",
    "upc": "0001111042852",
    "inventory": "HIGH"
  }]
}

POST /api/lists/{list_id}/items
{
  "item_name": "milk",
  "quantity": 1
}
```

### Example 2: Loading User Data

#### Dashboard Initialization:
1. **Page Load:** Dashboard component mounts
2. **Auth Check:** `getStoredUser()` retrieves user from localStorage
3. **API Call:** `getUserLists(userId)` fetches real grocery lists
4. **Database Query:** Backend queries PostgreSQL for user's lists
5. **Data Transform:** Backend converts database records to API format
6. **UI Render:** Frontend displays real grocery lists with items and prices

#### Database Schema Integration:
```sql
-- Data flows through these tables:
users (user_id, username, email, preferred_location)
  ↓
grocery_lists (list_id, user_id, timestamp)
  ↓
grocery_list_items (list_id, name, price, brand, upc, quantity)
```

---

## Error Handling & UX

### Comprehensive Error Strategy:

#### 1. Network Errors
```typescript
// API function wrapper with error handling
async function apiCall<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, options)
    const data = await response.json()
    
    if (response.ok && data.success) {
      return { success: true, data: data }
    } else {
      return { 
        success: false, 
        error: data.error || `HTTP ${response.status}: ${response.statusText}` 
      }
    }
  } catch (error) {
    return { 
      success: false, 
      error: error instanceof Error ? error.message : 'Network error' 
    }
  }
}
```

#### 2. User-Friendly Messages
- **Product Not Found:** "Product 'xyz' not found in Kroger catalog"
- **Network Issues:** "Network error. Please try again."
- **Authentication:** "Email and password are required"
- **Backend Issues:** Specific error messages from Flask API

#### 3. Loading States
```typescript
// Button loading state
{isAddingItem ? (
  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
) : (
  <Plus className="h-4 w-4" />
)}

// Page loading state
if (isLoading) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading your grocery data...</p>
      </div>
    </div>
  )
}
```

#### 4. Error Display Components
```typescript
// Error message display
{error && (
  <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
    <p className="text-red-700 text-sm">{error}</p>
  </div>
)}
```

---

## Testing & Debugging

### Debug Tool (`/app/debug/page.tsx`)

**Purpose:** Comprehensive testing interface for API functions.

#### Features:
- **Individual Function Testing:** Test each API endpoint separately
- **Full Workflow Testing:** Complete user journey simulation
- **Real-time Results:** Console-style output with timestamps
- **Error Diagnosis:** Identifies exactly where failures occur

#### Test Functions:
```typescript
// Backend Health Check
const testBackendHealth = async () => {
  const response = await checkBackendHealth()
  // Logs: Backend Status, Database Connection, Kroger API Status
}

// Product Search Test
const testProductSearch = async () => {
  const response = await searchProducts(testItem, 1)
  // Logs: Search results, product details, pricing
}

// Full Workflow Test
const testFullWorkflow = async () => {
  await testBackendHealth()
  await testProductSearch()
  await testAddItem()
  // Complete end-to-end test
}
```

### Console Debugging

#### Added Comprehensive Logging:
```typescript
const addItem = async () => {
  console.log("🚀 addItem called with:", { newItem: newItem.trim(), user: user?.username, currentListId })
  
  // List creation logging
  if (!listId) {
    console.log("No existing list found, creating new list for user:", user.id)
    // ... create list
    console.log("Created new list with ID:", listId)
  }

  // Product search logging
  console.log("Searching for product:", newItem.trim())
  // ... search
  console.log("Found product:", product.name, "- $" + product.price)
  
  // Backend integration logging
  console.log("Adding product to list:", listId)
  // ... add to list
  console.log("Successfully added item to backend")
}
```

### Testing Workflow

#### Quick Test Process:
1. **Start Backend:** `cd backend && python3 app.py`
2. **Visit Debug Page:** `http://localhost:5001/debug`
3. **Run Full Workflow Test:** Click "🚀 Test Full Workflow"
4. **Verify Results:** Check console output and database

#### Manual Testing:
1. **Profile Creation:** Test user signup with various inputs
2. **Dashboard Loading:** Verify data loads correctly
3. **Product Addition:** Test adding various products
4. **Error Scenarios:** Test with invalid inputs, network issues
5. **Cross-browser Testing:** Verify localStorage works across browsers

---

## Deployment Configuration

### Production Setup

#### Build Process:
```bash
# Frontend build
cd frontend
npm run build  # Creates optimized static files in /out

# Backend serves both frontend and API
cd backend
python3 app.py  # Serves on http://localhost:5001
```

#### Flask Configuration:
```python
# Serves static frontend files
app = Flask(
    __name__,
    static_folder='../frontend/out',  # Next.js build output
    static_url_path=''                # Serve at root URL
)

# API routes at /api/*
@app.route('/api/health', methods=['GET'])
@app.route('/api/auth/login', methods=['POST'])
# ... other API routes

# Catch-all for React routing
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    # Serve static files or fallback to index.html
```

### Environment Configuration

#### Development Mode:
```typescript
// Frontend calls backend on different port
const API_BASE = 'http://localhost:5001/api'

// Run separately:
// Terminal 1: cd backend && python3 app.py
// Terminal 2: cd frontend && npm run dev
```

#### Production Mode:
```typescript
// Frontend served by same Flask server
const API_BASE = '/api'

// Single server:
// cd backend && python3 app.py
// Visit: http://localhost:5001
```

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. "Submit button not responsive"
**Symptoms:** Button clicks don't trigger API calls
**Cause:** Missing `currentListId` for new users
**Solution:** Auto-create grocery list if none exists

#### 2. "Product not found" errors
**Symptoms:** All product searches fail
**Cause:** Kroger API connection issues
**Solution:** Check environment variables, test with debug tool

#### 3. "User not found" on dashboard
**Symptoms:** Dashboard redirects to profile repeatedly
**Cause:** localStorage cleared or user data corrupted
**Solution:** Clear localStorage and recreate profile

#### 4. CORS errors in development
**Symptoms:** API calls blocked by browser
**Cause:** Frontend and backend on different ports
**Solution:** Ensure Flask-CORS is enabled in backend

#### 5. TypeScript errors
**Symptoms:** Build failures or type errors
**Cause:** API response types don't match interfaces
**Solution:** Update type definitions in `/lib/api.ts`

### Debug Commands

#### Backend Health Check:
```bash
curl http://localhost:5001/api/health
```

#### Database Verification:
```sql
SELECT * FROM users;
SELECT * FROM grocery_lists;
SELECT * FROM grocery_list_items;
```

#### Clear Browser Data:
```javascript
// In browser console
localStorage.clear()
location.reload()
```

---

## Future Enhancements

### Planned Integrations

#### 1. List Builder Page Enhancement
```typescript
// Connect AI prompts to real product search
const handleAIGenerate = async () => {
  const prompt = "healthy meals for family of 4"
  const aiResponse = await generateMealPlan(prompt)
  
  // Search for each suggested item in Kroger API
  for (const item of aiResponse.items) {
    const products = await searchProducts(item.name, 1)
    // Add to list with AI-suggested quantities
  }
}
```

#### 2. Real Store Integration
```typescript
// Use Kroger Locations API for actual stores
const getNearbyStores = async (zipCode: string) => {
  const response = await fetch('/api/stores/nearby', {
    body: JSON.stringify({ zipCode, radius: 10 })
  })
  // Replace mock store data with real Kroger locations
}
```

#### 3. User Preferences Backend
```python
# New API endpoint for profile data
@app.route('/api/profile/update', methods=['POST'])
def update_profile():
    data = request.get_json()
    # Save dietary restrictions, cuisines, allergies to database
    # Update user preferences in PostgreSQL
```

#### 4. Real-time Price Updates
```typescript
// WebSocket integration for live price changes
const priceSocket = new WebSocket('ws://localhost:5001/prices')
priceSocket.onmessage = (event) => {
  const priceUpdate = JSON.parse(event.data)
  // Update product prices in real-time
}
```

#### 5. Qloo Cultural Integration
```python
# Enhanced recommendations with Qloo API
@app.route('/api/recommendations/cultural', methods=['POST'])
def get_cultural_recommendations():
    user_profile = request.get_json()
    qloo_response = qloo_api.get_recommendations(user_profile)
    # Return culturally-relevant grocery suggestions
```

### Code Organization Improvements

#### 1. Custom Hooks
```typescript
// useGroceryList hook for state management
const useGroceryList = (userId: string) => {
  const [lists, setLists] = useState<GroceryList[]>([])
  const [loading, setLoading] = useState(true)
  
  const addItem = async (item: string) => {
    // Encapsulate all addItem logic
  }
  
  return { lists, loading, addItem }
}
```

#### 2. API Response Caching
```typescript
// Cache API responses for better performance
const apiCache = new Map<string, { data: any, timestamp: number }>()

const getCachedResponse = (key: string, maxAge: number = 300000) => {
  const cached = apiCache.get(key)
  if (cached && Date.now() - cached.timestamp < maxAge) {
    return cached.data
  }
  return null
}
```

#### 3. Error Boundary Components
```typescript
// Global error handling for API failures
class APIErrorBoundary extends React.Component {
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    if (error.message.includes('API')) {
      // Handle API-specific errors
      this.setState({ hasApiError: true })
    }
  }
}
```

---

## Summary

This integration successfully connects a modern React frontend with a Flask backend, providing:

- ✅ **Real User Management** with PostgreSQL persistence
- ✅ **Live Product Data** from Kroger API integration
- ✅ **Type-Safe API Layer** with comprehensive error handling
- ✅ **Professional UX** with loading states and error messages
- ✅ **Auto-scaling Lists** that create themselves as needed
- ✅ **Debug Tools** for easy troubleshooting
- ✅ **Production Ready** deployment configuration

The platform now provides a complete grocery optimization experience with real data, real users, and real products, laying the foundation for advanced AI-powered features.

**Total Integration Points:** 6 API endpoints, 3 major components, 1 utility layer, full authentication flow
**Technologies Connected:** Next.js ↔ Flask ↔ PostgreSQL ↔ Kroger API
**User Experience:** Seamless, real-time, error-resilient grocery list management