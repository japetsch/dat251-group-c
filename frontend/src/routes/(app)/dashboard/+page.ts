import { createLoadClient } from "$lib/api/client";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, url }) => {
  const client = createLoadClient(fetch, url);
  const r = await client.GET("/appointment");

  if (!r.response.ok || !r.data) {
    return { upcoming: [], completed: 0 };
  }

  const now = new Date();
  const upcoming = r.data
    .filter((a) => !a.cancelled && new Date(a.time) >= now)
    .sort((a, b) => new Date(a.time).getTime() - new Date(b.time).getTime());

  const completed = r.data.filter(
    (a) => !a.cancelled && new Date(a.time) < now,
  ).length;

  return { upcoming, completed };
};
