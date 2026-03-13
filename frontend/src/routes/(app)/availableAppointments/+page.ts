import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	try {
		const response = await fetch('/api/appointment/available');

		if (!response.ok) {
			return {
				availableAppointments: [],
				error: 'Failed to load available appointments'
			};
		}

		return {
			availableAppointments: await response.json(),
			error: null
		};
	} catch {
		return {
			availableAppointments: [],
			error: 'Failed to load available appointments'
		};
	}
};
