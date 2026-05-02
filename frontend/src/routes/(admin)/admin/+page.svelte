<script lang="ts">
  import { invalidateAll } from "$app/navigation";
  import type { PageData } from "./$types";

  export let data: PageData;

  let selectedAppointment: PageData["appointments"][number] | null = null;
  let newNote = "";
  let savingNote = false;

  const formatDateTime = (value: string) =>
    new Date(value).toLocaleString("en-GB", {
      day: "numeric",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

  const formatTime = (value: string) =>
    new Date(value).toLocaleTimeString("en-GB", {
      hour: "2-digit",
      minute: "2-digit",
    });

async function addNote(appointmentId: number) {
  const message = newNote.trim();

  if (!message) {
    alert("Write a note first");
    return;
  }

  savingNote = true;

  const res = await fetch(`/api/admin/appointment/${appointmentId}/note`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  savingNote = false;

  if (!res.ok) {
    alert("Failed to save note");
    return;
  }

  newNote = "";
  selectedAppointment = null;
  await invalidateAll();
}

  const quickLinks = [
    { label: "Day-to-day appointments", href: "/admin/appointments" },
    { label: "Register donation", href: "/admin/appointments" },
    { label: "Register interview", href: "/admin/appointments" },
    { label: "Register donation test", href: "/admin/appointments" },
  ];
</script>

<svelte:head>
  <title>Admin Dashboard</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-6 py-10">
  <div class="mb-8">
    <h1 class="text-5xl font-bold tracking-tight text-slate-950">
      Admin Dashboard
    </h1>
    <p class="mt-3 max-w-2xl text-base leading-7 text-slate-500">
      Get an overview of today’s appointments and move quickly between important
      admin pages.
    </p>
  </div>

  <div class="grid gap-6 lg:grid-cols-12">
    <div class="space-y-6 lg:col-span-4">
      <section class="rounded-[28px] border border-slate-200 bg-white p-6 shadow-sm">
        <div class="mb-4 flex items-start justify-between gap-4">
          <div>
            <h2 class="text-2xl font-semibold text-slate-950">Up next</h2>
            <p class="mt-1 text-sm text-slate-500">
              {#if data.bloodbank}
                {data.bloodbank.name}
              {:else}
                No assigned blood bank
              {/if}
            </p>
          </div>

          <span class="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-600">
            {data.stats.todayCount} today
          </span>
        </div>

        {#if data.nextAppointment}
          <div class="rounded-3xl bg-slate-50 p-5">
            <p class="text-2xl font-semibold">{data.nextAppointment.donorName}</p>
            <p class="mt-2">{formatDateTime(data.nextAppointment.time)}</p>
          </div>
        {:else}
          <div class="rounded-3xl bg-slate-50 p-5 text-sm text-slate-500">
            No upcoming appointments today.
          </div>
        {/if}
      </section>

      <section class="rounded-[28px] border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="text-2xl font-semibold text-slate-950">Quick access</h2>

        <div class="mt-5 space-y-3">
          {#each quickLinks as link}
            <a
              href={link.href}
              class="flex items-center justify-between rounded-2xl border px-4 py-4 hover:bg-slate-50"
            >
              <span>{link.label}</span>
              <span>→</span>
            </a>
          {/each}
        </div>
      </section>
    </div>

    <div class="space-y-6 lg:col-span-8">
      <section class="rounded-[28px] border border-slate-200 bg-white p-6 shadow-sm">
        <div class="mb-5 flex justify-between">
          <h2 class="text-2xl font-semibold">Today’s appointments</h2>
          <span class="text-sm">{data.appointments.length} items</span>
        </div>

        <div class="space-y-4">
          {#each data.appointments as appointment}
            <div class="rounded-[24px] border p-5">
              <div class="flex justify-between">
                <div>
                  <p class="text-xl font-semibold">{appointment.donorName}</p>
                  <p>{formatTime(appointment.time)}</p>
                </div>

                <button
                  type="button"
                  class="rounded-xl border px-4 py-2"
                  on:click={() => {
                    selectedAppointment = appointment;
                    newNote = "";
                  }}
                >
                  View
                </button>
              </div>

              {#if appointment.notes.length > 0}
                <div class="mt-3 text-sm text-slate-600">
                  Latest note: {appointment.notes[appointment.notes.length - 1].message}
                </div>
              {/if}
            </div>
          {/each}
        </div>
      </section>
    </div>
  </div>
</div>

{#if selectedAppointment}
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-6">
    <div class="w-full max-w-2xl rounded-[28px] bg-white p-6 shadow-xl">
      <div class="mb-4 flex justify-between">
        <h2 class="text-xl font-semibold">{selectedAppointment.donorName}</h2>

        <button
          type="button"
          on:click={() => selectedAppointment = null}
        >
          Close
        </button>
      </div>

      <h3 class="mb-3 font-semibold">All notes</h3>

      {#if selectedAppointment.notes.length > 0}
        {#each selectedAppointment.notes as note}
          <div class="mb-2 rounded bg-slate-50 p-3">
            {note.message}
          </div>
        {/each}
      {:else}
        <p>No notes yet</p>
      {/if}

      <textarea
        bind:value={newNote}
        class="mt-4 w-full border p-3"
        placeholder="Add note..."
      />

      <button
        type="button"
        disabled={savingNote}
        class="mt-3 rounded bg-black px-4 py-2 text-white disabled:opacity-50"
        on:click|preventDefault={() => addNote(selectedAppointment!.appointmentId)}
      >
        {savingNote ? "Saving..." : "Save note"}
      </button>
    </div>
  </div>
{/if}