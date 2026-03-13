<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();

  const navItems = [
    { name: "Home", href: "/dashboard" },
    { name: "My Appointments", href: "/appointment/list" },
    { name: "New Appointment", href: "/appointment/new" }
  ];
  import "../layout.css";
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<header class="w-full border-b bg-white">
  <div class="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">

    <a href="/dashboard" class="flex items-center">
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
    </nav>

  </div>
</header>

<div class="container mx-auto mt-4">
    {@render children()}
</div>
