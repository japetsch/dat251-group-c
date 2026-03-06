import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const response = await fetch('/api/appointment');

	if (!response.ok) {
		return {
			appointments: [],
			error: 'Failed to load appointments'
		};
	}

	const appointments = await response.json();

	return {
		appointments,
		error: null
	};
};

