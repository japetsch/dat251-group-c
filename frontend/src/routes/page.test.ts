import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';

import Page from './+page.svelte';

describe('Home page', () => {
	it('renders the welcome heading', () => {
		render(Page);

		expect(screen.getByRole('heading', { name: 'Welcome to SvelteKit' })).toBeInTheDocument();
	});
});
