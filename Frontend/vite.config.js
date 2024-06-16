import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    outDir: 'dist', // Output directory for production build
    assetsDir: '', // Relative directory for assets
    minify: true, // Minify code for production
    sourcemap: false, // Disable sourcemaps for production
  },
});