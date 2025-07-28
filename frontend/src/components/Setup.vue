<template>
  <!-- Profile Creation Page - No longer conditionally rendered -->
  <div class="min-h-screen">
    <!-- Header -->
    <header class="border-b bg-white/80 backdrop-blur-sm h-20">
      <div class="container mx-auto px-4 h-full flex items-center justify-between">
        <!-- Clicking the logo takes the user back to the landing page -->
        <button @click="goBack" class="flex items-center space-x-3">
          <div class="w-[60px] h-[60px] bg-orange-500 rounded-full flex items-center justify-center">
            <span class="text-white font-bold text-lg">T</span>
          </div>
          <h1 class="text-2xl font-bold text-stone-800">tangerine profile</h1>
        </button>
        <!-- Button to skip profile creation and go to the dashboard -->
        <button
          @click="goBack"
          class="px-4 py-2 border border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent rounded transition-colors"
        >
          Return Home
        </button>
      </div>
    </header>

    <div class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto">
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-stone-800 mb-4">Create Your Taste Profile</h2>
          <p class="text-lg text-stone-600">
            Help us understand your preferences to provide personalized grocery recommendations
          </p>
        </div>

        <div class="grid lg:grid-cols-2 gap-8">
          <!-- Basic Information -->
          <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
            <div class="p-6 border-b">
              <h3 class="text-lg font-medium text-stone-800 flex items-center gap-2">
                <User class="h-5 w-5 text-orange-600" />
                Basic Information
              </h3>
              <p class="text-stone-600 mt-1">Tell us about yourself</p>
            </div>
            <div class="p-6 space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-stone-700 mb-1">First Name</label>
                  <input
                    v-model="userProfile.firstName"
                    placeholder="John"
                    class="w-full px-3 py-2 border border-stone-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-stone-700 mb-1">Last Name</label>
                  <input
                    v-model="userProfile.lastName"
                    placeholder="Doe"
                    class="w-full px-3 py-2 border border-stone-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                  />
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Email</label>
                <input
                  v-model="userProfile.email"
                  type="email"
                  placeholder="john@example.com"
                  class="w-full px-3 py-2 border border-stone-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Location (ZIP Code)</label>
                <input
                  v-model="userProfile.zipCode"
                  placeholder="12345"
                  class="w-full px-3 py-2 border border-stone-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>
            </div>
          </div>

          <!-- Budget Preferences -->
          <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
            <div class="p-6 border-b">
              <h3 class="text-lg font-medium text-stone-800 flex items-center gap-2">
                <DollarSign class="h-5 w-5 text-amber-600" />
                Budget & Shopping Preferences
              </h3>
              <p class="text-stone-600 mt-1">Set your budget and shopping frequency</p>
            </div>
            <div class="p-6 space-y-6">
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-2">Weekly Grocery Budget</label>
                <div class="mt-2">
                  <input
                    type="range"
                    v-model="userProfile.budget"
                    min="50"
                    max="500"
                    step="25"
                    class="w-full h-2 bg-stone-200 rounded-lg appearance-none cursor-pointer slider"
                  />
                  <div class="flex justify-between text-sm text-stone-500 mt-1">
                    <span>$50</span>
                    <span class="font-medium text-orange-600">${{ userProfile.budget }}</span>
                    <span>$500+</span>
                  </div>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Shopping Frequency</label>
                <select
                  v-model="userProfile.shoppingFrequency"
                  class="w-full px-3 py-2 border border-stone-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                >
                  <option value="">How often do you shop?</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="biweekly">Bi-weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Shopping Priority</label>
                <select
                  v-model="userProfile.shoppingPriority"
                  class="w-full px-3 py-2 border border-stone-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                >
                  <option value="">What matters most?</option>
                  <option value="cost">Lowest Cost</option>
                  <option value="quality">Highest Quality</option>
                  <option value="health">Healthiest Options</option>
                  <option value="convenience">Convenience</option>
                  <option value="balanced">Balanced Approach</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Dietary Restrictions -->
          <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
            <div class="p-6 border-b">
              <h3 class="text-lg font-medium text-stone-800 flex items-center gap-2">
                <Heart class="h-5 w-5 text-red-600" />
                Dietary Restrictions & Health
              </h3>
              <p class="text-stone-600 mt-1">Select any dietary restrictions or health considerations</p>
            </div>
            <div class="p-6 space-y-4">
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-3">Dietary Restrictions</label>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="diet in dietaryRestrictions"
                    :key="diet"
                    @click="toggleDiet(diet)"
                    :class="[
                      'px-3 py-1 text-sm rounded-full border transition-colors cursor-pointer',
                      userProfile.selectedDiets.includes(diet)
                        ? 'bg-orange-500 text-white border-orange-500'
                        : 'border-stone-300 text-stone-600 hover:bg-orange-50'
                    ]"
                  >
                    {{ diet }}
                  </button>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-stone-700 mb-3">Allergies</label>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="allergy in commonAllergies"
                    :key="allergy"
                    @click="toggleAllergy(allergy)"
                    :class="[
                      'px-3 py-1 text-sm rounded-full border transition-colors cursor-pointer',
                      userProfile.selectedAllergies.includes(allergy)
                        ? 'bg-red-500 text-white border-red-500'
                        : 'border-stone-300 text-stone-600 hover:bg-red-50'
                    ]"
                  >
                    {{ allergy }}
                  </button>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Health Goals (Optional)</label>
                <textarea
                  v-model="userProfile.healthGoals"
                  placeholder="e.g., lose weight, build muscle, improve heart health..."
                  class="w-full px-3 py-2 border border-stone-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 min-h-[80px] resize-none"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Cultural Preferences -->
          <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
            <div class="p-6 border-b">
              <h3 class="text-lg font-medium text-stone-800 flex items-center gap-2">
                <Globe class="h-5 w-5 text-amber-600" />
                Cultural & Taste Preferences
              </h3>
              <p class="text-stone-600 mt-1">Help us understand your cultural background and taste preferences</p>
            </div>
            <div class="p-6 space-y-4">
              <div>
                <label class="block text-sm font-medium text-stone-700 mb-3">Favorite Cuisines</label>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="cuisine in cuisinePreferences"
                    :key="cuisine"
                    @click="toggleCuisine(cuisine)"
                    :class="[
                      'px-3 py-1 text-sm rounded-full border transition-colors cursor-pointer',
                      userProfile.selectedCuisines.includes(cuisine)
                        ? 'bg-amber-500 text-white border-amber-500'
                        : 'border-stone-300 text-stone-600 hover:bg-amber-50'
                    ]"
                  >
                    {{ cuisine }}
                  </button>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Cultural Background (Optional)</label>
                <input
                  v-model="userProfile.culturalBackground"
                  placeholder="e.g., Italian-American, Mexican, Indian..."
                  class="w-full px-3 py-2 border border-stone-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-stone-700 mb-1">Favorite Foods & Ingredients</label>
                <textarea
                  v-model="userProfile.favoriteFoods"
                  placeholder="Tell us about foods you love, ingredients you use often, or dishes you enjoy cooking..."
                  class="w-full px-3 py-2 border border-stone-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 min-h-[80px] resize-none"
                ></textarea>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <button
            @click="saveProfile"
            class="px-8 py-3 bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            Create Profile & Continue
            <ArrowRight class="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'; // Import ref for reactive data
import { useRouter } from 'vue-router'; // Import useRouter for navigation
import {
  User,
  DollarSign,
  Heart,
  Globe,
  ArrowRight,
} from 'lucide-vue-next'; // Import Lucide icons

const router = useRouter(); // Initialize router instance

// Define reactive data for the user profile form
const userProfile = ref({
  firstName: '',
  lastName: '',
  email: '',
  ageRange: '',
  householdSize: '',
  zipCode: '',
  budget: 200, // Default budget
  shoppingFrequency: '',
  shoppingPriority: '',
  selectedDiets: [],
  selectedAllergies: [],
  healthGoals: '',
  selectedCuisines: [],
  culturalBackground: '',
  cookingLevel: '',
  favoriteFoods: '',
});

// Predefined lists for selections
const dietaryRestrictions = ref([
  'Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free', 'Keto', 'Paleo', 'Pescatarian', 'Halal', 'Kosher'
]);
const commonAllergies = ref([
  'Peanuts', 'Tree Nuts', 'Dairy', 'Eggs', 'Soy', 'Wheat', 'Fish', 'Shellfish'
]);
const cuisinePreferences = ref([
  'American', 'Italian', 'Mexican', 'Chinese', 'Indian', 'Japanese', 'Mediterranean', 'Thai', 'French', 'Korean'
]);

// --- Methods for interaction and navigation ---

// Function to navigate back to the landing page (root)
const goBack = () => {
  router.push('/');
};

// Function to navigate to the dashboard
const goToDashboard = () => {
  router.push('/dashboard'); // Assuming you have a /dashboard route configured
};

// Function to toggle selected dietary restrictions
const toggleDiet = (diet) => {
  const index = userProfile.value.selectedDiets.indexOf(diet);
  if (index > -1) {
    userProfile.value.selectedDiets.splice(index, 1); // Remove if already selected
  } else {
    userProfile.value.selectedDiets.push(diet); // Add if not selected
  }
};

// Function to toggle selected allergies
const toggleAllergy = (allergy) => {
  const index = userProfile.value.selectedAllergies.indexOf(allergy);
  if (index > -1) {
    userProfile.value.selectedAllergies.splice(index, 1); // Remove if already selected
  } else {
    userProfile.value.selectedAllergies.push(allergy); // Add if not selected
  }
};

// Function to toggle selected cuisines
const toggleCuisine = (cuisine) => {
  const index = userProfile.value.selectedCuisines.indexOf(cuisine);
  if (index > -1) {
    userProfile.value.selectedCuisines.splice(index, 1); // Remove if already selected
  } else {
    userProfile.value.selectedCuisines.push(cuisine); // Add if not selected
  }
};

// Function to save the profile (placeholder for actual logic)
const saveProfile = () => {
  // In a real application, you would send userProfile.value data to a backend API
  console.log('User Profile Saved:', userProfile.value);
  // After saving, navigate to the dashboard or a confirmation page
  router.push('/dashboard');
};
</script>

<style scoped>
/* Add any specific scoped styles here if needed, but Tailwind handles most of the styling */
/* Custom slider track color for better visual consistency */
input[type="range"]::-webkit-slider-runnable-track {
  background: #fbd38d; /* A lighter orange/amber tone */
  border-radius: 9999px; /* Fully rounded */
}

input[type="range"]::-moz-range-track {
  background: #fbd38d; /* A lighter orange/amber tone */
  border-radius: 9999px; /* Fully rounded */
}

/* Custom slider thumb color */
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  border: 2px solid #ea580c; /* Orange-600 border */
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background: #f97316; /* Orange-500 fill */
  cursor: grab;
  margin-top: -7px; /* Adjust to center vertically on the track */
  box-shadow: 0 0 0 3px rgba(251, 197, 100, 0.4); /* Light orange glow */
}

input[type="range"]::-moz-range-thumb {
  border: 2px solid #ea580c; /* Orange-600 border */
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background: #f97316; /* Orange-500 fill */
  cursor: grab;
  box-shadow: 0 0 0 3px rgba(251, 197, 100, 0.4); /* Light orange glow */
}
</style>