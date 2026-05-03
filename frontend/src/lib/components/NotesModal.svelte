<style>
  .backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    width: 400px;
  }

  .note {
    border-bottom: 1px solid #ddd;
    margin-bottom: 0.5rem;
    padding-bottom: 0.5rem;
  }

  .note-header {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    align-items: flex-start;
  }

  .note-header small {
    color: #64748b;
    white-space: nowrap;
  }

  textarea {
    width: 100%;
    margin-top: 1rem;
  }
</style>

<script lang="ts">
  import { goto, invalidateAll } from "$app/navigation";
  import client from "$lib/api/client";
  import type { components } from "$lib/api/schema";

  export let appointmentId: number;
  export let notes: components["schemas"]["NoteType"][] = [];
  export let isAdmin = false;
  export let open = false;

  let message = "";
  let loading = false;

  $: sortedNotes = [...notes].sort(
    (a, b) => new Date(b.time).getTime() - new Date(a.time).getTime(),
  );

  const formatNoteTime = (value: string) =>
    new Date(value).toLocaleString("en-DK", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

  async function addNote() {
    if (!message.trim()) return;

    loading = true;

    const path = isAdmin
      ? "/admin/appointment/{appointment_id}/note"
      : "/appointment/{appointment_id}/note";

    try {
      await client.POST(path, {
        params: { path: { appointment_id: appointmentId } },
        body: { message },
      });

      message = "";
      open = false;

      await invalidateAll();
      await goto(isAdmin ? "/admin/appointments" : "/appointment/list");
    } finally {
      loading = false;
    }
  }
</script>

{#if open}
  <div class="backdrop" on:click={() => (open = false)}>
    <div class="modal" on:click|stopPropagation>
      <h2>Notes</h2>

      {#if sortedNotes.length === 0}
        <p>No notes yet.</p>
      {:else}
        {#each sortedNotes as note}
          <div class="note">
            <div class="note-header">
              <strong>{note.author_name}</strong>
              <small>{formatNoteTime(note.time)}</small>
            </div>
            <p>{note.message}</p>
          </div>
        {/each}
      {/if}

      <textarea bind:value={message} placeholder="Write a note..."></textarea>

      <button type="button" on:click={addNote} disabled={loading}>
        {loading ? "Saving..." : "Add note"}
      </button>

      <button type="button" on:click={() => (open = false)}> Close </button>
    </div>
  </div>
{/if}
