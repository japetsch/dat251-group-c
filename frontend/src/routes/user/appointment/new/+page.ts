import type { PageLoad } from "./$types";
import type { components } from "$lib/api/schema";
import { createLoadClient } from "$lib/api/client";

type GetAvailableAppointmentsRow =
  components["schemas"]["GetAvailableAppointmentsRow"];

function addMinutes(time: string, minutes: number): string {
  const date = new Date(time);
  date.setMinutes(date.getMinutes() + minutes);
  return date.toISOString();
}

function createEvents(available: Array<GetAvailableAppointmentsRow>) {
  var events = [];
  for (const a of available) {
    events.push({
      start: a.time,
      end: addMinutes(a.time, 30),
      title: a.locationname,
      editable: false,
      startEditable: false,
      durationEditable: false,
      extendedProps: {
        locationId: a.location_id,
        id: a.id,
      },
    });
  }

  return events;
}

export const load: PageLoad = async ({ fetch, url }) => {
  const client = createLoadClient(fetch, url);
  const r = await client.GET("/appointment/available");

  if (!r.response.ok || !r.data) {
    return {
      events: [],
      error: "Failed to load available appointments",
    };
  }

  return { events: createEvents(r.data) };
};
