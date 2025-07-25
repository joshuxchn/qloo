/**
 * API utility functions for connecting frontend to the Flask backend
 * All backend API calls go through these functions
 */

// Base API URL - this will be your Flask server
const API_BASE = process.env.NODE_ENV === 'production' 
  ? '/api'  // In production, served by same Flask server
  : 'http://localhost:5001/api'  // In development, proxy to Flask

// Type definitions matching your backend
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

export interface GroceryItem {
  name: string
  price: number
  brand: string
  upc: string
  quantity: number
  subtotal: number
}

// API Response types
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

/**
 * Generic API call function with error handling
 */
async function apiCall<T>(
  endpoint: string, 
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    })

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

/**
 * USER AUTHENTICATION
 * Connect to your backend user management
 */
export async function loginUser(email: string, password: string): Promise<ApiResponse<{ user: User }>> {
  return apiCall('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

/**
 * PRODUCT SEARCH
 * Connect to your Kroger API integration
 */
export async function searchProducts(query: string, limit: number = 5): Promise<ApiResponse<{ products: Product[], count: number }>> {
  return apiCall('/products/search', {
    method: 'POST',
    body: JSON.stringify({ query, limit }),
  })
}

/**
 * GROCERY LIST MANAGEMENT
 * Connect to your list management functions
 */
export async function createGroceryList(userId: string): Promise<ApiResponse<{ list: { id: string, user_id: string, timestamp: string, items: any[] } }>> {
  return apiCall('/lists', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId }),
  })
}

export async function addItemToList(listId: string, itemName: string, quantity: number = 1): Promise<ApiResponse<{ item: GroceryItem }>> {
  return apiCall(`/lists/${listId}/items`, {
    method: 'POST',
    body: JSON.stringify({ item_name: itemName, quantity }),
  })
}

export async function getUserLists(userId: string): Promise<ApiResponse<{ lists: GroceryList[], count: number }>> {
  return apiCall(`/lists/user/${userId}`)
}

/**
 * HEALTH CHECK
 * Test backend connectivity
 */
export async function checkBackendHealth(): Promise<ApiResponse<{ status: string, database: string, kroger_api: string }>> {
  return apiCall('/health')
}

/**
 * UTILITY FUNCTIONS
 */

/**
 * Format price for display
 */
export function formatPrice(price: number | null | undefined): string {
  if (price === null || price === undefined) return 'N/A'
  return `$${price.toFixed(2)}`
}

/**
 * Format inventory status for display
 */
export function formatInventory(inventory: string): { text: string, color: string } {
  switch (inventory.toUpperCase()) {
    case 'HIGH':
      return { text: 'In Stock', color: 'text-green-600' }
    case 'MEDIUM':
      return { text: 'Limited', color: 'text-yellow-600' }
    case 'LOW':
      return { text: 'Low Stock', color: 'text-orange-600' }
    case 'OUT_OF_STOCK':
      return { text: 'Out of Stock', color: 'text-red-600' }
    default:
      return { text: 'Unknown', color: 'text-gray-600' }
  }
}

/**
 * Store user data locally (simple implementation)
 */
export function storeUser(user: User): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('qloo_user', JSON.stringify(user))
  }
}

export function getStoredUser(): User | null {
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem('qloo_user')
    return stored ? JSON.parse(stored) : null
  }
  return null
}

export function clearStoredUser(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('qloo_user')
  }
}