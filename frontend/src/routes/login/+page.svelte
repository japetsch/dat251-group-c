<script lang="ts">
  import { page } from "$app/stores";

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
        // TODO: change to sveltekit redirect
        const next = $page.url.searchParams.get("next") ?? "/dashboard";
        window.location.href = next;
      }
    } finally {
      loading = false;
    }
  }
</script>

<div>
  <div>
    <h1>Sign in</h1>

    <form onsubmit={handleSubmit}>
      <div>
        <label for="email">Email</label>
        <input
          id="email"
          type="email"
          bind:value={email}
          required
          autocomplete="email"
        />
      </div>

      <div>
        <label for="password">Password</label>
        <input
          id="password"
          type="password"
          bind:value={password}
          required
          autocomplete="current-password"
        />
      </div>

      {#if error}
        <p>{error}</p>
      {/if}

      <button type="submit" disabled={loading}>
        {loading ? "Signing in..." : "Sign in"}
      </button>
    </form>
  </div>
</div>
