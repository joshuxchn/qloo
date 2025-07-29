<template>
  <!-- User Settings Page View -->
  <div class="min-h-screen">
    <!-- Header -->
    <header class="border-b bg-white/80 backdrop-blur-sm h-20">
      <div class="container mx-auto px-4 h-full flex items-center justify-between">
        <button @click="$emit('set-current-view', 'dashboard')" class="flex items-center space-x-3">
          <span class="text-white font-bold text-lg">🍊</span>
          <h1 class="text-2xl font-bold text-stone-800">tangerine</h1>
        </button>
        <div class="flex items-center space-x-3">
          <button
            @click=redirectToDashboard
            class="px-3 py-1 text-sm text-stone-600 hover:text-orange-600 hover:bg-orange-50 rounded transition-colors"
          >
            Dashboard
          </button>
          <button 
          @click=redirectToHome
          class="px-3 py-1 text-sm border border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent rounded transition-colors">
            Sign Out
          </button>
        </div>
      </div>
    </header>

    <div class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto">
        <div class="mb-8">
          <h2 class="text-3xl font-bold text-stone-800 mb-2">Profile Settings</h2>
          <p class="text-lg text-stone-600">Manage your account and preferences</p>
        </div>

        <!-- Settings Tabs -->
        <div class="space-y-6">
          <div class="grid w-full grid-cols-3 bg-stone-100 border-0 rounded-lg p-1">
            <button
              @click="settingsTab = 'preferences'"
              :class="[
                'text-sm px-4 py-2 rounded transition-colors flex items-center justify-center gap-2',
                settingsTab === 'preferences'
                  ? 'bg-white text-stone-800 shadow-sm'
                  : 'text-stone-600 hover:text-stone-800'
              ]"
            >
              <!-- Placeholder for icon -->
              <span class="text-red-500">❤️</span>
              Preferences
            </button>
            <button
              @click="settingsTab = 'account'"
              :class="[
                'text-sm px-4 py-2 rounded transition-colors flex items-center justify-center gap-2',
                settingsTab === 'account'
                  ? 'bg-white text-stone-800 shadow-sm'
                  : 'text-stone-600 hover:text-stone-800'
              ]"
            >
              <!-- Placeholder for icon -->
              <span class="text-blue-500">👤</span>
              Account
            </button>
            <button
              @click="settingsTab = 'settings'"
              :class="[
                'text-sm px-4 py-2 rounded transition-colors flex items-center justify-center gap-2',
                settingsTab === 'settings'
                  ? 'bg-white text-stone-800 shadow-sm'
                  : 'text-stone-600 hover:text-stone-800'
              ]"
            >
              <!-- Placeholder for icon -->
              <span class="text-gray-500">⚙️</span>
              Settings
            </button>
          </div>

          <!-- Content for each settings tab -->
          <div v-if="settingsTab === 'preferences'" class="bg-white border-0 shadow-sm rounded-lg p-6">
            <h3 class="text-lg font-medium text-stone-800 mb-4">Your Preferences</h3>
            <p class="text-stone-600">Customize your app experience here.</p>
            <!-- Add preference settings forms/inputs here -->
          </div>
          <div v-else-if="settingsTab === 'account'" class="bg-white border-0 shadow-sm rounded-lg p-6">
            <h3 class="text-lg font-medium text-stone-800 mb-4">Account Information</h3>
            <p class="text-stone-600">Manage your login details and personal info.</p>
            <!-- Add account settings forms/inputs here -->
          </div>
          <div v-else-if="settingsTab === 'budget'" class="bg-white border-0 shadow-sm rounded-lg p-6">
            <h3 class="text-lg font-medium text-stone-800 mb-4">Budget Settings</h3>
            <p class="text-stone-600">Set and adjust your weekly spending budget.</p>
            <div class="mt-4">
              <label for="budget-input" class="block text-sm font-medium text-stone-700 mb-1">Weekly Budget</label>
              <input
                id="budget-input"
                type="number"
                v-model.number="userProfile.budget"
                class="w-full px-3 py-2 border-0 bg-stone-50 text-stone-800 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                placeholder="e.g., 150.00"
              />
              <p class="mt-2 text-xs text-stone-500">Your current weekly budget is ${{ userProfile.budget.toFixed(2) }}.</p>
            </div>
          </div>
          <div v-else-if="settingsTab === 'settings'" class="bg-white border-0 shadow-sm rounded-lg p-6">
            <h3 class="text-lg font-medium text-stone-800 mb-4">General Settings</h3>
            <p class="text-stone-600">Configure general application settings.</p>
            <!-- Add general settings forms/inputs here -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile', // Name of this component
  props: {
    userProfile: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      settingsTab: 'preferences' // Controls which tab is active on user settings
    };
    
  },
  methods: {
    redirectToDashboard() {
      window.location.href = '/dashboard';
    },
    redirectToHome() {
      window.location.href = '/';
    }
  }
  
};

</script>

<style scoped>
/* Scoped styles for Profile component if any */
</style>
