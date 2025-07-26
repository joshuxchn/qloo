"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  ShoppingCart,
  Plus,
  Wand2,
  Upload,
  Camera,
  FileText,
  Sparkles,
  CheckCircle,
  Clock,
  ArrowRight,
} from "lucide-react"
import Link from "next/link"
import Image from "next/image"

interface GeneratedItem {
  id: string
  name: string
  category: string
  confidence: number
  alternatives: string[]
}

export default function ListBuilderPage() {
  const [inputMethod, setInputMethod] = useState<"manual" | "ai" | "recipe" | "photo">("manual")
  const [manualItem, setManualItem] = useState("")
  const [aiPrompt, setAiPrompt] = useState("")
  const [recipe, setRecipe] = useState("")
  const [generatedItems, setGeneratedItems] = useState<GeneratedItem[]>([])
  const [isGenerating, setIsGenerating] = useState(false)

  const handleManualAdd = () => {
    if (manualItem.trim()) {
      const newItem: GeneratedItem = {
        id: Date.now().toString(),
        name: manualItem,
        category: "Manual",
        confidence: 100,
        alternatives: [],
      }
      setGeneratedItems([...generatedItems, newItem])
      setManualItem("")
    }
  }

  const handleAIGenerate = async () => {
    if (!aiPrompt.trim()) return

    setIsGenerating(true)

    // Simulate AI processing
    setTimeout(() => {
      const mockItems: GeneratedItem[] = [
        {
          id: "1",
          name: "Organic Chicken Breast (2 lbs)",
          category: "Meat",
          confidence: 95,
          alternatives: ["Free-range Chicken", "Chicken Thighs", "Turkey Breast"],
        },
        {
          id: "2",
          name: "Brown Rice (2 lbs)",
          category: "Grains",
          confidence: 90,
          alternatives: ["Quinoa", "Wild Rice", "Cauliflower Rice"],
        },
        {
          id: "3",
          name: "Mixed Vegetables (Frozen)",
          category: "Produce",
          confidence: 88,
          alternatives: ["Fresh Broccoli", "Stir-fry Mix", "Steam-in-bag Vegetables"],
        },
        {
          id: "4",
          name: "Olive Oil (Extra Virgin)",
          category: "Pantry",
          confidence: 92,
          alternatives: ["Avocado Oil", "Coconut Oil", "Vegetable Oil"],
        },
      ]

      setGeneratedItems([...generatedItems, ...mockItems])
      setIsGenerating(false)
      setAiPrompt("")
    }, 2000)
  }

  const handleRecipeAnalysis = async () => {
    if (!recipe.trim()) return

    setIsGenerating(true)

    // Simulate recipe analysis
    setTimeout(() => {
      const mockRecipeItems: GeneratedItem[] = [
        {
          id: "r1",
          name: "Ground Beef (1 lb)",
          category: "Meat",
          confidence: 98,
          alternatives: ["Ground Turkey", "Plant-based Ground", "Ground Chicken"],
        },
        {
          id: "r2",
          name: "Onion (Large)",
          category: "Produce",
          confidence: 95,
          alternatives: ["Yellow Onion", "Sweet Onion", "Red Onion"],
        },
        {
          id: "r3",
          name: "Canned Tomatoes (14 oz)",
          category: "Pantry",
          confidence: 90,
          alternatives: ["Fresh Tomatoes", "Tomato Sauce", "Crushed Tomatoes"],
        },
        {
          id: "r4",
          name: "Pasta (1 lb)",
          category: "Pantry",
          confidence: 85,
          alternatives: ["Whole Wheat Pasta", "Gluten-free Pasta", "Zucchini Noodles"],
        },
      ]

      setGeneratedItems([...generatedItems, ...mockRecipeItems])
      setIsGenerating(false)
      setRecipe("")
    }, 2500)
  }

  const removeItem = (id: string) => {
    setGeneratedItems(generatedItems.filter((item) => item.id !== id))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 h-20">
        <div className="container mx-auto px-4 h-full flex items-center justify-between">
          <Link href="/dashboard" className="flex items-center space-x-3">
            <Image
              src="/images/tangerine-logo.png"
              alt="Tangerine Logo"
              width={60}
              height={60}
              className="rounded-full"
            />
            <h1 className="text-2xl font-bold text-stone-800">tangerine ai list builder</h1>
          </Link>
          <div className="flex items-center space-x-4">
            <Button
              variant="outline"
              asChild
              className="border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent"
            >
              <Link href="/dashboard">Back to Dashboard</Link>
            </Button>
            {generatedItems.length > 0 && (
              <Button asChild className="bg-orange-500 hover:bg-orange-600 text-white">
                <Link href="/dashboard">
                  Add {generatedItems.length} Items
                  <ArrowRight className="h-4 w-4 ml-2" />
                </Link>
              </Button>
            )}
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-stone-800 mb-4">Build Your Grocery List</h2>
            <p className="text-lg text-stone-600">
              Use AI to generate optimized grocery lists from recipes, meal plans, or natural language
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-8">
            {/* Input Methods */}
            <div className="space-y-6">
              <Card className="border border-stone-200 shadow-sm">
                <CardHeader>
                  <CardTitle className="text-stone-800">Choose Your Input Method</CardTitle>
                  <CardDescription className="text-stone-600">
                    Select how you'd like to build your grocery list
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Tabs value={inputMethod} onValueChange={(value) => setInputMethod(value as any)}>
                    <TabsList className="grid w-full grid-cols-4 bg-stone-100">
                      <TabsTrigger
                        value="manual"
                        className="text-stone-600 data-[state=active]:bg-white data-[state=active]:text-stone-800"
                      >
                        Manual
                      </TabsTrigger>
                      <TabsTrigger
                        value="ai"
                        className="text-stone-600 data-[state=active]:bg-white data-[state=active]:text-stone-800"
                      >
                        AI Prompt
                      </TabsTrigger>
                      <TabsTrigger
                        value="recipe"
                        className="text-stone-600 data-[state=active]:bg-white data-[state=active]:text-stone-800"
                      >
                        Recipe
                      </TabsTrigger>
                      <TabsTrigger
                        value="photo"
                        className="text-stone-600 data-[state=active]:bg-white data-[state=active]:text-stone-800"
                      >
                        Photo
                      </TabsTrigger>
                    </TabsList>

                    <TabsContent value="manual" className="space-y-4">
                      <div>
                        <h3 className="font-medium mb-2 text-stone-800">Add Items Manually</h3>
                        <p className="text-sm text-stone-600 mb-4">Type grocery items one by one</p>
                        <div className="flex gap-2">
                          <Input
                            placeholder="Enter grocery item (e.g., 'milk', 'bananas', 'chicken')"
                            value={manualItem}
                            onChange={(e) => setManualItem(e.target.value)}
                            onKeyPress={(e) => e.key === "Enter" && handleManualAdd()}
                            className="border-stone-300"
                          />
                          <Button onClick={handleManualAdd} className="bg-orange-500 hover:bg-orange-600">
                            <Plus className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </TabsContent>

                    <TabsContent value="ai" className="space-y-4">
                      <div>
                        <h3 className="font-medium mb-2 text-stone-800">AI-Powered Generation</h3>
                        <p className="text-sm text-stone-600 mb-4">
                          Describe what you want to cook or eat, and AI will generate a grocery list
                        </p>
                        <Textarea
                          placeholder="e.g., 'I want to make healthy meals for a family of 4 this week, including chicken dinners and vegetarian lunches'"
                          value={aiPrompt}
                          onChange={(e) => setAiPrompt(e.target.value)}
                          className="min-h-[100px] border-stone-300"
                        />
                        <Button
                          onClick={handleAIGenerate}
                          disabled={isGenerating || !aiPrompt.trim()}
                          className="w-full mt-2 bg-orange-500 hover:bg-orange-600"
                        >
                          {isGenerating ? (
                            <>
                              <Clock className="h-4 w-4 mr-2 animate-spin" />
                              Generating List...
                            </>
                          ) : (
                            <>
                              <Sparkles className="h-4 w-4 mr-2" />
                              Generate Grocery List
                            </>
                          )}
                        </Button>
                      </div>
                    </TabsContent>

                    <TabsContent value="recipe" className="space-y-4">
                      <div>
                        <h3 className="font-medium mb-2 text-stone-800">Recipe Analysis</h3>
                        <p className="text-sm text-stone-600 mb-4">Paste a recipe and we'll extract the ingredients</p>
                        <Textarea
                          placeholder="Paste your recipe here..."
                          value={recipe}
                          onChange={(e) => setRecipe(e.target.value)}
                          className="min-h-[120px] border-stone-300"
                        />
                        <Button
                          onClick={handleRecipeAnalysis}
                          disabled={isGenerating || !recipe.trim()}
                          className="w-full mt-2 bg-orange-500 hover:bg-orange-600"
                        >
                          {isGenerating ? (
                            <>
                              <Clock className="h-4 w-4 mr-2 animate-spin" />
                              Analyzing Recipe...
                            </>
                          ) : (
                            <>
                              <FileText className="h-4 w-4 mr-2" />
                              Extract Ingredients
                            </>
                          )}
                        </Button>
                      </div>
                    </TabsContent>

                    <TabsContent value="photo" className="space-y-4">
                      <div>
                        <h3 className="font-medium mb-2 text-stone-800">Photo Recognition</h3>
                        <p className="text-sm text-stone-600 mb-4">
                          Upload a photo of a recipe, meal plan, or handwritten list
                        </p>
                        <div className="border-2 border-dashed border-stone-300 rounded-lg p-8 text-center">
                          <Camera className="h-12 w-12 text-stone-400 mx-auto mb-4" />
                          <p className="text-stone-600 mb-4">Drag and drop an image here, or click to browse</p>
                          <Button variant="outline" disabled className="border-stone-300 text-stone-700 bg-transparent">
                            <Upload className="h-4 w-4 mr-2" />
                            Upload Photo (Coming Soon)
                          </Button>
                        </div>
                      </div>
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>

              {/* Quick Templates */}
              <Card className="border border-stone-200 shadow-sm">
                <CardHeader>
                  <CardTitle className="text-stone-800">Quick Templates</CardTitle>
                  <CardDescription className="text-stone-600">
                    Start with pre-made templates for common meal plans
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-3">
                    <Button
                      variant="outline"
                      className="h-auto p-4 flex flex-col items-start bg-transparent border-stone-300 text-stone-700 hover:bg-orange-50"
                      onClick={() =>
                        setAiPrompt(
                          "Weekly meal prep for healthy eating, including proteins, vegetables, and whole grains",
                        )
                      }
                    >
                      <span className="font-medium">Meal Prep</span>
                      <span className="text-xs text-stone-500">Healthy weekly prep</span>
                    </Button>

                    <Button
                      variant="outline"
                      className="h-auto p-4 flex flex-col items-start bg-transparent border-stone-300 text-stone-700 hover:bg-orange-50"
                      onClick={() => setAiPrompt("Family dinner ingredients for a week, kid-friendly meals")}
                    >
                      <span className="font-medium">Family Dinners</span>
                      <span className="text-xs text-stone-500">Kid-friendly meals</span>
                    </Button>

                    <Button
                      variant="outline"
                      className="h-auto p-4 flex flex-col items-start bg-transparent border-stone-300 text-stone-700 hover:bg-orange-50"
                      onClick={() => setAiPrompt("Vegetarian meals for the week with high protein options")}
                    >
                      <span className="font-medium">Vegetarian</span>
                      <span className="text-xs text-stone-500">Plant-based meals</span>
                    </Button>

                    <Button
                      variant="outline"
                      className="h-auto p-4 flex flex-col items-start bg-transparent border-stone-300 text-stone-700 hover:bg-orange-50"
                      onClick={() => setAiPrompt("Budget-friendly grocery list for basic meals under $50")}
                    >
                      <span className="font-medium">Budget Meals</span>
                      <span className="text-xs text-stone-500">Under $50</span>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Generated Items */}
            <div className="space-y-6">
              <Card className="border border-stone-200 shadow-sm">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between text-stone-800">
                    Generated Items
                    {generatedItems.length > 0 && (
                      <Badge variant="secondary" className="bg-stone-100 text-stone-600">
                        {generatedItems.length} items
                      </Badge>
                    )}
                  </CardTitle>
                  <CardDescription className="text-stone-600">
                    Review and modify your AI-generated grocery list
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {generatedItems.length === 0 ? (
                    <div className="text-center py-12 text-stone-400">
                      <ShoppingCart className="h-12 w-12 mx-auto mb-4 opacity-50" />
                      <p>No items generated yet.</p>
                      <p className="text-sm">Use one of the input methods to get started!</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {generatedItems.map((item) => (
                        <div key={item.id} className="p-4 border border-stone-200 rounded-lg hover:bg-stone-50">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-2">
                                <h4 className="font-medium text-stone-800">{item.name}</h4>
                                <Badge variant="outline" className="text-xs border-stone-300 text-stone-600">
                                  {item.category}
                                </Badge>
                                <div className="flex items-center gap-1">
                                  <CheckCircle className="h-3 w-3 text-emerald-500" />
                                  <span className="text-xs text-stone-600">{item.confidence}% match</span>
                                </div>
                              </div>

                              {item.alternatives.length > 0 && (
                                <div className="mt-2">
                                  <p className="text-xs text-stone-600 mb-1">Alternatives:</p>
                                  <div className="flex flex-wrap gap-1">
                                    {item.alternatives.slice(0, 3).map((alt, index) => (
                                      <Badge
                                        key={index}
                                        variant="secondary"
                                        className="text-xs bg-stone-100 text-stone-600"
                                      >
                                        {alt}
                                      </Badge>
                                    ))}
                                  </div>
                                </div>
                              )}
                            </div>

                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => removeItem(item.id)}
                              className="text-red-600 hover:text-red-700 ml-2"
                            >
                              ×
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* AI Processing Status */}
              {isGenerating && (
                <Card className="border-orange-200 bg-orange-50">
                  <CardContent className="p-6">
                    <div className="flex items-center gap-3">
                      <div className="animate-spin">
                        <Sparkles className="h-6 w-6 text-orange-600" />
                      </div>
                      <div>
                        <h4 className="font-medium text-orange-800">AI Processing</h4>
                        <p className="text-sm text-orange-700">
                          Analyzing your request and generating optimized grocery items...
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Action Buttons */}
              {generatedItems.length > 0 && (
                <Card className="border border-stone-200 shadow-sm">
                  <CardContent className="p-6">
                    <div className="flex flex-col gap-3">
                      <Button size="lg" className="w-full bg-orange-500 hover:bg-orange-600 text-white" asChild>
                        <Link href="/dashboard">
                          <CheckCircle className="h-5 w-5 mr-2" />
                          Add {generatedItems.length} Items to List
                        </Link>
                      </Button>
                      <Button
                        variant="outline"
                        size="lg"
                        className="w-full bg-transparent border-stone-300 text-stone-700 hover:bg-stone-50"
                      >
                        <Wand2 className="h-5 w-5 mr-2" />
                        Optimize with AI
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
