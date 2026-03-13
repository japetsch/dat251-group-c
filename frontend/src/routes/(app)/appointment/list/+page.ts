import { createLoadClient } from "$lib/api/client";
import type { components } from '$lib/api/schema';
import type { PageLoad } from './$types';

type ApptListPreloaded = {
  appointments: components["schemas"]["GetAllAppointmentsRow"][];
  error: string | null;
}

export const load: PageLoad<ApptListPreloaded> = async ({ fetch, url }) => {
  const client = createLoadClient(fetch, url);
	const r = await client.GET("/appointment");

	if (!r.response.ok || !r.data) {
		return {
			appointments: [],
			error: 'Failed to load appointments'
		};
	}

	return {
		appointments: r.data,
		error: null
	};
};