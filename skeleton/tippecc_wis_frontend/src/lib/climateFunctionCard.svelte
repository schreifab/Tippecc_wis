<script lang="ts">
	import type { ClimateFunction } from '../model';
	export let climateFunction: ClimateFunction;

	//event to handle clicked button
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	function handleClick(id: number) {
		dispatch('functionSelected', { id });
	}
</script>

<div class="card snap-start">
	<header class="card-header flex justify-between items-center">
		<h2>{climateFunction.name}</h2>
		<button
			class="rounded p-2 variant-glass-primary"
			on:click={() => handleClick(climateFunction.id)}>&#8594;</button
		>
	</header>
	<div class="card-body pb-3 pl-3">
		<p>
			{climateFunction.description}
		</p>
	</div>
</div>
