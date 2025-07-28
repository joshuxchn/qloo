import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },

  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      // 👇 FIX: This rule is now more specific.
      // It will proxy '/auth/google' and '/auth/google/callback' to the backend,
      // but it will IGNORE the frontend-only '/auth/callback' route.
      '/auth/google': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        // Optional: rewrite path if backend expects /google instead of /auth/google
        // rewrite: (path) => path.replace(/^\/auth/, '') 
      },
      // Proxies for other backend routes
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/me': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/logout': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      }
    },
    hmr: {
      host: 'localhost'
    },
    allowedHosts: [
      'localhost',
      '127.0.0.1'
    ]
  },
  
  preview: {
    host: '0.0.0.0',
    port: 3000
  }
})