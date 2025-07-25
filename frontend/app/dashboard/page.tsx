"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { 
  getUserLists, 
  addItemToList, 
  searchProducts, 
  createGroceryList,
  getStoredUser,
  formatPrice, 
  formatInventory,
  type User,
  type GroceryList as ApiGroceryList,
  type Product 
} from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import {
  ShoppingCart,
  Plus,
  DollarSign,
  MapPin,
  TrendingDown,
  Star,
  Clock,
  CheckCircle,
  AlertCircle,
  Trash2,
} from "lucide-react"
import Link from "next/link"

interface GroceryItem {
  id: string
  name: string
  category: string
  price: number
  originalPrice?: number
  store: string
  inStock: boolean
  alternatives?: number
  healthScore?: number
}

interface Store {
  id: string
  name: string
  distance: string
  address: string
  hours: string
  totalItems: number
  totalCost: number
}

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<User | null>(null)
  const [newItem, setNewItem] = useState("")
  const [groceryList, setGroceryList] = useState<GroceryItem[]>([])
  const [userLists, setUserLists] = useState<ApiGroceryList[]>([])
  const [currentListId, setCurrentListId] = useState<string | null>(null)
  
  // Loading states
  const [isLoading, setIsLoading] = useState(true)
  const [isAddingItem, setIsAddingItem] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Load user and their lists on component mount
  useEffect(() => {
    const loadUserData = async () => {
      // Check if user is logged in
      const storedUser = getStoredUser()
      if (!storedUser) {
        router.push('/profile')
        return
      }

      setUser(storedUser)

      try {
        // Load user's grocery lists from backend
        const listsResponse = await getUserLists(storedUser.id)
        
        if (listsResponse.success && listsResponse.data) {
          setUserLists(listsResponse.data.lists)
          
          // If user has lists, use the first one
          if (listsResponse.data.lists.length > 0) {
            const firstList = listsResponse.data.lists[0]
            setCurrentListId(firstList.id)
            setGroceryList(firstList.items.map(item => ({
              id: item.upc,
              name: item.name,
              category: "Kroger", // We could enhance this with category mapping
              price: item.price,
              originalPrice: item.price, // Could enhance with promo_price logic
              store: "Kroger",
              inStock: true, // Could enhance with inventory status
              alternatives: 0, // Could enhance with alternative products
              healthScore: 85, // Could enhance with nutritional data
            })))
          }
        } else {
          setError(listsResponse.error || "Failed to load grocery lists")
        }
      } catch (err) {
        setError("Failed to load user data")
      } finally {
        setIsLoading(false)
      }
    }

    loadUserData()
  }, [])

  const [nearbyStores] = useState<Store[]>([
    {
      id: "1",
      name: "Kroger - Main Street",
      distance: "0.8 miles",
      address: "123 Main St, Your City",
      hours: "Open until 11 PM",
      totalItems: 4,
      totalCost: 21.26,
    },
    {
      id: "2",
      name: "Kroger - Oak Avenue",
      distance: "1.2 miles",
      address: "456 Oak Ave, Your City",
      hours: "Open 24 hours",
      totalItems: 4,
      totalCost: 22.15,
    },
    {
      id: "3",
      name: "Kroger - Downtown",
      distance: "2.1 miles",
      address: "789 Downtown Blvd, Your City",
      hours: "Open until 10 PM",
      totalItems: 3,
      totalCost: 18.27,
    },
  ])

  const addItem = async () => {
    console.log("🚀 addItem called with:", { newItem: newItem.trim(), user: user?.username, currentListId })
    
    if (!newItem.trim()) {
      console.log("❌ No item name provided")
      return
    }
    
    if (!user) {
      console.log("❌ No user found")
      return
    }

    setIsAddingItem(true)
    setError(null)

    try {
      // If no current list exists, create one first
      let listId = currentListId
      if (!listId) {
        console.log("No existing list found, creating new list for user:", user.id)
        const createListResponse = await createGroceryList(user.id)
        
        if (createListResponse.success && createListResponse.data) {
          listId = createListResponse.data.list.id
          setCurrentListId(listId)
          console.log("Created new list with ID:", listId)
        } else {
          setError("Failed to create grocery list")
          return
        }
      }

      // First, search for the product to get real data
      console.log("Searching for product:", newItem.trim())
      const searchResponse = await searchProducts(newItem.trim(), 1)
      
      if (searchResponse.success && searchResponse.data && searchResponse.data.products.length > 0) {
        const product = searchResponse.data.products[0]
        console.log("Found product:", product.name, "- $" + product.price)
        
        // Add the real product to the list
        console.log("Adding product to list:", listId)
        const addResponse = await addItemToList(listId!, newItem.trim(), 1)
        
        if (addResponse.success && addResponse.data) {
          console.log("Successfully added item to backend")
          // Add to local state with real product data
          const newGroceryItem: GroceryItem = {
            id: product.upc,
            name: product.name,
            category: "Kroger",
            price: product.price || 0,
            originalPrice: product.promo_price ? product.price : undefined,
            store: "Kroger",
            inStock: product.inventory !== "OUT_OF_STOCK",
            alternatives: 0,
            healthScore: 85,
          }
          
          setGroceryList([...groceryList, newGroceryItem])
          setNewItem("")
        } else {
          setError(addResponse.error || "Failed to add item to list")
        }
      } else {
        // Product not found, show error
        setError(`Product "${newItem}" not found in Kroger catalog`)
      }
    } catch (err) {
      console.error("Error adding item:", err)
      setError("Failed to add item. Please try again.")
    } finally {
      setIsAddingItem(false)
    }
  }

  const removeItem = (id: string) => {
    setGroceryList(groceryList.filter((item) => item.id !== id))
  }

  const totalCost = groceryList.reduce((sum, item) => sum + item.price, 0)
  const totalSavings = groceryList.reduce(
    (sum, item) => sum + (item.originalPrice ? item.originalPrice - item.price : 0),
    0,
  )

  // Show loading state
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-2">
            <ShoppingCart className="h-6 w-6 text-green-600" />
            <h1 className="text-xl font-medium text-gray-900">groceryai</h1>
          </Link>
          <div className="flex items-center space-x-3">
            {user && (
              <span className="text-sm text-gray-600">
                Welcome, {user.username}!
              </span>
            )}
            <Button variant="ghost" size="sm" asChild>
              <Link href="/profile">profile</Link>
            </Button>
            <Button size="sm" asChild>
              <Link href="/list-builder">new list</Link>
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Quick Stats */}
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          <Card className="border-0 shadow-sm">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-gray-500">total</p>
                  <p className="text-xl font-medium text-gray-900">${totalCost.toFixed(2)}</p>
                </div>
                <DollarSign className="h-5 w-5 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-sm">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-gray-500">saved</p>
                  <p className="text-xl font-medium text-green-600">${totalSavings.toFixed(2)}</p>
                </div>
                <TrendingDown className="h-5 w-5 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-sm">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-gray-500">items</p>
                  <p className="text-xl font-medium text-gray-900">{groceryList.length}</p>
                </div>
                <ShoppingCart className="h-5 w-5 text-blue-600" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-sm">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-gray-500">stores</p>
                  <p className="text-xl font-medium text-gray-900">{nearbyStores.length}</p>
                </div>
                <MapPin className="h-5 w-5 text-purple-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="list" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 bg-gray-50 border-0">
            <TabsTrigger value="list" className="text-sm">
              list
            </TabsTrigger>
            <TabsTrigger value="stores" className="text-sm">
              stores
            </TabsTrigger>
            <TabsTrigger value="recommendations" className="text-sm">
              suggestions
            </TabsTrigger>
            <TabsTrigger value="analytics" className="text-sm">
              insights
            </TabsTrigger>
          </TabsList>

          {/* Grocery List Tab */}
          <TabsContent value="list" className="space-y-6">
            <Card className="border-0 shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg font-medium">grocery list</CardTitle>
              </CardHeader>
              <CardContent>
                {/* Error Display */}
                {error && (
                  <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-red-700 text-sm">{error}</p>
                  </div>
                )}

                <div className="flex gap-2 mb-6">
                  <Input
                    placeholder="add item (e.g., 'milk', 'bananas', 'chicken')..."
                    value={newItem}
                    onChange={(e) => setNewItem(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && !isAddingItem && addItem()}
                    className="flex-1 border-0 bg-gray-50"
                    disabled={isAddingItem}
                  />
                  <Button 
                    onClick={addItem} 
                    size="sm"
                    disabled={isAddingItem || !newItem.trim()}
                  >
                    {isAddingItem ? (
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    ) : (
                      <Plus className="h-4 w-4" />
                    )}
                  </Button>
                </div>

                <div className="space-y-3">
                  {groceryList.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <div className="flex-1">
                        <div className="flex items-center gap-3">
                          <div className="flex-1">
                            <h4 className="font-medium text-gray-900 text-sm">{item.name}</h4>
                            <div className="flex items-center gap-3 mt-1">
                              <Badge variant="outline" className="text-xs lowercase">
                                {item.category}
                              </Badge>
                              <span className="text-xs text-gray-500">{item.store}</span>
                              {item.healthScore && (
                                <div className="flex items-center gap-1">
                                  <Star className="h-3 w-3 text-yellow-500" />
                                  <span className="text-xs text-gray-500">{item.healthScore}</span>
                                </div>
                              )}
                            </div>
                          </div>

                          <div className="text-right">
                            <div className="flex items-center gap-2">
                              {item.originalPrice && (
                                <span className="text-xs text-gray-400 line-through">
                                  ${item.originalPrice.toFixed(2)}
                                </span>
                              )}
                              <span className="font-medium text-green-600 text-sm">${item.price.toFixed(2)}</span>
                            </div>
                            {item.alternatives && item.alternatives > 0 && (
                              <span className="text-xs text-blue-600">{item.alternatives} options</span>
                            )}
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 ml-4">
                        {item.inStock ? (
                          <CheckCircle className="h-4 w-4 text-green-500" />
                        ) : (
                          <AlertCircle className="h-4 w-4 text-orange-500" />
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removeItem(item.id)}
                          className="text-gray-400 hover:text-red-500 h-6 w-6 p-0"
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>

                {groceryList.length === 0 && (
                  <div className="text-center py-12 text-gray-400">
                    <ShoppingCart className="h-8 w-8 mx-auto mb-3 opacity-50" />
                    <p className="text-sm">no items yet</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Nearby Stores Tab */}
          <TabsContent value="stores" className="space-y-4">
            {nearbyStores.map((store) => (
              <Card key={store.id} className="border-0 shadow-sm hover:shadow-md transition-shadow">
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900 mb-2 text-sm">{store.name}</h3>
                      <div className="space-y-1 text-xs text-gray-500">
                        <div className="flex items-center gap-2">
                          <MapPin className="h-3 w-3" />
                          <span>{store.address}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Clock className="h-3 w-3" />
                          <span>{store.hours}</span>
                        </div>
                      </div>
                    </div>

                    <div className="text-right">
                      <div className="text-xs text-gray-500 mb-1">{store.distance}</div>
                      <div className="font-medium text-green-600 mb-1">${store.totalCost.toFixed(2)}</div>
                      <div className="text-xs text-gray-500 mb-2">{store.totalItems} items</div>
                      <Button size="sm" variant="outline" className="text-xs bg-transparent">
                        view
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </TabsContent>

          {/* Recommendations Tab */}
          <TabsContent value="recommendations" className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <Card className="border-0 shadow-sm">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium">alternatives</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-sm">greek yogurt</h4>
                      <Badge className="bg-green-100 text-green-800 text-xs">healthier</Badge>
                    </div>
                    <p className="text-xs text-gray-600 mb-2">higher protein</p>
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-500">was $4.99</span>
                      <span className="text-green-600 font-medium">now $5.99</span>
                    </div>
                  </div>

                  <div className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-sm">whole wheat bread</h4>
                      <Badge className="bg-blue-100 text-blue-800 text-xs">better value</Badge>
                    </div>
                    <p className="text-xs text-gray-600 mb-2">more nutritious</p>
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-500">was $2.99</span>
                      <span className="text-green-600 font-medium">now $3.29</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-sm">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium">suggestions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <h4 className="font-medium mb-2 text-sm">mediterranean</h4>
                    <div className="space-y-1 text-xs">
                      <div className="flex justify-between">
                        <span>olive oil</span>
                        <span className="text-green-600">$8.99</span>
                      </div>
                      <div className="flex justify-between">
                        <span>fresh basil</span>
                        <span className="text-green-600">$2.49</span>
                      </div>
                    </div>
                  </div>

                  <div className="p-3 bg-gray-50 rounded-lg">
                    <h4 className="font-medium mb-2 text-sm">seasonal</h4>
                    <div className="space-y-1 text-xs">
                      <div className="flex justify-between">
                        <span>winter squash</span>
                        <span className="text-green-600">$1.99/lb</span>
                      </div>
                      <div className="flex justify-between">
                        <span>brussels sprouts</span>
                        <span className="text-green-600">$3.49/lb</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Analytics Tab */}
          <TabsContent value="analytics" className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <Card className="border-0 shadow-sm">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium">budget</CardTitle>
                  <CardDescription className="text-xs">weekly limit: $200</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-xs mb-2">
                        <span>current</span>
                        <span>${totalCost.toFixed(2)} / $200</span>
                      </div>
                      <Progress value={(totalCost / 200) * 100} className="h-1" />
                    </div>

                    <div className="grid grid-cols-2 gap-3 text-center">
                      <div className="p-3 bg-green-50 rounded-lg">
                        <div className="text-sm font-medium text-green-600">${(200 - totalCost).toFixed(2)}</div>
                        <div className="text-xs text-gray-600">remaining</div>
                      </div>
                      <div className="p-3 bg-blue-50 rounded-lg">
                        <div className="text-sm font-medium text-blue-600">${totalSavings.toFixed(2)}</div>
                        <div className="text-xs text-gray-600">saved</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-sm">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium">insights</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium mb-2 text-xs text-gray-600">categories</h4>
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span>produce</span>
                          <span className="text-green-600">35%</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span>meat</span>
                          <span className="text-blue-600">25%</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span>dairy</span>
                          <span className="text-purple-600">20%</span>
                        </div>
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium mb-2 text-xs text-gray-600">health score</h4>
                      <div className="flex items-center gap-2">
                        <Progress value={85} className="flex-1 h-1" />
                        <span className="text-xs font-medium">85</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
