<style>
  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.35);
    border: none;
    padding: 0;
    cursor: default;
  }

  .modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    min-width: 60%;
    z-index: 10;
  }

  .modal-buttons {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }

  .modal-buttons button {
    padding: 0.75rem 1rem;
    border: 1px solid #999;
    border-radius: 10px;
    background: white;
    cursor: pointer;
  }

  .modal-card {
    min-height: 100px;
    width: 100%;
    background: white;
    border-radius: 24px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    padding: 1rem;
    margin-bottom: 1rem;
  }
  h2,
  h3 {
    all: revert;
  }
</style>

<script lang="ts">
  import type {
    AdminCalendarAppointment,
    DonationType,
    NoteType,
  } from "$lib/types/admin";
  import type { DonorCalendarAppointment } from "$lib/types/appointment";

  export let selectedAppointment:
    | AdminCalendarAppointment
    | DonorCalendarAppointment
    | null;
  export let onClose: () => void;
  export let data: any;

  let appointmentNotes: NoteType[];
  let appointmentDonations: DonationType[];

  let newNote = "";
  let savingNote = false;

  async function addNote() {
    if (!selectedAppointment) return;

    const message = newNote.trim();

    if (!message) {
      alert("Skriv et notat først");
      return;
    }

    savingNote = true;

    const res = await fetch(
      "appointment_id" in selectedAppointment
        ? `/api/admin/appointment/${selectedAppointment.appointment_id}/note`
        : `/api/appointment/${selectedAppointment.id}/note`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      },
    );

    savingNote = false;

    if (!res.ok) {
      alert("Kunne ikke lagre notat");
      return;
    }

    selectedAppointment.notes = [
      ...selectedAppointment.notes,
      {
        author_user_id: 0, // or some value
        author_name: "You",
        message,
        time: new Date().toISOString(),
      },
    ];
    newNote = "";
  }

  const formatDateTime = (value: string) =>
    new Date(value).toLocaleString("en-GB", {
      day: "numeric",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

  $: {
    appointmentNotes = [];
    appointmentDonations = [];

    if (selectedAppointment) {
      appointmentNotes = selectedAppointment.notes;
      if ("donations" in selectedAppointment) {
        appointmentDonations = selectedAppointment.donations;
      }
    }
  }
</script>

{#if selectedAppointment}
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-6"
  >
    <div
      class="flex max-h-[90vh] w-full max-w-3xl flex-col rounded-[28px] bg-white shadow-xl"
    >
      <div class="flex items-start justify-between border-b p-6">
        <div>
          <h2 class="text-3xl font-bold text-slate-950">Timedetaljer</h2>
          <p class="mt-1 text-sm text-slate-500">
            {"donor_name" in selectedAppointment
              ? selectedAppointment.donor_name
              : selectedAppointment.username} · {formatDateTime(
              selectedAppointment.time,
            )}
          </p>
        </div>

        <button
          type="button"
          class="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-700 hover:bg-slate-200"
          on:click={() => (selectedAppointment = null)}
        >
          Lukk
        </button>
      </div>

      <div class="flex-1 overflow-y-auto p-6">
        <div class="grid gap-4 sm:grid-cols-2">
          <div class="rounded-2xl bg-slate-50 p-4">
            <p class="text-xs uppercase text-slate-400">Donor</p>
            <p class="mt-2 font-semibold">
              {"donor_name" in selectedAppointment
                ? selectedAppointment.donor_name
                : selectedAppointment.username}
            </p>
          </div>

          <div class="rounded-2xl bg-slate-50 p-4">
            <p class="text-xs uppercase text-slate-400">Tid</p>
            <p class="mt-2 font-semibold">
              {formatDateTime(selectedAppointment.time)}
            </p>
          </div>
        </div>

        {#if appointmentDonations !== undefined && appointmentDonations.length !== 0}
          {#each appointmentDonations as donation}
            <div class="rounded-2xl bg-slate-50 p-4 mt-4">
              <p class="text-xs uppercase text-slate-400">Donasjon</p>
              <p class="mt-2 font-semibold">
                <strong>Donert mengde (ml):</strong>
                {donation.amount_ml}ml
              </p>
              <p class="mt-2 font-semibold">
                <strong>Er blod (ikke plasma):</strong>
                {donation.is_blood_not_plasma}
              </p>
            </div>
          {/each}
        {/if}

        <div class="mt-8">
          <h3 class="text-xl font-semibold text-slate-950">Alle notater</h3>

          {#if selectedAppointment.notes.length > 0}
            <div class="mt-4 space-y-3">
              {#each [...selectedAppointment.notes].sort((a, b) => new Date(b.time).getTime() - new Date(a.time).getTime()) as note}
                <div
                  class="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700"
                >
                  <div class="mb-2 flex justify-between gap-4">
                    <strong>{note.author_name}</strong>
                    <span class="whitespace-nowrap text-xs text-slate-400">
                      {formatDateTime(note.time)}
                    </span>
                  </div>

                  <p>{note.message}</p>
                </div>
              {/each}
            </div>
          {:else}
            <p class="mt-4 text-sm text-slate-500">Ingen notater ennå.</p>
          {/if}
        </div>
      </div>

      <div class="border-t p-6">
        <textarea
          bind:value={newNote}
          rows="3"
          class="w-full rounded-2xl border border-slate-200 p-4 text-sm"
          placeholder="Legg til notat..."
        ></textarea>

        <div class="mt-3 flex justify-end gap-2">
          <button
            type="button"
            class="rounded-2xl border px-4 py-2"
            on:click={() => (selectedAppointment = null)}
          >
            Avbryt
          </button>

          <button
            type="button"
            disabled={savingNote}
            class="rounded-2xl bg-slate-950 px-5 py-2 text-sm text-white disabled:opacity-50"
            on:click={addNote}
          >
            {savingNote ? "Lagrer..." : "Lagre notat"}
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}
