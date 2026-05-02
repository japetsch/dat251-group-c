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

  async function addNote() {
    if (!selectedAppointment) return;

    const message = newNote.trim();

    if (!message) {
      alert("Write a note first");
      return;
    }

    savingNote = true;

    const appointmentId = selectedAppointment.appointmentId;

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

    selectedAppointment.notes = [
      ...selectedAppointment.notes,
      {
        message,
        time: new Date().toISOString(),
      },
    ];

    newNote = "";
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
            <div class="mb-4">
              <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">
                Donor
              </p>
              <p class="mt-2 text-2xl font-semibold text-slate-950">
                {data.nextAppointment.donorName}
              </p>
            </div>

            <div class="mb-4">
              <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">
                Time
              </p>
              <p class="mt-2 text-lg font-semibold text-slate-950">
                {formatDateTime(data.nextAppointment.time)}
              </p>
            </div>

            <div>
              <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">
                Blood type
              </p>
              <p class="mt-2 text-sm text-slate-700">
                {data.nextAppointment.donorBloodType ?? "Not registered"}
              </p>
            </div>
          </div>
        {:else}
          <div class="rounded-3xl bg-slate-50 p-5 text-sm text-slate-500">
            No upcoming appointments today.
          </div>
        {/if}
      </section>

      <section class="rounded-[28px] border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="text-2xl font-semibold text-slate-950">Quick access</h2>
        <p class="mt-1 text-sm text-slate-500">Go to the pages you use most.</p>

        <div class="mt-5 space-y-3">
          {#each quickLinks as link}
            <a
              href={link.href}
              class="flex items-center justify-between rounded-2xl border border-slate-200 px-4 py-4 text-slate-800 transition hover:bg-slate-50"
            >
              <span>{link.label}</span>
              <span class="text-slate-400">→</span>
            </a>
          {/each}
        </div>
      </section>
    </div>

    <div class="space-y-6 lg:col-span-8">
      <section class="rounded-[28px] border border-slate-200 bg-white p-6 shadow-sm">
        <div class="mb-5 flex items-start justify-between gap-4">
          <div>
            <h2 class="text-2xl font-semibold text-slate-950">
              Today’s appointments
            </h2>
            <p class="mt-1 text-sm text-slate-500">
              Live data from the backend for your blood bank.
            </p>
          </div>

          <span class="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-600">
            {data.appointments.length} items
          </span>
        </div>

        {#if data.appointments.length === 0}
          <div class="rounded-3xl bg-slate-50 p-5 text-sm text-slate-500">
            No appointments found.
          </div>
        {:else}
          <div class="space-y-4">
            {#each data.appointments as appointment}
              <div class="rounded-[24px] border border-slate-200 p-5 transition hover:bg-slate-50">
                <div class="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
                  <div class="grid gap-4 sm:grid-cols-2 xl:flex-1">
                    <div>
                      <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">
                        Donor
                      </p>
                      <p class="mt-2 text-xl font-semibold text-slate-950">
                        {appointment.donorName}
                      </p>
                    </div>

                    <div>
                      <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">
                        Time
                      </p>
                      <p class="mt-2 text-lg font-semibold text-slate-950">
                        {formatTime(appointment.time)}
                      </p>
                    </div>

                    <div>
                      <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">
                        Email
                      </p>
                      <p class="mt-2 text-sm text-slate-700">
                        {appointment.donorEmail}
                      </p>
                    </div>

                    <div>
                      <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">
                        Blood type
                      </p>
                      <p class="mt-2 text-sm text-slate-700">
                        {appointment.donorBloodType ?? "Not registered"}
                      </p>
                    </div>
                  </div>

                  <div class="flex min-w-[220px] flex-col items-start gap-3 xl:items-end">
                    <span
                      class={`rounded-full px-3 py-1.5 text-xs font-medium ${
                        appointment.donations.length > 0
                          ? "bg-slate-100 text-slate-700"
                          : "bg-emerald-50 text-emerald-700"
                      }`}
                    >
                      {appointment.donations.length > 0
                        ? "Donation recorded"
                        : "No donation recorded"}
                    </span>

                    <div class="flex flex-wrap gap-2 xl:justify-end">
                      <button
                        type="button"
                        class="rounded-2xl border border-slate-200 px-4 py-2 text-sm text-slate-800 transition hover:bg-slate-100"
                        on:click={() => {
                          selectedAppointment = appointment;
                          newNote = "";
                        }}
                      >
                        View
                      </button>

                      <a
                        href={`/admin/appointments?appointment=${appointment.appointmentId}`}
                        class="rounded-2xl bg-slate-950 px-4 py-2 text-sm text-white transition hover:opacity-90"
                      >
                        Register donation
                      </a>
                    </div>
                  </div>
                </div>

                {#if appointment.notes.length > 0}
                  <div class="mt-4 rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600">
                    <span class="font-medium text-slate-700">Latest note:</span>
                    {appointment.notes[appointment.notes.length - 1].message}
                  </div>
                {/if}
              </div>
            {/each}
          </div>
        {/if}
      </section>
    </div>
  </div>
</div>

{#if selectedAppointment}
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-6">
    <div class="flex max-h-[90vh] w-full max-w-3xl flex-col rounded-[28px] bg-white shadow-xl">

      <!-- HEADER -->
      <div class="flex items-start justify-between p-6 border-b">
        <div>
          <h2 class="text-3xl font-bold text-slate-950">
            Appointment details
          </h2>
          <p class="mt-1 text-sm text-slate-500">
            {selectedAppointment.donorName} · {formatDateTime(selectedAppointment.time)}
          </p>
        </div>

        <button
          type="button"
          class="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-700 hover:bg-slate-200"
          on:click={() => selectedAppointment = null}
        >
          Close
        </button>
      </div>

      <!-- SCROLLABLE CONTENT -->
      <div class="flex-1 overflow-y-auto p-6">

        <div class="grid gap-4 sm:grid-cols-2">
          <div class="rounded-2xl bg-slate-50 p-4">
            <p class="text-xs uppercase text-slate-400">Donor</p>
            <p class="mt-2 font-semibold">{selectedAppointment.donorName}</p>
          </div>

          <div class="rounded-2xl bg-slate-50 p-4">
            <p class="text-xs uppercase text-slate-400">Time</p>
            <p class="mt-2 font-semibold">
              {formatDateTime(selectedAppointment.time)}
            </p>
          </div>
        </div>

        <!-- NOTES -->
        <div class="mt-8">
          <h3 class="text-xl font-semibold text-slate-950">All notes</h3>

          {#if selectedAppointment.notes.length > 0}
            <div class="mt-4 space-y-3">
              {#each selectedAppointment.notes as note}
                <div class="rounded-2xl bg-slate-50 px-4 py-3 text-sm">
                  {note.message}
                </div>
              {/each}
            </div>
          {:else}
            <p class="mt-4 text-sm text-slate-500">No notes yet.</p>
          {/if}
        </div>
      </div>

      <!-- STICKY FOOTER -->
      <div class="border-t p-6">
        <textarea
          bind:value={newNote}
          rows="3"
          class="w-full rounded-2xl border border-slate-200 p-4 text-sm"
          placeholder="Write a note..."
        />

        <div class="mt-3 flex justify-end gap-2">
          <button
            type="button"
            class="rounded-2xl border px-4 py-2"
            on:click={() => selectedAppointment = null}
          >
            Cancel
          </button>

          <button
            type="button"
            disabled={savingNote}
            class="rounded-2xl bg-slate-950 px-5 py-2 text-sm text-white disabled:opacity-50"
            on:click={addNote}
          >
            {savingNote ? "Saving..." : "Save note"}
          </button>
        </div>
      </div>

    </div>
  </div>
{/if}