<style>
  .toolbar {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-top: 3rem;
    margin-bottom: -1px;
    position: relative;
    z-index: 2;
  }

  .week-label {
    padding: 0.75rem 1.25rem;
    border: 1px solid #999;
    border-bottom: none;
    border-radius: 14px 14px 0 0;
    background: white;
    font-size: 1.1rem;
  }

  .week-buttons {
    display: flex;
    gap: 0.75rem;
    align-items: flex-end;
    margin-bottom: 0.5rem;
  }

  .week-buttons button {
    padding: 0.75rem 1rem;
    border: 1px solid #999;
    border-radius: 10px;
    background: white;
    cursor: pointer;
  }

  .planner-wrapper {
    overflow-x: auto;
    margin: 0;
    padding: 0;
  }

  .planner {
    display: grid;
    grid-template-columns: repeat(7, minmax(180px, 1fr));
    min-width: 1260px;
    min-height: 500px;
    background: white;
    border: 2px solid #999;
    border-radius: 0 30px 30px 30px;
    overflow: hidden;
    margin-top: 0;
  }

  .column {
    display: flex;
    flex-direction: column;
    border-right: 1px solid #999;
  }

  .column:last-child {
    border-right: none;
  }

  .column-header {
    padding: 1.25rem 1rem;
    text-align: center;
    border-bottom: 1px solid #999;
    background: #fafafa;
    min-height: 100px;
  }

  .day-name {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
  }

  .date {
    color: #666;
  }

  .column-body {
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    flex: 1;
  }

  .appointment-card {
    width: 100%;
    padding: 1rem;
    border: 1px solid #aaa;
    border-radius: 18px;
    background: white;
    text-align: left;
    cursor: pointer;
  }

  .appointment-time {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
  }

  .appointment-place {
    color: #666;
  }

  .empty {
    min-height: 40px;
  }
</style>

<script lang="ts">
  import type {
    AppointmentWithFormattedTime,
    PlannerColumn,
  } from "$lib/types/appointment";

  interface Props {
    columns: PlannerColumn[];
    currentWeekNumber: number;
    onPreviousWeek: () => void;
    onNextWeek: () => void;
    onSelectAppointment: (appointment: AppointmentWithFormattedTime) => void;
  }

  let {
    columns,
    currentWeekNumber,
    onPreviousWeek,
    onNextWeek,
    onSelectAppointment,
  }: Props = $props();
</script>

<div class="toolbar">
  <div class="week-label">Week {currentWeekNumber}</div>

  <div class="week-buttons">
    <button type="button" onclick={onPreviousWeek}>Previous</button>
    <button type="button" onclick={onNextWeek}>Next</button>
  </div>
</div>

<div class="planner-wrapper">
  <div class="planner">
    {#each columns as column}
      <div class="column">
        <div class="column-header">
          <div class="day-name">{column.dayName}</div>
          <div class="date">{column.dateLabel}</div>
        </div>

        <div class="column-body">
          {#if column.appointments.length === 0}
            <div class="empty"></div>
          {:else}
            {#each column.appointments as appointment}
              <button
                type="button"
                class="appointment-card"
                onclick={() => onSelectAppointment(appointment)}
              >
                <div class="appointment-time">{appointment.formattedTime}</div>
                <div class="appointment-place">{appointment.locationname}</div>
              </button>
            {/each}
          {/if}
        </div>
      </div>
    {/each}
  </div>
</div>
