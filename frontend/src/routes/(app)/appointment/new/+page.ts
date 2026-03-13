import { createLoadClient } from "$lib/api/client";
import type { Appointment } from "$lib/types/appointment";
import type { PageLoad } from "./$types";

type NewApptPreloaded = {
  availableAppointments: Appointment[];
  error: string | null;
};

export const load: PageLoad<NewApptPreloaded> = async ({ fetch, url }) => {
  const client = createLoadClient(fetch, url);
  const r = await client.GET("/appointment/available");

  if (!r.response.ok || !r.data) {
    return {
      availableAppointments: [],
      error: "Failed to load available appointments",
    };
  }

  return {
    availableAppointments: r.data,
    error: null,
  };
};
