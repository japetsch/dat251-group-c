import { createLoadClient } from "$lib/api/client";
import { redirect } from "@sveltejs/kit";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ fetch, url }) => {
  const client = createLoadClient(fetch, url);
  const r = await client.GET("/auth/me");

  if (!r.response.ok || !r.data) {
    throw redirect(303, `/login?next=${encodeURIComponent(url.pathname)}`);
  }

  if (!("admin_id" in r.data)) {
    throw redirect(303, "/dashboard");
  }

  return { user: r.data };
};
