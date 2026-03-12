import createClient from "openapi-fetch";
import type { paths } from "./schema";

export function createLoadClient(fetch: typeof globalThis.fetch, url: URL) {
  return createClient<paths>({ baseUrl: `${url.origin}/api`, fetch });
}

const client = createClient<paths>({ baseUrl: "/api" });
export default client;
