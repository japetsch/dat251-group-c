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

  interface Props {
    selectedAppointment: AppointmentWithFormattedTime | null;
    isBooking: boolean;
    bookingMessage: string;
    onClose: () => void;
    onBook: () => void;
  }

  let {
    selectedAppointment,
    isBooking,
    bookingMessage,
    onClose,
    onBook,
  }: Props = $props();

  let appointmentDate = $derived(selectedAppointment?.time.split("T")[0] ?? "");
  let appointmentPlace = $derived(selectedAppointment?.locationname ?? "");
  let appointmentTime = $derived(selectedAppointment?.formattedTime ?? "");
</script>

{#if selectedAppointment}
  <button
    type="button"
    class="modal-backdrop"
    aria-label="Close modal"
    onclick={onClose}
  ></button>

  <div class="modal">
    <h2>Book appointment</h2>

    <p><strong>Place:</strong> {appointmentPlace}</p>
    <p><strong>Date:</strong> {appointmentDate}</p>
    <p><strong>Time:</strong> {appointmentTime}</p>

    <div class="modal-buttons">
      <button type="button" onclick={onClose}> Cancel </button>

      <button type="button" onclick={onBook} disabled={isBooking}>
        {#if isBooking}
          Booking...
        {:else}
          Book
        {/if}
      </button>
    </div>

    {#if bookingMessage}
      <p>{bookingMessage}</p>
    {/if}
  </div>
{/if}
