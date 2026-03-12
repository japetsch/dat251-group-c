<script lang="ts">
	export let sidebarOpen: boolean;
	export let onToggle: () => void;
</script>

{#if sidebarOpen}
	<aside class="sidebar">
		<button type="button" class="sidebar-toggle" on:click={onToggle}></button>

		<a href="/" class="sidebar-button">Home</a>
		<a href="/myAppointments" class="sidebar-button">My appointments</a>
	</aside>
{:else}
	<button
		type="button"
		class="sidebar-collapsed"
		on:click={onToggle}
		aria-label="Open sidebar"
	>
		<span class="sidebar-collapsed-handle"></span>
	</button>
{/if}

<style>
	.sidebar {
		width: 220px;
		min-height: 100vh;
		background: #dfe7f2;
		border-right: 3px solid #999;
		padding: 2.5rem 1.5rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		position: relative;
		flex-shrink: 0;
	}

	.sidebar-toggle {
		position: absolute;
		top: 50%;
		right: -18px;
		transform: translateY(-50%);
		width: 36px;
		height: 72px;
		border: 3px solid #999;
		border-left: none;
		border-radius: 0 18px 18px 0;
		background: #dfe7f2;
		cursor: pointer;
	}

	.sidebar-button {
		display: inline-block;
		padding: 1rem 1.5rem;
		border: 1px solid #999;
		border-radius: 20px;
		background: white;
		color: #222;
		text-decoration: none;
		font-size: 1.5rem;
	}

	.sidebar-button:first-of-type {
		margin-top: 3rem;
	}

	.sidebar-collapsed {
		width: 28px;
		min-height: 100vh;
		border: none;
		border-right: 3px solid #999;
		background: #c62828;
		padding: 0;
		position: relative;
		cursor: pointer;
		flex-shrink: 0;
	}

	.sidebar-collapsed-handle {
		position: absolute;
		top: 140px;
		right: -3px;
		width: 22px;
		height: 56px;
		border-radius: 0 16px 16px 0;
		background: #c62828;
		border: 3px solid #999;
		border-left: none;
	}
</style>
