<script lang="ts">
  type Appointment = {
    datetime: string;
    location: string;
  };

  let nextAppointment: Appointment | null = {
    datetime: "2026-03-18T17:30:00",
    location: "Haukeland universitetssjukehus",
  };

  let completedAppointments = 1;
  let yearlyGoal = 4;

  const formatDate = (value: string) =>
    new Date(value).toLocaleString("en-GB", {
      day: "numeric",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

  const progress =
    yearlyGoal > 0 ? Math.round((completedAppointments / yearlyGoal) * 100) : 0;

  const links = [
    { label: "Appointments", href: "/appointment/list" },
    { label: "My Blood", href: "/my-blood" },
    { label: "Settings", href: "/settings" },
    { label: "More Info", href: "/more-info" },
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
        Here you can get an overview of your next donation, navigate to
        important pages, and follow your progress this year.
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
              <h2 class="text-2xl font-bold text-[#061b49]">Up next</h2>
              <p class="mt-2 text-lg text-[#5d7598]">
                Your next scheduled donation.
              </p>
            </div>

            <span
              class="rounded-full bg-[#eef2f7] px-4 py-2 text-base font-medium text-[#48678e]"
            >
              {nextAppointment ? "1 appointment" : "0 appointments"}
            </span>
          </div>

          <div class="rounded-[1.5rem] bg-[#f2f5f9] px-6 py-5">
            {#if nextAppointment}
              <div class="space-y-2">
                <p class="text-sm uppercase tracking-[0.25em] text-[#94a8c4]">
                  Time
                </p>
                <p class="text-xl font-semibold text-[#061b49]">
                  {formatDate(nextAppointment.datetime)}
                </p>

                <p
                  class="pt-3 text-sm uppercase tracking-[0.25em] text-[#94a8c4]"
                >
                  Location
                </p>
                <p class="text-lg text-[#1d3557]">{nextAppointment.location}</p>
              </div>
            {:else}
              <p class="text-lg text-[#5d7598]">No upcoming appointments.</p>
            {/if}
          </div>
        </section>

        <!-- Navigation -->
        <section
          class="rounded-[2rem] border border-[#e6e7eb] bg-white p-8 shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
        >
          <div class="mb-6">
            <h2 class="text-2xl font-bold text-[#061b49]">Quick access</h2>
            <p class="mt-2 text-lg text-[#5d7598]">
              Go to the pages you use most.
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
              <h2 class="text-2xl font-bold text-[#061b49]">Progress</h2>
              <p class="mt-2 text-lg text-[#5d7598]">
                Donations you have completed this year.
              </p>
            </div>

            <span
              class="rounded-full bg-[#eef2f7] px-4 py-2 text-base font-medium text-[#48678e]"
            >
              {completedAppointments} of {yearlyGoal}
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
                  You’ve had {completedAppointments} out of {yearlyGoal} appointments
                </h3>
              </div>
            </div>

            <div class="mt-8">
              <div class="mb-3 flex items-center justify-between">
                <span class="text-base text-[#5d7598]">Yearly progress</span>
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
            <h2 class="text-2xl font-bold text-[#061b49]">Donation overview</h2>
            <p class="mt-2 text-lg text-[#5d7598]">
              A simple summary of where you are right now.
            </p>
          </div>

          <div class="grid gap-4 md:grid-cols-2">
            <div class="rounded-[1.5rem] bg-[#f2f5f9] p-6">
              <p class="text-sm uppercase tracking-[0.25em] text-[#94a8c4]">
                Completed
              </p>
              <p class="mt-3 text-3xl font-bold text-[#061b49]">
                {completedAppointments}
              </p>
            </div>

            <div class="rounded-[1.5rem] bg-[#f2f5f9] p-6">
              <p class="text-sm uppercase tracking-[0.25em] text-[#94a8c4]">
                Remaining
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
