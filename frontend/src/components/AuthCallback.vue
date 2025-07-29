<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-50">
    <div class="text-center p-8 bg-white shadow-md rounded-lg">
      <p class="text-lg font-medium text-gray-800">Processing your login...</p>
      <p class="text-sm text-gray-500 mt-2">Please wait a moment.</p>
      <div class="mt-6 animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500 mx-auto"></div>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { userStore } from './userStore'; // Fixed relative path

export default {
  name: 'AuthCallback',
  setup() {
    const router = useRouter();
    const route = useRoute();

    onMounted(async () => {
      const token = route.query.token;

      if (token) {
        try {
          // 1. Set the token in our store, which also saves it to localStorage.
          userStore.setToken(token);
          console.log("JWT token received.");

          // 2. Fetch the user's profile from the backend using the new token.
          await userStore.fetchUser();
          
          // 3. Redirect to the dashboard after the user is fully authenticated and stored.
          if (userStore.user) {
            router.push('/dashboard');
          } else {
            // This case might happen if fetchUser fails without throwing an error.
            throw new Error("User data could not be retrieved after login.");
          }
        } catch (error) {
          console.error("Authentication process failed:", error);
          userStore.logout(); // Clean up on failure
          router.push('/login?error=auth_failed');
        }
      } else {
        console.error("Authentication failed: No token found in callback URL.");
        router.push('/login?error=no_token');
      }
    });
  },
};
</script>

<style scoped>
/* Scoped styles remain the same */
</style>