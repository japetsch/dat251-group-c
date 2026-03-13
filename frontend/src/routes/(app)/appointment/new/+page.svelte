<style>
  .layout {
    display: flex;
    align-items: stretch;
    min-height: 100vh;
  }

  .content {
    flex: 1;
  }

  .page {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    background: #f5f5f5;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 2rem;
    margin-bottom: 1.5rem;
  }

  .filter {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    min-width: 250px;
  }

  .filter label {
    font-weight: 600;
  }

  .filter select {
    padding: 0.8rem 3rem 0.8rem 1rem;
    border: 1px solid #bbb;
    border-radius: 10px;
    background: white;
    font-size: 1rem;
  }

  @media (max-width: 900px) {
    .layout {
      flex-direction: column;
    }

    .home-button {
      margin-top: 0;
    }

    .header {
      flex-direction: column;
    }

    .page {
      padding: 2rem;
    }
  }
</style>

<script lang="ts">
  import {
    addDays,
    formatDateKey,
    getStartOfWeek,
    getWeekNumber,
  } from "$lib/utils/date";
  import BookingModal from "$lib/components/BookingModal.svelte";
  import WeekPlanner from "$lib/components/WeekPlanner.svelte";
  import type {
    Appointment,
    AppointmentWithFormattedTime,
    PlannerColumn,
  } from "$lib/types/appointment";
  import type { PageData } from "./$types";

  export let data: PageData;

  // Filters and page state
  let selectedBloodbank = "All";
  let currentWeekStart: Date;
  let sidebarOpen = true;
  let filteredAppointments: Appointment[] = [];

  // Booking modal state
  let selectedAppointment: AppointmentWithFormattedTime | null = null;
  let isBooking = false;
  let bookingMessage = "";

  // Date and time formatters
  const dayFormatter = new Intl.DateTimeFormat("en-GB", {
    weekday: "long",
    timeZone: "UTC",
  });

  const dateFormatter = new Intl.DateTimeFormat("en-GB", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    timeZone: "UTC",
  });

  const timeFormatter = new Intl.DateTimeFormat("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "UTC",
  });

  // Sort appointments once
  const sortedAppointments = [...data.availableAppointments].sort((a, b) =>
    a.time.localeCompare(b.time),
  );

  // Start on the week of the first appointment
  const firstAppointment = sortedAppointments[0];

  if (firstAppointment) {
    currentWeekStart = getStartOfWeek(firstAppointment.time);
  } else {
    currentWeekStart = getStartOfWeek(new Date().toISOString());
  }

  // Bloodbank options
  $: bloodbanks = [
    "All",
    ...new Set(sortedAppointments.map((item) => item.locationname)),
  ];

  // Filter appointments by selected bloodbank
  $: {
    if (selectedBloodbank === "All") {
      filteredAppointments = sortedAppointments;
    } else {
      filteredAppointments = sortedAppointments.filter((item) => {
        return item.locationname === selectedBloodbank;
      });
    }
  }

  // Build the current week
  $: daysInWeek = Array.from({ length: 7 }, (_, index) =>
    addDays(currentWeekStart, index),
  );

  // Build planner columns
  $: columns = daysInWeek.map((date): PlannerColumn => {
    const dateKey = formatDateKey(date);

    const appointmentsForDay = filteredAppointments
      .filter((appointment) => appointment.time.startsWith(dateKey))
      .map((appointment) => {
        return {
          ...appointment,
          formattedTime: timeFormatter.format(new Date(appointment.time)),
        };
      });

    return {
      dayName: dayFormatter.format(date),
      dateLabel: dateFormatter.format(date),
      appointments: appointmentsForDay,
    };
  });

  // Week number shown in the tab
  $: currentWeekNumber = getWeekNumber(currentWeekStart);

  function showPreviousWeek() {
    currentWeekStart = addDays(currentWeekStart, -7);
  }

  function showNextWeek() {
    currentWeekStart = addDays(currentWeekStart, 7);
  }

  function openBookingModal(appointment: AppointmentWithFormattedTime) {
    selectedAppointment = appointment;
    bookingMessage = "";
  }

  function closeBookingModal() {
    selectedAppointment = null;
    bookingMessage = "";
  }

  async function bookAppointment() {
    if (!selectedAppointment) {
      return;
    }

    isBooking = true;
    bookingMessage = "";

    try {
      const response = await fetch("/api/appointment/book", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          free_appointment_id: selectedAppointment.id,
          user_id: 1,
        }),
      });

      if (!response.ok) {
        bookingMessage = "Could not book appointment.";
        return;
      }

      bookingMessage = "Appointment booked successfully.";
    } catch {
      bookingMessage = "Could not book appointment.";
    } finally {
      isBooking = false;
    }
  }

  function toggleSidebar() {
    sidebarOpen = !sidebarOpen;
  }
</script>

<svelte:head>
  <title>Available Appointments</title>
</svelte:head>

<BookingModal
  selectedAppointment={selectedAppointment}
  isBooking={isBooking}
  bookingMessage={bookingMessage}
  onClose={closeBookingModal}
  onBook={bookAppointment}
/>

<div class="layout">
  <div class="page content">
    <div class="header">
      <h1 class="text-3xl">Available appointments</h1>

      <div class="filter">
        <label for="bloodbank">Choose bloodbank</label>
        <select id="bloodbank" bind:value={selectedBloodbank}>
          {#each bloodbanks as bloodbank}
            <option value={bloodbank}>{bloodbank}</option>
          {/each}
        </select>
      </div>
    </div>

    <WeekPlanner
      columns={columns}
      currentWeekNumber={currentWeekNumber}
      onPreviousWeek={showPreviousWeek}
      onNextWeek={showNextWeek}
      onSelectAppointment={openBookingModal}
    />
  </div>
</div>
