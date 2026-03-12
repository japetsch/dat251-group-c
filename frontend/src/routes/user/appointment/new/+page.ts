import type { PageLoad } from "./$types";
import type { components } from "$lib/api/schema";

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

export const load: PageLoad = async ({ fetch }) => {
  const response = await fetch("/api/appointment/available");

  if (!response.ok) {
    return {
      availabe: [],
      error: "Failed to load available appointments",
    };
  }

  const available: Array<GetAvailableAppointmentsRow> = await response.json();

  return { events: createEvents(available) };
};
