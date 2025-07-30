<template>
  <div class="min-h-screen">
    <header class="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 h-20">
      <div class="container mx-auto px-4 h-full flex items-center justify-between">
        <button @click="backToDashboard" class="flex items-center space-x-3">
          <span class="text-white font-bold text-lg">🍊</span>
          <h1 class="text-2xl font-bold text-stone-800">tangerine</h1>
        </button>
        <div class="flex items-center space-x-4">
          <button @click="backToDashboard" class="px-4 py-2 border border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent rounded transition-colors">
            Back to Dashboard
          </button>
          <button v-if="generatedItems.length > 0" @click="saveList" :disabled="isSaving" class="px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white rounded transition-colors flex items-center gap-2 disabled:bg-stone-400">
            Save List & View
          </button>
        </div>
      </div>
    </header>

    <div class="container mx-auto px-4 py-8">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-stone-800 mb-4">Build Your Grocery List</h2>
          <p class="text-lg text-stone-600">
            Use AI to generate optimized grocery lists from recipes, meal plans, or natural language
          </p>
        </div>

        <div class="grid lg:grid-cols-2 gap-8">
          <div class="space-y-6">
            <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
              <div class="p-6 border-b">
                <h3 class="text-lg font-medium text-stone-800">Name Your Grocery List</h3>
              </div>
              <div class="p-6">
                <input 
                  v-model="listName" 
                  placeholder="e.g., Weekly Groceries, Party Prep" 
                  class="w-full px-3 py-2 border border-stone-300 rounded-md" 
                />
              </div>
            </div>
            <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
              <div class="p-6 border-b">
                <h3 class="text-lg font-medium text-stone-800">Choose Your Input Method</h3>
              </div>
              <div class="p-6">
                <div class="grid w-full grid-cols-4 bg-stone-100 border-0 rounded-lg p-1 mb-6">
                  <button @click="inputMethod = 'manual'" :class="getTabClass('manual')">Manual</button>
                  <button @click="inputMethod = 'ai'" :class="getTabClass('ai')">AI Prompt</button>
                  <button @click="inputMethod = 'recipe'" :class="getTabClass('recipe')">Recipe</button>
                  <button @click="inputMethod = 'photo'" :class="getTabClass('photo')">Photo</button>
                </div>

                <div v-if="inputMethod === 'manual'" class="space-y-4">
                  <h4 class="font-medium mb-2 text-stone-800">Add Items Manually</h4>
                  <div class="flex gap-2">
                    <input v-model="manualItem" @keyup.enter="addManualItem" placeholder="e.g., 'milk', 'bananas'" class="flex-1 px-3 py-2 border border-stone-300 rounded-md" />
                    <button @click="addManualItem" class="px-3 py-2 bg-orange-500 hover:bg-orange-600 text-white rounded-md">
                      <Plus class="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <div v-if="inputMethod === 'ai'" class="space-y-4">
                  <h4 class="font-medium mb-2 text-stone-800">AI-Powered Generation</h4>
                  <textarea v-model="aiPrompt" placeholder="e.g., 'Healthy meals for a family of 4 this week...'" class="w-full px-3 py-2 border border-stone-300 rounded-md min-h-[100px]"></textarea>
                  <button @click="generateAIList" :disabled="isGenerating || !aiPrompt.trim()" class="w-full mt-2 px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:bg-stone-300 text-white rounded-md flex-center-gap">
                    <Clock v-if="isGenerating" class="h-4 w-4 animate-spin" />
                    <Sparkles v-else class="h-4 w-4" />
                    {{ isGenerating ? 'Generating...' : 'Generate List' }}
                  </button>
                </div>

                <div v-if="inputMethod === 'recipe'" class="space-y-4">
                  <h4 class="font-medium mb-2 text-stone-800">Recipe Analysis</h4>
                  <textarea v-model="recipe" placeholder="Paste your recipe here..." class="w-full px-3 py-2 border border-stone-300 rounded-md min-h-[120px]"></textarea>
                  <button @click="analyzeRecipe" :disabled="isGenerating || !recipe.trim()" class="w-full mt-2 px-4 py-2 bg-orange-500 hover:bg-orange-600 disabled:bg-stone-300 text-white rounded-md flex-center-gap">
                    <Clock v-if="isGenerating" class="h-4 w-4 animate-spin" />
                    <FileText v-else class="h-4 w-4" />
                    {{ isGenerating ? 'Analyzing...' : 'Extract Ingredients' }}
                  </button>
                </div>

                <div v-if="inputMethod === 'photo'" class="space-y-4">
                  <h4 class="font-medium mb-2 text-stone-800">Photo Recognition</h4>
                  <div class="border-2 border-dashed border-stone-300 rounded-lg p-8 text-center">
                    <Camera class="h-12 w-12 text-stone-400 mx-auto mb-4" />
                    <p class="text-stone-600 mb-4">Drag and drop an image here</p>
                    <button disabled class="px-4 py-2 border border-stone-300 text-stone-700 bg-transparent rounded flex-center-gap mx-auto">
                      <Upload class="h-4 w-4" />
                      Upload Photo (Coming Soon)
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
              <div class="p-6 border-b">
                <h3 class="text-lg font-medium text-stone-800">Quick Templates</h3>
                <p class="text-stone-600 mt-1">Start with pre-made templates for common meal plans</p>
              </div>
              <div class="p-6 grid grid-cols-2 gap-3">
                <button @click="setTemplate('Weekly meal prep for healthy eating, including proteins, vegetables, and whole grains')" class="template-button">
                  <div class="font-medium text-stone-800">Meal Prep</div>
                  <div class="text-xs text-stone-500">Healthy weekly prep</div>
                </button>
                <button @click="setTemplate('Family dinner ingredients for a week, kid-friendly meals')" class="template-button">
                  <div class="font-medium text-stone-800">Family Dinners</div>
                  <div class="text-xs text-stone-500">Kid-friendly meals</div>
                </button>
              </div>
            </div>
          </div>

          <div class="space-y-6">
            <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
              <div class="p-6 border-b">
                <div class="flex items-center justify-between">
                  <h3 class="text-lg font-medium text-stone-800">Generated Items</h3>
                  <span v-if="generatedItems.length > 0" class="px-2 py-1 bg-stone-100 text-stone-600 text-sm rounded">{{ generatedItems.length }} items</span>
                </div>
              </div>
              <div class="p-6">
                <div v-if="isGenerating" class="text-center py-12 text-stone-500">
                    <div class="inline-block animate-spin"><Sparkles class="h-8 w-8 text-orange-500" /></div>
                    <p class="mt-4">AI is thinking...</p>
                </div>
                <div v-else-if="generatedItems.length === 0" class="text-center py-12 text-stone-400">
                  <ShoppingCart class="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>No items generated yet.</p>
                </div>
                <div v-else class="space-y-3">
                  <div v-for="item in generatedItems" :key="item.id" class="flex items-center text-sm bg-stone-50 p-3 rounded-md shadow-sm">
                    <div class="flex-1">
                      <div class="flex justify-between items-start">
                        <div>
                          <p class="font-semibold text-stone-800">{{ item.name }} (x{{ item.quantity }})</p>
                          <p class="text-xs text-stone-500">{{ item.brand }} • {{ item.size }}</p>
                          <p class="text-xs text-stone-500">{{ item.fulfillment_type }} • <span :class="item.inventory === 'In Stock' ? 'text-emerald-600' : 'text-amber-600'">{{ item.inventory }}</span></p>
                        </div>
                        <div class="text-right">
                          <p v-if="item.promo_price" class="font-semibold text-emerald-600">${{ (parseFloat(item.promo_price) || 0).toFixed(2) }}</p>
                          <p :class="item.promo_price ? 'text-xs text-stone-400 line-through' : 'font-semibold text-stone-800'">
                            ${{ (parseFloat(item.price) || 0).toFixed(2) }}
                          </p>
                        </div>
                      </div>
                    </div>
                    <div class="ml-4 flex flex-col gap-2">
                      <button @click="swapItem(item.id)" class="text-blue-500 hover:text-blue-700 p-1" title="Swap Item">🔄</button>
                      <button @click="removeGeneratedItem(item.id)" class="text-red-500 hover:text-red-700 p-1" title="Remove Item">🗑️</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { userStore } from '@/stores/userStore';
import {
  ArrowRight, Plus, Sparkles, Clock, FileText, Camera, Upload, ShoppingCart
} from 'lucide-vue-next';

const router = useRouter();
const base_url = import.meta.env.VITE_API_BASE_URL;

const listName = ref('My Weekly Groceries');
const isSaving = ref(false);
const inputMethod = ref('ai');
const manualItem = ref('');
const aiPrompt = ref('');
const recipe = ref('');
const isGenerating = ref(false);
const generatedItems = ref([]);

// --- MOCK PRODUCT DATABASE ---
// MODIFIED: This is now the single source of truth for all mock products.
// It includes fulfillment_type and more variety.
const mockProductDatabase = [
  { name: 'Organic Milk', quantity: 1, price: 4.50, promo_price: null, brand: 'Horizon', size: 'Half Gallon', inventory: 'In Stock', category: 'Dairy', fulfillment_type: 'In-Store Pickup' },
  { name: 'Avocados', quantity: 3, price: 5.00, promo_price: 4.50, brand: 'Calavo', size: '3-pack', inventory: 'In Stock', category: 'Produce', fulfillment_type: 'In-Store Pickup' },
  { name: 'Sourdough Bread', quantity: 1, price: 5.99, promo_price: null, brand: 'Local Bakery', size: '1 loaf', inventory: 'Low Stock', category: 'Bakery', fulfillment_type: 'In-Store Pickup' },
  { name: 'Ground Turkey', quantity: 1, price: 6.99, promo_price: null, brand: 'Jennie-O', size: '1 lb', inventory: 'In Stock', category: 'Meat', fulfillment_type: 'Delivery' },
  { name: 'Spinach', quantity: 1, price: 3.50, promo_price: null, brand: 'Organic Girl', size: '5 oz', inventory: 'In Stock', category: 'Produce', fulfillment_type: 'Delivery' },
  { name: 'Chicken Breast', quantity: 2, price: 10.99, promo_price: null, brand: 'Tyson', size: '1.5 lbs', inventory: 'In Stock', category: 'Meat', fulfillment_type: 'In-Store Pickup' },
  { name: 'Broccoli', quantity: 1, price: 2.50, promo_price: null, brand: 'Fresh Farms', size: '1 bunch', inventory: 'In Stock', category: 'Produce', fulfillment_type: 'Delivery' },
  { name: 'Brown Rice', quantity: 1, price: 3.99, promo_price: null, brand: 'Uncle Ben\'s', size: '2 lb bag', inventory: 'In Stock', category: 'Grains', fulfillment_type: 'Shipping' },
  { name: 'Flour', quantity: 1, price: 3.49, promo_price: null, brand: 'Gold Medal', size: '5 lb bag', inventory: 'In Stock', category: 'Baking', fulfillment_type: 'Shipping' },
  { name: 'Eggs', quantity: 1, price: 4.99, promo_price: null, brand: 'Eggland\'s Best', size: '1 dozen', inventory: 'In Stock', category: 'Dairy', fulfillment_type: 'In-Store Pickup' },
];

const backToDashboard = () => {
  router.push('/dashboard');
};

const saveList = async () => {
  if (!listName.value.trim() || generatedItems.value.length === 0) return;
  isSaving.value = true;
  try {
    const payload = { name: listName.value, items: generatedItems.value };
    const response = await fetch(`${base_url}/api/grocery-list/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${userStore.token}`
      },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error('Failed to save list.');
    router.push('/dashboard');
  } catch (error) {
    console.error("Error saving list:", error);
    alert("There was an error saving your list.");
  } finally {
    isSaving.value = false;
  }
};

const getTabClass = (method) => {
  const base = 'text-xs px-2 py-2 rounded transition-colors';
  return inputMethod.value === method ? `${base} bg-white text-stone-800 shadow-sm` : `${base} text-stone-600 hover:text-stone-800`;
};

const addManualItem = () => {
  if (!manualItem.value.trim()) return;
  generatedItems.value.push({
    id: Date.now(),
    name: manualItem.value.trim(),
    quantity: 1, price: 0.00, promo_price: null, brand: 'N/A', size: 'N/A',
    inventory: 'Unknown', category: 'Uncategorized', fulfillment_type: 'In-Store Pickup',
  });
  manualItem.value = '';
};

// MODIFIED: AI functions now pull random items from the mock database
const mockAPICall = (itemCount = 3) => {
  isGenerating.value = true;
  generatedItems.value = [];
  return new Promise(resolve => {
    setTimeout(() => {
      // Shuffle and pick a few random items
      const shuffled = [...mockProductDatabase].sort(() => 0.5 - Math.random());
      generatedItems.value = shuffled.slice(0, itemCount).map((item, index) => ({ id: Date.now() + index, ...item }));
      isGenerating.value = false;
      resolve();
    }, 1500);
  });
};

const generateAIList = () => {
  mockAPICall(4); // Generate 4 random items
};

const analyzeRecipe = () => {
  mockAPICall(3); // Generate 3 random items
};

const setTemplate = (template) => {
  inputMethod.value = 'ai';
  aiPrompt.value = template;
};

const removeGeneratedItem = (id) => {
  generatedItems.value = generatedItems.value.filter(item => item.id !== id);
};

const swapItem = (itemId) => {
  const itemIndex = generatedItems.value.findIndex(item => item.id === itemId);
  if (itemIndex > -1) {
    let newItem;
    do {
      newItem = mockProductDatabase[Math.floor(Math.random() * mockProductDatabase.length)];
    } while (newItem.name === generatedItems.value[itemIndex].name);
    
    generatedItems.value[itemIndex] = { ...newItem, id: itemId };
  }
};
</script>

<style scoped>
.flex-center-gap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}
.template-button {
  @apply p-4 border border-stone-300 rounded-lg hover:bg-orange-50 transition-colors text-left;
}
textarea {
  resize: vertical;
}
</style>