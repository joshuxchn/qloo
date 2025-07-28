<template>
  <!-- This is the content that will be displayed while the login is being processed. -->
  <!-- It provides visual feedback to the user so they know something is happening. -->
  <div class="flex items-center justify-center min-h-screen bg-gray-50">
    <div class="text-center p-8 bg-white shadow-md rounded-lg">
      <p class="text-lg font-medium text-gray-800">Processing your login...</p>
      <p class="text-sm text-gray-500 mt-2">Please wait a moment.</p>
      <!-- A simple spinning animation to indicate loading -->
      <div class="mt-6 animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
    </div>
  </div>
</template>

<script>
// We need to import functions from Vue and Vue Router to make this work.
import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'AuthCallback',
  setup() {
    // useRouter allows us to programmatically redirect the user.
    const router = useRouter();
    // useRoute allows us to access information about the current URL, including query parameters.
    const route = useRoute();

    // 'onMounted' is a lifecycle hook that runs its code as soon as the component
    // has been added to the page. This is the perfect place to handle the redirect logic.
    onMounted(() => {
      // 1. Get the token from the URL.
      // The backend redirects to a URL like: /auth/callback?token=ey...
      // 'route.query.token' will grab the value of the 'token' parameter.
      const token = route.query.token;

      // 2. Check if a token was actually found in the URL.
      if (token) {
        // If a token exists, we store it in the browser's localStorage.
        // This makes it persistent, so the user stays logged in even if they
        // refresh the page or close the tab.
        localStorage.setItem('jwt_token', token);
        console.log("JWT token received and stored successfully.");

        // 3. Redirect to the main dashboard.
        // Now that the user is authenticated, we can send them to the protected
        // part of the application.
        router.push('/dashboard');
      } else {
        // If for some reason the token is missing, something went wrong.
        console.error("Authentication failed: No token found in callback URL.");
        
        // 4. Redirect back to the login page with an error flag.
        // This allows the login page to show an error message to the user.
        router.push('/login?error=auth_failed');
      }
    });

    // This component's main purpose is the logic within onMounted.
    // We don't need to return anything else from the setup function.
  },
};
</script>

<style scoped>
/* You can add component-specific styles here if needed.
   The Tailwind CSS classes in the template handle the styling for this component. */
</style>
