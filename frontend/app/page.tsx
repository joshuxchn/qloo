import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ShoppingCart, DollarSign, MapPin, Brain, TrendingDown, Users } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 h-20">
        <div className="container mx-auto px-4 h-full flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Image
              src="/images/tangerine-logo.png"
              alt="Tangerine Logo"
              width={75}
              height={75}
              className="rounded-full"
            />
            <h1 className="text-2xl font-bold text-stone-800">tangerine</h1>
          </div>
          <nav className="hidden md:flex items-center space-x-6">
            <Link href="#features" className="text-stone-600 hover:text-orange-600 transition-colors">
              features
            </Link>
            <Link href="#how-it-works" className="text-stone-600 hover:text-orange-600 transition-colors">
              how it works
            </Link>
            <Link href="/dashboard" className="text-stone-600 hover:text-orange-600 transition-colors">
              dashboard
            </Link>
          </nav>
          <div className="flex items-center space-x-4">
            <Button
              variant="outline"
              asChild
              className="border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent"
            >
              <Link href="/signin">sign in</Link>
            </Button>
            <Button asChild className="bg-orange-500 hover:bg-orange-600 text-white">
              <Link href="/profile">get started</Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <Badge className="mb-4 bg-orange-100 text-orange-800 hover:bg-orange-100 border-orange-200">
            ai-powered grocery optimization
          </Badge>
          <h2 className="text-5xl font-bold text-stone-800 mb-6 leading-tight">
            smart grocery lists that
            <span className="text-orange-600"> save money</span> &
            <span className="text-emerald-700"> match your taste</span>
          </h2>
          <p className="text-xl text-stone-600 mb-8 max-w-3xl mx-auto">
            build optimized grocery lists with ai that understands your preferences, budget, and cultural background.
            get real-time prices, alternatives, and deals from kroger stores.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="text-lg px-8 py-3 bg-orange-500 hover:bg-orange-600" asChild>
              <Link href="/profile">start building lists</Link>
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="text-lg px-8 py-3 bg-transparent border-stone-300 text-stone-700 hover:bg-stone-50"
              asChild
            >
              <Link href="#features">learn more</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-white">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h3 className="text-3xl font-bold text-stone-800 mb-4">powerful features</h3>
            <p className="text-lg text-stone-600 max-w-2xl mx-auto">
              our ai-powered platform combines taste profiling, cost optimization, and real-time grocery data
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="border border-stone-200 hover:border-orange-300 transition-colors shadow-sm">
              <CardHeader>
                <Brain className="h-12 w-12 text-orange-600 mb-4" />
                <CardTitle className="text-stone-800">ai taste profiling</CardTitle>
                <CardDescription className="text-stone-600">
                  dynamic preference learning that adapts to your taste and cultural background
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-stone-600">
                  <li>• personalized recommendations</li>
                  <li>• cultural intelligence via qloo api</li>
                  <li>• continuous preference learning</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border border-stone-200 hover:border-emerald-300 transition-colors shadow-sm">
              <CardHeader>
                <DollarSign className="h-12 w-12 text-emerald-700 mb-4" />
                <CardTitle className="text-stone-800">cost optimization</CardTitle>
                <CardDescription className="text-stone-600">
                  real-time price comparison and budget-friendly alternatives
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-stone-600">
                  <li>• live kroger api pricing</li>
                  <li>• budget-optimized baskets</li>
                  <li>• deal and promotion alerts</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border border-stone-200 hover:border-amber-300 transition-colors shadow-sm">
              <CardHeader>
                <MapPin className="h-12 w-12 text-amber-600 mb-4" />
                <CardTitle className="text-stone-800">store integration</CardTitle>
                <CardDescription className="text-stone-600">
                  find the best stores with real-time inventory and location data
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-stone-600">
                  <li>• local store finder</li>
                  <li>• real-time availability</li>
                  <li>• store hours and directions</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border border-stone-200 hover:border-orange-300 transition-colors shadow-sm">
              <CardHeader>
                <TrendingDown className="h-12 w-12 text-orange-600 mb-4" />
                <CardTitle className="text-stone-800">smart alternatives</CardTitle>
                <CardDescription className="text-stone-600">
                  healthier, cheaper, or more preferred alternatives when needed
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-stone-600">
                  <li>• health-conscious swaps</li>
                  <li>• budget-friendly options</li>
                  <li>• taste-matched alternatives</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border border-stone-200 hover:border-emerald-300 transition-colors shadow-sm">
              <CardHeader>
                <ShoppingCart className="h-12 w-12 text-emerald-700 mb-4" />
                <CardTitle className="text-stone-800">list validation</CardTitle>
                <CardDescription className="text-stone-600">
                  convert generic items to specific products with full details
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-stone-600">
                  <li>• generic to specific matching</li>
                  <li>• nutritional information</li>
                  <li>• product availability check</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border border-stone-200 hover:border-amber-300 transition-colors shadow-sm">
              <CardHeader>
                <Users className="h-12 w-12 text-amber-600 mb-4" />
                <CardTitle className="text-stone-800">cultural intelligence</CardTitle>
                <CardDescription className="text-stone-600">
                  recommendations that respect your cultural preferences and dietary needs
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm text-stone-600">
                  <li>• cross-cultural recommendations</li>
                  <li>• dietary restriction support</li>
                  <li>• regional preference matching</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 px-4 bg-stone-50">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h3 className="text-3xl font-bold text-stone-800 mb-4">how it works</h3>
            <p className="text-lg text-stone-600 max-w-2xl mx-auto">four simple steps to optimized grocery shopping</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h4 className="text-xl font-semibold mb-2 text-stone-800">create profile</h4>
              <p className="text-stone-600">set up your taste preferences, dietary restrictions, and budget goals</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-emerald-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h4 className="text-xl font-semibold mb-2 text-stone-800">add items</h4>
              <p className="text-stone-600">add generic items to your list - our ai will find specific products</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-amber-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h4 className="text-xl font-semibold mb-2 text-stone-800">get optimized</h4>
              <p className="text-stone-600">ai optimizes your list for cost, taste, and availability</p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-orange-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                4
              </div>
              <h4 className="text-xl font-semibold mb-2 text-stone-800">shop smart</h4>
              <p className="text-stone-600">get your optimized list with store locations and best deals</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-orange-500 to-amber-500 text-white">
        <div className="container mx-auto text-center">
          <h3 className="text-3xl font-bold mb-4">ready to transform your grocery shopping?</h3>
          <p className="text-xl mb-8 opacity-90">
            join thousands of users saving money and time with ai-powered grocery optimization
          </p>
          <Button
            size="lg"
            variant="secondary"
            className="text-lg px-8 py-3 bg-white text-orange-600 hover:bg-stone-50"
            asChild
          >
            <Link href="/profile">start your free trial</Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-stone-800 text-stone-200 py-12 px-4">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <Image
                  src="/images/tangerine-logo.png"
                  alt="Tangerine Logo"
                  width={60}
                  height={60}
                  className="rounded-full"
                />
                <span className="text-xl font-bold">tangerine</span>
              </div>
              <p className="text-stone-400">
                ai-powered grocery optimization platform that saves you money and matches your taste.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-4">features</h4>
              <ul className="space-y-2 text-stone-400">
                <li>taste profiling</li>
                <li>cost optimization</li>
                <li>store integration</li>
                <li>smart alternatives</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">company</h4>
              <ul className="space-y-2 text-stone-400">
                <li>about us</li>
                <li>privacy policy</li>
                <li>terms of service</li>
                <li>contact</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">support</h4>
              <ul className="space-y-2 text-stone-400">
                <li>help center</li>
                <li>api documentation</li>
                <li>developer guide</li>
                <li>status</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-stone-700 mt-8 pt-8 text-center text-stone-400">
            <p>&copy; 2025 tangerine. all rights reserved. powered by kroger api and qloo.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
