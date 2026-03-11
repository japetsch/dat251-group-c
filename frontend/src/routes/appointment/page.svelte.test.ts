import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';
import Page from './+page.svelte';

describe('+page.svelte', () => {
	it('renders heading and appointments table', () => {
		render(Page, {
			data: {
				appointments: [
					{
						id: 1,
						username: 'alice',
						locationname: 'Oslo',
						time: '2025-03-06T10:00:00Z'
					},
					{
						id: 2,
						username: 'bob',
						locationname: 'Bergen',
						time: '2025-03-06T12:00:00Z'
					}
				],
				error: null
			}
		});

		expect(screen.getByRole('heading', { name: /appointments/i })).toBeInTheDocument();
		expect(screen.getByText('alice')).toBeInTheDocument();
		expect(screen.getByText('bob')).toBeInTheDocument();
		expect(screen.getByText('Oslo')).toBeInTheDocument();
		expect(screen.getByText('Bergen')).toBeInTheDocument();
		expect(screen.getByText('Hello world!')).toBeInTheDocument();
	});

	it('renders error message', () => {
		render(Page, {
			data: {
				appointments: [],
				error: 'Failed to load appointments'
			}
		});

		expect(screen.getByText('Failed to load appointments')).toBeInTheDocument();
		expect(screen.getByText('Hello world!')).toBeInTheDocument();
	});

	it('renders empty state when there are no appointments', () => {
		render(Page, {
			data: {
				appointments: [],
				error: null
			}
		});

		expect(screen.getByText('No appointments found.')).toBeInTheDocument();
		expect(screen.getByText('Hello world!')).toBeInTheDocument();
	});
});