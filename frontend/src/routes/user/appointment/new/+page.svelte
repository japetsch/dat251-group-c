<script lang="ts">
  import { Calendar, DayGrid, TimeGrid } from "@event-calendar/core";
  import { writable } from "svelte/store";
  import type {
    EventClickArg,
    EventDidMountArg,
    EventContentArg,
  } from "@event-calendar/core";

  import "@event-calendar/core/index.css";

  export let data;
  const plugins = [DayGrid, TimeGrid];

  const selectedEvent = writable<EventClickArg | null>(null);

  const options = {
    view: "timeGridWeek",

    headerToolbar: {
      start: "prev,next today",
      center: "title",
      end: "dayGridMonth,timeGridWeek,timeGridDay",
    },
    selectable: false,
    editable: false,

    scrollTime: "09:00",
    events: data.events,
    eventClick(info: EventClickArg) {
      selectedEvent.set(info); // opens modal
    },
    eventDidMount(info: EventDidMountArg) {
      info.el.title = info.event.title;
    },
    eventContent(info: EventContentArg) {
      const h = String(info.event.start.getHours()).padStart(2, "0");
      const m = String(info.event.start.getMinutes()).padStart(2, "0");
      return {
        html: `<span class="tiny">${h}:${m} - ${info.event.title}</span>`,
      };
    },

    views: {
      timeGridWeek: { pointer: true },
    },

    dayMaxEvents: true,
    nowIndicator: true,
  };
  function closeModal() {
    selectedEvent.set(null);
  }

  function doSomething() {
    selectedEvent.update((e) => {
      console.log("Button clicked for:", e?.event.title);
      return e;
    });
  }
</script>

<main class="row">
  {#if $selectedEvent}
    <div class="modal-backdrop" on:click={closeModal}></div>
    <div class="modal">
      <h3>{$selectedEvent.event.title}</h3>
      <p>Start: {$selectedEvent.event.start?.toLocaleString()}</p>
      <p>End: {$selectedEvent.event.end?.toLocaleString()}</p>
      <p>Location Id: {$selectedEvent.event.extendedProps.locationId}</p>
      <button on:click={doSomething}>Do Something</button>
      <button on:click={closeModal}>Close</button>
    </div>
  {/if}
  <Calendar {plugins} {options} />
</main>

<style>
  /* .modal-backdrop { */
  /*   position: fixed; */
  /*   inset: 0; */
  /*   background: rgba(0,0,0,0.3); */
  /* } */
  .modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.25);
    z-index: 10;
    min-width: 250px;
  }
</style>
