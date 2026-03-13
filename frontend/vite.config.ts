import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	test: {
		environment: 'jsdom',
		setupFiles: ['./src/lib/test/setup.ts'],
		include: ['src/**/*.test.ts']
	},
	server: {
		proxy: {
			"/api": "http://localhost:8000",
		}
	},
});
