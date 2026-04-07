<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

  const formatDate = (value: string) =>
    new Date(value).toLocaleString("nb-NO", {
      day: "numeric",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
</script>

<svelte:head>
  <title>Mine avtaler</title>
  <!-- <h1 class="text-3xl mb-4">My appointments</h1>-->
</svelte:head>

<div class="mb-8">
  <h1 class="text-4xl font-bold tracking-tight text-slate-900">Mine avtaler</h1>
  <p class="mt-2 max-w-2xl text-base text-slate-500">
    Her ser du kommende og tidligere avtaler. Hold oversikten og planlegg neste
    donasjon.
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
    <h2 class="text-2xl font-semibold text-slate-900">Ingen avtaler ennå</h2>
    <p class="mt-2 text-slate-500">
      Du har ingen registrerte avtaler akkurat nå.
    </p>

    <a
      href="/appointment/new"
      class="mt-6 inline-flex items-center rounded-full bg-red-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-red-600"
    >
      Bestill ny time
    </a>
  </div>
{:else}
  <div class="space-y-8">
    <section
      class="rounded-[32px] bg-white p-6 shadow-[0_16px_50px_rgba(15,23,42,0.06)] ring-1 ring-black/5 md:p-8"
    >
      <div class="mb-6 flex items-center justify-between gap-4">
        <div>
          <h2 class="text-2xl font-semibold text-slate-900">Kommende</h2>
          <p class="mt-1 text-sm text-slate-500">
            Dine neste planlagte donasjoner.
          </p>
        </div>

        <span
          class="rounded-full bg-red-50 px-3 py-1 text-sm font-medium text-red-600"
        >
          {data.upcoming.length}
          {data.upcoming.length === 1 ? "avtale" : "avtaler"}
        </span>
      </div>

      {#if data.upcoming.length === 0}
        <div class="rounded-2xl bg-slate-50 px-5 py-4 text-slate-500">
          Ingen kommende avtaler.
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
                    Kommende
                  </span>
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
          <h2 class="text-2xl font-semibold text-slate-900">Tidligere</h2>
          <p class="mt-1 text-sm text-slate-500">
            Donasjoner du allerede har gjennomført.
          </p>
        </div>

        <span
          class="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-600"
        >
          {data.previous.length}
          {data.previous.length === 1 ? "avtale" : "avtaler"}
        </span>
      </div>

      {#if data.previous.length === 0}
        <div class="rounded-2xl bg-slate-50 px-5 py-4 text-slate-500">
          Ingen tidligere avtaler.
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
                    class="mt-3 inline-flex rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-600"
                  >
                    Fullført
                  </span>
                </div>
              </div>
            </article>
          {/each}
        </div>
      {/if}
    </section>
  </div>
{/if}
