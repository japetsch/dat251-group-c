import { createLoadClient } from "$lib/api/client";
import type { components } from '$lib/api/schema';
import type { PageLoad } from './$types';

type ApptListPreloaded = {
  upcoming: components["schemas"]["GetAllAppointmentsRow"][];
  previous: components["schemas"]["GetAllAppointmentsRow"][];
  error: string | null;
}

export const load: PageLoad<ApptListPreloaded> = async ({ fetch, url }) => {
  const client = createLoadClient(fetch, url);
	const r = await client.GET("/appointment");

	if (!r.response.ok || !r.data) {
		return {
			upcoming: [],
			previous: [],
			error: 'Failed to load appointments'
		};
	}

	return {
		previous: r.data.filter((x) => new Date(x.time) < new Date()),
		upcoming: r.data.filter((x) => new Date(x.time) >= new Date()),
		error: null
	};
};