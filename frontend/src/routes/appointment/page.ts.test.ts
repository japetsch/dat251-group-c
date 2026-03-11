import { describe, expect, it, vi } from 'vitest';
import { load } from './+page';

describe('+page.ts load', () => {
	it('returns appointments when fetch succeeds', async () => {
		const mockAppointments = [
			{
				id: 1,
				username: 'alice',
				locationname: 'Oslo',
				time: '2025-03-06T10:00:00Z'
			}
		];

		const fetch = vi.fn().mockResolvedValue({
			ok: true,
			json: vi.fn().mockResolvedValue(mockAppointments)
		});

		const result = await load({ fetch } as never);

		expect(fetch).toHaveBeenCalledWith('/api/appointment');
		expect(result).toEqual({
			appointments: mockAppointments,
			error: null
		});
	});

	it('returns error and empty appointments when fetch fails', async () => {
		const fetch = vi.fn().mockResolvedValue({
			ok: false
		});

		const result = await load({ fetch } as never);

		expect(fetch).toHaveBeenCalledWith('/api/appointment');
		expect(result).toEqual({
			appointments: [],
			error: 'Failed to load appointments'
		});
	});
});