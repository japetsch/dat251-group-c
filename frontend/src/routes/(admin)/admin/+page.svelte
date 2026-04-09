<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

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
    <h1 class="text-5xl font-bold tracking-tight text-slate-950">Admin Dashboard</h1>
    <p class="mt-3 max-w-2xl text-base leading-7 text-slate-500">
      Get an overview of today’s appointments and move quickly between important admin pages.
    </p>
  </div>

  <div class="grid gap-6 lg:grid-cols-12">
    <!-- LEFT COLUMN -->
    <div class="space-y-6 lg:col-span-4">
      <!-- Up next -->
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
              <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">Donor</p>
              <p class="mt-2 text-2xl font-semibold text-slate-950">
                {data.nextAppointment.donorName}
              </p>
            </div>

            <div class="mb-4">
              <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">Time</p>
              <p class="mt-2 text-lg font-semibold text-slate-950">
                {formatDateTime(data.nextAppointment.time)}
              </p>
            </div>

            <div>
              <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">Blood type</p>
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

      <!-- Quick access -->
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

    <!-- RIGHT COLUMN -->
    <div class="space-y-6 lg:col-span-8">
      <!-- Today’s appointments -->
      <section class="rounded-[28px] border border-slate-200 bg-white p-6 shadow-sm">
        <div class="mb-5 flex items-start justify-between gap-4">
          <div>
            <h2 class="text-2xl font-semibold text-slate-950">Today’s appointments</h2>
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
                      <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">Donor</p>
                      <p class="mt-2 text-xl font-semibold text-slate-950">{appointment.donorName}</p>
                    </div>

                    <div>
                      <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">Time</p>
                      <p class="mt-2 text-lg font-semibold text-slate-950">
                        {formatTime(appointment.time)}
                      </p>
                    </div>

                    <div>
                      <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">Email</p>
                      <p class="mt-2 text-sm text-slate-700">{appointment.donorEmail}</p>
                    </div>

                    <div>
                      <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">Blood type</p>
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
                      <a
                        href="/admin/appointments"
                        class="rounded-2xl border border-slate-200 px-4 py-2 text-sm text-slate-700 transition hover:bg-slate-100"
                      >
                        View
                      </a>

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