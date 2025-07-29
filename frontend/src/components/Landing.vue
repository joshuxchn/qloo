<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50">
    <div>
      <header class="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 h-20">
        <div class="container mx-auto px-4 h-full flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <span class="text-white font-bold text-lg">🍊</span>
            <h1 class="text-2xl font-bold text-stone-800">tangerine</h1>
          </div>
          <nav class="hidden md:flex items-center space-x-6">
            <a href="#features" class="text-stone-600 hover:text-orange-600 transition-colors">features</a>
            <a href="#how-it-works" class="text-stone-600 hover:text-orange-600 transition-colors">how it works</a>
          </nav>
          <div class="flex items-center space-x-4">
            <button
              @click="goToLogin"
              class="px-4 py-2 border border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent rounded transition-colors"
            >
              sign in
            </button>
            <button
            @click="goToSetup"
              class="px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white rounded transition-colors"
            >
              get started
            </button>
          </div>
        </div>
      </header>

      <section class="py-20 px-4">
        <div class="container mx-auto text-center">
          <div class="mb-4 inline-block px-3 py-1 bg-orange-100 text-orange-800 border border-orange-200 rounded-full text-sm">
            ai-powered grocery optimization
          </div>
          <h2 class="text-5xl font-bold text-stone-800 mb-6 leading-tight">
            smart grocery lists that
            <span class="text-orange-600"> save money</span> &
            <span class="text-emerald-700"> match your taste</span>
          </h2>
          <p class="text-xl text-stone-600 mb-8 max-w-3xl mx-auto">
            build optimized grocery lists with ai that understands your preferences, budget, and cultural background.
            get real-time prices, alternatives, and deals from kroger stores.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              @click="goToSetup"
              class="text-lg px-8 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded transition-colors"
            >
              start building lists
            </button>
          </div>
        </div>
      </section>

      <section id="features" class="py-20 px-4 bg-white">
        <div class="container mx-auto">
          <div class="text-center mb-16">
            <h3 class="text-3xl font-bold text-stone-800 mb-4">powerful features</h3>
            <p class="text-lg text-stone-600 max-w-2xl mx-auto">
              our ai-powered platform combines taste profiling, cost optimization, and real-time grocery data
            </p>
          </div>

          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div class="border border-stone-200 hover:border-orange-300 transition-colors shadow-sm rounded-lg">
              <div class="p-6">
                <Brain class="h-12 w-12 text-orange-600 mb-4" />
                <h4 class="text-lg font-semibold text-stone-800 mb-2">ai taste profiling</h4>
                <p class="text-stone-600 mb-4">
                  dynamic preference learning that adapts to your taste and cultural background
                </p>
                <ul class="space-y-2 text-sm text-stone-600">
                  <li>• personalized recommendations</li>
                  <li>• cultural intelligence via qloo api</li>
                  <li>• continuous preference learning</li>
                </ul>
              </div>
            </div>

            <div class="border border-stone-200 hover:border-emerald-300 transition-colors shadow-sm rounded-lg">
              <div class="p-6">
                <DollarSign class="h-12 w-12 text-emerald-700 mb-4" />
                <h4 class="text-lg font-semibold text-stone-800 mb-2">cost optimization</h4>
                <p class="text-stone-600 mb-4">
                  real-time price comparison and budget-friendly alternatives
                </p>
                <ul class="space-y-2 text-sm text-stone-600">
                  <li>• live kroger api pricing</li>
                  <li>• budget-optimized baskets</li>
                  <li>• deal and promotion alerts</li>
                </ul>
              </div>
            </div>

            <div class="border border-stone-200 hover:border-amber-300 transition-colors shadow-sm rounded-lg">
              <div class="p-6">
                <MapPin class="h-12 w-12 text-amber-600 mb-4" />
                <h4 class="text-lg font-semibold text-stone-800 mb-2">store integration</h4>
                <p class="text-stone-600 mb-4">
                  find the best stores with real-time inventory and location data
                </p>
                <ul class="space-y-2 text-sm text-stone-600">
                  <li>• local store finder</li>
                  <li>• real-time availability</li>
                  <li>• store hours and directions</li>
                </ul>
              </div>
            </div>

            <div class="border border-stone-200 hover:border-orange-300 transition-colors shadow-sm rounded-lg">
              <div class="p-6">
                <TrendingDown class="h-12 w-12 text-orange-600 mb-4" />
                <h4 class="text-lg font-semibold text-stone-800 mb-2">smart alternatives</h4>
                <p class="text-stone-600 mb-4">
                  healthier, cheaper, or more preferred alternatives when needed
                </p>
                <ul class="space-y-2 text-sm text-stone-600">
                  <li>• health-conscious swaps</li>
                  <li>• budget-friendly options</li>
                  <li>• taste-matched alternatives</li>
                </ul>
              </div>
            </div>

            <div class="border border-stone-200 hover:border-emerald-300 transition-colors shadow-sm rounded-lg">
              <div class="p-6">
                <ShoppingCart class="h-12 w-12 text-emerald-700 mb-4" />
                <h4 class="text-lg font-semibold text-stone-800 mb-2">list validation</h4>
                <p class="text-stone-600 mb-4">
                  convert generic items to specific products with full details
                </p>
                <ul class="space-y-2 text-sm text-stone-600">
                  <li>• generic to specific matching</li>
                  <li>• nutritional information</li>
                  <li>• product availability check</li>
                </ul>
              </div>
            </div>

            <div class="border border-stone-200 hover:border-amber-300 transition-colors shadow-sm rounded-lg">
              <div class="p-6">
                <Users class="h-12 w-12 text-amber-600 mb-4" />
                <h4 class="text-lg font-semibold text-stone-800 mb-2">cultural intelligence</h4>
                <p class="text-stone-600 mb-4">
                  recommendations that respect your cultural preferences and dietary needs
                </p>
                <ul class="space-y-2 text-sm text-stone-600">
                  <li>• cross-cultural recommendations</li>
                  <li>• dietary restriction support</li>
                  <li>• regional preference matching</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="how-it-works" class="py-20 px-4 bg-stone-50">
        <div class="container mx-auto">
          <div class="text-center mb-16">
            <h3 class="text-3xl font-bold text-stone-800 mb-4">how it works</h3>
            <p class="text-lg text-stone-600 max-w-2xl mx-auto">four simple steps to optimized grocery shopping</p>
          </div>

          <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div class="text-center">
              <div class="w-16 h-16 bg-orange-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h4 class="text-xl font-semibold mb-2 text-stone-800">create profile</h4>
              <p class="text-stone-600">set up your taste preferences, dietary restrictions, and budget goals</p>
            </div>

            <div class="text-center">
              <div class="w-16 h-16 bg-emerald-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h4 class="text-xl font-semibold mb-2 text-stone-800">add items</h4>
              <p class="text-stone-600">add generic items to your list - our ai will find specific products</p>
            </div>

            <div class="text-center">
              <div class="w-16 h-16 bg-amber-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h4 class="text-xl font-semibold mb-2 text-stone-800">get optimized</h4>
              <p class="text-stone-600">ai optimizes your list for cost, taste, and availability</p>
            </div>

            <div class="text-center">
              <div class="w-16 h-16 bg-orange-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                4
              </div>
              <h4 class="text-xl font-semibold mb-2 text-stone-800">shop smart</h4>
              <p class="text-stone-600">get your optimized list with store locations and best deals</p>
            </div>
          </div>
        </div>
      </section>

      <section class="py-20 px-4 bg-gradient-to-r from-orange-500 to-amber-500 text-white">
        <div class="container mx-auto text-center">
          <h3 class="text-3xl font-bold mb-4">ready to transform your grocery shopping?</h3>
          <p class="text-xl mb-8 opacity-90">
            join thousands of users saving money and time with ai-powered grocery optimization
          </p>
          <button
            @click="goToSetup"
            class="text-lg px-8 py-3 bg-white text-orange-600 hover:bg-stone-50 rounded transition-colors"
          >
            start your free trial
          </button>
        </div>
      </section>

      <footer class="bg-stone-800 text-stone-200 py-12 px-4">
        <div class="container mx-auto">
          <div class="grid md:grid-cols-4 gap-8">
            <div>
              <div class="flex items-center space-x-3 mb-4">
                <div class="w-[60px] h-[60px] bg-orange-500 rounded-full flex items-center justify-center">
                  <span class="text-white font-bold text-lg">T</span>
                </div>
                <span class="text-xl font-bold">tangerine</span>
              </div>
              <p class="text-stone-400">
                ai-powered grocery optimization platform that saves you money and matches your taste.
              </p>
            </div>

            <div>
              <h4 class="font-semibold mb-4">features</h4>
              <ul class="space-y-2 text-stone-400">
                <li>taste profiling</li>
                <li>cost optimization</li>
                <li>store integration</li>
                <li>smart alternatives</li>
              </ul>
            </div>

            <div>
              <h4 class="font-semibold mb-4">company</h4>
              <ul class="space-y-2 text-stone-400">
                <li>about us</li>
                <li>privacy policy</li>
                <li>terms of service</li>
                <li>contact</li>
              </ul>
            </div>

            <div>
              <h4 class="font-semibold mb-4">support</h4>
              <ul class="space-y-2 text-stone-400">
                <li>help center</li>
                <li>api documentation</li>
                <li>developer guide</li>
                <li>status</li>
              </ul>
            </div>
          </div>

          <div class="border-t border-stone-700 mt-8 pt-8 text-center text-stone-400">
            <p>&copy; 2025 tangerine. all rights reserved. powered by kroger api and qloo.</p>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'; // Import useRouter
import {
  ShoppingCart,
  DollarSign,
  TrendingDown,
  Brain,
  MapPin,
  Users,
} from 'lucide-vue-next'

const router = useRouter(); // Initialize router

const goToLogin = () => {
  router.push('/login'); // Navigate to the /login route
};
const goToSetup = () => {
  router.push('/setup'); // Navigate to the /login route
};
</script>