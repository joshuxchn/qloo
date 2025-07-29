<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-50">
    <div class="text-center p-8 bg-white shadow-md rounded-lg">
      <p class="text-lg font-medium text-gray-800">{{ statusMessage }}</p>
      <p class="text-sm text-gray-500 mt-2">Please wait a moment.</p>
      <div class="mt-6 animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500 mx-auto"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { userStore } from '@/stores/userStore'; // Ensure this path is correct

const router = useRouter();
const route = useRoute();
const base_url = import.meta.env.VITE_API_BASE_URL;
const statusMessage = ref('Processing your login...');

onMounted(async () => {
  const token = route.query.token;

  if (!token) {
    console.error("Authentication failed: No token found.");
    router.push('/login?error=no_token');
    return;
  }

  // Set the token immediately for subsequent API calls
  userStore.setToken(token);
  console.log("JWT token received.");

  // Check for pending profile data from the setup form
  const pendingProfileJSON = localStorage.getItem('pendingUserProfile');

  if (pendingProfileJSON) {
    statusMessage.value = 'Finalizing your profile...';
    try {
      const profileData = JSON.parse(pendingProfileJSON);
      
      // Send the profile data to the new backend endpoint
      const response = await fetch(`${base_url}/api/user/finalize-profile`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(profileData)
      });

      if (!response.ok) {
        throw new Error('Failed to finalize profile on the backend.');
      }

      console.log("✅ Profile finalized successfully.");
      // Clean up the stored data now that it's been sent
      localStorage.removeItem('pendingUserProfile');

    } catch (error) {
      console.error("Error finalizing profile:", error);
      userStore.logout();
      localStorage.removeItem('pendingUserProfile'); // Clean up on error too
      router.push('/login?error=profile_failed');
      return;
    }
  }

  // Whether a profile was finalized or not, fetch the complete user data
  await userStore.fetchUser();
  if (userStore.user) {
    router.push('/dashboard');
  } else {
    router.push('/login?error=fetch_failed');
  }
});
</script>