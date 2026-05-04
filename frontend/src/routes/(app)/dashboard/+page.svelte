<script lang="ts">
  import type { PageData } from "./$types";

  let { data }: { data: PageData } = $props();

  const nextAppointment = data.upcoming[0] ?? null;
  const completedAppointments = data.completed;
  const yearlyGoal = 4;

  const formatDate = (value: string) =>
    new Date(value).toLocaleString("nb-NO", {
      day: "numeric",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

  const progress =
    yearlyGoal > 0 ? Math.round((completedAppointments / yearlyGoal) * 100) : 0;

  const links = [
    { label: "Mine timer", href: "/appointment/list" },
    { label: "Ny time", href: "/appointment/new" },
  ];
</script>

<svelte:head>
  <title>Dashboard</title>
</svelte:head>

<div class="min-h-screen bg-[#f7f7f8] px-6 py-10 md:px-10 lg:px-14">
  <div class="mx-auto max-w-[1600px]">
    <!-- Header -->
    <div class="mb-10">
      <h1 class="text-4xl font-bold tracking-tight text-[#061b49] md:text-5xl">
        Dashboard
      </h1>
      <p class="mt-3 max-w-3xl text-lg leading-relaxed text-[#5d7598]">
        Her kan du få oversikt over din neste donasjon, navigere til viktige
        sider og følge fremgangen din i år.
      </p>
    </div>

    <div class="grid gap-8 xl:grid-cols-[420px_minmax(0,1fr)]">
      <!-- Left column -->
      <div class="space-y-8">
        <!-- Up next -->
        <section
          class="rounded-[2rem] border border-[#e6e7eb] bg-white p-8 shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
        >
          <div class="mb-6 flex items-start justify-between gap-4">
            <div>
              <h2 class="text-2xl font-bold text-[#061b49]">Neste time</h2>
              <p class="mt-2 text-lg text-[#5d7598]">
                Din neste planlagte donasjon.
              </p>
            </div>

            <span
              class="rounded-full bg-[#eef2f7] px-4 py-2 text-base font-medium text-[#48678e]"
            >
              {nextAppointment ? "1 time" : "0 timer"}
            </span>
          </div>

          <div class="rounded-[1.5rem] bg-[#f2f5f9] px-6 py-5">
            {#if nextAppointment}
              <div class="space-y-2">
                <p class="text-sm uppercase tracking-[0.25em] text-[#94a8c4]">
                  Tid
                </p>
                <p class="text-xl font-semibold text-[#061b49]">
                  {formatDate(nextAppointment.time)}
                </p>

                <p
                  class="pt-3 text-sm uppercase tracking-[0.25em] text-[#94a8c4]"
                >
                  Sted
                </p>
                <p class="text-lg text-[#1d3557]">
                  {nextAppointment.bloodbank_name}
                </p>
              </div>
            {:else}
              <p class="text-lg text-[#5d7598]">Ingen kommende timer.</p>
            {/if}
          </div>
        </section>

        <!-- Navigation -->
        <section
          class="rounded-[2rem] border border-[#e6e7eb] bg-white p-8 shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
        >
          <div class="mb-6">
            <h2 class="text-2xl font-bold text-[#061b49]">Hurtigvalg</h2>
            <p class="mt-2 text-lg text-[#5d7598]">
              Gå til de sidene du bruker mest.
            </p>
          </div>

          <div class="space-y-4">
            {#each links as link}
              <a
                href={link.href}
                class="flex items-center justify-between rounded-[1.3rem] border border-[#e8eaef] bg-[#fafbfc] px-5 py-4 text-lg font-medium text-[#12305f] transition hover:bg-[#f2f5f9] hover:border-[#d9e1ec]"
              >
                <span>{link.label}</span>
                <span class="text-[#8ba0bd]">→</span>
              </a>
            {/each}
          </div>
        </section>
      </div>

      <!-- Right column -->
      <div class="space-y-8">
        <!-- Progress -->
        <section
          class="rounded-[2rem] border border-[#e6e7eb] bg-white p-8 shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
        >
          <div class="mb-6 flex items-start justify-between gap-4">
            <div>
              <h2 class="text-2xl font-bold text-[#061b49]">Fremgang</h2>
              <p class="mt-2 text-lg text-[#5d7598]">
                Donasjoner du har fullført dette året.
              </p>
            </div>

            <span
              class="rounded-full bg-[#eef2f7] px-4 py-2 text-base font-medium text-[#48678e]"
            >
              {completedAppointments} av {yearlyGoal}
            </span>
          </div>

          <div
            class="rounded-[1.5rem] border border-[#ece7e7] bg-[#fcfbfb] p-6"
          >
            <div class="mb-5 flex items-start justify-between gap-4">
              <div>
                <p class="text-sm uppercase tracking-[0.25em] text-[#94a8c4]">
                  Status
                </p>
                <h3 class="mt-2 text-3xl font-bold text-[#061b49]">
                  Du har hatt {completedAppointments} av {yearlyGoal} timer i år.
                </h3>
              </div>
            </div>

            <div class="mt-8">
              <div class="mb-3 flex items-center justify-between">
                <span class="text-base text-[#5d7598]">Årslig fremgang</span>
                <span class="text-base font-medium text-[#12305f]"
                  >{progress}%</span
                >
              </div>

              <div class="h-5 w-full overflow-hidden rounded-full bg-[#edf2f7]">
                <div
                  class="h-full rounded-full bg-[#061b49] transition-all duration-500"
                  style={`width: ${progress}%`}
                ></div>
              </div>
            </div>
          </div>
        </section>

        <!-- Extra info card -->
        <section
          class="rounded-[2rem] border border-[#e6e7eb] bg-white p-8 shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
        >
          <div class="mb-6">
            <h2 class="text-2xl font-bold text-[#061b49]">Donasjonsoversikt</h2>
            <p class="mt-2 text-lg text-[#5d7598]">
              En enkel oversikt over hvor du er nå.
            </p>
          </div>

          <div class="grid gap-4 md:grid-cols-2">
            <div class="rounded-[1.5rem] bg-[#f2f5f9] p-6">
              <p class="text-sm uppercase tracking-[0.25em] text-[#94a8c4]">
                Fullført
              </p>
              <p class="mt-3 text-3xl font-bold text-[#061b49]">
                {completedAppointments}
              </p>
            </div>

            <div class="rounded-[1.5rem] bg-[#f2f5f9] p-6">
              <p class="text-sm uppercase tracking-[0.25em] text-[#94a8c4]">
                Gjenstående
              </p>
              <p class="mt-3 text-3xl font-bold text-[#061b49]">
                {Math.max(yearlyGoal - completedAppointments, 0)}
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</div>
