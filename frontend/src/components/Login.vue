<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50 flex flex-col">
    <header class="border-b bg-white/80 backdrop-blur-sm h-20">
      <div class="container mx-auto px-4 h-full flex items-center justify-between">
        <button @click="goBack" class="flex items-center space-x-3">
          <span class="text-white font-bold text-lg">🍊</span>
          <h1 class="text-2xl font-bold text-stone-800">tangerine</h1>
        </button>
        <div class="flex items-center space-x-4">
          <span class="text-sm text-stone-600">Don't have an account?</span>
          <router-link to="/setup" class="px-4 py-2 border border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent rounded transition-colors">
            Get Started
          </router-link>
        </div>
      </div>
    </header>

    <div class="container mx-auto px-4 py-16 flex-grow flex items-center justify-center">
      <div class="max-w-md w-full">
        <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
          <div class="p-6 text-center border-b">
            <h2 class="text-2xl font-bold text-stone-800 mb-2">Welcome Back</h2>
            <p class="text-stone-600">Sign in to your account</p>
          </div>
          <div class="p-6">
            <div v-if="errorMessage" class="mb-4 p-3 bg-red-100 border border-red-300 text-red-800 rounded-lg text-sm text-left">
              {{ errorMessage }}
            </div>
            
            <button @click="loginWithGoogle" class="w-full mb-4 flex items-center justify-center py-3 px-4 rounded-lg font-semibold shadow-md transition-all duration-200 bg-white text-stone-700 hover:bg-stone-50 border border-stone-300">
              <img src="https://developers.google.com/identity/images/g-logo.png" class="w-5 h-5 mr-3" alt="Google logo" />
              Sign In with Google
            </button>

            <div class="mt-6 text-center">
              <button type="button" @click="goBack" class="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors duration-200 inline-flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                </svg>
                <span>Return Home</span>
              </button>

              <p class="text-xs text-stone-600 mt-4 text-center">
                By signing in, you agree to our
                <router-link to="/terms" class="underline text-orange-600 hover:text-orange-700">Terms of Service</router-link> and
                <router-link to="/privacy" class="underline text-orange-600 hover:text-orange-700">Privacy Policy</router-link>.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const base_url = import.meta.env.VITE_API_BASE_URL;
const errorMessage = ref('');

// Watch for changes on the route's query parameters.
watch(
  () => route.query,
  (newQuery) => {
    if (newQuery.error === 'not_found') {
      errorMessage.value = 'No account found with this Google account. Please click "Get Started" to create a new profile.';
    } else if (newQuery.error === 'email_exists') {
      errorMessage.value = 'An account with this email already exists. Please sign in instead.';
    }

    if (newQuery.error) {
      // Clean the error from the URL after displaying the message
      setTimeout(() => {
        router.replace({ query: {} });
      }, 0);
    }
  },
  { immediate: true } // Run this check immediately when the page loads
);

const goBack = () => {
  router.push('/');
};

const loginWithGoogle = () => {
  errorMessage.value = ''; // Clear previous errors
  localStorage.clear();
  sessionStorage.clear();
  window.location.href = `${base_url}/auth/google/login`;
};
</script>

<style scoped>
/* No style changes needed */
</style>