"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { 
  checkBackendHealth, 
  searchProducts, 
  loginUser, 
  getStoredUser,
  createGroceryList,
  addItemToList 
} from "@/lib/api"

export default function DebugPage() {
  const [testItem, setTestItem] = useState("milk")
  const [testEmail, setTestEmail] = useState("debug@test.com")
  const [testPassword, setTestPassword] = useState("debug123")
  const [results, setResults] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const log = (message: string) => {
    console.log(message)
    setResults(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`])
  }

  const clearResults = () => {
    setResults([])
  }

  const testBackendHealth = async () => {
    setIsLoading(true)
    log("🩺 Testing backend health...")
    
    try {
      const response = await checkBackendHealth()
      if (response.success && response.data) {
        log(`✅ Backend Status: ${response.data.status}`)
        log(`✅ Database: ${response.data.database}`)
        log(`✅ Kroger API: ${response.data.kroger_api}`)
      } else {
        log(`❌ Backend health check failed: ${response.error}`)
      }
    } catch (error) {
      log(`❌ Backend health check error: ${error}`)
    }
    
    setIsLoading(false)
  }

  const testProductSearch = async () => {
    setIsLoading(true)
    log(`🔍 Searching for product: "${testItem}"`)
    
    try {
      const response = await searchProducts(testItem, 1)
      if (response.success && response.data) {
        const product = response.data.products[0]
        if (product) {
          log(`✅ Found product: ${product.name} - $${product.price}`)
          log(`   Brand: ${product.brand}, UPC: ${product.upc}`)
          log(`   Inventory: ${product.inventory}`)
        } else {
          log(`❌ No products found for "${testItem}"`)
        }
      } else {
        log(`❌ Product search failed: ${response.error}`)
      }
    } catch (error) {
      log(`❌ Product search error: ${error}`)
    }
    
    setIsLoading(false)
  }

  const testUserLogin = async () => {
    setIsLoading(true)
    log(`👤 Testing user login: ${testEmail}`)
    
    try {
      const response = await loginUser(testEmail, testPassword)
      if (response.success && response.data) {
        log(`✅ User login successful: ${response.data.user.username}`)
        log(`   User ID: ${response.data.user.id}`)
        return response.data.user
      } else {
        log(`❌ User login failed: ${response.error}`)
      }
    } catch (error) {
      log(`❌ User login error: ${error}`)
    }
    
    setIsLoading(false)
    return null
  }

  const testCreateList = async () => {
    setIsLoading(true)
    
    // First login
    const user = await testUserLogin()
    if (!user) return
    
    log(`📝 Creating grocery list for user: ${user.id}`)
    
    try {
      const response = await createGroceryList(user.id)
      if (response.success && response.data) {
        log(`✅ Grocery list created: ${response.data.list.id}`)
        return response.data.list.id
      } else {
        log(`❌ List creation failed: ${response.error}`)
      }
    } catch (error) {
      log(`❌ List creation error: ${error}`)
    }
    
    setIsLoading(false)
    return null
  }

  const testAddItem = async () => {
    setIsLoading(true)
    
    // Create list first
    const listId = await testCreateList()
    if (!listId) return
    
    log(`➕ Adding "${testItem}" to list: ${listId}`)
    
    try {
      const response = await addItemToList(listId, testItem, 1)
      if (response.success && response.data) {
        log(`✅ Item added successfully: ${response.data.item.name}`)
        log(`   Price: $${response.data.item.price}, Quantity: ${response.data.item.quantity}`)
      } else {
        log(`❌ Add item failed: ${response.error}`)
      }
    } catch (error) {
      log(`❌ Add item error: ${error}`)
    }
    
    setIsLoading(false)
  }

  const testFullWorkflow = async () => {
    clearResults()
    log("🚀 Starting full workflow test...")
    
    await testBackendHealth()
    await testProductSearch()
    await testAddItem()
    
    log("🎉 Full workflow test complete!")
  }

  const checkStoredUser = () => {
    const user = getStoredUser()
    if (user) {
      log(`👤 Stored user found: ${user.username} (${user.id})`)
    } else {
      log(`❌ No stored user found`)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-8">
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>🔧 API Debug Tool</CardTitle>
            <CardDescription>
              Test individual API functions to diagnose issues with adding products
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Test Inputs */}
            <div className="grid md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Test Item</label>
                <Input 
                  value={testItem} 
                  onChange={(e) => setTestItem(e.target.value)}
                  placeholder="e.g., milk, bread, apples"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Test Email</label>
                <Input 
                  value={testEmail} 
                  onChange={(e) => setTestEmail(e.target.value)}
                  placeholder="test@example.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Test Password</label>
                <Input 
                  value={testPassword} 
                  onChange={(e) => setTestPassword(e.target.value)}
                  placeholder="password"
                />
              </div>
            </div>

            {/* Test Buttons */}
            <div className="flex flex-wrap gap-3">
              <Button onClick={testBackendHealth} disabled={isLoading}>
                🩺 Test Backend Health
              </Button>
              <Button onClick={testProductSearch} disabled={isLoading}>
                🔍 Test Product Search
              </Button>
              <Button onClick={testUserLogin} disabled={isLoading}>
                👤 Test User Login
              </Button>
              <Button onClick={testCreateList} disabled={isLoading}>
                📝 Test Create List
              </Button>
              <Button onClick={testAddItem} disabled={isLoading}>
                ➕ Test Add Item
              </Button>
              <Button onClick={testFullWorkflow} disabled={isLoading} variant="default">
                🚀 Test Full Workflow
              </Button>
              <Button onClick={checkStoredUser} variant="outline">
                👤 Check Stored User
              </Button>
              <Button onClick={clearResults} variant="outline">
                🗑️ Clear Results
              </Button>
            </div>

            {/* Results */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">📋 Test Results</CardTitle>
              </CardHeader>
              <CardContent>
                {isLoading && (
                  <div className="flex items-center gap-2 mb-4">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-green-600"></div>
                    <span className="text-sm text-gray-600">Running test...</span>
                  </div>
                )}
                
                <div className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm max-h-96 overflow-y-auto">
                  {results.length === 0 ? (
                    <div className="text-gray-500">No tests run yet. Click a test button above.</div>
                  ) : (
                    results.map((result, index) => (
                      <div key={index} className="mb-1">
                        {result}
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}