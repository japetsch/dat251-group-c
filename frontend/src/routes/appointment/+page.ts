import client from '$lib/api/client';

export async function load() {
    const { data: appointments } = await client.GET('/appointment');

    if (!appointments) {
        return {
            appointments: [],
            error: 'Failed to load appointments'
        };
    }
    return {
        appointments,
        error: null
    };
}
