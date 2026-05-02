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
      await goto(isAdmin ? "/admin/appointment/list" : "/appointment/list");
    } finally {
      loading = false;
    }
  }
</script>

{#if open}
  <div class="backdrop" on:click={() => (open = false)}>
    <div class="modal" on:click|stopPropagation>
      <h2>Notes</h2>

      {#if notes.length === 0}
        <p>No notes yet.</p>
      {:else}
        {#each notes as note}
          <div class="note">
            <strong>{note.author_name}</strong>
            <small>{new Date(note.time).toLocaleString()}</small>
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
