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
    height: 600px;
    display: flex;
    flex-direction: column;
    padding: 10px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 0px rgba(0, 0, 0, 0.3);
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
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
  }
  button:disabled {
    background-color: #ccc;
    color: #666;
    cursor: not-allowed;
    opacity: 0.7;
  }
  .tooltip {
    color: red;
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

  .date.today span {
    background: rgba(0, 255, 0, 0.3);
    color: white;
  }

  .date.inactive {
    color: #ccc;
  }

  .date.inactive:hover {
    color: white;
  }

  .appointment-dot {
    position: absolute;
    bottom: 10px;
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
  }

  .appointment-dot-grey {
    position: absolute;
    bottom: 10px;
    width: 8px;
    height: 8px;
    background: #aaaaaa;
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
</style>

<script lang="ts">
  import BookingModal from "$lib/components/BookingModal.svelte";
  import type {
    Appointment,
    AppointmentWithFormattedTime,
  } from "$lib/types/appointment";
  import type { PageData } from "./$types";

  export let data: PageData;

  type CalendarDate = {
    day: number;
    inactive: boolean;
    active: boolean;
    datekey: string | null;
    hasAppointment: boolean;
    hasOnlyInvalidAppointment: boolean;
  };

  let selectedDate: CalendarDate | null = null;

  let currentDate = new Date();
  let monthYear = "";
  let calendarDates: CalendarDate[] = [];
  let appointments: Appointment[] = data.availableAppointments;
  let selectedAppointments: Appointment[] = [];
  let selectedAppointment: AppointmentWithFormattedTime | null = null;
  let isBooking = false;
  let bookingMessage = "";

  const timeFormatter = new Intl.DateTimeFormat("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "UTC",
  });

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
        hasOnlyInvalidAppointment: false,
      });
    }

    for (let i = 1; i <= totalDays; i++) {
      const date = new Date(currentYear, currentMonth, i);
      const isToday = date.toDateString() === new Date().toDateString();
      const datekey = date.toLocaleDateString("en-CA");
      const appointmentsOnDay = appointments.filter((appointment) =>
        appointment.time.startsWith(datekey),
      );
      const hasAppointment = appointments.some((appointment) =>
        appointment.time.startsWith(datekey),
      );
      const hasOnlyInvalidAppointment = appointmentsOnDay.every(
        (appointment) =>
          appointment.valid === false && appointment.booked_by_user === false,
      );

      calendarDates.push({
        day: i,
        inactive: false,
        active: isToday,
        datekey,
        hasAppointment,
        hasOnlyInvalidAppointment,
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

  function isToday(date: CalendarDate): boolean {
    return date.datekey === new Date().toLocaleDateString("en-CA");
  }

  function selectDate(date: CalendarDate | null) {
    if (!date) return;
    selectedDate = date;
  }

  function openBookingModal(appointment: Appointment) {
    selectedAppointment = {
      ...appointment,
      formattedTime: timeFormatter.format(new Date(appointment.time)),
    };
    bookingMessage = "";
  }

  function closeBookingModal() {
    selectedAppointment = null;
    bookingMessage = "";
  }

  async function bookAppointment() {
    if (!selectedAppointment) return;

    isBooking = true;
    bookingMessage = "";

    try {
      const response = await fetch("/api/bookingslot/book", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          bookingslot_id: selectedAppointment.id,
        }),
      });

      if (!response.ok) {
        bookingMessage = "Kunne ikke bestille time.";
        return;
      }

      bookingMessage = "Time bestilt!";
    } catch {
      bookingMessage = "Kunne ikke bestille time.";
    } finally {
      isBooking = false;
    }
  }

  function appointmentValid(appointment: Appointment): boolean {
    return !appointment.valid;
  }

  $: {
    if (selectedDate === null) {
      selectedAppointments = [];
    } else {
      const datekey = selectedDate.datekey;
      selectedAppointments = datekey
        ? appointments.filter((appointment) =>
            appointment.time.startsWith(datekey),
          )
        : [];
    }
  }

  updateCalendar();
</script>

<BookingModal
  selectedAppointment={selectedAppointment}
  isBooking={isBooking}
  bookingMessage={bookingMessage}
  onClose={closeBookingModal}
  onBook={bookAppointment}
/>

<div class="header">
  <h1 class="page-title">Ny time</h1>
</div>
<div class="page-shell">
  <div class="calendar">
    <div class="header">
      <button type="button" on:click={showPreviousMonth}>&#8249;</button>
      <div class="monthYear">{monthYear}</div>
      <button type="button" on:click={showNextMonth}>&#8250;</button>
    </div>

    <div class="days">
      <div class="day">Søn</div>
      <div class="day">Man</div>
      <div class="day">Tir</div>
      <div class="day">Ons</div>
      <div class="day">Tor</div>
      <div class="day">Fre</div>
      <div class="day">Lør</div>
    </div>

    <div class="dates">
      {#each calendarDates as date}
        <div
          class="date"
          class:inactive={date.inactive}
          class:active={selectedDate === date}
          class:today={isToday(date)}
          on:click={() => selectDate(date)}
        >
          {#if date.day !== 0}
            <span>{date.day}</span>
            {#if date.hasAppointment && !date.hasOnlyInvalidAppointment}
              <div class="appointment-dot"></div>
            {/if}
            {#if date.hasAppointment && date.hasOnlyInvalidAppointment}
              <div class="appointment-dot-grey"></div>
            {/if}
          {/if}
        </div>
      {/each}
    </div>
  </div>

  <div class="appointments-panel">
    {#if selectedAppointments.length === 0}
      <div class="appointment-card">Ingen ledige timer</div>
    {:else}
      {#if selectedDate && selectedDate.hasOnlyInvalidAppointment}
        <span class="tooltip"
          >Appointment not bookable because of exisitng appointment within
          last/next 4 months</span
        >
      {/if}
      {#each selectedAppointments as appointment}
        {#if appointment.capacity === 0}
          <span class="tooltip">No free slots at this time</span>
        {/if}
        <button
          type="button"
          class="appointment-card"
          on:click={() => openBookingModal(appointment)}
          disabled={appointmentValid(appointment)}
        >
          {#if appointment.booked_by_user}
            <p>Booked</p>
          {/if}
          <p>
            {new Date(appointment.time).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </p>
          <p>{appointment.bloodbank_name}</p>
          <p>Slots left: {appointment.capacity}</p>
        </button>
      {/each}
    {/if}
  </div>
</div>
