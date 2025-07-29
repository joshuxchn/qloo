<template>
  <div class="min-h-screen">
    <header class="border-b bg-white/80 backdrop-blur-sm h-20 sticky top-0 z-50">
      <div class="container mx-auto px-4 h-full flex items-center justify-between">
        <button @click="redirectToDashboard" class="flex items-center space-x-3">
          <span class="text-white font-bold text-lg">🍊</span>
          <h1 class="text-2xl font-bold text-stone-800">tangerine</h1>
        </button>
        <div class="flex items-center space-x-3">
          <button @click="redirectToDashboard" class="px-3 py-1 text-sm text-stone-600 hover:text-orange-600 hover:bg-orange-50 rounded transition-colors">
            Dashboard
          </button>
          <button @click="signOut" class="px-3 py-1 text-sm border border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent rounded transition-colors">
            Sign Out
          </button>
        </div>
      </div>
    </header>

    <div class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto" v-if="editableProfile">
        <div class="mb-8">
          <h2 class="text-3xl font-bold text-stone-800 mb-2">Profile Settings</h2>
          <p class="text-lg text-stone-600">Manage your account and preferences, {{ editableProfile.firstName || 'user' }}.</p>
        </div>

        <div class="space-y-8">
          <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
            <div class="p-6 border-b">
              <h3 class="text-lg font-medium text-stone-800">Basic Information</h3>
            </div>
            <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">First Name</label>
                <input v-model="editableProfile.firstName" class="w-full px-3 py-2 border border-stone-300 rounded-md"/>
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Last Name</label>
                <input v-model="editableProfile.lastName" class="w-full px-3 py-2 border border-stone-300 rounded-md"/>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-stone-700 mb-1">Email</label>
                <input :value="editableProfile.email" disabled class="w-full px-3 py-2 border border-stone-300 rounded-md bg-stone-100 text-stone-500 cursor-not-allowed"/>
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Location (ZIP Code)</label>
                <input v-model="editableProfile.preferredLocation" class="w-full px-3 py-2 border border-stone-300 rounded-md"/>
              </div>

              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Age</label>
                <input type="number" v-model.number="editableProfile.age" placeholder="e.g., 30" class="w-full px-3 py-2 border border-stone-300 rounded-md"/>
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Gender</label>
                <select v-model="editableProfile.gender" class="w-full px-3 py-2 border border-stone-300 rounded-md">
                   <option disabled value="">Select...</option>
                   <option>Male</option>
                   <option>Female</option>
                   <option>Non-binary</option>
                   <option>Prefer not to say</option>
                </select>
              </div>
              </div>
          </div>

          <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
            <div class="p-6 border-b">
              <h3 class="text-lg font-medium text-stone-800">Budget & Shopping</h3>
            </div>
            <div class="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-stone-700 mb-2">Weekly Grocery Budget: <span class="font-semibold text-orange-600">${{ editableProfile.budget }}</span></label>
                <input type="range" v-model.number="editableProfile.budget" min="50" max="500" step="5" class="w-full h-2 bg-stone-200 rounded-lg appearance-none cursor-pointer"/>
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Shopping Frequency</label>
                <select v-model="editableProfile.shoppingFrequency" class="w-full px-3 py-2 border border-stone-300 rounded-md">
                  <option>Daily</option>
                  <option>Weekly</option>
                  <option>Bi-weekly</option>
                  <option>Monthly</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Shopping Priority</label>
                <select v-model="editableProfile.shoppingPriority" class="w-full px-3 py-2 border border-stone-300 rounded-md">
                  <option>Lowest Cost</option>
                  <option>Highest Quality</option>
                  <option>Healthiest Options</option>
                  <option>Convenience</option>
                  <option>Balanced Approach</option>
                </select>
              </div>
            </div>
          </div>

          <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
            <div class="p-6 border-b">
              <h3 class="text-lg font-medium text-stone-800">Dietary & Health</h3>
            </div>
            <div class="p-6 space-y-4">
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-3">Dietary Restrictions</label>
                <div class="flex flex-wrap gap-2">
                  <button v-for="diet in dietaryRestrictions" :key="diet" @click="toggleSelection(editableProfile.dietaryRestrictions, diet)" :class="getButtonClass(editableProfile.dietaryRestrictions.includes(diet), 'orange')">
                    {{ diet }}
                  </button>
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-3">Allergies</label>
                <div class="flex flex-wrap gap-2">
                  <button v-for="allergy in commonAllergies" :key="allergy" @click="toggleSelection(editableProfile.allergies, allergy)" :class="getButtonClass(editableProfile.allergies.includes(allergy), 'orange')">
                    {{ allergy }}
                  </button>
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Health Goals (Optional)</label>
                <textarea v-model="editableProfile.healthGoals" placeholder="e.g., lose weight, build muscle..." class="w-full px-3 py-2 border border-stone-300 rounded-md min-h-[80px] resize-none"></textarea>
              </div>
            </div>
          </div>
          
          <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
            <div class="p-6 border-b">
              <h3 class="text-lg font-medium text-stone-800">Taste Preferences</h3>
            </div>
            <div class="p-6 space-y-4">
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-3">Favorite Cuisines</label>
                <div class="flex flex-wrap gap-2">
                  <button v-for="cuisine in cuisinePreferences" :key="cuisine" @click="toggleSelection(editableProfile.favoriteCuisines, cuisine)" :class="getButtonClass(editableProfile.favoriteCuisines.includes(cuisine), 'orange')">
                    {{ cuisine }}
                  </button>
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Cultural Background (Optional)</label>
                <input v-model="editableProfile.culturalBackground" placeholder="e.g., Italian-American, Mexican..." class="w-full px-3 py-2 border border-stone-300 rounded-md"/>
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Favorite Foods & Ingredients (Optional)</label>
                <textarea v-model="editableProfile.favoriteFoods" placeholder="e.g., I love spicy food, fresh pasta..." class="w-full px-3 py-2 border border-stone-300 rounded-md min-h-[80px] resize-none"></textarea>
              </div>
            </div>
          </div>
          
          <div class="flex justify-end items-center gap-4">
            <p v-if="statusMessage" :class="statusMessageColor" class="text-sm transition-opacity duration-300">{{ statusMessage }}</p>
            <button @click="saveChanges" class="px-6 py-2 bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors">
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { userStore } from '@/stores/userStore';

const router = useRouter();
const base_url = import.meta.env.VITE_API_BASE_URL;

const editableProfile = ref(null);
const statusMessage = ref('');
const isError = ref(false);

const dietaryRestrictions = ref(['Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free', 'Keto', 'Paleo', 'Pescatarian', 'Halal', 'Kosher']);
const commonAllergies = ref(['Peanuts', 'Tree Nuts', 'Dairy', 'Eggs', 'Soy', 'Wheat', 'Fish', 'Shellfish']);
const cuisinePreferences = ref(['American', 'Italian', 'Mexican', 'Chinese', 'Indian', 'Japanese', 'Mediterranean', 'Thai', 'French', 'Korean']);

onMounted(() => {
  if (userStore.user) {
    editableProfile.value = JSON.parse(JSON.stringify(userStore.user));
  } else {
    router.push('/login');
  }
});

const saveChanges = async () => {
  if (!editableProfile.value) return;
  try {
    const response = await fetch(`${base_url}/api/user/update-profile`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${userStore.token}`
      },
      body: JSON.stringify(editableProfile.value)
    });
    if (!response.ok) throw new Error('Failed to save profile.');
    
    await userStore.fetchUser();
    isError.value = false;
    statusMessage.value = 'Profile saved successfully!';
  } catch (error) {
    console.error('Error saving profile:', error);
    isError.value = true;
    statusMessage.value = 'Failed to save. Please try again.';
  } finally {
    setTimeout(() => { statusMessage.value = ''; }, 3000);
  }
};

const toggleSelection = (selectionArray, item) => {
  if (!selectionArray) {
    selectionArray = [];
  }
  const index = selectionArray.indexOf(item);
  if (index > -1) {
    selectionArray.splice(index, 1);
  } else {
    selectionArray.push(item);
  }
};

const getButtonClass = (isSelected, color) => {
  const base = 'px-3 py-1 text-sm rounded-full border transition-colors cursor-pointer';
  if (isSelected) {
    return `${base} bg-${color}-500 text-white border-${color}-500`;
  }
  return `${base} border-stone-300 text-stone-600 hover:bg-${color}-50`;
};

const statusMessageColor = computed(() => {
  return isError.value ? 'text-red-600' : 'text-emerald-600';
});

const redirectToDashboard = () => router.push('/dashboard');
const signOut = () => {
  userStore.logout();
  router.push('/login');
};
</script>

<style scoped>
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 1rem;
  height: 1rem;
  background: #f97316; /* orange-500 */
  border-radius: 9999px;
  cursor: pointer;
  margin-top: -4px;
}
input[type="range"]::-moz-range-thumb {
  width: 1rem;
  height: 1rem;
  background: #f97316; /* orange-500 */
  border-radius: 9999px;
  cursor: pointer;
}
</style>