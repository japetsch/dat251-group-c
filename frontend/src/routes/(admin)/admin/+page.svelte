<script lang="ts">
  import AdminAppointmentModal from "$lib/components/AdminAppointmentModal.svelte";
  import DonationModal from "$lib/components/DonationModal.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

  let selectedAppointment: PageData["appointments"][number] | null = null;
  let donationAppointment: PageData["appointments"][number] | null = null;

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

  function closeAppointmentModal() {
    selectedAppointment = null;
  }

  function closeDonationModal() {
    donationAppointment = null;
  }

  const quickLinks = [
    { label: "Dagens timer", href: "/admin/appointments" },
    { label: "Registrer donasjon", href: "/admin/appointments" },
    { label: "Registrer intervju", href: "/admin/appointments" },
    { label: "Registrer donasjonstest", href: "/admin/appointments" },
  ];
</script>

<svelte:head>
  <title>Admin Dashboard</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-6 py-10">
  <div class="mb-8">
    <h1 class="text-5xl font-bold tracking-tight text-slate-950">
      Administrasjonspanel
    </h1>
    <p class="mt-3 max-w-2xl text-base leading-7 text-slate-500">
      Få oversikt over dagens timer og naviger raskt mellom viktige
      administrasjonssider.
    </p>
  </div>

  <div class="grid gap-6 lg:grid-cols-12">
    <div class="space-y-6 lg:col-span-4">
      <section
        class="rounded-[28px] border border-slate-200 bg-white p-6 shadow-sm"
      >
        <div class="mb-4 flex items-start justify-between gap-4">
          <div>
            <h2 class="text-2xl font-semibold text-slate-950">Neste time</h2>
            <p class="mt-1 text-sm text-slate-500">
              {#if data.bloodbank}
                {data.bloodbank.name}
              {:else}
                No assigned blood bank
              {/if}
            </p>
          </div>

          <span
            class="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-600"
          >
            {data.stats.todayCount} i dag
          </span>
        </div>

        {#if data.nextAppointment}
          <div class="rounded-3xl bg-slate-50 p-5">
            <div class="mb-4">
              <p
                class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400"
              >
                Donor
              </p>
              <p class="mt-2 text-2xl font-semibold text-slate-950">
                {data.nextAppointment.donor_name}
              </p>
            </div>

            <div class="mb-4">
              <p
                class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400"
              >
                Tid
              </p>
              <p class="mt-2 text-lg font-semibold text-slate-950">
                {formatDateTime(data.nextAppointment.time)}
              </p>
            </div>

            <div>
              <p
                class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400"
              >
                Blodtype
              </p>
              <p class="mt-2 text-sm text-slate-700">
                {data.nextAppointment.donor_blood_type ?? "Ikke registrert"}
              </p>
            </div>
          </div>
        {:else}
          <div class="rounded-3xl bg-slate-50 p-5 text-sm text-slate-500">
            Ingen kommende timer i dag.
          </div>
        {/if}
      </section>

      <section
        class="rounded-[28px] border border-slate-200 bg-white p-6 shadow-sm"
      >
        <h2 class="text-2xl font-semibold text-slate-950">Hurtigtilgang</h2>
        <p class="mt-1 text-sm text-slate-500">Gå til sidene du bruker mest.</p>

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
      <section
        class="rounded-[28px] border border-slate-200 bg-white p-6 shadow-sm"
      >
        <div class="mb-5 flex items-start justify-between gap-4">
          <div>
            <h2 class="text-2xl font-semibold text-slate-950">Dagens timer</h2>
            <p class="mt-1 text-sm text-slate-500">
              Direktedata fra systemet for din blodbank.
            </p>
          </div>

          <span
            class="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-600"
          >
            {data.appointments.length}
          </span>
        </div>

        {#if data.appointments.length === 0}
          <div class="rounded-3xl bg-slate-50 p-5 text-sm text-slate-500">
            Ingen timer funnet.
          </div>
        {:else}
          <div class="space-y-4">
            {#each data.appointments as appointment}
              <div
                class="rounded-[24px] border border-slate-200 p-5 transition hover:bg-slate-50"
              >
                <div
                  class="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between"
                >
                  <div class="grid gap-4 sm:grid-cols-2 xl:flex-1">
                    <div>
                      <p
                        class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400"
                      >
                        Donor
                      </p>
                      <p class="mt-2 text-xl font-semibold text-slate-950">
                        {appointment.donor_name}
                      </p>
                    </div>

                    <div>
                      <p
                        class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400"
                      >
                        Tid
                      </p>
                      <p class="mt-2 text-lg font-semibold text-slate-950">
                        {formatTime(appointment.time)}
                      </p>
                    </div>

                    <div>
                      <p
                        class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400"
                      >
                        E-post
                      </p>
                      <p class="mt-2 text-sm text-slate-700">
                        {appointment.donor_email}
                      </p>
                    </div>

                    <div>
                      <p
                        class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400"
                      >
                        Blodtype
                      </p>
                      <p class="mt-2 text-sm text-slate-700">
                        {appointment.donor_blood_type ?? "Ikke registrert"}
                      </p>
                    </div>
                  </div>

                  <div
                    class="flex min-w-[220px] flex-col items-start gap-3 xl:items-end"
                  >
                    <span
                      class={`rounded-full px-3 py-1.5 text-xs font-medium ${
                        appointment.donations.length > 0
                          ? "bg-slate-100 text-slate-700"
                          : "bg-emerald-50 text-emerald-700"
                      }`}
                    >
                      {appointment.donations.length > 0
                        ? "Donasjon registrert"
                        : "Ingen donasjon registrert"}
                    </span>

                    <div class="flex flex-wrap gap-2 xl:justify-end">
                      <button
                        type="button"
                        class="rounded-2xl border border-slate-200 px-4 py-2 text-sm text-slate-800 transition hover:bg-slate-100"
                        on:click={() => {
                          selectedAppointment = appointment;
                          // newNote = "";
                        }}
                      >
                        Vis time
                      </button>

                      <button
                        type="button"
                        disabled={appointment.donations.length > 0}
                        class="rounded-2xl bg-slate-950 px-4 py-2 text-sm text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
                        on:click={() => {
                          donationAppointment = appointment;
                        }}
                      >
                        Registrer donasjon
                      </button>
                    </div>
                  </div>
                </div>

                {#if appointment.notes.length > 0}
                  <div
                    class="mt-4 rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600"
                  >
                    <span class="font-medium text-slate-700">Siste notat:</span>
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

<AdminAppointmentModal
  selectedAppointment={selectedAppointment}
  onClose={closeAppointmentModal}
  data={data}
/>

<DonationModal
  donationAppointment={donationAppointment}
  onClose={closeDonationModal}
  data={data}
/>
