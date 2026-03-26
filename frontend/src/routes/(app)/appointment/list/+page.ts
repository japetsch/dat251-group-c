import { createLoadClient } from "$lib/api/client";
import type { components } from "$lib/api/schema";
import type { PageLoad } from "./$types";

type ApptListPreloaded = {
  upcoming: components["schemas"]["GetAppointmentsByDonorIdRow"][];
  previous: components["schemas"]["GetAppointmentsByDonorIdRow"][];
  error: string | null;
};

export const load: PageLoad<ApptListPreloaded> = async ({ fetch, url }) => {
  const client = createLoadClient(fetch, url);
  const r = await client.GET("/appointment");

  if (!r.response.ok || !r.data) {
    return {
      upcoming: [],
      previous: [],
      error: "Failed to load appointments",
    };
  }

  const now = new Date();
  return {
    previous: r.data.filter((x) => new Date(x.time) < now),
    upcoming: r.data.filter((x) => new Date(x.time) >= now),
    error: null,
  };
};
