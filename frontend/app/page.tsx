import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ShoppingCart, DollarSign, MapPin, Brain, TrendingDown, Users } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <ShoppingCart className="h-8 w-8 text-green-600" />
            <h1 className="text-2xl font-bold text-gray-900">GroceryAI</h1>
          </div>
          <nav className="hidden md:flex items-center space-x-6">
            <Link href="#features" className="text-gray-600 hover:text-green-600 transition-colors">
              Features
            </Link>
            <Link href="#how-it-works" className="text-gray-600 hover:text-green-600 transition-colors">
              How It Works
            </Link>
            <Link href="/dashboard" className="text-gray-600 hover:text-green-600 transition-colors">
              Dashboard
            </Link>
          </nav>
          <div className="flex items-center space-x-4">
            <Button variant="outline" asChild>
              <Link href="/profile">Sign In</Link>
            </Button>
            <Button asChild>
              <Link href="/profile">Get Started</Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <Badge className="mb-4 bg-green-100 text-green-800 hover:bg-green-100">AI-Powered Grocery Optimization</Badge>
          <h2 className="text-5xl font-bold text-gray-900 mb-6 leading-tight">
            Smart Grocery Lists That
            <span className="text-green-600"> Save Money</span> &
            <span className="text-blue-600"> Match Your Taste</span>
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Build optimized grocery lists with AI that understands your preferences, budget, and cultural background.
            Get real-time prices, alternatives, and deals from Kroger stores.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="text-lg px-8 py-3" asChild>
              <Link href="/profile">Start Building Lists</Link>
            </Button>
            <Button size="lg" variant="outline" className="text-lg px-8 py-3 bg-transparent" asChild>
              <Link href="#features">Learn More</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-white">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">Powerful Features</h3>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our AI-powered platform combines taste profiling, cost optimization, and real-time grocery data
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="border-2 hover:border-green-200 transition-colors">
              <CardHeader>
                <Brain className="h-12 w-12 text-green-600 mb-4" />
                <CardTitle>AI Taste Profiling</CardTitle>
                <CardDescription>
                  Dynamic preference learning that adapts to your taste and cultural background
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• Personalized recommendations</li>
                  <li>• Cultural intelligence via Qloo API</li>
                  <li>• Continuous preference learning</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-blue-200 transition-colors">
              <CardHeader>
                <DollarSign className="h-12 w-12 text-blue-600 mb-4" />
                <CardTitle>Cost Optimization</CardTitle>
                <CardDescription>Real-time price comparison and budget-friendly alternatives</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• Live Kroger API pricing</li>
                  <li>• Budget-optimized baskets</li>
                  <li>• Deal and promotion alerts</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-purple-200 transition-colors">
              <CardHeader>
                <MapPin className="h-12 w-12 text-purple-600 mb-4" />
                <CardTitle>Store Integration</CardTitle>
                <CardDescription>Find the best stores with real-time inventory and location data</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• Local store finder</li>
                  <li>• Real-time availability</li>
                  <li>• Store hours and directions</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-orange-200 transition-colors">
              <CardHeader>
                <TrendingDown className="h-12 w-12 text-orange-600 mb-4" />
                <CardTitle>Smart Alternatives</CardTitle>
                <CardDescription>Healthier, cheaper, or more preferred alternatives when needed</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• Health-conscious swaps</li>
                  <li>• Budget-friendly options</li>
                  <li>• Taste-matched alternatives</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-red-200 transition-colors">
              <CardHeader>
                <ShoppingCart className="h-12 w-12 text-red-600 mb-4" />
                <CardTitle>List Validation</CardTitle>
                <CardDescription>Convert generic items to specific products with full details</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• Generic to specific matching</li>
                  <li>• Nutritional information</li>
                  <li>• Product availability check</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-teal-200 transition-colors">
              <CardHeader>
                <Users className="h-12 w-12 text-teal-600 mb-4" />
                <CardTitle>Cultural Intelligence</CardTitle>
                <CardDescription>
                  Recommendations that respect your cultural preferences and dietary needs
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• Cross-cultural recommendations</li>
                  <li>• Dietary restriction support</li>
                  <li>• Regional preference matching</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 px-4 bg-gray-50">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">How It Works</h3>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">Four simple steps to optimized grocery shopping</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-green-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h4 className="text-xl font-semibold mb-2">Create Profile</h4>
              <p className="text-gray-600">Set up your taste preferences, dietary restrictions, and budget goals</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h4 className="text-xl font-semibold mb-2">Add Items</h4>
              <p className="text-gray-600">Add generic items to your list - our AI will find specific products</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-purple-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h4 className="text-xl font-semibold mb-2">Get Optimized</h4>
              <p className="text-gray-600">AI optimizes your list for cost, taste, and availability</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-orange-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                4
              </div>
              <h4 className="text-xl font-semibold mb-2">Shop Smart</h4>
              <p className="text-gray-600">Get your optimized list with store locations and best deals</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-green-600 to-blue-600 text-white">
        <div className="container mx-auto text-center">
          <h3 className="text-3xl font-bold mb-4">Ready to Transform Your Grocery Shopping?</h3>
          <p className="text-xl mb-8 opacity-90">
            Join thousands of users saving money and time with AI-powered grocery optimization
          </p>
          <Button size="lg" variant="secondary" className="text-lg px-8 py-3" asChild>
            <Link href="/profile">Start Your Free Trial</Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <ShoppingCart className="h-6 w-6 text-green-400" />
                <span className="text-xl font-bold">GroceryAI</span>
              </div>
              <p className="text-gray-400">
                AI-powered grocery optimization platform that saves you money and matches your taste.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Features</h4>
              <ul className="space-y-2 text-gray-400">
                <li>Taste Profiling</li>
                <li>Cost Optimization</li>
                <li>Store Integration</li>
                <li>Smart Alternatives</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li>About Us</li>
                <li>Privacy Policy</li>
                <li>Terms of Service</li>
                <li>Contact</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li>Help Center</li>
                <li>API Documentation</li>
                <li>Developer Guide</li>
                <li>Status</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 GroceryAI. All rights reserved. Powered by Kroger API and Qloo.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
