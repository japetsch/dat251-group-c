import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const response = await fetch('http://127.0.0.1:8000/api/appointment');

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
