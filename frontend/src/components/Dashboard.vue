<template>
  <div>
    <header class="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 h-20">
      <div class="container mx-auto px-4 h-full flex items-center justify-between">
        <button @click="$emit('set-current-view', 'landing')" class="flex items-center space-x-3">
            <span class="text-white font-bold text-lg">🍊</span>
          <h1 class="text-xl font-bold text-stone-800">tangerine</h1>
        </button>
        <div class="flex items-center space-x-4">
          <button
            @click="redirectToProfile"
            class="px-3 py-1 text-sm text-stone-600 hover:text-orange-600 hover:bg-orange-50 rounded transition-colors"
          >
            Profile
          </button>
          <button 
            @click="signOut"
            class="px-3 py-1 text-sm border border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent rounded transition-colors"
          >
            Sign Out
          </button>
        </div>
      </div>
    </header>

    <div class="container mx-auto px-4 py-8">
      <div class="grid md:grid-cols-3 gap-4 mb-8">
        <div class="bg-white border-0 shadow-sm rounded-lg p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs text-stone-500">total</p>
              <p class="text-xl font-medium text-stone-800">${{ totalCost.toFixed(2) }}</p>
            </div>
            <div class="h-5 w-5 bg-orange-200 rounded-full flex items-center justify-center text-orange-600 text-xs">$$</div>
          </div>
        </div>

        <div class="bg-white border-0 shadow-sm rounded-lg p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs text-stone-500">saved</p>
              <p class="text-xl font-medium text-emerald-700">${{ totalSavings.toFixed(2) }}</p>
            </div>
            <div class="h-5 w-5 bg-emerald-200 rounded-full flex items-center justify-center text-emerald-700 text-xs">📉</div>
          </div>
        </div>

        <div class="bg-white border-0 shadow-sm rounded-lg p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-xs text-stone-500">items</p>
              <p class="text-xl font-medium text-stone-800">{{ groceryList.length }}</p>
            </div>
            <div class="h-5 w-5 bg-amber-200 rounded-full flex items-center justify-center text-amber-600 text-xs">🛒</div>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="grid w-full grid-cols-3 bg-stone-100 border-0 rounded-lg p-1">
          <button
            @click="activeTab = 'list'"
            :class="[
              'text-sm px-4 py-2 rounded transition-colors',
              activeTab === 'list'
                ? 'bg-white text-stone-800 shadow-sm'
                : 'text-stone-600 hover:text-stone-800'
            ]"
          >
            list
          </button>
          <button
            @click="activeTab = 'recommendations'"
            :class="[
              'text-sm px-4 py-2 rounded transition-colors',
              activeTab === 'recommendations'
                ? 'bg-white text-stone-800 shadow-sm'
                : 'text-stone-600 hover:text-stone-800'
            ]"
          >
            suggestions
          </button>
          <button
            @click="activeTab = 'analytics'"
            :class="[
              'text-sm px-4 py-2 rounded transition-colors',
              activeTab === 'analytics'
                ? 'bg-white text-stone-800 shadow-sm'
                : 'text-stone-600 hover:text-stone-800'
            ]"
          >
            insights
          </button>
        </div>

        <div v-if="activeTab === 'list'" class="bg-white border-0 shadow-sm rounded-lg">
          <div class="p-6 border-b">
             <span class="text-sm text-stone-600 hidden sm:block">
            Welcome, <span class="font-semibold">{{ currentUser?.firstName || currentUser?.username || 'Guest' }}</span>
          </span>
          </div>
          <div class="p-6">
            <div class="flex gap-2 mb-6">
              <input
                v-model="newItem"
                @keyup.enter="addItem"
                placeholder="add item..."
                class="flex-1 px-3 py-2 border-0 bg-stone-50 text-stone-800 placeholder:text-stone-500 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
              <button
                @click="addItem"
                class="px-3 py-2 bg-orange-500 hover:bg-orange-600 text-white rounded-md transition-colors"
              >
                <span class="text-white">+</span>
              </button>
            </div>

            <div class="space-y-3">
              <div
                v-for="item in groceryList"
                :key="item.id"
                class="flex items-center justify-between p-3 bg-stone-50 rounded-lg hover:bg-stone-100 transition-colors"
              >
                <div class="flex-1">
                  <div class="flex items-center gap-3">
                    <div class="flex-1">
                      <h4 class="font-medium text-stone-800 text-sm">{{ item.name }}</h4>
                      <div class="flex items-center gap-3 mt-1">
                        <span class="text-xs px-2 py-1 border border-stone-300 text-stone-600 rounded lowercase">
                          {{ item.category }}
                        </span>
                        <span class="text-xs text-stone-500">{{ item.store }}</span>
                        <div v-if="item.healthScore" class="flex items-center gap-1">
                          <span class="text-amber-500">⭐</span>
                          <span class="text-xs text-stone-500">{{ item.healthScore }}</span>
                        </div>
                      </div>
                    </div>

                    <div class="text-right">
                      <div class="flex items-center gap-2">
                        <span
                          v-if="item.originalPrice"
                          class="text-xs text-stone-400 line-through"
                        >
                          ${{ item.originalPrice.toFixed(2) }}
                        </span>
                        <span class="font-medium text-emerald-700 text-sm">
                          ${{ item.price.toFixed(2) }}
                        </span>
                      </div>
                      <span v-if="item.alternatives" class="text-xs text-orange-600">
                        {{ item.alternatives }} options
                      </span>
                    </div>
                  </div>
                </div>

                <div class="flex items-center gap-2 ml-4">
                  <span v-if="item.inStock" class="text-emerald-600">✅</span>
                  <span v-else class="text-amber-600">⚠️</span>
                  <button
                    @click="removeItem(item.id)"
                    class="text-stone-400 hover:text-red-500 h-6 w-6 p-0 transition-colors"
                  >
                    <span class="text-red-500">🗑️</span>
                  </button>
                </div>
              </div>
            </div>

            <div v-if="groceryList.length === 0" class="text-center py-12 text-stone-400">
              <span class="text-stone-400 text-4xl block mb-3 opacity-50">🛒</span>
              <p class="text-sm">no items yet</p>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'recommendations'" class="grid md:grid-cols-2 gap-4">
          <div class="bg-white border-0 shadow-sm rounded-lg">
            <div class="p-4 border-b">
              <h4 class="text-sm font-medium text-stone-800">alternatives</h4>
            </div>
            <div class="p-4 space-y-3">
              <div class="p-3 bg-stone-50 rounded-lg">
                <div class="flex justify-between items-start mb-2">
                  <h4 class="font-medium text-sm text-stone-800">greek yogurt</h4>
                  <span class="text-xs px-2 py-1 bg-emerald-100 text-emerald-800 rounded">healthier</span>
                </div>
                <p class="text-xs text-stone-600 mb-2">higher protein</p>
                <div class="flex justify-between text-xs">
                  <span class="text-stone-500">was $4.99</span>
                  <span class="text-emerald-700 font-medium">now $5.99</span>
                </div>
              </div>

              <div class="p-3 bg-stone-50 rounded-lg">
                <div class="flex justify-between items-start mb-2">
                  <h4 class="font-medium text-sm text-stone-800">whole wheat bread</h4>
                  <span class="text-xs px-2 py-1 bg-orange-100 text-orange-800 rounded">better value</span>
                </div>
                <p class="text-xs text-stone-600 mb-2">more nutritious</p>
                <div class="flex justify-between text-xs">
                  <span class="text-stone-500">was $2.99</span>
                  <span class="text-emerald-700 font-medium">now $3.29</span>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white border-0 shadow-sm rounded-lg">
            <div class="p-4 border-b">
              <h4 class="text-sm font-medium text-stone-800">suggestions</h4>
            </div>
            <div class="p-4 space-y-3">
              <div class="p-3 bg-stone-50 rounded-lg">
                <h4 class="font-medium mb-2 text-sm text-stone-800">mediterranean</h4>
                <div class="space-y-1 text-xs">
                  <div class="flex justify-between">
                    <span class="text-stone-600">olive oil</span>
                    <span class="text-emerald-700">$8.99</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-stone-600">fresh basil</span>
                    <span class="text-emerald-700">$2.49</span>
                  </div>
                </div>
              </div>

              <div class="p-3 bg-stone-50 rounded-lg">
                <h4 class="font-medium mb-2 text-sm text-stone-800">seasonal</h4>
                <div class="space-y-1 text-xs">
                  <div class="flex justify-between">
                    <span class="text-stone-600">winter squash</span>
                    <span class="text-emerald-700">$1.99/lb</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-stone-600">brussels sprouts</span>
                    <span class="text-emerald-700">$3.49/lb</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'analytics'" class="grid md:grid-cols-2 gap-4">
          <div class="bg-white border-0 shadow-sm rounded-lg">
            <div class="p-4 border-b">
              <h4 class="text-sm font-medium text-stone-800">budget</h4>
              <p class="text-xs text-stone-600">weekly limit: ${{ currentUser?.budget || 0 }}</p>
            </div>
            <div class="p-4">
              <div class="space-y-4">
                <div>
                  <div class="flex justify-between text-xs mb-2">
                    <span class="text-stone-600">current</span>
                    <span class="text-stone-600">${{ totalCost.toFixed(2) }} / ${{ currentUser?.budget || 0 }}</span>
                  </div>
                  <div class="w-full bg-stone-200 rounded-full h-1">
                    <div
                      class="bg-orange-500 h-1 rounded-full transition-all"
                      :style="{ width: `${Math.min((totalCost / (currentUser?.budget || 1)) * 100, 100)}%` }"
                    ></div>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-3 text-center">
                  <div class="p-3 bg-emerald-50 rounded-lg">
                    <div class="text-sm font-medium text-emerald-700">
                      ${{ ((currentUser?.budget || 0) - totalCost).toFixed(2) }}
                    </div>
                    <div class="text-xs text-stone-600">remaining</div>
                  </div>
                  <div class="p-3 bg-orange-50 rounded-lg">
                    <div class="text-sm font-medium text-orange-600">
                      ${{ totalSavings.toFixed(2) }}
                    </div>
                    <div class="text-xs text-stone-600">saved</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white border-0 shadow-sm rounded-lg">
            <div class="p-4 border-b">
              <h4 class="text-sm font-medium text-stone-800">insights</h4>
            </div>
            <div class="p-4">
              <div class="space-y-4">
                <div>
                  <h4 class="font-medium mb-2 text-xs text-stone-600">categories</h4>
                  <div class="space-y-2">
                    <div class="flex justify-between text-xs">
                      <span class="text-stone-600">produce</span>
                      <span class="text-emerald-700">35%</span>
                    </div>
                    <div class="flex justify-between text-xs">
                      <span class="text-stone-600">meat</span>
                      <span class="text-orange-600">25%</span>
                    </div>
                    <div class="flex justify-between text-xs">
                      <span class="text-stone-600">dairy</span>
                      <span class="text-amber-600">20%</span>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 class="font-medium mb-2 text-xs text-stone-600">health score</h4>
                  <div class="flex items-center gap-2">
                    <div class="flex-1 bg-stone-200 rounded-full h-1">
                      <div class="bg-orange-500 h-1 rounded-full w-[85%]"></div>
                    </div>
                    <span class="text-xs font-medium text-stone-800">85</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-8 flex justify-center">
        <button
          @click="handleCheckout"
          class="px-8 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors flex items-center gap-2"
        >
          Checkout at Kroger
          <span class="text-white">↗️</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { userStore } from '../stores/userStore.js';

export default {
  name: 'Dashboard',
  data() {
    return {
      activeTab: 'list',
      newItem: '',
      groceryList: [
        {
          id: 1,
          name: 'Organic Free-Range Eggs',
          category: 'dairy & alternatives',
          store: 'Whole Foods',
          healthScore: 9,
          originalPrice: 7.99,
          price: 6.50,
          alternatives: 3,
          inStock: true
        },
        {
          id: 2,
          name: 'Avocados (3-pack)',
          category: 'produce',
          store: 'Kroger',
          healthScore: 8,
          originalPrice: 5.49,
          price: 4.99,
          alternatives: 0,
          inStock: true
        },
        {
          id: 3,
          name: 'Artisan Sourdough Bread',
          category: 'bakery',
          store: 'Local Bakery',
          healthScore: 7,
          originalPrice: 4.29,
          price: 3.99,
          alternatives: 1,
          inStock: false
        },
        {
          id: 4,
          name: 'Grass-fed Ground Beef',
          category: 'meat',
          store: 'Butcher Shop',
          healthScore: 6,
          originalPrice: 10.99,
          price: 9.50,
          alternatives: 0,
          inStock: true
        }
      ]
    };
  },
  computed: {
    currentUser() {
      return userStore.user;
    },
    totalCost() {
      return this.groceryList.reduce((sum, item) => sum + item.price, 0);
    },
    totalSavings() {
      return this.groceryList.reduce((sum, item) => {
        if (item.originalPrice) {
          return sum + (item.originalPrice - item.price);
        }
        return sum;
      }, 0);
    }
  },
  methods: {
    signOut() {
      userStore.logout();
      this.$router.push('/login');
    },
    redirectToProfile() {
      this.$router.push('/profile');
    },
    redirectToNewList() {
      this.$router.push('/newList');
    },
    addItem() {
      if (this.newItem.trim()) {
        this.groceryList.push({
          id: Date.now(),
          name: this.newItem.trim(),
          category: 'uncategorized',
          store: 'unknown',
          price: 0.00,
          inStock: true
        });
        this.newItem = '';
      }
    },
    removeItem(id) {
      this.groceryList = this.groceryList.filter(item => item.id !== id);
    },
    handleCheckout() {
      alert('Simulating checkout process at Kroger!');
    }
  }
};
</script>

<style scoped>
/* Scoped styles for Dashboard component if any */
</style>