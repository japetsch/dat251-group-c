<script lang="ts">
	import type { AppointmentRow } from '$lib/api/appointments';

	export let data: {
		appointments: AppointmentRow[];
	};

	function formatDate(value: string) {
		return new Date(value).toLocaleString();
	}
</script>

<svelte:head>
	<title>Appointments</title>
</svelte:head>

<h1>Appointments</h1>

{#if data.appointments.length === 0}
	<p>No appointments found.</p>
{:else}
	<table>
		<thead>
			<tr>
				<th>ID</th>
				<th>User</th>
				<th>Location</th>
				<th>Time</th>
			</tr>
		</thead>
		<tbody>
			{#each data.appointments as appointment}
				<tr>
					<td>{appointment.id}</td>
					<td>{appointment.username}</td>
					<td>{appointment.locationname}</td>
					<td>{formatDate(appointment.time)}</td>
				</tr>
			{/each}
		</tbody>
	</table>
{/if}
