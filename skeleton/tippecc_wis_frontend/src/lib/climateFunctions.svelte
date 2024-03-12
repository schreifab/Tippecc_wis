<!--Main compnent. 
	This page is displayed when the application is launched.
	Manages and loads all other components
-->
<script lang="ts">
	import type { CreateQueryResult, QueryKey } from '@tanstack/svelte-query';
	import type { AxiosResponse, AxiosError } from 'axios';
	import type { ClimateFunctionDetail } from '../model';

	//imports
	import { createApiClimateIndicesList, createApiClimateIndicesRetrieve } from '../api/api';
	import ClimateFunctionCard from '$lib/climateFunctionCard.svelte';
	import FunctionDetailsCard from '$lib/functionDetailsCard.svelte';
	import ClimateScene from '$lib/climateScene.svelte';
	import DynamicOptions from './dynamicOptions.svelte';

	//load functions from api
	const climate_funcs = createApiClimateIndicesList();
	let id_selected: number = 0;

	//load details from api when id changes
	$: funcDetails = createApiClimateIndicesRetrieve(id_selected);

	//ste new id when function selected
	function handleFunctionSelected(event: CustomEvent<{ id: number }>) {
		id_selected = event.detail.id;
	}
</script>

<h2 class="text-center text-xl">TIPPECC climate indices web information system</h2>
<br />
<!--Split Interface in grid wirh 4 colums-->
<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-5">
		<div class="grid h-screen grid-cols-4 pl-1 pr-1 gap-5">
			<div>
				<!--first column: Climate Scene-->
				<ClimateScene />
			</div>
			<div>
				<!--Second column: Dynamic options-->
				<DynamicOptions />
			</div>
			<div class="max-h-96 overflow-y-auto snap-y">
				<div class="grid gap-y-1">
					<!--third column: Function list-->
					{#if $climate_funcs.isLoading}
						<p>Loading...</p>
					{:else if $climate_funcs.isError}
						<span>Error: {$climate_funcs.error}</span>
					{:else}
						{#each $climate_funcs.data.data as climateFunction}
							<div>
								<ClimateFunctionCard
									{climateFunction}
									on:functionSelected={handleFunctionSelected}
								/>
							</div>
						{/each}
					{/if}
				</div>
			</div>

			<div>
				<!--fourth column: function details-->
				{#key id_selected}
					{#if $funcDetails?.data?.data !== undefined}
						<FunctionDetailsCard functionDetails={$funcDetails.data.data} />
					{/if}
				{/key}
			</div>
		</div>
	</div>
</div>
