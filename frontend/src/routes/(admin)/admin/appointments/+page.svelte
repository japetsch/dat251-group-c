<style>
  .page-shell {
    min-height: 100vh;
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 2rem;
    gap: 10rem;
  }

  .calendar {
    width: 600px;
    min-height: 600px;
    display: flex;
    flex-direction: column;
    padding: 10px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
  }

  .header button {
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    width: 40px;
    height: 40px;
    background: white;
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
  }

  .days {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
  }

  .day {
    text-align: center;
    padding: 5px;
    color: #999fa6;
    font-weight: 500;
  }

  .dates {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 5px;
  }

  .date {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 70px;
  }

  .date span {
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: 0.2s;
  }

  .date:hover span,
  .date.active span {
    background: pink;
    color: white;
  }

  .date.inactive {
    color: #ccc;
  }

  .appointment-dot {
    position: absolute;
    bottom: 10px;
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
  }

  .appointments-panel {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 320px;
  }

  .appointment-card {
    min-height: 100px;
    width: 100%;
    background: white;
    border-radius: 24px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    padding: 1rem;
  }

  .page-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1rem;
  }

  .error-text {
    color: #dc2626;
  }
</style>

<script lang="ts">
  import AdminAppointmentModal from "$lib/components/AdminAppointmentModal.svelte";
  import type { AdminCalendarAppointment } from "$lib/types/admin";
  import type { PageData } from "./$types";

  export let data: PageData;

  let selectedDate: string | null = null;
  let currentDate = new Date();
  let monthYear = "";

  let calendarDates: {
    day: number;
    inactive: boolean;
    active: boolean;
    datekey: string | null;
    hasAppointment: boolean;
  }[] = [];

  let appointments: PageData["upcoming"] = data.upcoming;
  let selectedAppointment: AdminCalendarAppointment | null = null;
  let selectedAppointments: PageData["upcoming"] = [];

  function updateCalendar() {
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);

    const firstDayIndex = firstDay.getDay();
    const totalDays = lastDay.getDate();

    monthYear = currentDate.toLocaleString("en-GB", {
      month: "long",
      year: "numeric",
    });

    calendarDates = [];

    for (let i = firstDayIndex; i > 0; i--) {
      const prevDate = new Date(currentYear, currentMonth, 0 - i + 1);
      calendarDates.push({
        day: prevDate.getDate(),
        inactive: true,
        active: false,
        datekey: null,
        hasAppointment: false,
      });
    }

    for (let i = 1; i <= totalDays; i++) {
      const date = new Date(currentYear, currentMonth, i);
      const isToday = date.toDateString() === new Date().toDateString();
      const datekey = date.toLocaleDateString("en-CA");

      const hasAppointment = appointments.some((appointment) =>
        appointment.time.startsWith(datekey),
      );

      calendarDates.push({
        day: i,
        inactive: false,
        active: isToday,
        datekey,
        hasAppointment,
      });
    }
  }

  function showPreviousMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
  }

  function showNextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
  }

  function selectDate(datekey: string | null) {
    if (!datekey) return;
    selectedDate = datekey;
  }

  $: {
    if (selectedDate === null) {
      selectedAppointments = [];
    } else {
      const datekey = selectedDate;
      selectedAppointments = appointments.filter((appointment) =>
        appointment.time.startsWith(datekey),
      );
    }
  }

  function openAppointmentModal(appointment: AdminCalendarAppointment) {
    selectedAppointment = appointment;
  }

  function closeAppointmentModal() {
    selectedAppointment = null;
  }

  updateCalendar();
</script>

<AdminAppointmentModal
  selectedAppointment={selectedAppointment}
  onClose={closeAppointmentModal}
/>

<div class="header">
  <h1 class="page-title">Admin Appointments</h1>
</div>

{#if data.error}
  <p class="error-text">{data.error}</p>
{:else}
  <div class="page-shell">
    <div class="calendar">
      <div class="header">
        <button type="button" on:click={showPreviousMonth}>&#8249;</button>
        <div class="monthYear">{monthYear}</div>
        <button type="button" on:click={showNextMonth}>&#8250;</button>
      </div>

      <div class="days">
        <div class="day">Mon</div>
        <div class="day">Tue</div>
        <div class="day">Wed</div>
        <div class="day">Thu</div>
        <div class="day">Fri</div>
        <div class="day">Sat</div>
        <div class="day">Sun</div>
      </div>

      <div class="dates">
        {#each calendarDates as date}
          <div
            class="date"
            class:inactive={date.inactive}
            class:active={selectedDate === date.datekey}
            on:click={() => selectDate(date.datekey)}
          >
            {#if date.day !== 0}
              <span>{date.day}</span>
              {#if date.hasAppointment}
                <div class="appointment-dot"></div>
              {/if}
            {/if}
          </div>
        {/each}
      </div>
    </div>

    <div class="appointments-panel">
      {#if selectedAppointments.length === 0}
        <div class="appointment-card">No bookings on this date</div>
      {:else}
        {#each selectedAppointments as appointment}
          <div
            class="appointment-card"
            on:click={() => openAppointmentModal(appointment)}
          >
            <p><strong>{appointment.donor_name}</strong></p>
            <p>
              {new Date(appointment.time).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })}
            </p>
            <p>{appointment.bloodbank_name}</p>
          </div>
        {/each}
      {/if}
    </div>
  </div>
{/if}
