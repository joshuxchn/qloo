import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './index.css'
import VueApexCharts from 'vue3-apexcharts'

// --- Import components ---
import Landing from './components/Landing.vue'
import Login from './components/Login.vue'
import Privacy from './components/Privacy.vue'
import TOS from './components/TOS.vue'
import Cookies from './components/Cookies.vue'
import Setup from './components/Setup.vue'
import dashboard from './components/dashboard.vue'
import profile from './components/Profile.vue'
import list from './components/ListBuilder.vue'
// 👇 1. IMPORT THE AUTH CALLBACK COMPONENT
import AuthCallback from './components/AuthCallback.vue';


// --- Define routes ---
const routes = [
  { path: '/', component: Landing },
  { path: '/setup', component: Setup },
  { path: '/cookies', component: Cookies },
  { path: '/privacy', component: Privacy },
  { path: '/list', component: list },
  { path: '/terms', component: TOS },
  { path: '/login', component: Login },
  { path: '/profile', component: profile },
  { path: '/dashboard', component: dashboard },
  // 👇 2. ADD THE ROUTE FOR THE AUTHENTICATION CALLBACK
  // This line is the critical fix for the "Not Found" error.
  { path: '/auth/callback', name: 'AuthCallback', component: AuthCallback },
  { path: '/:pathMatch(.*)*', redirect: '/login' } // Catch-all
]

// --- Create router ---
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  }
});

// --- 🔐 Navigation guard ---
router.beforeEach(async (to, from, next) => {
  // 👇 3. ADD '/auth/callback' TO THE PUBLIC PATHS
  // This allows the callback component to run without being blocked by the guard.
  const publicPaths = ['/', '/login', '/setup', '/privacy', '/terms', '/cookies', '/auth/callback'];
  
  if (publicPaths.includes(to.path)) {
    return next();
  }

  // This logic now correctly checks for the token set by AuthCallback.vue
  try {
    const token = localStorage.getItem('jwt_token');
    if (token) {
        // User has a token, so they are allowed to proceed.
        return next();
    }
    
    // If no token is found, redirect to the login page.
    return next('/login');

  } catch (err) {
    console.error('Auth check failed:', err);
    return next('/login');
  }
});


// --- Create and mount app ---
const app = createApp(App)
app.use(VueApexCharts)
app.use(router)
app.mount('#app')