import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/driverInfo': 'http://localhost:3000',  // Proxy API calls to the backend
      '/trackInfo': 'http://localhost:3000',  // Proxy API calls to the backend

    },      
  },
});
