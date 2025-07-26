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
  TrendingDown,
  Star,
  CheckCircle,
  AlertCircle,
  Trash2,
  ExternalLink,
} from "lucide-react"
import Link from "next/link"
import Image from "next/image"

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

  const handleCheckout = () => {
    window.open("https://www.kroger.com", "_blank")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 h-20">
        <div className="container mx-auto px-4 h-full flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-3">
            <Image
              src="/images/tangerine-logo.png"
              alt="Tangerine Logo"
              width={60}
              height={60}
              className="rounded-full"
            />
            <h1 className="text-xl font-bold text-stone-800">tangerine</h1>
          </Link>
          <div className="flex items-center space-x-3">
            <Button
              variant="ghost"
              size="sm"
              asChild
              className="text-stone-600 hover:text-orange-600 hover:bg-orange-50"
            >
              <Link href="/user-profile">profile</Link>
            </Button>
            <Button size="sm" asChild className="bg-orange-500 hover:bg-orange-600 text-white">
              <Link href="/list-builder">new list</Link>
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Quick Stats */}
        <div className="grid md:grid-cols-3 gap-4 mb-8">
          <Card className="border-0 shadow-sm bg-white">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-stone-500">total</p>
                  <p className="text-xl font-medium text-stone-800">${totalCost.toFixed(2)}</p>
                </div>
                <DollarSign className="h-5 w-5 text-orange-600" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-sm bg-white">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-stone-500">saved</p>
                  <p className="text-xl font-medium text-emerald-700">${totalSavings.toFixed(2)}</p>
                </div>
                <TrendingDown className="h-5 w-5 text-emerald-700" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-sm bg-white">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-stone-500">items</p>
                  <p className="text-xl font-medium text-stone-800">{groceryList.length}</p>
                </div>
                <ShoppingCart className="h-5 w-5 text-amber-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="list" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 bg-stone-100 border-0">
            <TabsTrigger
              value="list"
              className="text-sm text-stone-600 data-[state=active]:bg-white data-[state=active]:text-stone-800"
            >
              list
            </TabsTrigger>
            <TabsTrigger
              value="recommendations"
              className="text-sm text-stone-600 data-[state=active]:bg-white data-[state=active]:text-stone-800"
            >
              suggestions
            </TabsTrigger>
            <TabsTrigger
              value="analytics"
              className="text-sm text-stone-600 data-[state=active]:bg-white data-[state=active]:text-stone-800"
            >
              insights
            </TabsTrigger>
          </TabsList>

          {/* Grocery List Tab */}
          <TabsContent value="list" className="space-y-6">
            <Card className="border-0 shadow-sm bg-white">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg font-medium text-stone-800">grocery list</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex gap-2 mb-6">
                  <Input
                    placeholder="add item..."
                    value={newItem}
                    onChange={(e) => setNewItem(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && addItem()}
                    className="flex-1 border-0 bg-stone-50 text-stone-800 placeholder:text-stone-500"
                  />
                  <Button onClick={addItem} size="sm" className="bg-orange-500 hover:bg-orange-600">
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>

                <div className="space-y-3">
                  {groceryList.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between p-3 bg-stone-50 rounded-lg hover:bg-stone-100 transition-colors"
                    >
                      <div className="flex-1">
                        <div className="flex items-center gap-3">
                          <div className="flex-1">
                            <h4 className="font-medium text-stone-800 text-sm">{item.name}</h4>
                            <div className="flex items-center gap-3 mt-1">
                              <Badge variant="outline" className="text-xs lowercase border-stone-300 text-stone-600">
                                {item.category}
                              </Badge>
                              <span className="text-xs text-stone-500">{item.store}</span>
                              {item.healthScore && (
                                <div className="flex items-center gap-1">
                                  <Star className="h-3 w-3 text-amber-500" />
                                  <span className="text-xs text-stone-500">{item.healthScore}</span>
                                </div>
                              )}
                            </div>
                          </div>

                          <div className="text-right">
                            <div className="flex items-center gap-2">
                              {item.originalPrice && (
                                <span className="text-xs text-stone-400 line-through">
                                  ${item.originalPrice.toFixed(2)}
                                </span>
                              )}
                              <span className="font-medium text-emerald-700 text-sm">${item.price.toFixed(2)}</span>
                            </div>
                            {item.alternatives && item.alternatives > 0 && (
                              <span className="text-xs text-orange-600">{item.alternatives} options</span>
                            )}
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 ml-4">
                        {item.inStock ? (
                          <CheckCircle className="h-4 w-4 text-emerald-600" />
                        ) : (
                          <AlertCircle className="h-4 w-4 text-amber-600" />
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => removeItem(item.id)}
                          className="text-stone-400 hover:text-red-500 h-6 w-6 p-0"
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>

                {groceryList.length === 0 && (
                  <div className="text-center py-12 text-stone-400">
                    <ShoppingCart className="h-8 w-8 mx-auto mb-3 opacity-50" />
                    <p className="text-sm">no items yet</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Recommendations Tab */}
          <TabsContent value="recommendations" className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <Card className="border-0 shadow-sm bg-white">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-stone-800">alternatives</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="p-3 bg-stone-50 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-sm text-stone-800">greek yogurt</h4>
                      <Badge className="bg-emerald-100 text-emerald-800 text-xs">healthier</Badge>
                    </div>
                    <p className="text-xs text-stone-600 mb-2">higher protein</p>
                    <div className="flex justify-between text-xs">
                      <span className="text-stone-500">was $4.99</span>
                      <span className="text-emerald-700 font-medium">now $5.99</span>
                    </div>
                  </div>

                  <div className="p-3 bg-stone-50 rounded-lg">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-sm text-stone-800">whole wheat bread</h4>
                      <Badge className="bg-orange-100 text-orange-800 text-xs">better value</Badge>
                    </div>
                    <p className="text-xs text-stone-600 mb-2">more nutritious</p>
                    <div className="flex justify-between text-xs">
                      <span className="text-stone-500">was $2.99</span>
                      <span className="text-emerald-700 font-medium">now $3.29</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-sm bg-white">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-stone-800">suggestions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="p-3 bg-stone-50 rounded-lg">
                    <h4 className="font-medium mb-2 text-sm text-stone-800">mediterranean</h4>
                    <div className="space-y-1 text-xs">
                      <div className="flex justify-between">
                        <span className="text-stone-600">olive oil</span>
                        <span className="text-emerald-700">$8.99</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-stone-600">fresh basil</span>
                        <span className="text-emerald-700">$2.49</span>
                      </div>
                    </div>
                  </div>

                  <div className="p-3 bg-stone-50 rounded-lg">
                    <h4 className="font-medium mb-2 text-sm text-stone-800">seasonal</h4>
                    <div className="space-y-1 text-xs">
                      <div className="flex justify-between">
                        <span className="text-stone-600">winter squash</span>
                        <span className="text-emerald-700">$1.99/lb</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-stone-600">brussels sprouts</span>
                        <span className="text-emerald-700">$3.49/lb</span>
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
              <Card className="border-0 shadow-sm bg-white">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-stone-800">budget</CardTitle>
                  <CardDescription className="text-xs text-stone-600">weekly limit: $200</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-xs mb-2">
                        <span className="text-stone-600">current</span>
                        <span className="text-stone-600">${totalCost.toFixed(2)} / $200</span>
                      </div>
                      <Progress value={(totalCost / 200) * 100} className="h-1" />
                    </div>

                    <div className="grid grid-cols-2 gap-3 text-center">
                      <div className="p-3 bg-emerald-50 rounded-lg">
                        <div className="text-sm font-medium text-emerald-700">${(200 - totalCost).toFixed(2)}</div>
                        <div className="text-xs text-stone-600">remaining</div>
                      </div>
                      <div className="p-3 bg-orange-50 rounded-lg">
                        <div className="text-sm font-medium text-orange-600">${totalSavings.toFixed(2)}</div>
                        <div className="text-xs text-stone-600">saved</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-sm bg-white">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-stone-800">insights</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium mb-2 text-xs text-stone-600">categories</h4>
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-stone-600">produce</span>
                          <span className="text-emerald-700">35%</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span className="text-stone-600">meat</span>
                          <span className="text-orange-600">25%</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span className="text-stone-600">dairy</span>
                          <span className="text-amber-600">20%</span>
                        </div>
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium mb-2 text-xs text-stone-600">health score</h4>
                      <div className="flex items-center gap-2">
                        <Progress value={85} className="flex-1 h-1" />
                        <span className="text-xs font-medium text-stone-800">85</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>

        {/* Checkout Button */}
        <div className="mt-8 flex justify-center">
          <Button onClick={handleCheckout} size="lg" className="bg-orange-500 hover:bg-orange-600 text-white px-8">
            Checkout at Kroger
            <ExternalLink className="h-4 w-4 ml-2" />
          </Button>
        </div>
      </div>
    </div>
  )
}
