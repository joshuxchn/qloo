"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Badge } from "@/components/ui/badge"
import { User, DollarSign, Heart, Globe, ArrowRight } from "lucide-react"
import Link from "next/link"

export default function ProfilePage() {
  const [budget, setBudget] = useState([200])
  const [selectedDiets, setSelectedDiets] = useState<string[]>([])
  const [selectedCuisines, setSelectedCuisines] = useState<string[]>([])
  const [selectedAllergies, setSelectedAllergies] = useState<string[]>([])

  const dietaryRestrictions = [
    "Vegetarian",
    "Vegan",
    "Gluten-Free",
    "Keto",
    "Paleo",
    "Low-Carb",
    "Dairy-Free",
    "Nut-Free",
  ]

  const cuisinePreferences = [
    "Italian",
    "Mexican",
    "Asian",
    "Mediterranean",
    "Indian",
    "American",
    "French",
    "Thai",
    "Japanese",
    "Middle Eastern",
  ]

  const commonAllergies = ["Nuts", "Dairy", "Eggs", "Soy", "Wheat", "Fish", "Shellfish", "Sesame"]

  const toggleSelection = (item: string, list: string[], setList: (list: string[]) => void) => {
    if (list.includes(item)) {
      setList(list.filter((i) => i !== item))
    } else {
      setList([...list, item])
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-2">
            <User className="h-8 w-8 text-green-600" />
            <h1 className="text-2xl font-bold text-gray-900">GroceryAI Profile</h1>
          </Link>
          <Button variant="outline" asChild>
            <Link href="/dashboard">Skip to Dashboard</Link>
          </Button>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Create Your Taste Profile</h2>
            <p className="text-lg text-gray-600">
              Help us understand your preferences to provide personalized grocery recommendations
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-8">
            {/* Basic Information */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <User className="h-5 w-5 text-green-600" />
                  Basic Information
                </CardTitle>
                <CardDescription>Tell us about yourself and your household</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="firstName">First Name</Label>
                    <Input id="firstName" placeholder="John" />
                  </div>
                  <div>
                    <Label htmlFor="lastName">Last Name</Label>
                    <Input id="lastName" placeholder="Doe" />
                  </div>
                </div>

                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input id="email" type="email" placeholder="john@example.com" />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="age">Age Range</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select age range" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="18-25">18-25</SelectItem>
                        <SelectItem value="26-35">26-35</SelectItem>
                        <SelectItem value="36-45">36-45</SelectItem>
                        <SelectItem value="46-55">46-55</SelectItem>
                        <SelectItem value="56+">56+</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="household">Household Size</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select size" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1">1 person</SelectItem>
                        <SelectItem value="2">2 people</SelectItem>
                        <SelectItem value="3">3 people</SelectItem>
                        <SelectItem value="4">4 people</SelectItem>
                        <SelectItem value="5+">5+ people</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div>
                  <Label htmlFor="location">Location (ZIP Code)</Label>
                  <Input id="location" placeholder="12345" />
                </div>
              </CardContent>
            </Card>

            {/* Budget Preferences */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <DollarSign className="h-5 w-5 text-blue-600" />
                  Budget & Shopping Preferences
                </CardTitle>
                <CardDescription>Set your budget and shopping frequency</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <Label className="text-base font-medium">Weekly Grocery Budget</Label>
                  <div className="mt-2">
                    <Slider value={budget} onValueChange={setBudget} max={500} min={50} step={25} className="w-full" />
                    <div className="flex justify-between text-sm text-gray-500 mt-1">
                      <span>$50</span>
                      <span className="font-medium text-green-600">${budget[0]}</span>
                      <span>$500+</span>
                    </div>
                  </div>
                </div>

                <div>
                  <Label htmlFor="shopping-frequency">Shopping Frequency</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="How often do you shop?" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="daily">Daily</SelectItem>
                      <SelectItem value="weekly">Weekly</SelectItem>
                      <SelectItem value="biweekly">Bi-weekly</SelectItem>
                      <SelectItem value="monthly">Monthly</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="priority">Shopping Priority</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="What matters most?" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="cost">Lowest Cost</SelectItem>
                      <SelectItem value="quality">Highest Quality</SelectItem>
                      <SelectItem value="health">Healthiest Options</SelectItem>
                      <SelectItem value="convenience">Convenience</SelectItem>
                      <SelectItem value="balanced">Balanced Approach</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>

            {/* Dietary Restrictions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Heart className="h-5 w-5 text-red-600" />
                  Dietary Restrictions & Health
                </CardTitle>
                <CardDescription>Select any dietary restrictions or health considerations</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label className="text-base font-medium mb-3 block">Dietary Restrictions</Label>
                  <div className="flex flex-wrap gap-2">
                    {dietaryRestrictions.map((diet) => (
                      <Badge
                        key={diet}
                        variant={selectedDiets.includes(diet) ? "default" : "outline"}
                        className="cursor-pointer hover:bg-green-100"
                        onClick={() => toggleSelection(diet, selectedDiets, setSelectedDiets)}
                      >
                        {diet}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div>
                  <Label className="text-base font-medium mb-3 block">Allergies</Label>
                  <div className="flex flex-wrap gap-2">
                    {commonAllergies.map((allergy) => (
                      <Badge
                        key={allergy}
                        variant={selectedAllergies.includes(allergy) ? "destructive" : "outline"}
                        className="cursor-pointer hover:bg-red-100"
                        onClick={() => toggleSelection(allergy, selectedAllergies, setSelectedAllergies)}
                      >
                        {allergy}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div>
                  <Label htmlFor="health-goals">Health Goals (Optional)</Label>
                  <Textarea
                    id="health-goals"
                    placeholder="e.g., lose weight, build muscle, improve heart health..."
                    className="mt-1"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Cultural Preferences */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Globe className="h-5 w-5 text-purple-600" />
                  Cultural & Taste Preferences
                </CardTitle>
                <CardDescription>Help us understand your cultural background and taste preferences</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label className="text-base font-medium mb-3 block">Favorite Cuisines</Label>
                  <div className="flex flex-wrap gap-2">
                    {cuisinePreferences.map((cuisine) => (
                      <Badge
                        key={cuisine}
                        variant={selectedCuisines.includes(cuisine) ? "default" : "outline"}
                        className="cursor-pointer hover:bg-purple-100"
                        onClick={() => toggleSelection(cuisine, selectedCuisines, setSelectedCuisines)}
                      >
                        {cuisine}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div>
                  <Label htmlFor="cultural-background">Cultural Background (Optional)</Label>
                  <Input id="cultural-background" placeholder="e.g., Italian-American, Mexican, Indian..." />
                </div>

                <div>
                  <Label htmlFor="cooking-level">Cooking Experience</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="How would you rate your cooking skills?" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="beginner">Beginner</SelectItem>
                      <SelectItem value="intermediate">Intermediate</SelectItem>
                      <SelectItem value="advanced">Advanced</SelectItem>
                      <SelectItem value="expert">Expert/Professional</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="favorite-foods">Favorite Foods & Ingredients</Label>
                  <Textarea
                    id="favorite-foods"
                    placeholder="Tell us about foods you love, ingredients you use often, or dishes you enjoy cooking..."
                    className="mt-1"
                  />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Action Buttons */}
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="text-lg px-8 py-3" asChild>
              <Link href="/dashboard" className="flex items-center gap-2">
                Create Profile & Continue
                <ArrowRight className="h-5 w-5" />
              </Link>
            </Button>
            <Button size="lg" variant="outline" className="text-lg px-8 py-3 bg-transparent" asChild>
              <Link href="/">Back to Home</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
