<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50 flex flex-col">

    <header class="border-b bg-white/80 backdrop-blur-sm h-20">
      <div class="container mx-auto px-4 h-full flex items-center justify-between">
        <button @click="goBack" class="flex items-center space-x-3">
          <div class="w-[60px] h-[60px] bg-orange-500 rounded-full flex items-center justify-center">
            <span class="text-white font-bold text-lg">T</span>
          </div>
          <h1 class="text-2xl font-bold text-stone-800">tangerine</h1>
        </button>
        <div class="flex items-center space-x-4">
          <span class="text-sm text-stone-600">Don't have an account?</span>
          <router-link to="/setup"
            @click="goSetup"
            class="px-4 py-2 border border-stone-300 text-stone-700 hover:bg-stone-50 bg-transparent rounded transition-colors"
          >
            Get Started
          </router-link>
        </div>
      </div>
    </header>

    <div class="container mx-auto px-4 py-16 flex-grow flex items-center justify-center">
      <div class="max-w-md w-full">
        <div class="bg-white border border-stone-200 shadow-sm rounded-lg">
          <div class="p-6 text-center border-b">
            <h2 class="text-2xl font-bold text-stone-800 mb-2">welcome back to tangerine</h2>
            <p class="text-stone-600">Sign in to your account </p>
          </div>
          <div class="p-6">
            <button @click="loginWithGoogle"
              class="w-full mb-4 flex items-center justify-center py-3 px-4 rounded-lg font-semibold shadow-md transition-all duration-200 bg-white text-stone-700 hover:bg-stone-50 border border-stone-300">
              <img src="https://developers.google.com/identity/images/g-logo.png" class="w-5 h-5 mr-3"
                alt="Google logo" />
              Login / Create Account
            </button>

            <div class="mt-6 text-center">
              <button type="button" @click="goBack"
                class="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors duration-200 inline-flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                </svg>
                <span>Return Home</span>
              </button>

              <p class="text-xs text-stone-600 mt-4 text-center">
                By signing in, you agree to our
                <router-link to="/terms" class="underline text-orange-600 hover:text-orange-700">Terms of Service</router-link>,
                <router-link to="/privacy" class="underline text-orange-600 hover:text-orange-700">Privacy Policy</router-link>, and
                <router-link to="/cookies" class="underline text-orange-600 hover:text-orange-700">Cookie Policy</router-link>.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer class="bg-stone-800 text-stone-200 py-8 md:py-12 mt-auto">
      <div class="container mx-auto px-4 text-center">
        <h3 class="font-bold text-xl md:text-2xl mb-3 md:mb-4">tangerine</h3>
        <p class="text-stone-400 text-sm md:text-base mb-2 md:mb-3">
          AI-powered grocery optimization platform that saves you money and matches your taste.
        </p>
        <div class="flex flex-col md:flex-row items-center justify-center gap-2">
          <router-link to="/terms" class="text-stone-400 hover:underline text-xs md:text-sm">
            Terms of Service
          </router-link>
          <span class="hidden md:block mx-2 text-stone-400"> | </span>
          <router-link to="/privacy" class="text-stone-400 hover:underline text-xs md:text-sm">
            Privacy Policy
          </router-link>
          <span class="hidden md:block mx-2 text-stone-400"> | </span>
          <router-link to="/cookies" class="text-stone-400 hover:underline text-xs md:text-sm">
            Cookie Policy
          </router-link>
        </div>
        <p class="text-stone-400 text-xs md:text-sm mt-2 md:mt-3">
          Contact us at
          <a href="mailto:tangerine.inquries@gmail.com"
            class="text-orange-500 underline">tangerine.inquries@gmail.com</a>
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'; // Import useRouter

export default {
  name: 'LoginPage', // Renamed for clarity, original was 'Login'
  setup() {
    const router = useRouter(); // Initialize router

    // Data properties are now reactive in setup if needed, but not explicitly used for form inputs here
    const base_url = import.meta.env.VITE_API_BASE_URL;

    const goBack = () => {
      router.push('/'); // Navigate to the root/home page as per your previous request
    };
    const goSetup = () => {
      router.push('/setup'); // Navigate to the root/home page as per your previous request
    };
    const loginWithGoogle = () => {
      clearAllLocalData();
      window.location.href = `${base_url}/auth/google`;
    };

    const clearAllLocalData = () => {
      localStorage.clear();
      sessionStorage.clear();
    };

    // No direct form handling in this version, as it's been replaced by Google login/continue without account
    // If you need email/password login, you'd reintroduce signInForm and handleSignIn method here.

    return {
      goBack,
      loginWithGoogle,
      // If you reintroduce form fields, they'd be returned here too
    };
  },
}
</script>

<style scoped>
</style>