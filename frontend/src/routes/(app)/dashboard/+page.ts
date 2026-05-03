import { createLoadClient } from "$lib/api/client";
import type { components } from "$lib/api/schema";
import type { PageLoad } from "./$types";

type Appointment = components["schemas"]["AppointmentType"];

type DashboardData = {
  nextAppointment: Appointment | null;
  completedThisYear: number;
  totalCompleted: number;
  error: string | null;
};

export const load: PageLoad<DashboardData> = async ({ fetch, url }) => {
  const client = createLoadClient(fetch, url);
  const r = await client.GET("/appointment");

  if (!r.response.ok || !r.data) {
    return {
      nextAppointment: null,
      completedThisYear: 0,
      totalCompleted: 0,
      error: "Kunne ikke laste inn timer",
    };
  }

  const now = new Date();
  const thisYear = now.getFullYear();
  const active = r.data.filter((a) => !a.cancelled);

  const upcoming = active
    .filter((a) => new Date(a.time) >= now)
    .sort((a, b) => new Date(a.time).getTime() - new Date(b.time).getTime());

  const previous = active.filter((a) => new Date(a.time) < now);

  return {
    nextAppointment: upcoming[0] ?? null,
    completedThisYear: previous.filter(
      (a) => new Date(a.time).getFullYear() === thisYear,
    ).length,
    totalCompleted: previous.length,
    error: null,
  };
};
