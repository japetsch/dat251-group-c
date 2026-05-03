<script lang="ts">
  import type { PageData } from "./$types";
  import NotesModal from "$lib/components/NotesModal.svelte";

  export let data: PageData;

  
  let notesOpen = false;
  let selectedAppointment: any = null;

let newNote = "";
let savingNote = false;

async function addNote() {
  if (!selectedAppointment) return;

  const message = newNote.trim();
  if (!message) return;

  savingNote = true;

  const res = await fetch(
    `/api/appointment/${selectedAppointment.id}/note`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    }
  );

  savingNote = false;

  if (!res.ok) {
    alert("Failed to save note");
    return;
  }

  selectedAppointment.notes = [
    ...(selectedAppointment.notes || []),
    { message },
  ];

  newNote = "";
}

  const formatDate = (value: string) =>
    new Date(value).toLocaleString("en-DK", {
      day: "numeric",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

  function openNotes(appointment: any) {
    selectedAppointment = appointment;
    notesOpen = true;
  }
</script>

<svelte:head>
  <title>My appointments</title>
</svelte:head>

<div class="mb-8">
  <h1 class="text-4xl font-bold tracking-tight text-slate-900">
    My appointments
  </h1>
  <p class="mt-2 max-w-2xl text-base text-slate-500">
    Here you can see upcoming and past appointments. Stay organized and plan
    your next donation.
  </p>
</div>

{#if data.error}
  <div
    class="rounded-[28px] border border-red-200 bg-red-50 px-5 py-4 text-red-700 shadow-sm"
  >
    {data.error}
  </div>
{:else if data.upcoming.length === 0 && data.previous.length === 0}
  <div
    class="rounded-[32px] bg-white p-8 shadow-[0_16px_50px_rgba(15,23,42,0.06)] ring-1 ring-black/5"
  >
    <h2 class="text-2xl font-semibold text-slate-900">No appointments yet</h2>
    <p class="mt-2 text-slate-500">
      You have no registered appointments at the moment.
    </p>

    <a
      href="/appointment/new"
      class="mt-6 inline-flex items-center rounded-full bg-red-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-red-600"
    >
      Book new appointment
    </a>
  </div>
{:else}
  <div class="space-y-8">
    <section
      class="rounded-[32px] bg-white p-6 shadow-[0_16px_50px_rgba(15,23,42,0.06)] ring-1 ring-black/5 md:p-8"
    >
      <div class="mb-6 flex items-center justify-between gap-4">
        <div>
          <h2 class="text-2xl font-semibold text-slate-900">Upcoming</h2>
          <p class="mt-1 text-sm text-slate-500">
            Your upcoming scheduled donations.
          </p>
        </div>

        <span
          class="rounded-full bg-red-50 px-3 py-1 text-sm font-medium text-red-600"
        >
          {data.upcoming.length}
          {data.upcoming.length === 1 ? "appointment" : "appointments"}
        </span>
      </div>

      {#if data.upcoming.length === 0}
        <div class="rounded-2xl bg-slate-50 px-5 py-4 text-slate-500">
          No upcoming appointments.
        </div>
      {:else}
        <div class="space-y-4">
          {#each data.upcoming as appointment}
            <article
              class="rounded-[24px] bg-[#fcfbfb] p-5 shadow-sm ring-1 ring-[#efe7e7] transition hover:-translate-y-0.5 hover:shadow-md"
            >
              <div
                class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between"
              >
                <div class="space-y-3">
                  <div>
                    <p
                      class="text-sm font-medium uppercase tracking-[0.18em] text-slate-400"
                    >
                      Donor
                    </p>
                    <p class="mt-1 text-lg font-semibold text-slate-900">
                      {appointment.username}
                    </p>
                  </div>

                  <div>
                    <p
                      class="text-sm font-medium uppercase tracking-[0.18em] text-slate-400"
                    >
                      Sted
                    </p>
                    <p class="mt-1 text-base text-slate-700">
                      {appointment.bloodbank_name}
                    </p>
                  </div>
                </div>

                <div class="md:text-right">
                  <p
                    class="text-sm font-medium uppercase tracking-[0.18em] text-slate-400"
                  >
                    Tid
                  </p>
                  <p class="mt-1 text-base font-semibold text-slate-900">
                    {formatDate(appointment.time)}
                  </p>

                  <span
                    class="mt-3 inline-flex rounded-full bg-red-50 px-3 py-1 text-sm font-medium text-red-600"
                  >
                    Upcoming
                  </span>

                  <button
                    class="mt-3 block rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-600 transition hover:bg-slate-200 md:ml-auto"
                    on:click={() => openNotes(appointment)}
                  >
                    Notes ({appointment.notes?.length ?? 0})
                  </button>
                </div>
              </div>
            </article>
          {/each}
        </div>
      {/if}
    </section>

    <section
      class="rounded-[32px] bg-white p-6 shadow-[0_16px_50px_rgba(15,23,42,0.06)] ring-1 ring-black/5 md:p-8"
    >
      <div class="mb-6 flex items-center justify-between gap-4">
        <div>
          <h2 class="text-2xl font-semibold text-slate-900">Previous</h2>
          <p class="mt-1 text-sm text-slate-500">
            Donations you have already completed.
          </p>
        </div>

        <span
          class="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-600"
        >
          {data.previous.length}
          {data.previous.length === 1 ? "appointment" : "appointments"}
        </span>
      </div>

      {#if data.previous.length === 0}
        <div class="rounded-2xl bg-slate-50 px-5 py-4 text-slate-500">
          No previous appointments.
        </div>
      {:else}
        <div class="space-y-4">
          {#each data.previous as appointment}
            <article
              class="rounded-[24px] bg-[#fcfbfb] p-5 shadow-sm ring-1 ring-[#efe7e7] transition hover:-translate-y-0.5 hover:shadow-md"
            >
              <div
                class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between"
              >
                <div class="space-y-3">
                  <div>
                    <p
                      class="text-sm font-medium uppercase tracking-[0.18em] text-slate-400"
                    >
                      Donor
                    </p>
                    <p class="mt-1 text-lg font-semibold text-slate-900">
                      {appointment.username}
                    </p>
                  </div>

                  <div>
                    <p
                      class="text-sm font-medium uppercase tracking-[0.18em] text-slate-400"
                    >
                      Location
                    </p>
                    <p class="mt-1 text-base text-slate-700">
                      {appointment.bloodbank_name}
                    </p>
                  </div>
                </div>

                <div class="md:text-right">
                  <p
                    class="text-sm font-medium uppercase tracking-[0.18em] text-slate-400"
                  >
                    Time
                  </p>
                  <p class="mt-1 text-base font-semibold text-slate-900">
                    {formatDate(appointment.time)}
                  </p>

                  <span
                    class="mt-3 inline-flex rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-600"
                  >
                    Completed
                  </span>

                  <button
                    class="mt-3 block rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-600 transition hover:bg-slate-200 md:ml-auto"
                    on:click={() => openNotes(appointment)}
                  >
                    Notes ({appointment.notes?.length ?? 0})
                  </button>
                </div>
              </div>
            </article>
          {/each}
        </div>
      {/if}
    </section>
  </div>
{/if}

{#if selectedAppointment}
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-6">
    <div class="flex max-h-[90vh] w-full max-w-3xl flex-col rounded-[28px] bg-white shadow-xl">

      <!-- HEADER -->
      <div class="flex items-start justify-between border-b p-6">
        <div>
          <h2 class="text-3xl font-bold text-slate-950">
            Appointment details
          </h2>
          <p class="mt-1 text-sm text-slate-500">
            {selectedAppointment.username} · {formatDate(selectedAppointment.time)}
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
            <p class="mt-2 font-semibold">{selectedAppointment.username}</p>
          </div>

          <div class="rounded-2xl bg-slate-50 p-4">
            <p class="text-xs uppercase text-slate-400">Time</p>
            <p class="mt-2 font-semibold">
              {formatDate(selectedAppointment.time)}
            </p>
          </div>

          <div class="rounded-2xl bg-slate-50 p-4 sm:col-span-2">
            <p class="text-xs uppercase text-slate-400">Location</p>
            <p class="mt-2 font-semibold">
              {selectedAppointment.bloodbank_name}
            </p>
          </div>
        </div>

        <!-- NOTES -->
        <div class="mt-8">
          <h3 class="text-xl font-semibold text-slate-950">All notes</h3>

          {#if selectedAppointment.notes?.length > 0}
            <div class="mt-4 space-y-3">
              {#each [...selectedAppointment.notes].sort((a, b) => new Date(b.time).getTime() - new Date(a.time).getTime()) as note}
                <div class="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
                  <div class="mb-2 flex justify-between gap-4">
                    <strong>{note.author_name}</strong>
                    <span class="whitespace-nowrap text-xs text-slate-400">
                      {formatDate(note.time)}
                    </span>
                  </div>

                  <p>{note.message}</p>
                </div>
              {/each}
            </div>
          {:else}
            <p class="mt-4 text-sm text-slate-500">No notes yet.</p>
          {/if}
        </div>
      </div>

      <!-- FOOTER (ADD NOTE) -->
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
            class="rounded-2xl bg-red-500 px-5 py-2 text-sm text-white disabled:opacity-50"
            on:click={addNote}
          >
            {savingNote ? "Saving..." : "Save note"}
          </button>
        </div>
      </div>

    </div>
  </div>
{/if}