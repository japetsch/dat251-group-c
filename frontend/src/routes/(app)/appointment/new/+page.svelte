<style>
  .selected {
    background: #fff1f2;
    box-shadow:
      inset 0 0 0 2px rgba(239, 68, 68, 0.45),
      0 10px 30px rgba(239, 68, 68, 0.12);
  }
  .active-toggle {
    background: white;
    color: #0f172a;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
  }
</style>

<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

  type Slot = Record<string, unknown>;

  let selectedBloodbank = "all";
  let weekOffset = 0;
  let selectedSlotId: string | number | null = null;
  let viewMode: "week" | "month" = "week";

  const weekdayNames = [
    "Mandag",
    "Tirsdag",
    "Onsdag",
    "Torsdag",
    "Fredag",
    "Lørdag",
    "Søndag",
  ];

  const safeSlots = (data.availableAppointments ?? []) as Slot[];

  function getSlotId(slot: Slot) {
    return (slot.id ??
      slot.booking_slot_id ??
      slot.bookingslot_id ??
      slot.slot_id ??
      "") as string | number;
  }

  function getSlotTime(slot: Slot) {
    return (slot.time ??
      slot.start_time ??
      slot.start ??
      slot.datetime ??
      "") as string;
  }

  function getBloodbankName(slot: Slot) {
    return (slot.bloodbank_name ??
      slot.bloodbank ??
      slot.bloodbankName ??
      "Blodbank") as string;
  }

  function getBloodbankId(slot: Slot) {
    return (slot.bloodbank_id ?? slot.bloodbankId ?? getBloodbankName(slot)) as
      | string
      | number;
  }

  function formatDateLabel(value: string) {
    return new Date(value).toLocaleDateString("nb-NO", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  }

  function formatTime(value: string) {
    return new Date(value).toLocaleTimeString("nb-NO", {
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  function startOfWeek(date: Date) {
    const result = new Date(date);
    const day = result.getDay();
    const diff = day === 0 ? -6 : 1 - day;
    result.setDate(result.getDate() + diff);
    result.setHours(0, 0, 0, 0);
    return result;
  }

  $: now = new Date();
  $: currentWeekStart = startOfWeek(
    new Date(now.getFullYear(), now.getMonth(), now.getDate() + weekOffset * 7),
  );

  $: weekDays = Array.from({ length: 7 }, (_, index) => {
    const date = new Date(currentWeekStart);
    date.setDate(currentWeekStart.getDate() + index);
    return date;
  });

  $: bloodbanks = [
    ...new Set(safeSlots.map((slot) => getBloodbankName(slot)).filter(Boolean)),
  ];

  $: filteredSlots = safeSlots.filter((slot) => {
    if (selectedBloodbank === "all") return true;
    return getBloodbankName(slot) === selectedBloodbank;
  });

  $: slotsThisWeek = filteredSlots.filter((slot) => {
    const slotDate = new Date(getSlotTime(slot));
    const weekEnd = new Date(currentWeekStart);
    weekEnd.setDate(currentWeekStart.getDate() + 7);
    return slotDate >= currentWeekStart && slotDate < weekEnd;
  });

  $: groupedByDay = weekDays.map((day) => {
    const items = slotsThisWeek.filter((slot) => {
      const slotDate = new Date(getSlotTime(slot));
      return (
        slotDate.getFullYear() === day.getFullYear() &&
        slotDate.getMonth() === day.getMonth() &&
        slotDate.getDate() === day.getDate()
      );
    });

    return {
      day,
      items,
    };
  });

  function startOfMonthGrid(date: Date) {
    const first = new Date(date.getFullYear(), date.getMonth(), 1);
    const day = first.getDay();
    const diff = day === 0 ? -6 : 1 - day;
    first.setDate(first.getDate() + diff);
    first.setHours(0, 0, 0, 0);
    return first;
  }

  function endOfMonth(date: Date) {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0);
  }

  $: monthStart = new Date(now.getFullYear(), now.getMonth() + weekOffset, 1);
  $: monthGridStart = startOfMonthGrid(monthStart);
  $: monthEnd = endOfMonth(monthStart);

  $: monthDays = Array.from({ length: 42 }, (_, index) => {
    const date = new Date(monthGridStart);
    date.setDate(monthGridStart.getDate() + index);
    return date;
  });

  $: slotsThisMonth = filteredSlots.filter((slot) => {
    const slotDate = new Date(getSlotTime(slot));
    return (
      slotDate.getMonth() === monthStart.getMonth() &&
      slotDate.getFullYear() === monthStart.getFullYear()
    );
  });

  $: groupedMonthDays = monthDays.map((day) => {
    const items = filteredSlots.filter((slot) => {
      const slotDate = new Date(getSlotTime(slot));
      return (
        slotDate.getFullYear() === day.getFullYear() &&
        slotDate.getMonth() === day.getMonth() &&
        slotDate.getDate() === day.getDate()
      );
    });

    return {
      day,
      items,
      inCurrentMonth:
        day.getMonth() === monthStart.getMonth() &&
        day.getFullYear() === monthStart.getFullYear(),
    };
  });

  $: selectedSlot =
    safeSlots.find(
      (slot) => String(getSlotId(slot)) === String(selectedSlotId),
    ) ?? null;
</script>

<svelte:head>
  <title>Ny avtale</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-6 py-10 md:px-8">
  <div class="mb-8">
    <h1 class="text-4xl font-bold tracking-tight text-slate-900">
      Bestill ny time
    </h1>
    <p class="mt-2 max-w-2xl text-base text-slate-500">
      Finn et tidspunkt som passer deg og velg ønsket blodbank.
    </p>
  </div>

  {#if data.error}
    <div
      class="rounded-[28px] border border-red-200 bg-red-50 px-5 py-4 text-red-700 shadow-sm"
    >
      {data.error}
    </div>
  {:else}
    <div class="space-y-6">
      <section
        class="rounded-[32px] bg-white p-6 shadow-[0_16px_50px_rgba(15,23,42,0.06)] ring-1 ring-black/5 md:p-8"
      >
        <div
          class="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between"
        >
          <div class="max-w-xl">
            <h2 class="text-2xl font-semibold text-slate-900">
              Tilgjengelige timer
            </h2>
            <p class="mt-2 text-sm text-slate-500">
              Filtrer etter blodbank og bla mellom ukene for å se ledige
              tidspunkt.
            </p>
          </div>

          <div class="grid gap-4 sm:grid-cols-[minmax(220px,320px)_auto]">
            <div
              class="inline-flex rounded-full bg-[#f3eded] p-1 ring-1 ring-[#eadede]"
            >
              <button
                type="button"
                class:active-toggle={viewMode === "week"}
                class="rounded-full px-4 py-2 text-sm font-semibold text-slate-600 transition"
                on:click={() => (viewMode = "week")}
              >
                Ukeoversikt
              </button>

              <button
                type="button"
                class:active-toggle={viewMode === "month"}
                class="rounded-full px-4 py-2 text-sm font-semibold text-slate-600 transition"
                on:click={() => (viewMode = "month")}
              >
                Månedsoversikt
              </button>
            </div>

            <label class="block">
              <span class="mb-2 block text-sm font-medium text-slate-700"
                >Velg blodbank</span
              >
              <select
                bind:value={selectedBloodbank}
                class="w-full rounded-2xl border border-[#eadede] bg-[#fcfbfb] px-4 py-3 text-slate-900 outline-none transition focus:border-red-300 focus:ring-4 focus:ring-red-100"
              >
                <option value="all">Alle</option>
                {#each bloodbanks as bloodbank}
                  <option value={bloodbank}>{bloodbank}</option>
                {/each}
              </select>
            </label>

            <div class="flex items-end gap-3">
              <button
                type="button"
                class="rounded-full border border-[#eadede] bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-red-200 hover:bg-red-50 hover:text-red-600"
                on:click={() => (weekOffset -= 1)}
              >
                {viewMode === "week" ? "Forrige uke" : "Forrige måned"}
              </button>

              <button
                type="button"
                class="rounded-full border border-[#eadede] bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:border-red-200 hover:bg-red-50 hover:text-red-600"
                on:click={() => (weekOffset += 1)}
              >
                {viewMode === "week" ? "Neste uke" : "Neste måned"}
              </button>
            </div>
          </div>
        </div>
      </section>

      <section
        class="rounded-[32px] bg-white p-4 shadow-[0_16px_50px_rgba(15,23,42,0.06)] ring-1 ring-black/5 md:p-6"
      >
        <div class="mb-4 flex items-center justify-between px-2">
          <div>
            <p
              class="text-sm font-medium uppercase tracking-[0.18em] text-slate-400"
            >
              {viewMode === "week" ? "Ukeoversikt" : "Månedsoversikt"}
            </p>
            <p class="mt-1 text-lg font-semibold text-slate-900">
              {#if viewMode === "week"}
                {formatDateLabel(weekDays[0].toISOString())} – {formatDateLabel(
                  weekDays[6].toISOString(),
                )}
              {:else}
                {monthStart.toLocaleDateString("nb-NO", {
                  month: "long",
                  year: "numeric",
                })}
              {/if}
            </p>
          </div>

          <span
            class="rounded-full bg-red-50 px-3 py-1 text-sm font-medium text-red-600"
          >
            {viewMode === "week" ? slotsThisWeek.length : slotsThisMonth.length} ledige
            tider
          </span>
        </div>

        {#if viewMode === "week"}
          <div class="grid gap-4 lg:grid-cols-7">
            {#each groupedByDay as { day, items }, index}
              <div
                class="min-h-[280px] rounded-[28px] bg-[#fcfbfb] p-4 ring-1 ring-[#efe7e7]"
              >
                <div class="mb-4 border-b border-[#efe7e7] pb-3">
                  <p
                    class="text-sm font-medium uppercase tracking-[0.16em] text-slate-400"
                  >
                    {weekdayNames[index]}
                  </p>
                  <p class="mt-1 text-base font-semibold text-slate-900">
                    {formatDateLabel(day.toISOString())}
                  </p>
                </div>

                {#if items.length === 0}
                  <div
                    class="rounded-2xl bg-white px-4 py-5 text-sm text-slate-400 ring-1 ring-[#f2ebeb]"
                  >
                    Ingen ledige tider
                  </div>
                {:else}
                  <div class="space-y-3">
                    {#each items as slot}
                      <button
                        type="button"
                        class:selected={String(selectedSlotId) ===
                          String(getSlotId(slot))}
                        class="w-full rounded-[22px] bg-white p-4 text-left shadow-sm ring-1 ring-[#efe7e7] transition hover:-translate-y-0.5 hover:shadow-md hover:ring-red-200"
                        on:click={() => (selectedSlotId = getSlotId(slot))}
                      >
                        <div
                          class="text-2xl font-bold tracking-tight text-slate-900"
                        >
                          {formatTime(getSlotTime(slot))}
                        </div>
                        <div class="mt-2 text-sm leading-6 text-slate-500">
                          {getBloodbankName(slot)}
                        </div>
                      </button>
                    {/each}
                  </div>
                {/if}
              </div>
            {/each}
          </div>
        {:else}
          <div class="grid gap-4 lg:grid-cols-7">
            {#each groupedMonthDays as { day, items, inCurrentMonth }, index}
              <div
                class:opacity-50={!inCurrentMonth}
                class="min-h-[180px] rounded-[24px] bg-[#fcfbfb] p-4 ring-1 ring-[#efe7e7]"
              >
                <div class="mb-3 flex items-center justify-between">
                  <div>
                    <p
                      class="text-xs font-medium uppercase tracking-[0.16em] text-slate-400"
                    >
                      {weekdayNames[index % 7]}
                    </p>
                    <p class="mt-1 text-base font-semibold text-slate-900">
                      {day.getDate()}
                    </p>
                  </div>

                  {#if items.length > 0}
                    <span
                      class="rounded-full bg-red-50 px-2 py-1 text-xs font-medium text-red-600"
                    >
                      {items.length}
                    </span>
                  {/if}
                </div>

                {#if items.length > 0}
                  <div class="space-y-2">
                    {#each items.slice(0, 3) as slot}
                      <button
                        type="button"
                        class:selected={String(selectedSlotId) ===
                          String(getSlotId(slot))}
                        class="w-full rounded-xl bg-white p-3 text-left text-sm shadow-sm ring-1 ring-[#efe7e7] transition hover:shadow-md hover:ring-red-200"
                        on:click={() => (selectedSlotId = getSlotId(slot))}
                      >
                        <div class="font-semibold text-slate-900">
                          {formatTime(getSlotTime(slot))}
                        </div>
                        <div class="mt-1 truncate text-xs text-slate-500">
                          {getBloodbankName(slot)}
                        </div>
                      </button>
                    {/each}

                    {#if items.length > 3}
                      <div class="pt-1 text-xs font-medium text-slate-400">
                        + {items.length - 3} flere
                      </div>
                    {/if}
                  </div>
                {:else}
                  <div class="text-xs text-slate-300">Ingen tider</div>
                {/if}
              </div>
            {/each}
          </div>
        {/if}
      </section>

      <section
        class="rounded-[32px] bg-white p-6 shadow-[0_16px_50px_rgba(15,23,42,0.06)] ring-1 ring-black/5 md:p-8"
      >
        <div
          class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between"
        >
          <div>
            <h2 class="text-2xl font-semibold text-slate-900">Valgt time</h2>

            {#if selectedSlot}
              <div class="mt-3 space-y-1 text-slate-600">
                <p>
                  <span class="font-medium text-slate-900">Blodbank:</span>
                  {getBloodbankName(selectedSlot)}
                </p>
                <p>
                  <span class="font-medium text-slate-900">Tid:</span>
                  {formatDateLabel(getSlotTime(selectedSlot))} kl. {formatTime(
                    getSlotTime(selectedSlot),
                  )}
                </p>
              </div>
            {:else}
              <p class="mt-3 text-slate-500">
                Velg en tid i kalenderen over for å fortsette.
              </p>
            {/if}
          </div>

          {#if selectedSlot}
            <!-- If your current action name differs, change ?/book -->
            <form method="POST" action="?/book" class="shrink-0">
              <!-- If your current field name differs, change bookingSlotId -->
              <input
                type="hidden"
                name="bookingSlotId"
                value={String(getSlotId(selectedSlot))}
              />
              <button
                type="submit"
                class="inline-flex items-center rounded-full bg-red-500 px-6 py-3 text-sm font-semibold text-white transition hover:bg-red-600"
              >
                Bekreft time
              </button>
            </form>
          {:else}
            <button
              type="button"
              disabled
              class="inline-flex cursor-not-allowed items-center rounded-full bg-slate-200 px-6 py-3 text-sm font-semibold text-slate-500"
            >
              Velg en tid først
            </button>
          {/if}
        </div>
      </section>
    </div>
  {/if}
</div>
