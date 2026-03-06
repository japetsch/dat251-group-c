import client from '$lib/api/client';
import type { components } from '$lib/api/schema';

export type AppointmentRow = components['schemas']['GetAllAppointmentsRow'];

export async function getAppointments(): Promise<AppointmentRow[]> {
	const { data, error } = await client.GET('/appointment');

	if (error) {
		throw new Error('Failed to fetch appointments');
	}

	return data ?? [];
}
