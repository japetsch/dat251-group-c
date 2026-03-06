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

		const availableAppointments = await response.json();

		return {
			availableAppointments,
			error: null
		};
	} catch {
		return {
			availableAppointments: [],
			error: 'Failed to load available appointments'
		};
	}
};
