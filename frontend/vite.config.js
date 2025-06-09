import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        ws: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          ui: ['@headlessui/react', '@heroicons/react']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  },  preview: {
    port: 4173,
    host: true,
    allowedHosts: [
      'ecommerce-frontend-1qfw.onrender.com',
      '.onrender.com'
    ]
  },
  server: {
    port: 5173,
    host: true
  }
})
