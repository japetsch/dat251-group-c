<script lang="ts">
  import type {
    AdminCalendarAppointment,
    DonationType,
    NoteType,
  } from "$lib/types/admin";

  export let donationAppointment: AdminCalendarAppointment | null;
  export let onClose: () => void;
  export let data: any;

  let amountMl = 450;
  let isBloodNotPlasma = true;
  let savingDonation = false;

  async function registerDonation() {
    if (!donationAppointment) return;

    savingDonation = true;

    const res = await fetch(
      `/api/admin/appointment/${donationAppointment.appointment_id}/donation`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          amount_ml: amountMl,
          is_blood_not_plasma: isBloodNotPlasma,
        }),
      },
    );

    savingDonation = false;

    if (!res.ok) {
      alert("Kunne ikke registrere donasjon");
      return;
    }

    const savedDonation = {
      amountMl,
      isBloodNotPlasma,
    } as any;

    data.appointments = data.appointments.map(
      (appointment: AdminCalendarAppointment) =>
        appointment.appointment_id === donationAppointment?.appointment_id
          ? {
              ...appointment,
              donations: [...appointment.donations, savedDonation],
            }
          : appointment,
    );

    donationAppointment = null;
    amountMl = 450;
    isBloodNotPlasma = true;
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
    amountMl = 450;
    isBloodNotPlasma = true;
  }
</script>

{#if donationAppointment}
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-6"
  >
    <div
      class="flex w-full max-w-xl flex-col rounded-[28px] bg-white shadow-xl"
    >
      <div class="flex items-start justify-between border-b p-6">
        <div>
          <h2 class="text-3xl font-bold text-slate-950">Registrer donasjon</h2>
          <p class="mt-1 text-sm text-slate-500">
            {donationAppointment.donor_name} · {formatDateTime(
              donationAppointment.time,
            )}
          </p>
        </div>

        <button
          type="button"
          class="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-700 hover:bg-slate-200"
          on:click={() => (donationAppointment = null)}
        >
          Lukk
        </button>
      </div>

      <div class="p-6">
        <label class="text-sm font-medium text-slate-700" for="amount">
          Donert mengde (ml)
        </label>
        <input
          id="amount"
          type="number"
          min="1"
          bind:value={amountMl}
          class="mt-2 w-full rounded-2xl border border-slate-200 p-4 text-sm outline-none focus:border-slate-400"
        />

        <div class="mt-5 rounded-2xl bg-slate-50 p-4">
          <p class="text-sm font-medium text-slate-700">Donasjonstype</p>

          <label class="mt-3 flex items-center gap-2 text-sm text-slate-700">
            <input type="radio" bind:group={isBloodNotPlasma} value={true} />
            Blod
          </label>

          <label class="mt-2 flex items-center gap-2 text-sm text-slate-700">
            <input type="radio" bind:group={isBloodNotPlasma} value={false} />
            Plasma
          </label>
        </div>
      </div>

      <div class="flex justify-end gap-2 border-t p-6">
        <button
          type="button"
          class="rounded-2xl border px-4 py-2"
          on:click={() => (donationAppointment = null)}
        >
          Avbryt
        </button>

        <button
          type="button"
          disabled={savingDonation}
          class="rounded-2xl bg-slate-950 px-5 py-2 text-sm text-white disabled:opacity-50"
          on:click={registerDonation}
        >
          {savingDonation ? "Lagrer..." : "Lagre donasjon"}
        </button>
      </div>
    </div>
  </div>
{/if}
