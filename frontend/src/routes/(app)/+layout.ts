import { createLoadClient } from "$lib/api/client";
import type { LayoutLoad } from "./$types";

export const load: LayoutLoad = async ({ fetch, url }) => {
  const client = createLoadClient(fetch, url);
  const r = await client.GET("/auth/me");

  if (!r.response.ok || !r.data) {
    // TODO: change to sveltekit redirect when tailwind is globally loaded
    window.location.href = `/login?next=${encodeURIComponent(url.pathname)}`;
    return {};
  }

  if ("admin_id" in r.data) {
    window.location.href = "/admin";
    return {};
  }

  return { user: r.data };
};
