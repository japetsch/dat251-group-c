<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<h1>Appointments</h1>

{#if data.error}
	<p>{data.error}</p>

{:else if data.appointments.length === 0}
	<p>No appointments found.</p>

{:else}
	<table>
		<thead>
			<tr>
				<th>User</th>
				<th>Location</th>
				<th>Time</th>
			</tr>
		</thead>

		<tbody>
			{#each data.appointments as appointment}
				<tr>
					<td>{appointment.username}</td>
					<td>{appointment.locationname}</td>
					<td>{new Date(appointment.time).toLocaleString()}</td>
				</tr>
			{/each}
		</tbody>
	</table>
{/if}

<p>Hello world!</p>

