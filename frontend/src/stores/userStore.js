import { reactive } from 'vue';
import { jwtDecode } from 'jwt-decode';

// Retrieve the API base URL from environment variables
const base_url = import.meta.env.VITE_API_BASE_URL;

export const userStore = reactive({
    token: localStorage.getItem('jwt_token') || null,
    user: null,

    /**
     * Sets the authentication token and stores it in localStorage.
     * @param {string | null} newToken - The new JWT.
     */
    setToken(newToken) {
        this.token = newToken;
        if (newToken) {
            localStorage.setItem('jwt_token', newToken);
        } else {
            localStorage.removeItem('jwt_token');
        }
    },

    /**
     * Fetches the current user's profile from the backend using the stored token.
     */
    async fetchUser() {
        if (!this.token) {
            console.warn("No token available to fetch user.");
            return;
        }
        try {
            const response = await fetch(`${base_url}/api/user/profile`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                },
            });
            if (!response.ok) {
                throw new Error('Failed to fetch user profile.');
            }
            this.user = await response.json();
            console.log("✅ User profile fetched and stored:", this.user);
        } catch (error) {
            console.error("Error fetching user:", error);
            this.logout(); // Log out if token is invalid or fetching fails
        }
    },

    /**
     * Clears user data and token from the store and localStorage.
     */
    logout() {
        this.setToken(null);
        this.user = null;
        console.log("🔒 User logged out.");
    },

    /**
     * A getter to easily check if the user is authenticated.
     * @returns {boolean}
     */
    get isAuthenticated() {
        return !!this.token && !!this.user;
    }
});

// On application load, check for an existing token and fetch the user.
if (userStore.token) {
    const decoded = jwtDecode(userStore.token);
    const isExpired = decoded.exp * 1000 < Date.now();
    if (isExpired) {
        userStore.logout();
    } else {
        userStore.fetchUser();
    }
}