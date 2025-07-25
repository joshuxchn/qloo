"use client"

import { useState } from "react"
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
  const [newItem, setNewItem] = useState("")
  const [groceryList, setGroceryList] = useState<GroceryItem[]>([
    {
      id: "1",
      name: "Organic Bananas (2 lbs)",
      category: "Produce",
      price: 2.99,
      originalPrice: 3.49,
      store: "Kroger",
      inStock: true,
      alternatives: 3,
      healthScore: 95,
    },
    {
      id: "2",
      name: "Whole Wheat Bread",
      category: "Bakery",
      price: 3.29,
      store: "Kroger",
      inStock: true,
      alternatives: 5,
      healthScore: 78,
    },
    {
      id: "3",
      name: "Greek Yogurt (32oz)",
      category: "Dairy",
      price: 5.99,
      originalPrice: 6.99,
      store: "Kroger",
      inStock: false,
      alternatives: 4,
      healthScore: 88,
    },
    {
      id: "4",
      name: "Chicken Breast (2 lbs)",
      category: "Meat",
      price: 8.99,
      store: "Kroger",
      inStock: true,
      alternatives: 2,
      healthScore: 85,
    },
  ])

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

  const addItem = () => {
    if (newItem.trim()) {
      const newGroceryItem: GroceryItem = {
        id: Date.now().toString(),
        name: newItem,
        category: "Pending",
        price: 0,
        store: "Processing...",
        inStock: true,
        alternatives: 0,
      }
      setGroceryList([...groceryList, newGroceryItem])
      setNewItem("")
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
                <div className="flex gap-2 mb-6">
                  <Input
                    placeholder="add item..."
                    value={newItem}
                    onChange={(e) => setNewItem(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && addItem()}
                    className="flex-1 border-0 bg-gray-50"
                  />
                  <Button onClick={addItem} size="sm">
                    <Plus className="h-4 w-4" />
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
