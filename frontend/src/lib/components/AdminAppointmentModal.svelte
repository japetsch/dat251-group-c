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
    min-width: 60%;
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

  .modal-card {
    min-height: 100px;
    width: 100%;
    background: white;
    border-radius: 24px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    padding: 1rem;
    margin-bottom: 1rem;
  }
  h2,
  h3 {
    all: revert;
  }
</style>

<script lang="ts">
  import type {
    AdminCalendarAppointment,
    DonationType,
    NoteType,
  } from "$lib/types/admin";

  export let selectedAppointment: AdminCalendarAppointment | null;
  export let onClose: () => void;

  let appointmentNotes: NoteType[];
  let appointmentDonations: DonationType[];

  $: {
    appointmentNotes = [];
    appointmentDonations = [];

    if (selectedAppointment) {
      appointmentNotes = selectedAppointment.notes;
      appointmentDonations = selectedAppointment.donations;
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
    <h2>Details</h2>

    <p><strong>Appointment time:</strong> {selectedAppointment.time}</p>

    <hr />
    <h3>Donor</h3>
    <p><strong>Name:</strong> {selectedAppointment.donor_name}</p>
    <p><strong>Phone:</strong> {selectedAppointment.donor_phone}</p>
    <p><strong>Mail:</strong> {selectedAppointment.donor_email}</p>
    <p><strong>Bloodtype:</strong> {selectedAppointment.donor_blood_type}</p>
    <p>
      <strong>Cancelled:</strong>
      {selectedAppointment.appointment_cancelled}
    </p>

    {#if appointmentNotes.length !== 0}
      <hr />
      <h3>Notes</h3>
      {#each appointmentNotes as note}
        <div class="modal-card">
          <p><strong>From:</strong> {note.author_name}</p>
          <p><strong>Time:</strong> {note.time}</p>
          <p><strong>Message:</strong> {note.message}</p>
        </div>
      {/each}
    {/if}

    {#if appointmentDonations.length !== 0}
      <hr />
      <h3>Donations</h3>
      {#each appointmentDonations as donation}
        <div class="modal-card">
          <p><strong>Amount:</strong> {donation.amount_ml}ml</p>
          <p>
            <strong>Is blood (not plasma):</strong>
            {donation.is_blood_not_plasma}
          </p>
        </div>
      {/each}
    {/if}

    <div class="modal-buttons">
      <button type="button" on:click={onClose}> Cancel </button>
    </div>
  </div>
{/if}
