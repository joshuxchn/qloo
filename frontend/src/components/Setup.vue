<template>
  <div class="min-h-screen">
    <header class="border-b bg-white/80 backdrop-blur-sm h-20">
      <div class="container mx-auto px-4 h-full flex items-center justify-between">
        <button @click="goBack" class="flex items-center space-x-3">
          <span class="text-white font-bold text-lg">🍊</span>
          <h1 class="text-2xl font-bold text-stone-800">tangerine</h1>
        </button>
        <button @click="goBack" class="px-4 py-2 border border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent rounded transition-colors">
          Return Home
        </button>
      </div>
    </header>

    <div class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto">
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-stone-800 mb-4">Create Your Taste Profile</h2>
          <p class="text-lg text-stone-600">Help us personalize your grocery recommendations.</p>
        </div>

        <div class="grid lg:grid-cols-2 gap-8">
          <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
            <div class="p-6 border-b">
              <h3 class="text-lg font-medium text-stone-800">Basic Information *</h3>
              <p class="text-stone-600 mt-1">Fields marked with an asterisk are required</p>
            </div>
            <div class="p-6 space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-stone-700 mb-1">First Name *</label>
                  <input v-model="userProfile.firstName" placeholder="John" class="w-full px-3 py-2 border border-stone-300 rounded-md"/>
                </div>
                <div>
                  <label class="block text-sm font-medium text-stone-700 mb-1">Last Name *</label>
                  <input v-model="userProfile.lastName" placeholder="Doe" class="w-full px-3 py-2 border border-stone-300 rounded-md"/>
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Location (ZIP Code) *</label>
                <input v-model="userProfile.zipCode" placeholder="12345" class="w-full px-3 py-2 border border-stone-300 rounded-md"/>
              </div>
              <div class="grid grid-cols-2 gap-4">
                 <div>
                    <label class="block text-sm font-medium text-stone-700 mb-1">Age</label>
                    <input type="number" v-model.number="userProfile.age" placeholder="30" class="w-full px-3 py-2 border border-stone-300 rounded-md"/>
                 </div>
                 <div>
                    <label class="block text-sm font-medium text-stone-700 mb-1">Gender</label>
                    <select v-model="userProfile.gender" class="w-full px-3 py-2 border border-stone-300 rounded-md">
                       <option disabled value="">Select...</option>
                       <option>Male</option>
                       <option>Female</option>
                       <option>Non-binary</option>
                       <option>Prefer not to say</option>
                    </select>
                 </div>
              </div>
            </div>
          </div>

          <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
            <div class="p-6 border-b">
              <h3 class="text-lg font-medium text-stone-800">Budget & Shopping *</h3>
            </div>
            <div class="p-6 space-y-6">
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-2">Weekly Grocery Budget *</label>
                <div class="mt-2">
                  <input type="range" v-model="userProfile.budget" min="50" max="500" step="5" class=" text-orange-600 w-full h-2 bg-stone-200 rounded-lg appearance-none cursor-pointer"/>
                  <div class="flex justify-between text-sm text-stone-500 mt-1">
                    <span>$50</span>
                    <span class="font-medium text-orange-600">${{ userProfile.budget }}</span>
                    <span>$500+</span>
                  </div>
                </div>
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Shopping Frequency *</label>
                <select v-model="userProfile.shoppingFrequency" class="w-full px-3 py-2 border border-stone-300 rounded-md">
                  <option disabled value="">How often do you shop?</option>
                  <option>Daily</option>
                  <option>Weekly</option>
                  <option>Bi-weekly</option>
                  <option>Monthly</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Shopping Priority *</label>
                <select v-model="userProfile.shoppingPriority" class="w-full px-3 py-2 border border-stone-300 rounded-md">
                  <option disabled value="">What matters most?</option>
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
                      <button v-for="diet in dietaryRestrictions" :key="diet" @click="toggleSelection(userProfile.selectedDiets, diet)" :class="getButtonClass(userProfile.selectedDiets.includes(diet), 'orange')">
                         {{ diet }}
                      </button>
                   </div>
                </div>
                <div>
                   <label class="block text-sm font-medium text-stone-700 mb-3">Allergies</label>
                   <div class="flex flex-wrap gap-2">
                      <button v-for="allergy in commonAllergies" :key="allergy" @click="toggleSelection(userProfile.selectedAllergies, allergy)" :class="getButtonClass(userProfile.selectedAllergies.includes(allergy), 'orange')">
                         {{ allergy }}
                      </button>
                   </div>
                </div>
                <div>
                   <label class="block text-sm font-medium text-stone-700 mb-1">Health Goals</label>
                   <textarea v-model="userProfile.healthGoals" placeholder="e.g., lose weight, build muscle..." class="w-full px-3 py-2 border border-stone-300 rounded-md min-h-[80px] resize-none"></textarea>
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
                      <button v-for="cuisine in cuisinePreferences" :key="cuisine" @click="toggleSelection(userProfile.selectedCuisines, cuisine)" :class="getButtonClass(userProfile.selectedCuisines.includes(cuisine), 'orange')">
                         {{ cuisine }}
                      </button>
                   </div>
                </div>
                <div>
                   <label class="block text-sm font-medium text-stone-700 mb-1">Cultural Background</label>
                   <input v-model="userProfile.culturalBackground" placeholder="e.g., Italian-American, Mexican..." class="w-full px-3 py-2 border border-stone-300 rounded-md" />
                </div>
                <div>
                   <label class="block text-sm font-medium text-stone-700 mb-1">Favorite Foods & Ingredients</label>
                   <textarea v-model="userProfile.favoriteFoods" placeholder="e.g., I love spicy food, fresh pasta..." class="w-full px-3 py-2 border border-stone-300 rounded-md min-h-[80px] resize-none"></textarea>
                </div>
             </div>
          </div>
        </div>

        <div class="mt-8 flex flex-col items-center gap-4">
          <button @click="createAccountWithGoogle" :disabled="isFormInvalid" :class="['px-8 py-3 text-white rounded-lg transition-colors flex items-center justify-center gap-2', isFormInvalid ? 'bg-stone-400 cursor-not-allowed' : 'bg-orange-500 hover:bg-orange-600']">
            <img src="https://developers.google.com/identity/images/g-logo.png" class="w-5 h-5" alt="Google logo" />
            Create Account with Google
          </button>
          <p v-if="isFormInvalid" class="text-sm text-red-600">
            Please fill out all required (*) fields before creating an account.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { User, DollarSign, Heart, Globe } from 'lucide-vue-next';

const router = useRouter();
const base_url = import.meta.env.VITE_API_BASE_URL;

const userProfile = ref({
  firstName: '',
  lastName: '',
  zipCode: '',
  age: null,
  gender: '',
  budget: 200,
  shoppingFrequency: '',
  shoppingPriority: '',
  selectedDiets: [],
  selectedAllergies: [],
  healthGoals: '',
  selectedCuisines: [],
  culturalBackground: '',
  favoriteFoods: '',
});

const dietaryRestrictions = ref(['Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free', 'Keto', 'Paleo', 'Pescatarian', 'Halal', 'Kosher']);
const commonAllergies = ref(['Peanuts', 'Tree Nuts', 'Dairy', 'Eggs', 'Soy', 'Wheat', 'Fish', 'Shellfish']);
const cuisinePreferences = ref(['American', 'Italian', 'Mexican', 'Chinese', 'Indian', 'Japanese', 'Mediterranean', 'Thai', 'French', 'Korean']);

const isFormInvalid = computed(() => {
  return !userProfile.value.firstName || 
         !userProfile.value.lastName || 
         !userProfile.value.zipCode ||
         !userProfile.value.shoppingFrequency ||
         !userProfile.value.shoppingPriority;
});

const goBack = () => router.push('/');

const toggleSelection = (selectionArray, item) => {
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

const createAccountWithGoogle = () => {
  if (isFormInvalid.value) return;

  const profilePayload = {
    first_name: userProfile.value.firstName,
    last_name: userProfile.value.lastName,
    preferred_location: userProfile.value.zipCode,
    age: userProfile.value.age,
    gender: userProfile.value.gender,
    budget: parseInt(userProfile.value.budget, 10),
    shopping_frequency: userProfile.value.shoppingFrequency,
    shopping_priority: userProfile.value.shoppingPriority,
    dietary_restrictions: userProfile.value.selectedDiets,
    allergies: userProfile.value.selectedAllergies,
    health_goals: userProfile.value.healthGoals,
    favorite_cuisines: userProfile.value.selectedCuisines,
    cultural_background: userProfile.value.culturalBackground,
    favorite_foods: userProfile.value.favoriteFoods,
  };

  localStorage.setItem('pendingUserProfile', JSON.stringify(profilePayload));
  window.location.href = `${base_url}/auth/google/signup`;
};
</script>