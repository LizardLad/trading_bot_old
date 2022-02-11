import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            '@assets': path.resolve(__dirname, 'src/assets'),
            '@components': path.resolve(__dirname, 'src/components'),
            '@testing': path.resolve(__dirname, 'src/testing')
        }
    },
    server: {
    proxy: {
        '/api': {
            target: 'http://localhost:8080',
            changeOrigin: false
        }
    }}
});
