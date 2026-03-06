import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';
import Page from './+page.svelte';

describe('appointments page', () => {
	it('renders appointments', () => {
		render(Page, {
			data: {
				appointments: [
					{
						id: 1,
						username: 'alice',
						locationname: 'Main Clinic',
						time: '2025-03-06T10:00:00Z'
					},
					{
						id: 2,
						username: 'bob',
						locationname: 'Downtown Office',
						time: '2025-03-06T11:00:00Z'
					}
				]
			}
		});

		expect(screen.getByRole('heading', { name: /appointments/i })).toBeInTheDocument();
		expect(screen.getByText('alice')).toBeInTheDocument();
		expect(screen.getByText('bob')).toBeInTheDocument();
		expect(screen.getByText('Main Clinic')).toBeInTheDocument();
		expect(screen.getByText('Downtown Office')).toBeInTheDocument();
	});

	it('renders empty state', () => {
		render(Page, {
			data: {
				appointments: []
			}
		});

		expect(screen.getByText(/no appointments found/i)).toBeInTheDocument();
	});
});
