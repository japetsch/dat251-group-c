<style>
  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.35);
    border: none;
    padding: 0;
    cursor: default;
  }

  .modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    min-width: 320px;
    z-index: 10;
  }

  .modal-buttons {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }

  .modal-buttons button {
    padding: 0.75rem 1rem;
    border: 1px solid #999;
    border-radius: 10px;
    background: white;
    cursor: pointer;
  }
</style>

<script lang="ts">
  import type { AppointmentWithFormattedTime } from "$lib/types/appointment";

  export let selectedAppointment: AppointmentWithFormattedTime | null;
  export let isBooking: boolean;
  export let bookingMessage: string;
  export let onClose: () => void;
  export let onBook: () => void;
  // export let selectedAppointment: AppointmentWithFormattedTime | null;

  let appointmentDate = "";
  let appointmentPlace = "";
  let appointmentTime = "";

  $: {
    appointmentDate = "";
    appointmentPlace = "";
    appointmentTime = "";

    if (selectedAppointment) {
      appointmentDate = selectedAppointment.time.split("T")[0];
      appointmentPlace = selectedAppointment.bloodbank_name;
      appointmentTime = selectedAppointment.formattedTime;
    }
  }
</script>

{#if selectedAppointment}
  <button
    type="button"
    class="modal-backdrop"
    aria-label="Close modal"
    on:click={onClose}
  ></button>

  <div class="modal">
    <h2>Bestill time</h2>

    <p><strong>Sted:</strong> {appointmentPlace}</p>
    <p><strong>Dato:</strong> {appointmentDate}</p>
    <p><strong>Tid:</strong> {appointmentTime}</p>

    <div class="modal-buttons">
      <button type="button" on:click={onClose}> Avbryt </button>

      <button type="button" on:click={onBook} disabled={isBooking}>
        {#if isBooking}
          Bestiller...
        {:else}
          Bestill
        {/if}
      </button>
    </div>

    {#if bookingMessage}
      <p>{bookingMessage}</p>
      {#if bookingMessage === "Time bestilt!"}
        <a
          href="/appointment/list"
          style="display:inline-block;margin-top:0.75rem;padding:0.75rem 1.25rem;background:#dc2626;color:white;border-radius:10px;text-decoration:none;font-weight:600;"
        >
          Vis mine timer
        </a>
      {/if}
    {/if}
  </div>
{/if}
