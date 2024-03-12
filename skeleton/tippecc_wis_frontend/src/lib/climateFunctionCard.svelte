<!-- component for Climate Function as Card -->
<script lang="ts">
	// Has name, id and description
	//import Model and export card element ClimateFunction
	import type { ClimateFunction } from '../model';
	export let climateFunction: ClimateFunction;

	//event to handle clicked button
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	function handleClick(id: number) {
		dispatch('functionSelected', { id });
	}
</script>

<!-- html Block
Svelte Blocks makes Component dynamic
e.g. {climateFunction.name} Displays always the name of the object
-->
<div class="card snap-start">
	<header class="card-header flex justify-between items-center">
		<h2>{climateFunction.name}</h2>
		<!--&#8594;: Code for rigth arrow.-->
		<button
			class="rounded p-2 variant-glass-primary"
			on:click={() => handleClick(climateFunction.id)}>&#8594;</button
		>
	</header>
	<div class="card-body pb-3 pl-3">
		<!--Description block of the funktion-->
		<p>
			{climateFunction.description}
		</p>
	</div>
</div>
