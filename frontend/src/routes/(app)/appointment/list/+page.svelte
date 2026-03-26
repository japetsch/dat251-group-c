<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<h1 class="text-3xl mb-4">My appointments</h1>

{#if data.error}
  <p>{data.error}</p>
{:else if data.upcoming.length === 0 && data.previous.length === 0}
  <p>No appointments found.</p>
{:else}
  <h2 class="text-xl mb-4">Upcoming</h2>
  <hr />
  <table class="w-full border-collapse text-base mb-4">
    <thead>
      <tr
        class="border-b border-gray-200 text-left text-xs uppercase tracking-wider text-gray-500"
      >
        <th class="py-3 pr-6 font-medium">User</th>
        <th class="py-3 pr-6 font-medium">Location</th>
        <th class="py-3 font-medium">Time</th>
      </tr>
    </thead>

    <tbody class="divide-y divide-gray-100">
      {#each data.upcoming as appointment}
        <tr class="transition-colors hover:bg-gray-50">
          <td class="py-3 pr-6 font-medium text-gray-900"
            >{appointment.username}</td
          >
          <td class="py-3 pr-6 text-gray-600">{appointment.bloodbank_name}</td>
          <td class="py-3 text-gray-600"
            >{new Date(appointment.time).toLocaleString()}</td
          >
        </tr>
      {/each}
    </tbody>
  </table>

  <h2 class="text-xl mb-4">Previous</h2>
  <hr />
  <table class="w-full border-collapse text-base">
    <thead>
      <tr
        class="border-b border-gray-200 text-left text-xs uppercase tracking-wider text-gray-500"
      >
        <th class="py-3 pr-6 font-medium">User</th>
        <th class="py-3 pr-6 font-medium">Location</th>
        <th class="py-3 font-medium">Time</th>
      </tr>
    </thead>

    <tbody class="divide-y divide-gray-100">
      {#each data.previous as appointment}
        <tr class="transition-colors hover:bg-gray-50">
          <td class="py-3 pr-6 font-medium text-gray-900"
            >{appointment.username}</td
          >
          <td class="py-3 pr-6 text-gray-600">{appointment.bloodbank_name}</td>
          <td class="py-3 text-gray-600"
            >{new Date(appointment.time).toLocaleString()}</td
          >
        </tr>
      {/each}
    </tbody>
  </table>
{/if}
