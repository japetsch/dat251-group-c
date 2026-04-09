<script lang="ts">
  import "../../(app)/app.css";
  import favicon from "$lib/assets/favicon.svg";

  let { children } = $props();

  const navItems = [
    { name: "Home", href: "/admin" },
    { name: "Appointments", href: "/admin/appointments" },
  ];

  async function signout() {
    const res = await fetch("/api/auth/logout");
    if (res.ok) {
      // TODO: change to sveltekit redirect when tailwind is globally loaded
      window.location.href = "/";
    }
  }
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<header class="w-full border-b bg-white">
  <div class="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
    <a href="/admin" class="flex items-center">
      <img src="/tmp_logo.svg" alt="Logo" class="h-8 w-auto" />
    </a>

    <nav class="flex items-center gap-6 text-sm font-medium">
      {#each navItems as item}
        <a
          href={item.href}
          class="text-gray-700 transition hover:text-blue-600"
        >
          {item.name}
        </a>
      {/each}
      <button
        onclick={signout}
        class="text-gray-700 transition hover:text-blue-600 hover:cursor-pointer"
      >
        Sign Out
      </button>
    </nav>
  </div>
</header>

<div class="container mx-auto p-16">
  {@render children()}
</div>
