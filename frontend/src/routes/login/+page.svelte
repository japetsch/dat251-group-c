<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import Cards from "$lib/components/Cards.svelte";

  let email = $state("");
  let password = $state("");
  let error = $state<string | null>(null);
  let loading = $state(false);

  async function handleSubmit(e: SubmitEvent) {
    e.preventDefault();
    error = null;
    loading = true;

    try {
      const r = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (r.status === 401) {
        error = "Invalid email or password.";
      } else if (!r.ok) {
        error = "An error occurred. Please try again.";
      } else {
        const next = $page.url.searchParams.get("next") ?? "/dashboard";
        await goto(next);
      }
    } finally {
      loading = false;
    }
  }
</script>

<div
  class="flex min-h-screen items-center justify-center bg-[#f5f2f1] px-4 py-12"
>
  <a href="/" class="fixed left-6 top-6 z-50 transition hover:opacity-80">
    <img src="/tmp_logo.svg" alt="Til forsiden" class="h-20 w-20" />
  </a>
  <Cards orientation="vertical" tone="white" class="w-full max-w-[520px]">
    <div class="mb-8 text-center">
      <h1 class="text-2xl font-semibold tracking-tight text-slate-900">
        Logg inn
      </h1>
      <p class="mt-1 text-center text-sm text-slate-600">
        Logg inn for å fortsette i blodbankappen.
      </p>
    </div>

    <form onsubmit={handleSubmit} class="space-y-6">
      <div>
        <label for="email" class="mb-2 block text-sm font-medium text-slate-700"
          >Email</label
        >
        <input
          id="email"
          type="email"
          bind:value={email}
          required
          autocomplete="email"
          class="block h-11 w-full rounded-xl border border-slate-300 bg-white px-4 text-sm text-slate-900 shadow-sm outline-none transition focus:border-red-500 focus:ring-2 focus:ring-red-200"
        />
      </div>

      <div class="space-y-2">
        <label
          for="password"
          class="mb-2 block text-sm font-medium text-slate-700">Passord</label
        >
        <input
          id="password"
          type="password"
          bind:value={password}
          required
          autocomplete="current-password"
          class="block h-11 w-full rounded-xl border border-slate-300 bg-white px-4 text-sm text-slate-900 shadow-sm outline-none transition focus:border-red-500 focus:ring-2 focus:ring-red-200"
        />
      </div>

      {#if error}
        <p
          class="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
        >
          {error}
        </p>
      {/if}

      <button
        type="submit"
        disabled={loading}
        class="w-full rounded-xl bg-red-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-red-700 disabled:cursor-not-all-allowed disabled:opacity-70"
      >
        {loading ? "Logger inn..." : "Logg inn"}
      </button>
    </form>
  </Cards>
</div>
