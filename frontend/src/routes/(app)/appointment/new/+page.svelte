<script lang="ts">
  import BookingModal from "$lib/components/BookingModal.svelte";
  import type { Appointment, AppointmentWithFormattedTime } from "$lib/types/appointment";
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

  function updateCalendar(){
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);

    const firstDayIndex = firstDay.getDay();
    const totalDays = lastDay.getDate();

    monthYear = currentDate.toLocaleString("en-GB", { month: "long", year: "numeric" });

    calendarDates = [];

    for(let i = firstDayIndex; i>0; i--){
      const prevDate = new Date(currentYear, currentMonth, 0 - i + 1);
      calendarDates.push({
        day: prevDate.getDate(),
        inactive: true,
        active: false,
        datekey: null,
        hasAppointment: false
      });
    }

    for (let i = 1; i <= totalDays; i++){
      const date = new Date(currentYear, currentMonth, i);
      const isToday = date.toDateString() === new Date().toDateString();
      const datekey = date.toLocaleDateString("en-CA");
      const hasAppointment = appointments.some((appointment) =>
        appointment.time.startsWith(datekey)
      );

      calendarDates.push({
        day: i,
        inactive: false,
        active: isToday,
        datekey,
        hasAppointment
      });
    }
  }

  function showPreviousMonth(){
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
  }

  function showNextMonth(){
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
  }

  function selectDate(datekey: string | null){
    if (!datekey) return;
    selectedDate = datekey;
  }

  function openBookingModal(appointment: Appointment) {
    selectedAppointment = {
      ...appointment,
      formattedTime: timeFormatter.format(new Date(appointment.time))
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

  $: {
    if(selectedDate === null){
      selectedAppointments = [];
    }else{
      const datekey = selectedDate;
      selectedAppointments = appointments.filter((appointment) => appointment.time.startsWith(datekey)); 
    }
  }

  updateCalendar();
</script>


<style>
  .page-shell {
    min-height: 100vh;
    display: flex;
    align-items: flex-start; 
    justify-content: flex-start;
    padding: 2rem;
    gap: 10rem;
  }

  .calendar{
    width: 600px; 
    height: 600px;
    display: flex;
    flex-direction: column;
    padding:10px; 
    background: white;
    border-radius: 10px;
    box-shadow: 0 0px rgba(0, 0, 0, 0.3);
  }

  .header{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
      }

    .header button{
      display:flex;
      align-items: center;
      justify-content: center;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      width: 40px;
      height: 40px;
      box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
  }

  .days{
        display:grid;
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
      width:42px; 
      height: 42px;
      display: flex; 
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      transition: 0.2s;
    }

  .date:hover span,
  .date.active span{
    background: pink;
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

  .appointments-panel{
    display: flex;
    flex-direction: column;
    gap: 1rem; 
    width:320px;
  }

  .appointment-card{
    min-height: 100px;
    width: 100%;
    background: white;
    border-radius: 24px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    padding: 1rem;
  }

  .page-title{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1rem;
  }



</style>

<BookingModal
  selectedAppointment={selectedAppointment}
  isBooking={isBooking}
  bookingMessage={bookingMessage}
  onClose={closeBookingModal}
  onBook={bookAppointment}
/>

<div class= "header">
  <h1 class="page-title">New Appointment</h1>
</div>
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
          class:active={selectedDate === date.datekey }
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
    <div class="appointment-card">No available appointments</div>
    {:else}
     {#each selectedAppointments as appointment}
     <button
      type="button"
      class="appointment-card"
      on:click={() => openBookingModal(appointment)}
     >
      <p>
        {new Date(appointment.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </p>
      <p>{appointment.bloodbank_name}</p>
     </button>
    {/each}
  {/if}
</div>
</div>

