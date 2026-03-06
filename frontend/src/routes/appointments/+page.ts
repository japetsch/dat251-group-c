import type { PageLoad } from './$types';
import { getAppointments } from '$lib/api/appointments';

export const load: PageLoad = async () => {
	return {
		appointments: await getAppointments()
	};
};
