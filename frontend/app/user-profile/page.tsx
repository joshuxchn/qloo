"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { User, DollarSign, Heart, Settings, Save, Bell, Shield } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

export default function UserProfilePage() {
  const [budget, setBudget] = useState([200])
  const [selectedDiets, setSelectedDiets] = useState<string[]>(["Vegetarian", "Gluten-Free"])
  const [selectedCuisines, setSelectedCuisines] = useState<string[]>(["Italian", "Mediterranean", "Asian"])
  const [selectedAllergies, setSelectedAllergies] = useState<string[]>(["Nuts"])

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
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm h-20">
        <div className="container mx-auto px-4 h-full flex items-center justify-between">
          <Link href="/dashboard" className="flex items-center space-x-3">
            <Image
              src="/images/tangerine-logo.png"
              alt="Tangerine Logo"
              width={60}
              height={60}
              className="rounded-full"
            />
            <h1 className="text-2xl font-bold text-stone-800">tangerine</h1>
          </Link>
          <div className="flex items-center space-x-3">
            <Button
              variant="ghost"
              size="sm"
              asChild
              className="text-stone-600 hover:text-orange-600 hover:bg-orange-50"
            >
              <Link href="/dashboard">Dashboard</Link>
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent"
            >
              Sign Out
            </Button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-stone-800 mb-2">Profile Settings</h2>
            <p className="text-lg text-stone-600">Manage your account and preferences</p>
          </div>

          <Tabs defaultValue="preferences" className="space-y-6">
            <TabsList className="grid w-full grid-cols-4 bg-stone-100 border-0">
              <TabsTrigger
                value="preferences"
                className="text-sm text-stone-600 data-[state=active]:bg-white data-[state=active]:text-stone-800"
              >
                <Heart className="h-4 w-4 mr-2" />
                Preferences
              </TabsTrigger>
              <TabsTrigger
                value="account"
                className="text-sm text-stone-600 data-[state=active]:bg-white data-[state=active]:text-stone-800"
              >
                <User className="h-4 w-4 mr-2" />
                Account
              </TabsTrigger>
              <TabsTrigger
                value="budget"
                className="text-sm text-stone-600 data-[state=active]:bg-white data-[state=active]:text-stone-800"
              >
                <DollarSign className="h-4 w-4 mr-2" />
                Budget
              </TabsTrigger>
              <TabsTrigger
                value="settings"
                className="text-sm text-stone-600 data-[state=active]:bg-white data-[state=active]:text-stone-800"
              >
                <Settings className="h-4 w-4 mr-2" />
                Settings
              </TabsTrigger>
            </TabsList>

            {/* Preferences Tab */}
            <TabsContent value="preferences" className="space-y-6">
              <div className="grid lg:grid-cols-2 gap-6">
                <Card className="border border-stone-200 shadow-sm">
                  <CardHeader>
                    <CardTitle className="text-stone-800">Dietary Restrictions</CardTitle>
                    <CardDescription className="text-stone-600">
                      Update your dietary preferences and restrictions
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <Label className="text-base font-medium mb-3 block text-stone-700">Current Restrictions</Label>
                      <div className="flex flex-wrap gap-2">
                        {dietaryRestrictions.map((diet) => (
                          <Badge
                            key={diet}
                            variant={selectedDiets.includes(diet) ? "default" : "outline"}
                            className={`cursor-pointer transition-colors ${
                              selectedDiets.includes(diet)
                                ? "bg-orange-500 text-white hover:bg-orange-600"
                                : "border-stone-300 text-stone-600 hover:bg-orange-50"
                            }`}
                            onClick={() => toggleSelection(diet, selectedDiets, setSelectedDiets)}
                          >
                            {diet}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <div>
                      <Label className="text-base font-medium mb-3 block text-stone-700">Allergies</Label>
                      <div className="flex flex-wrap gap-2">
                        {commonAllergies.map((allergy) => (
                          <Badge
                            key={allergy}
                            variant={selectedAllergies.includes(allergy) ? "destructive" : "outline"}
                            className={`cursor-pointer transition-colors ${
                              selectedAllergies.includes(allergy)
                                ? "bg-red-500 text-white hover:bg-red-600"
                                : "border-stone-300 text-stone-600 hover:bg-red-50"
                            }`}
                            onClick={() => toggleSelection(allergy, selectedAllergies, setSelectedAllergies)}
                          >
                            {allergy}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="border border-stone-200 shadow-sm">
                  <CardHeader>
                    <CardTitle className="text-stone-800">Cuisine Preferences</CardTitle>
                    <CardDescription className="text-stone-600">
                      Select your favorite cuisines for better recommendations
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div>
                      <Label className="text-base font-medium mb-3 block text-stone-700">Favorite Cuisines</Label>
                      <div className="flex flex-wrap gap-2">
                        {cuisinePreferences.map((cuisine) => (
                          <Badge
                            key={cuisine}
                            variant={selectedCuisines.includes(cuisine) ? "default" : "outline"}
                            className={`cursor-pointer transition-colors ${
                              selectedCuisines.includes(cuisine)
                                ? "bg-amber-500 text-white hover:bg-amber-600"
                                : "border-stone-300 text-stone-600 hover:bg-amber-50"
                            }`}
                            onClick={() => toggleSelection(cuisine, selectedCuisines, setSelectedCuisines)}
                          >
                            {cuisine}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              <div className="flex justify-end">
                <Button className="bg-orange-500 hover:bg-orange-600 text-white">
                  <Save className="h-4 w-4 mr-2" />
                  Save Preferences
                </Button>
              </div>
            </TabsContent>

            {/* Account Tab */}
            <TabsContent value="account" className="space-y-6">
              <Card className="border border-stone-200 shadow-sm">
                <CardHeader>
                  <CardTitle className="text-stone-800">Account Information</CardTitle>
                  <CardDescription className="text-stone-600">
                    Update your personal information and account details
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="firstName" className="text-stone-700">
                        First Name
                      </Label>
                      <Input id="firstName" defaultValue="John" className="border-stone-300" />
                    </div>
                    <div>
                      <Label htmlFor="lastName" className="text-stone-700">
                        Last Name
                      </Label>
                      <Input id="lastName" defaultValue="Doe" className="border-stone-300" />
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="email" className="text-stone-700">
                      Email
                    </Label>
                    <Input id="email" type="email" defaultValue="john@example.com" className="border-stone-300" />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="phone" className="text-stone-700">
                        Phone Number
                      </Label>
                      <Input id="phone" placeholder="(555) 123-4567" className="border-stone-300" />
                    </div>
                    <div>
                      <Label htmlFor="location" className="text-stone-700">
                        ZIP Code
                      </Label>
                      <Input id="location" defaultValue="12345" className="border-stone-300" />
                    </div>
                  </div>
                </CardContent>
              </Card>

              <div className="flex justify-end">
                <Button className="bg-orange-500 hover:bg-orange-600 text-white">
                  <Save className="h-4 w-4 mr-2" />
                  Update Account
                </Button>
              </div>
            </TabsContent>

            {/* Budget Tab */}
            <TabsContent value="budget" className="space-y-6">
              <Card className="border border-stone-200 shadow-sm">
                <CardHeader>
                  <CardTitle className="text-stone-800">Budget Settings</CardTitle>
                  <CardDescription className="text-stone-600">
                    Manage your grocery budget and shopping preferences
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div>
                    <Label className="text-base font-medium text-stone-700">Weekly Grocery Budget</Label>
                    <div className="mt-2">
                      <Slider
                        value={budget}
                        onValueChange={setBudget}
                        max={500}
                        min={50}
                        step={25}
                        className="w-full"
                      />
                      <div className="flex justify-between text-sm text-stone-500 mt-1">
                        <span>$50</span>
                        <span className="font-medium text-orange-600">${budget[0]}</span>
                        <span>$500+</span>
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="shopping-frequency" className="text-stone-700">
                        Shopping Frequency
                      </Label>
                      <Select defaultValue="weekly">
                        <SelectTrigger className="border-stone-300">
                          <SelectValue />
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
                      <Label htmlFor="priority" className="text-stone-700">
                        Shopping Priority
                      </Label>
                      <Select defaultValue="balanced">
                        <SelectTrigger className="border-stone-300">
                          <SelectValue />
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
                  </div>
                </CardContent>
              </Card>

              <div className="flex justify-end">
                <Button className="bg-orange-500 hover:bg-orange-600 text-white">
                  <Save className="h-4 w-4 mr-2" />
                  Save Budget Settings
                </Button>
              </div>
            </TabsContent>

            {/* Settings Tab */}
            <TabsContent value="settings" className="space-y-6">
              <div className="grid gap-6">
                <Card className="border border-stone-200 shadow-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-stone-800">
                      <Bell className="h-5 w-5 text-orange-600" />
                      Notifications
                    </CardTitle>
                    <CardDescription className="text-stone-600">Manage your notification preferences</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium text-stone-800">Deal Alerts</h4>
                        <p className="text-sm text-stone-600">Get notified about price drops and special offers</p>
                      </div>
                      <input type="checkbox" defaultChecked className="rounded border-stone-300 text-orange-600" />
                    </div>
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium text-stone-800">Weekly Summary</h4>
                        <p className="text-sm text-stone-600">Receive weekly reports on your shopping habits</p>
                      </div>
                      <input type="checkbox" defaultChecked className="rounded border-stone-300 text-orange-600" />
                    </div>
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium text-stone-800">New Features</h4>
                        <p className="text-sm text-stone-600">Be the first to know about new platform features</p>
                      </div>
                      <input type="checkbox" className="rounded border-stone-300 text-orange-600" />
                    </div>
                  </CardContent>
                </Card>

                <Card className="border border-stone-200 shadow-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-stone-800">
                      <Shield className="h-5 w-5 text-orange-600" />
                      Privacy & Security
                    </CardTitle>
                    <CardDescription className="text-stone-600">
                      Manage your privacy settings and account security
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <Button
                      variant="outline"
                      className="w-full justify-start border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent"
                    >
                      Change Password
                    </Button>
                    <Button
                      variant="outline"
                      className="w-full justify-start border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent"
                    >
                      Download My Data
                    </Button>
                    <Button
                      variant="outline"
                      className="w-full justify-start border-red-300 text-red-700 hover:bg-red-50 bg-transparent"
                    >
                      Delete Account
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}
